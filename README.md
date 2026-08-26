# Simulador de Fila por Eventos Discretos

Simulador de filas `G/G/c/K` baseado em **simulação de eventos discretos**, com gerador de números
pseudoaleatórios próprio (Método da Congruência Linear).

> **Disciplina:** Simulação e Métodos Analíticos — PUCRS
> **Unidade de Aprendizagem:** UA2 | Fundamentos de Simulação por Computador
> **Módulo:** M4 | Desenvolvimento de Simulador para uma Fila
> **Professor:** Afonso Sales, Ph.D.

## Equipe — Grupo T1 - 691 - 12

| Integrante |
|---|
| Arthur Cavalheiro Marques |
| Lucas Fischer Azevedo |
| Bernardo Possani Kirsch |
| Pedro Turik Firmino |

---

## Sobre a disciplina

**Simulação e Métodos Analíticos** trata da modelagem de sistemas reais como modelos computacionais
capazes de reproduzir seu comportamento ao longo do tempo. A disciplina percorre a geração de
números pseudoaleatórios, a modelagem orientada a eventos, a construção de simuladores de filas e o
cálculo de índices de desempenho (vazão, utilização, população e tempo de resposta).

A questão norteadora deste módulo:

> **Como se pode modelar e simular o comportamento de uma fila em um sistema computacional de forma
> eficiente e que pareça representar a realidade?**

A fila é tratada não como uma estrutura de dados abstrata, mas como **ferramenta para modelar e
analisar sistemas complexos** — o fluxo de clientes em um banco, o escalonamento de tarefas em um
sistema operacional, a gestão de filas em aeroportos.

---

## Como funciona

O simulador acumula o **tempo de permanência em cada estado da fila** e converte esses tempos em
**probabilidades**, dividindo-os pelo tempo global da simulação.

### Gerador de números pseudoaleatórios

Método da Congruência Linear (Lehmer, 1951):

```
X(n+1) = (a · Xn + c) mod M
U(i)   = X(i) / M          →  normalizado em [0, 1)
```

| Parâmetro | Valor | Papel |
|---|---:|---|
| `a` | 1.103.515.245 | multiplicador |
| `c` | 12.345 | incremento |
| `M` | 2³¹ = 2.147.483.648 | módulo |
| `X0` | 7 | semente |

Parâmetros do glibc/GCC, os mesmos validados no M2 por gráfico de dispersão.

### Laço principal

O critério de parada é o **consumo de 100.000 números pseudoaleatórios**. A cada número solicitado
o contador é decrementado; quando se esgota, `NextRandom()` para de fornecer números, nenhum evento
novo é agendado e a simulação encerra.

```
count = 100000
while (count > 0):
    evento = NextEvent()          # menor tempo no escalonador
    if evento == chegada: CHEGADA(evento)
    elif evento == saida: SAIDA(evento)
```

### Eventos

- **`CHEGADA`** — acumula o tempo no estado atual; se houver espaço (`fila < K`) o cliente entra e,
  havendo servidor livre (`fila <= c`), agenda sua `SAIDA`; caso contrário contabiliza **perda**.
  Ao final, agenda a próxima chegada.
- **`SAIDA`** — acumula o tempo no estado atual, remove o cliente e, se ainda houver alguém
  aguardando (`fila >= c`), agenda a próxima saída.

---

## Execução

```bash
python3 simulador.py
```

Sem dependências externas — apenas a biblioteca padrão do Python 3. A saída é impressa no terminal
e gravada em `resultados.txt`.

---

## Resultados

Ambas as simulações partem da **fila vazia**, com o **primeiro cliente chegando no tempo 3,0** e
consumindo exatamente **100.000 aleatórios**.

