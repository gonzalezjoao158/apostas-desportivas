# Análise de apostas desportivas — futebol

Sistema de agentes para analisar jogos de futebol de forma disciplinada, à procura de **apostas de valor** (odd acima da probabilidade real estimada), com gestão de banca e revisão de resultados.

> ⚠️ **Aviso:** apostar envolve risco de perder dinheiro. Nenhuma análise garante lucro — a maioria dos apostadores perde a longo prazo. Apenas para maiores de 18 anos, em casas licenciadas pelo SRIJ. Se o jogo deixar de ser controlado: autoexclusão em www.srij.turismodeportugal.pt e linha SOS Jogo / SICAD.

## Os agentes (`.claude/agents/`)

| Agente | Função | Quando usar |
|---|---|---|
| `apostas-estatistico` | Dados do jogo (forma, xG, casa/fora, plantel) e probabilidades próprias | 1.º passo de cada jogo |
| `apostas-odds` | Odds, margem da casa, valor esperado e veredicto | 2.º passo |
| `apostas-banca` | Stake (1% fixo ou ¼ Kelly), limites e registo | Antes de apostar |
| `apostas-revisor` | ROI, taxa de acerto, CLV, calibração e ajustes | Semanal / fim de jornada |

## Fluxo de trabalho
1. Pedir: "Analisa o Benfica vs Porto de domingo" → `apostas-estatistico`.
2. `apostas-odds` compara com as odds e diz se há valor (muitas vezes não há — e está tudo bem).
3. `apostas-banca` define a stake e regista em `registo.csv`.
4. Depois dos jogos, `apostas-revisor` fecha as apostas e faz o relatório.

## Ficheiros
- `config.json` — banca inicial e regras de stake (método, % fixa, ¼ Kelly, tetos, VE mínimo, pausas).
- `ferramentas/apostas.py` — calculadora comum a todos os agentes (Poisson, margem, VE, stake, métricas).
- `analises/_modelo.md` — modelo de análise; uma análise por jogo (`AAAA-MM-DD-casa-vs-fora.md`).
- `registo.csv` — registo de todas as apostas (a banca calcula-se a partir de `config.json` + lucros).
- `relatorios/` — relatórios de desempenho.

## Calculadora
```bash
python3 ferramentas/apostas.py poisson 1.65 1.10      # probabilidades a partir dos golos esperados
python3 ferramentas/apostas.py margem 2.10 3.40 3.60  # margem da casa e prob. sem margem
python3 ferramentas/apostas.py ve 0.52 2.10           # valor esperado e veredicto
python3 ferramentas/apostas.py stake 0.52 2.10        # stake segundo config.json e apostas pendentes
python3 ferramentas/apostas.py metricas               # ROI, acerto, CLV, por mercado, calibração
```

## Conceitos-chave
- **Probabilidade implícita** = 1 / odd.
- **Margem da casa** = soma das probabilidades implícitas de um mercado − 100%.
- **Valor esperado (VE)** = probabilidade própria × odd − 1 (só apostar com VE ≥ +5%).
- **CLV** = apostar a odds melhores do que as de fecho; o melhor indicador de longo prazo.
