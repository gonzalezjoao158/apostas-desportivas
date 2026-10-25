# Pesquisa: como outros agentes de IA e modelos tentam acertar apostas de futebol

*Pesquisa feita a 2026-10-25. Quase todas as fontes são preprints, teses ou páginas comerciais com amostras pequenas: são indicações, não certezas.*

## 1. Conclusão principal
**Nenhum estudo encontrado mostra uma IA a bater o mercado de apostas de forma consistente.** A melhor estimativa pública da probabilidade de um jogo continua a ser a odd de fecho das casas mais eficientes (por ex. Pinnacle). Por isso, a "melhor maneira de acertar" não é tentar adivinhar mais resultados: é **apostar só quando há uma diferença clara face ao mercado e medir se essa diferença é real (CLV)**.

## 2. O que os estudos recentes com agentes de IA (LLM) mostram

| Estudo | O que testou | Resultado |
|---|---|---|
| WC2026-Agents (arXiv 2607.17765) | 4 modelos de topo (Claude, GPT, Gemini, Grok) nos 104 jogos do Mundial 2026 | Fizeram o mesmo palpite principal em 92% dos jogos; **nenhum bateu o Brier score do mercado**; ROI de −18% a +10%; apostar contra o mercado deu prejuízo nos 4. |
| WorldCupArena (arXiv 2607.18084) | 13 sistemas, incluindo agentes de "pesquisa profunda" | O melhor (com pesquisa na web) acertou ~70,7% dos resultados contra ~68,3% da linha de odds. Ganhos pequenos e numa só competição. |
| Estudo multiagente ao vivo (arXiv 2609.12495) | Agentes especializados (um para notícias, outro para estatística…) e um que junta tudo | O mercado continuou a ser o melhor no resultado exato mais provável (19,6%); o agente de notícias igualou o mercado no top‑3. Dar a cada agente uma especialidade e **restringir** a síntese final ajudou. |

**Lições para os nossos agentes:**
- Os LLM tendem a "seguir o favorito" e a concordar entre si — não trazem informação nova só por serem vários.
- O valor dos agentes está na **informação recente** (onzes, lesões, notícias) e em **disciplina**, não em "intuição".
- A odd do mercado deve ser o **ponto de partida**, não uma coisa a contrariar.

## 3. Modelos estatísticos clássicos
- **Poisson / Dixon‑Coles (1997):** estima a força de ataque e de defesa de cada equipa e calcula a probabilidade de cada resultado. A correção Dixon‑Coles dá mais peso a 0‑0 e 1‑1. No estudo original deu lucro **apenas** quando a diferença face às odds era grande. Estudos posteriores têm resultados mistos; os ganhos face ao Poisson simples são pequenos.
- **Modelos com xG:** usar golos esperados em vez de golos reais reduz o ruído. Prever estatísticas do jogo (remates, xG) e só depois o resultado também foi testado (arXiv 2001.09097).
- **Machine learning (XGBoost, etc.):** uma tese da Erasmus (Bundesliga) só teve lucro com XGBoost (até 6,6% em 276 apostas, uma época). Ren & Susnjak (2022, Premier League) só tiveram lucro sendo conservadores e apostando apenas nos jogos em que o modelo estava mais confiante.

## 4. Boas práticas que aparecem em todas as fontes
1. **Partir do mercado:** retirar a margem às odds de uma casa eficiente e usar essa probabilidade como base. Só ajustar com informação concreta (lesão, onze, rotação).
2. **Combinar** a probabilidade do nosso modelo com a do mercado (por ex. 70% mercado / 30% modelo) em vez de confiar só no modelo.
3. **Margem mínima de valor:** apostar só quando o VE é claramente positivo (≥ +5%) — as pequenas diferenças costumam ser erro do modelo.
4. **CLV como métrica principal:** conseguir odds melhores do que as de fecho é o único sinal precoce de vantagem real; o lucro de poucas semanas é sobretudo sorte.
5. **Mercados menos eficientes:** ligas menores, mercados secundários e apostas feitas cedo (antes de a odd "acertar") têm mais erros do que o 1X2 da Premier League no dia do jogo.
6. **Notícias de última hora:** confirmar o onze inicial antes de apostar — foi onde o agente de notícias teve vantagem.
7. **Stakes pequenas e Kelly fracionado**, registo de tudo e avaliação com Brier score / calibração.
8. **Amostras grandes:** só tirar conclusões depois de centenas de apostas.

## 5. Melhorias propostas para os nossos agentes
- `apostas-estatistico`: acrescentar a probabilidade do mercado sem margem como referência e uma probabilidade **combinada** (modelo + mercado).
- `apostas-odds`: usar a odd de uma casa eficiente como referência; calcular o VE com a probabilidade combinada; registar a odd de fecho.
- Novo agente `apostas-noticias`: onzes prováveis/confirmados, lesões, rotações e meteorologia nas horas antes do jogo.
- `apostas-revisor`: acrescentar o Brier score e comparar sempre com o mercado.

## Fontes
- [WC2026-Agents — arXiv 2607.17765](https://arxiv.org/abs/2607.17765)
- [WorldCupArena — arXiv 2607.18084](https://huggingface.co/papers/2607.18084)
- [Multi-agent LLM forecasting, Mundial 2026 — arXiv 2609.12495](https://arxiv.org/pdf/2609.12495)
- [Resumo WorldCupArena — AI Weekly](https://aiweekly.co/alerts/worldcuparena-grades-13-ai-models-on-104-fifa-2026-matches)
- [Dixon & Coles (1997) — Lancaster ePrints](https://eprints.lancs.ac.uk/id/eprint/19492)
- [Beating the bookie — Langseth (NTNU)](https://folk.idi.ntnu.no/helgel/papers/LangsethSCAI14.pdf)
- [Forecasting football matches by predicting match statistics — arXiv 2001.09097](https://arxiv.org/pdf/2001.09097)
- [Tese Erasmus — ML e odds da Pinnacle](https://thesis.eur.nl/pub/49939)
- [Ren & Susnjak — arXiv 2211.15734](https://arxiv.org/abs/2211.15734v1)
- [Mandadapu — arXiv 2403.16282](https://arxiv.org/abs/2403.16282?context=cs)
- [Power ratings a partir de odds de fecho — OddsPapi](https://oddspapi.io/blog/?p=3168)
