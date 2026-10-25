# Contexto do projeto — Análise de apostas desportivas (futebol)

Memória do projeto: todos os agentes leem este ficheiro antes de trabalhar. Atualizar sempre que houver uma decisão nova.

## Objetivo
- Analisar jogos de futebol de forma disciplinada e só apostar quando houver **valor** (VE ≥ +5%).
- Medir o método pelo **CLV** e pela **calibração**, não pelos resultados de poucas semanas.
- Nunca há promessa de lucro: a maioria dos apostadores perde a longo prazo.

## Percurso de cada jogo
Escolher jogo → `apostas-estatistico` (dados + golos esperados + probabilidades) → `apostas-odds`
(odds de casas SRIJ, margem, VE, veredicto) → `apostas-banca` (pausas, stake, registo) → jogo →
`apostas-revisor` (fecho, odd de fecho, CLV) → relatório semanal → ajustes ao método.

## Regras de banca (valores em `config.json`)
- Stake fixa de 1% da banca (alternativa: ¼ Kelly com teto de 2%).
- Máximo de 5% da banca em apostas pendentes.
- Pausa obrigatória com queda de 20% face ao pico ou 3 dias seguidos de perdas.
- Nada de martingale, recuperar perdas ou dinheiro emprestado.

## Ferramentas
- `ferramentas/apostas.py` — Poisson, margem, VE, stake e métricas (todas as contas passam por aqui).
- `analises/_modelo.md` — estrutura de cada análise.
- `registo.csv` — todas as apostas; a banca calcula-se a partir de `config.json` + lucros.

## Cuidados
Só casas licenciadas pelo SRIJ · maiores de 18 anos · fonte e data em todos os dados e odds ·
nunca inventar números · se o jogo deixar de ser controlado: autoexclusão no SRIJ e linha SOS Jogo/SICAD.

## Decisões
- (25/10) Estrutura com 4 agentes, calculadora comum e `config.json`.
- (25/10) Organização igual à do projeto de coaching: `docs/contexto.md`, `docs/progresso.md` e `docs/rotina.md`.

## Por decidir
1. Banca inicial (`banca_inicial` em `config.json`).
2. Método de stake: 1% fixo (atual) ou ¼ Kelly.
3. Ligas a seguir.
4. Casas de apostas SRIJ a usar.
