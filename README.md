# Simulador de Fila por Eventos Discretos

Simulador de filas `G/G/c/K` com gerador de números pseudoaleatórios pelo Método da Congruência
Linear.

**Disciplina:** Simulação e Métodos Analíticos — PUCRS
**Módulo:** M4 | Desenvolvimento de Simulador para uma Fila

## Grupo T1 - 691 - 12

- Arthur Cavalheiro Marques
- Lucas Fischer Azevedo
- Bernardo Possani Kirsch
- Pedro Turik Firmino

## Execução

```bash
python3 simulador.py
```

Sem dependências externas. A saída também é gravada em `resultados.txt`.

## Configuração

Gerador `X(n+1) = (a · Xn + c) mod M` com `a = 1.103.515.245`, `c = 12.345`, `M = 2³¹` e semente
`X0 = 7`. Ambas as simulações partem da fila vazia, com o primeiro cliente chegando no tempo 3,0 e
consumindo 100.000 aleatórios.

## Resultados

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
