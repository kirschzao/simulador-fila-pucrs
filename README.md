# Simulador de Filas por Eventos Discretos

Simulador de filas `G/G/c/K` com gerador de números pseudoaleatórios pelo Método da Congruência
Linear.

**Disciplina:** Simulação e Métodos Analíticos — PUCRS
**Módulos:** M4 | Simulador para uma Fila · M6 | Simulador para Filas em *Tandem*

## Grupo T1 - 691 - 12

- Arthur Cavalheiro Marques
- Lucas Fischer Azevedo
- Bernardo Possani Kirsch
- Pedro Turik Firmino

## Execução

```bash
python3 simulador.py       # M4 — fila única
python3 M6/simulador.py    # M6 — duas filas em tandem
```

Sem dependências externas. Cada simulador também grava a saída em `resultados.txt`.

## Configuração

Gerador `X(n+1) = (a · Xn + c) mod M` com `a = 1.103.515.245`, `c = 12.345`, `M = 2³¹` e semente
`X0 = 7`. Ambas as simulações partem da fila vazia, com o primeiro cliente chegando no tempo 3,0 e
consumindo 100.000 aleatórios.

## M4 | Resultados

### G/G/1/5 — chegadas 3...5, atendimento 4...5

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 3,0000 | 0,001416 % |
| 1 | 18,7544 | 0,008853 % |
| 2 | 29,4637 | 0,013909 % |
| 3 | 787,2037 | 0,371612 % |
| 4 | 101.802,2585 | 48,057395 % |
| 5 | 109.194,0608 | 51,546814 % |

Tempo global: **211.834,7411** · Perda de clientes: **5.883**

### G/G/2/5 — chegadas 3...5, atendimento 4...5

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 4.137,6213 | 2,069290 % |
| 1 | 166.503,0863 | 83,270832 % |
| 2 | 29.312,9642 | 14,659878 % |
| 3 | 0,0000 | 0,000000 % |
| 4 | 0,0000 | 0,000000 % |
| 5 | 0,0000 | 0,000000 % |

Tempo global: **199.953,6718** · Perda de clientes: **0**

Os estados 3 a 5 são zero por construção: as chegadas distam no mínimo 3 (duas chegadas
consecutivas, no mínimo 6) e o atendimento dura no máximo 5, então com 2 servidores todo cliente é
atendido de imediato e sai antes da segunda chegada seguinte — nunca há três clientes simultâneos.

## M6 | Filas em *tandem*

A rede é declarada no topo de `M6/simulador.py` por duas estruturas: `REDE`, com as características
de cada fila, e `ROTEAMENTO`, com as probabilidades de encaminhamento entre elas.

```python
REDE = {
    "F1": {"servidores": 2, "capacidade": 3, "atendimento": (4.0, 5.0), "chegada": (1.0, 5.0)},
    "F2": {"servidores": 1, "capacidade": 5, "atendimento": (1.0, 3.0)},
}

ROTEAMENTO = {
    "F1": [("F2", 1.0)],
    "F2": [(None, 1.0)],
}
```

Uma fila só recebe clientes do exterior se declarar `chegada`. Os três eventos tratados são
`CHEGADA` (entrada externa), `PASSAGEM` (saída de uma fila com destino a outra) e `SAIDA` (saída do
sistema). Cada evento acumula o tempo decorrido no estado atual de **todas** as filas antes de ser
processado.

Simulação: filas inicialmente vazias, primeiro cliente no tempo 2,5 e encerramento ao consumir o
100.000º aleatório.

### Fila 1 — G/G/2/3, chegadas 1...5, atendimento 4...5

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 1.150,8788 | 1,140997 % |
| 1 | 49.931,9324 | 49,503182 % |
| 2 | 43.356,4089 | 42,984121 % |
| 3 | 6.426,8866 | 6,371701 % |

Perda de clientes: **408**

### Fila 2 — G/G/1/5, atendimento 1...3

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 34.506,2755 | 34,209981 % |
| 1 | 60.161,2468 | 59,644660 % |
| 2 | 6.193,6531 | 6,140470 % |
| 3 | 4,9313 | 0,004889 % |
| 4 | 0,0000 | 0,000000 % |
| 5 | 0,0000 | 0,000000 % |

Perda de clientes: **0**

Tempo global da simulação: **100.866,1067**

Os resultados foram conferidos contra o simulador de rede de filas de referência da disciplina
(`simulator.jar`), alimentado com a mesma sequência de 100.000 aleatórios: as duas saídas coincidem
em todas as casas decimais reportadas.
