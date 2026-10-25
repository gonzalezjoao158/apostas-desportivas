# Progresso — Análise de apostas

Lista simples do que já está feito e do que falta (atualizar sempre que um passo é concluído).

## Feito
- [x] 4 agentes: estatístico, odds, banca e revisor (`.claude/agents/`)
- [x] Calculadora comum `ferramentas/apostas.py` (Poisson, margem, VE, stake, métricas)
- [x] `config.json` com as regras de banca
- [x] Modelo de análise `analises/_modelo.md` e `registo.csv` com colunas finais
- [x] Memória do projeto em `docs/` (contexto, progresso, rotina)

## A seguir
- [ ] Definir a banca inicial em `config.json`
- [ ] Escolher o método de stake (1% fixo ou ¼ Kelly)
- [ ] Escolher as ligas a seguir
- [ ] Escolher 2–3 casas licenciadas pelo SRIJ para comparar odds
- [ ] 1.ª análise completa de um jogo real (teste do fluxo)
- [ ] 1.º relatório semanal do `apostas-revisor`
