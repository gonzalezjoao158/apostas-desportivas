#!/usr/bin/env python3
"""Calculadora comum aos agentes de apostas (só biblioteca padrão).

Garante que todos os agentes fazem as mesmas contas, da mesma forma.

Exemplos:
  python3 ferramentas/apostas.py poisson 1.65 1.10
  python3 ferramentas/apostas.py margem 2.10 3.40 3.60
  python3 ferramentas/apostas.py ve 0.52 2.10
  python3 ferramentas/apostas.py stake 0.52 2.10
  python3 ferramentas/apostas.py metricas
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "config.json"
REGISTO = RAIZ / "registo.csv"
MAX_GOLOS = 10


def carregar_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def pct(x):
    return f"{x * 100:.1f}%"


def odd_justa(p):
    return f"{1 / p:.2f}" if p > 0 else "—"


def poisson_pmf(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)


def matriz_resultados(lam_casa, lam_fora, rho=0.0):
    """Matriz P(golos casa = i, golos fora = j), com correção Dixon-Coles opcional (rho)."""
    m = [[poisson_pmf(i, lam_casa) * poisson_pmf(j, lam_fora)
          for j in range(MAX_GOLOS + 1)] for i in range(MAX_GOLOS + 1)]
    if rho:
        m[0][0] *= 1 - lam_casa * lam_fora * rho
        m[0][1] *= 1 + lam_casa * rho
        m[1][0] *= 1 + lam_fora * rho
        m[1][1] *= 1 - rho
    total = sum(map(sum, m))
    return [[v / total for v in linha] for linha in m]


def cmd_poisson(a):
    m = matriz_resultados(a.golos_casa, a.golos_fora, a.rho)
    n = range(MAX_GOLOS + 1)
    casa = sum(m[i][j] for i in n for j in n if i > j)
    empate = sum(m[i][i] for i in n)
    fora = sum(m[i][j] for i in n for j in n if i < j)
    mais25 = sum(m[i][j] for i in n for j in n if i + j > 2)
    ambas = sum(m[i][j] for i in n for j in n if i > 0 and j > 0)
    print(f"Golos esperados: casa {a.golos_casa:.2f} | fora {a.golos_fora:.2f} | rho {a.rho}")
    print("| Mercado | Prob. própria | Odd justa |")
    print("|---|---|---|")
    for nome, p in [("1 (casa)", casa), ("X (empate)", empate), ("2 (fora)", fora),
                    ("Mais de 2,5", mais25), ("Menos de 2,5", 1 - mais25),
                    ("Ambas marcam — Sim", ambas), ("Ambas marcam — Não", 1 - ambas)]:
        print(f"| {nome} | {pct(p)} | {odd_justa(p)} |")
    top = sorted(((m[i][j], i, j) for i in n for j in n), reverse=True)[:5]
    print("\nResultados mais prováveis: " + ", ".join(f"{i}-{j} ({pct(p)})" for p, i, j in top))


def cmd_margem(a):
    impl = [1 / o for o in a.odds]
    soma = sum(impl)
    print(f"Margem da casa: {pct(soma - 1)}")
    print("| Odd | Prob. implícita | Prob. sem margem |")
    print("|---|---|---|")
    for o, p in zip(a.odds, impl):
        print(f"| {o:.2f} | {pct(p)} | {pct(p / soma)} |")


def valor_esperado(p, odd):
    return p * odd - 1


def cmd_ve(a):
    cfg = carregar_config()
    ve = valor_esperado(a.prob, a.odd)
    veredicto = "Valor" if ve >= cfg["ve_minimo"] else "Sem valor"
    print(f"VE = {a.prob:.3f} × {a.odd:.2f} − 1 = {ve * 100:+.1f}%  →  {veredicto} "
          f"(mínimo {pct(cfg['ve_minimo'])}); odd mínima para valor: "
          f"{(1 + cfg['ve_minimo']) / a.prob:.2f}")


def ler_registo():
    with open(REGISTO, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def banca_atual(cfg, linhas):
    lucro = sum(float(l["lucro"] or 0) for l in linhas if l["estado"] != "pendente")
    return cfg["banca_inicial"] + lucro


def cmd_stake(a):
    cfg = carregar_config()
    if cfg["banca_inicial"] is None:
        sys.exit("Define 'banca_inicial' em config.json antes de calcular stakes.")
    linhas = ler_registo()
    banca = a.banca if a.banca is not None else banca_atual(cfg, linhas)
    ve = valor_esperado(a.prob, a.odd)
    if ve < cfg["ve_minimo"]:
        print(f"VE {ve * 100:+.1f}% abaixo do mínimo ({pct(cfg['ve_minimo'])}): não apostar.")
        return
    if cfg["metodo_stake"] == "kelly":
        f = cfg["kelly_fracao"] * ve / (a.odd - 1)
        f = min(f, cfg["stake_maxima"])
        metodo = f"{cfg['kelly_fracao']:g} Kelly (teto {pct(cfg['stake_maxima'])})"
    else:
        f = cfg["stake_fixa"]
        metodo = f"fixa {pct(f)}"
    em_risco = sum(float(l["stake"] or 0) for l in linhas if l["estado"] == "pendente")
    livre = max(0.0, cfg["exposicao_maxima"] * banca - em_risco)
    stake = min(f * banca, livre)
    print(f"Banca: {banca:.2f} € | método: {metodo}")
    print(f"Em risco (pendentes): {em_risco:.2f} € | margem livre até {pct(cfg['exposicao_maxima'])}: {livre:.2f} €")
    print(f"Stake sugerida: {stake:.2f} €" + ("  (limitada pela exposição máxima)" if stake < f * banca else ""))


def cmd_metricas(a):
    cfg = carregar_config()
    linhas = [l for l in ler_registo() if l["estado"] in ("ganha", "perdida", "anulada")]
    if not linhas:
        print("Ainda não há apostas fechadas no registo.")
        return
    apostado = sum(float(l["stake"]) for l in linhas)
    lucro = sum(float(l["lucro"]) for l in linhas)
    decididas = [l for l in linhas if l["estado"] != "anulada"]
    ganhas = sum(l["estado"] == "ganha" for l in decididas)
    print(f"Apostas fechadas: {len(linhas)} | total apostado: {apostado:.2f} € | lucro: {lucro:+.2f} €")
    print(f"ROI: {lucro / apostado * 100:+.1f}% | taxa de acerto: "
          f"{pct(ganhas / len(decididas)) if decididas else '—'} | odd média: "
          f"{sum(float(l['odd']) for l in linhas) / len(linhas):.2f}")
    if cfg["banca_inicial"] is not None:
        print(f"Banca: {cfg['banca_inicial']:.2f} € → {cfg['banca_inicial'] + lucro:.2f} €")
    clv = [float(l["odd"]) / float(l["odd_fecho"]) - 1 for l in linhas if l["odd_fecho"]]
    if clv:
        pos = sum(c > 0 for c in clv)
        print(f"CLV médio: {sum(clv) / len(clv) * 100:+.1f}% ({pos}/{len(clv)} apostas com CLV positivo)")
    for campo in ("mercado", "competicao"):
        grupos = {}
        for l in linhas:
            g = grupos.setdefault(l[campo], [0, 0.0, 0.0])
            g[0] += 1
            g[1] += float(l["stake"])
            g[2] += float(l["lucro"])
        print(f"\nPor {campo}:\n| {campo} | apostas | lucro | ROI |\n|---|---|---|---|")
        for k, (n, s, p) in sorted(grupos.items()):
            print(f"| {k} | {n} | {p:+.2f} € | {p / s * 100:+.1f}% |")
    print("\nCalibração (prob. própria vs. frequência real):\n| Faixa | apostas | média prevista | real |\n|---|---|---|---|")
    faixas = {}
    for l in decididas:
        p = float(l["prob_propria"])
        faixas.setdefault(min(int(p * 10), 9), []).append((p, l["estado"] == "ganha"))
    for k in sorted(faixas):
        v = faixas[k]
        print(f"| {k * 10}–{k * 10 + 10}% | {len(v)} | {pct(sum(p for p, _ in v) / len(v))} | "
              f"{pct(sum(g for _, g in v) / len(v))} |")
    if len(linhas) < 200:
        print(f"\nAviso: só {len(linhas)} apostas — os resultados têm muita variância.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(required=True)

    p = sub.add_parser("poisson", help="probabilidades 1X2, mais/menos 2,5 e ambas marcam")
    p.add_argument("golos_casa", type=float, help="golos esperados da equipa da casa")
    p.add_argument("golos_fora", type=float, help="golos esperados da equipa de fora")
    p.add_argument("--rho", type=float, default=0.0, help="correção Dixon-Coles (ex.: -0.1)")
    p.set_defaults(func=cmd_poisson)

    p = sub.add_parser("margem", help="margem da casa e probabilidades sem margem")
    p.add_argument("odds", type=float, nargs="+", help="todas as odds do mercado (ex.: 1 X 2)")
    p.set_defaults(func=cmd_margem)

    p = sub.add_parser("ve", help="valor esperado e veredicto")
    p.add_argument("prob", type=float, help="probabilidade própria (0–1)")
    p.add_argument("odd", type=float)
    p.set_defaults(func=cmd_ve)

    p = sub.add_parser("stake", help="stake sugerida segundo config.json e o registo")
    p.add_argument("prob", type=float, help="probabilidade própria (0–1)")
    p.add_argument("odd", type=float)
    p.add_argument("--banca", type=float, help="forçar valor da banca (por defeito, calculado)")
    p.set_defaults(func=cmd_stake)

    p = sub.add_parser("metricas", help="ROI, acerto, CLV, mercados e calibração do registo")
    p.set_defaults(func=cmd_metricas)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
