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
- `analises/` — uma análise por jogo (`AAAA-MM-DD-casa-vs-fora.md`).
- `registo.csv` — registo de todas as apostas.
- `relatorios/` — relatórios de desempenho.

## Conceitos-chave
- **Probabilidade implícita** = 1 / odd.
- **Margem da casa** = soma das probabilidades implícitas de um mercado − 100%.
- **Valor esperado (VE)** = probabilidade própria × odd − 1 (só apostar com VE ≥ +5%).
- **CLV** = apostar a odds melhores do que as de fecho; o melhor indicador de longo prazo.