### G/G/1/5 — chegadas entre 3...5, atendimento entre 4...5

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 3,0000 | 0,001416 % |
| 1 | 18,7544 | 0,008853 % |
| 2 | 29,4637 | 0,013909 % |
| 3 | 787,2037 | 0,371612 % |
| 4 | 101.802,2585 | 48,057395 % |
| 5 | 109.194,0608 | 51,546814 % |
| **Total** | **211.834,7411** | **100,000000 %** |

**Tempo global:** 211.834,7411 · **Perda de clientes:** **5.883**

Taxa de chegada 1/4 = 0,25 contra taxa de atendimento 1/4,5 ≈ 0,222 → ρ = **1,125 > 1**. O sistema
é **saturado**: um único servidor não absorve a demanda. A fila passa **99,6 %** do tempo nos
estados 4 e 5, e os estados 0–2 aparecem apenas no transiente inicial.

### G/G/2/5 — chegadas entre 3...5, atendimento entre 4...5

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 4.137,6213 | 2,069290 % |
| 1 | 166.503,0863 | 83,270832 % |
| 2 | 29.312,9642 | 14,659878 % |
| 3 | 0,0000 | 0,000000 % |
| 4 | 0,0000 | 0,000000 % |
| 5 | 0,0000 | 0,000000 % |
| **Total** | **199.953,6718** | **100,000000 %** |

**Tempo global:** 199.953,6718 · **Perda de clientes:** **0**

Com dois servidores a capacidade sobe para 2/4,5 ≈ 0,444 contra 0,25 de chegada → ρ ≈ **0,5625**,
sistema **subcarregado**. Passar de 1 para 2 servidores **elimina completamente a perda de
clientes**.

#### Por que os estados 3, 4 e 5 são exatamente zero?

Não é erro de implementação — é uma **propriedade determinística** desta configuração:

- O intervalo entre chegadas é no mínimo **3**, logo duas chegadas consecutivas distam no mínimo
  **6** entre si.
- O tempo de atendimento é no máximo **5**.
- Com 2 servidores e partindo da fila vazia, todo cliente é atendido **imediatamente**. Quem inicia
  atendimento em `a₁` sai no máximo em `a₁ + 5` — portanto **antes** da segunda chegada seguinte
  (`a₃ ≥ a₁ + 6`).
- Por indução, nunca há três clientes simultâneos: o estado 3 exigiria que alguém tivesse esperado,
  o que por sua vez exigiria já se estar no estado 3.

Verificado empiricamente: estado máximo 2 e 0 perdas em todas as sementes testadas
(`7, 13, 42, 1234, 99991`).

### Comparativo

| Métrica | G/G/1/5 | G/G/2/5 |
|---|---:|---:|
| Tempo global | 211.834,74 | 199.953,67 |
| P(fila vazia) | 0,0014 % | 2,0693 % |
| P(fila cheia) | 51,5468 % | 0,0000 % |
| Perda de clientes | 5.883 | 0 |
| ρ (utilização) | 1,125 — saturado | 0,5625 — folgado |

---

## Verificações de consistência

| Checagem | G/G/1/5 | G/G/2/5 |
|---|---|---|
| Σ tempos acumulados = tempo global | ✅ delta 0,00 | ✅ delta 0,00 |
| Aleatórios consumidos = 100.000 | ✅ | ✅ |
| Σ probabilidades = 100 % | ✅ | ✅ |

Gerador — 100.000 valores em `[0, 1)`: mínimo 0,000022 · máximo 0,999999 · **média 0,501115**
(esperado ≈ 0,5).

---

## Estrutura

```
.
├── simulador.py           # gerador + simulador de eventos discretos
├── resultados.txt         # saída bruta da execução
├── RESULTADOS.md          # resultados formatados e análise
├── CONTEXTUALIZACAO.md    # especificação e contexto do módulo
└── README.md
```

---

## Próximos passos

Esta é a **primeira etapa** do trabalho e não vale nota — serve para receber feedback do professor.
O **simulador final** será entregue no **módulo 9**, incorporando os índices de desempenho tratados
no módulo *Cálculo dos Índices de Desempenho*.
