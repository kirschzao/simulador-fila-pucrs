# Simulador de Filas por Eventos Discretos

Simulador de filas `G/G/c/K` com gerador de números pseudoaleatórios pelo Método da Congruência
Linear.

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
python3 simulador.py                    # M4 — fila única
python3 M6/simulador.py                 # M6 — duas filas em tandem
python3 T1/simulador.py T1/modelo.yml   # T1 — rede de filas genérica, descrita em YAML
```

Sem dependências externas (Python 3.8+, apenas biblioteca padrão). Cada simulador também grava a
saída em um `.txt` ao lado do script.

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

## T1 (M8) | Simulador genérico para rede de filas

O simulador do T1 não tem topologia fixa: ele **carrega o modelo inteiro de um arquivo `.yml`**, no
mesmo estilo do simulador de referência do módulo 3. Para simular outra rede basta escrever outro
arquivo — nada muda no código.

```bash
python3 T1/simulador.py <modelo.yml> [saida.txt]
```

Sem instalar nada. Se o segundo argumento for omitido, a saída vai para `<modelo>.txt`. O relatório
sai no terminal e no arquivo.

```bash
python3 T1/simulador.py T1/modelo.yml              # modelo do enunciado do T1
python3 T1/simulador.py T1/modelo-fila2-4a6.yml    # variante: Fila 2 atendendo em 4..6
python3 T1/simulador.py T1/modelo-m6.yml           # rede do M6, usada como regressão
```

### Formato do arquivo de modelo

```yaml
arrivals:            # filas que recebem clientes de fora + instante da 1ª chegada
  F1: 2.0
queues:
  F1:
    servers: 1       # nº de servidores (c)
    minArrival: 2.0  # intervalo entre chegadas externas — só em filas de arrivals
    maxArrival: 4.0
    minService: 1.0  # intervalo de atendimento
    maxService: 2.0
                     # capacity ausente = capacidade INFINITA (G/G/1)
  F2:
    servers: 2
    capacity: 5      # capacidade total K, servidores inclusos (G/G/2/5)
    minService: 4.0
    maxService: 8.0
network:             # arestas de roteamento; o que faltar para 1,0 é saída do sistema
  - source: F1
    target: F2
    probability: 0.2
rndnumbersPerSeed: 100000   # a simulação encerra ao consumir este aleatório
seeds:
  - 7
```

O parser de YAML é próprio e cobre o subconjunto acima (mapas aninhados, listas e escalares, em
estilo de bloco ou inline `{...}` / `[...]`). Aceita comentários com `#`.

### Como o simulador funciona

Simulação por eventos discretos com dois tipos de evento — `CHEGADA` (cliente vindo de fora) e
`SAIDA` (fim de atendimento em uma fila). Todo evento, antes de ser tratado, contabiliza o tempo
decorrido no estado atual de **todas** as filas, então os tempos acumulados de cada fila sempre
somam o tempo global.

Gerador `X(n+1) = (a · Xn + c) mod M` com `a = 1.103.515.245`, `c = 12.345`, `M = 2³¹`, semente do
campo `seeds`.

**Ordem de consumo dos aleatórios** em uma saída de fila — é a convenção que faz os números
baterem com o simulador de referência, então fica explícita aqui:

1. contabiliza o tempo decorrido;
2. o cliente deixa a fila de origem; se ainda há alguém esperando, **sorteia o atendimento da
   origem**;
3. **sorteia o destino** — um único aleatório, e só quando a fila tem mais de uma rota de saída;
4. no destino, admite o cliente (ou registra perda, se cheio); se ele entra em serviço, **sorteia o
   atendimento do destino**.

### Validação

`T1/modelo-m6.yml` descreve em YAML exatamente a rede do M6. Rodado no simulador do T1, reproduz
`M6/resultados.txt` em todas as casas decimais — e o M6 já havia sido conferido contra o
`simulator.jar` da disciplina. Isso valida o motor genérico contra a referência.

### Modelo do enunciado

Fila 1 `G/G/1` (chegadas 2..4, atendimento 1..2) → 0,2 para a Fila 2 e 0,8 para a Fila 3.
Fila 2 `G/G/2/5` (atendimento 4..8) → 0,3 volta para a Fila 1, 0,5 para a Fila 3, 0,2 sai.
Fila 3 `G/G/2/10` (atendimento 5..15) → 0,7 para a Fila 2, 0,3 sai.
Filas vazias no início, primeiro cliente em `t = 2,0`, 100.000 aleatórios, semente 7.

#### Fila 1 — G/G/1, chegadas 2..4, atendimento 1..2

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 20.327,4236 | 40,000000 % |
| 1 | 26.856,1811 | 52,847192 % |
| 2 | 3.497,9298 | 6,883174 % |
| 3 | 135,2933 | 0,266228 % |
| 4 | 1,7307 | 0,003406 % |

Perda de clientes: **0** (capacidade infinita)

#### Fila 2 — G/G/2/5, atendimento 4..8

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 8.427,7911 | 16,584081 % |
| 1 | 18.050,1785 | 35,518872 % |
| 2 | 15.353,1846 | 30,211767 % |
| 3 | 6.765,0853 | 13,312234 % |
| 4 | 1.884,8714 | 3,709022 % |
| 5 | 337,4474 | 0,664024 % |

Perda de clientes: **41**

#### Fila 3 — G/G/2/10, atendimento 5..15

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

**Tempo global da simulação: 50.818,5584**

A Fila 3 é o gargalo: carga oferecida de ~7,1 clientes para 2 servidores, então ela passa 63 % do
tempo cheia e descarta 11.656 clientes. A Fila 2 sofre bem menos (41 perdas) e a Fila 1, de
capacidade infinita, fica estável com o servidor ocioso 40 % do tempo — o represamento nas filas 2
e 3 corta a realimentação que voltaria para ela.

### Variante Fila 2 em 4..6

O diagrama do enunciado marca `4..8min` na Fila 2, mas o arquivo modelo em Word rotula
"atendimento entre 4..6". `T1/modelo-fila2-4a6.yml` cobre a segunda leitura; resultado completo em
`T1/resultados-fila2-4a6.txt` (tempo global **50.944,4428**, perdas de **0 / 8 / 11.556**).
