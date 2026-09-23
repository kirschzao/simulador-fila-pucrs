# Simulador de Filas por Eventos Discretos

Simulador de filas `G/G/c/K` com gerador pelo Método da Congruência Linear
(`a = 1.103.515.245`, `c = 12.345`, `M = 2³¹`, semente `X0 = 7`, 100.000 aleatórios).

**Disciplina:** Simulação e Métodos Analíticos — PUCRS
**Módulos:** M4 | Simulador para uma Fila · M6 | Simulador para Filas em *Tandem* · T1 (M8) |
Simulador Genérico para Rede de Filas

## Grupo T1 - 691 - 12

- Arthur Cavalheiro Marques
- Lucas Fischer Azevedo
- Bernardo Possani Kirsch
- Pedro Turik Firmino

## Execução

```bash
python3 simulador.py
python3 M6/simulador.py
python3 T1/simulador.py T1/modelo.yml
```

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

## M6 | Filas em *tandem*

Filas vazias no início, primeiro cliente em `t = 2,5`, 100.000 aleatórios, semente 7.

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

## T1 (M8) | Rede de filas do enunciado

Filas vazias no início, primeiro cliente em `t = 2,0`.

### Fila 1 — G/G/1, chegadas 2..4, atendimento 1..2

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 20.327,4236 | 40,000000 % |
| 1 | 26.856,1811 | 52,847192 % |
| 2 | 3.497,9298 | 6,883174 % |
| 3 | 135,2933 | 0,266228 % |
| 4 | 1,7307 | 0,003406 % |

Perda de clientes: **0**

### Fila 2 — G/G/2/5, atendimento 4..8

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 8.427,7911 | 16,584081 % |
| 1 | 18.050,1785 | 35,518872 % |
| 2 | 15.353,1846 | 30,211767 % |
| 3 | 6.765,0853 | 13,312234 % |
| 4 | 1.884,8714 | 3,709022 % |
| 5 | 337,4474 | 0,664024 % |

Perda de clientes: **41**

### Fila 3 — G/G/2/10, atendimento 5..15

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 3,5971 | 0,007078 % |
| 1 | 2,9943 | 0,005892 % |
| 2 | 1,4563 | 0,002866 % |
| 3 | 3,1964 | 0,006290 % |
| 4 | 8,0643 | 0,015869 % |
| 5 | 5,3322 | 0,010493 % |
| 6 | 1,2906 | 0,002540 % |
| 7 | 83,4200 | 0,164153 % |
| 8 | 2.800,0114 | 5,509821 % |
| 9 | 15.920,9007 | 31,328911 % |
| 10 | 31.988,2951 | 62,946089 % |

Perda de clientes: **11.656**

Tempo global da simulação: **50.818,5584**

### Variante Fila 2 em 4..6

Tempo global: **50.944,4428** · Perda de clientes: **0 / 8 / 11.556** ·
modelo em `T1/modelo-fila2-4a6.yml`, saída completa em `T1/resultados-fila2-4a6.txt`.
