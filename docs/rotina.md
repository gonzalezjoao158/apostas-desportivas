# Rotina — Análise de apostas

Lista para ir riscando. Fluxo de cada jogo em `docs/contexto.md`.

## Início da jornada (1x por semana)
- [ ] Escolher os jogos a analisar (só das ligas definidas; poucos e bem analisados)
- [ ] Para cada jogo: pedir "Analisa o <Casa> vs <Fora>" → `apostas-estatistico`
- [ ] Confirmar que não há pausa ativa (`apostas-banca`)

## Dia do jogo (antes do início)
- [ ] `apostas-odds`: recolher odds em várias casas SRIJ e dar o veredicto
- [ ] Confirmar onzes iniciais e notícias de última hora (podem anular o valor)
- [ ] Só com veredicto "Valor": `apostas-banca` calcula a stake e regista
- [ ] Apontar a odd de fecho perto do início do jogo (para o CLV)

## Fim da jornada
- [ ] `apostas-revisor`: fechar apostas, correr `python3 ferramentas/apostas.py metricas` e gravar o relatório
- [ ] Atualizar `docs/progresso.md` e as decisões em `docs/contexto.md`

## Sinais para parar
- Vontade de recuperar perdas, aumentar stakes por impulso ou apostar sem análise → parar e falar com alguém.
