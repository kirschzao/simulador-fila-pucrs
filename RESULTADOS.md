# M4 | Resultados da simulação — Fila simples

**Código-fonte:** [`simulador.py`](./simulador.py) · **Saída bruta:** [`resultados.txt`](./resultados.txt)

## Configuração comum

| Item | Valor |
|---|---|
| Gerador | Congruência Linear — `X(n+1) = (a·Xn + c) mod M` |
| Parâmetros | `a = 1.103.515.245` · `c = 12.345` · `M = 2³¹` · `X0 = 7` |
| Normalização | `U(i) = X(i) / M` → `[0, 1)` |
| Aleatórios consumidos | **100.000** (exatos, em ambas as filas) |
| Estado inicial | fila vazia |
| Primeira chegada | tempo **3,0** (não consome aleatório) |

---

## G/G/1/5 — chegadas entre 3...5, atendimento entre 4...5

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 3,0000 | 0,001416 % |
| 1 | 18,7544 | 0,008853 % |
| 2 | 29,4637 | 0,013909 % |
| 3 | 787,2037 | 0,371612 % |
| 4 | 101.802,2585 | 48,057395 % |
| 5 | 109.194,0608 | 51,546814 % |
| **Total** | **211.834,7411** | **100,000000 %** |

- **Tempo global da simulação:** 211.834,7411
- **Número de perda de clientes:** **5.883**

**Leitura.** Taxa média de chegada = 1/4 = 0,25 cliente/u.t.; taxa média de atendimento = 1/4,5 ≈
0,222 cliente/u.t. Como ρ = 4,5/4 = **1,125 > 1**, o sistema é **saturado**: um único servidor não
dá conta da demanda. A fila passa **99,6 %** do tempo nos estados 4 e 5 (quase sempre cheia), os
estados 0–2 aparecem apenas no transiente inicial, e há perda expressiva de clientes.

---

## G/G/2/5 — chegadas entre 3...5, atendimento entre 4...5

| Estado | Tempo acumulado | Probabilidade |
|---:|---:|---:|
| 0 | 4.137,6213 | 2,069290 % |
| 1 | 166.503,0863 | 83,270832 % |
| 2 | 29.312,9642 | 14,659878 % |
| 3 | 0,0000 | 0,000000 % |
| 4 | 0,0000 | 0,000000 % |
| 5 | 0,0000 | 0,000000 % |
| **Total** | **199.953,6718** | **100,000000 %** |

- **Tempo global da simulação:** 199.953,6718
- **Número de perda de clientes:** **0** (não houve perda)

**Leitura.** Com dois servidores a capacidade de atendimento sobe para 2/4,5 ≈ 0,444 cliente/u.t.
contra 0,25 de chegada — ρ ≈ **0,5625**, sistema **subcarregado**. A fila fica a maior parte do
tempo com 1 cliente (83,3 %) e nunca chega a acumular espera. Passar de 1 para 2 servidores
elimina completamente a perda de clientes.

### Por que os estados 3, 4 e 5 são exatamente zero?

Não é erro de implementação — é uma **propriedade determinística** desta configuração:

- O intervalo entre chegadas é no mínimo **3**, logo duas chegadas consecutivas distam no mínimo
  **6** uma da outra.
- O tempo de atendimento é no máximo **5**.
- Com 2 servidores e partindo da fila vazia, todo cliente é atendido **imediatamente** ao chegar.
  Um cliente que inicia atendimento em `a₁` sai no máximo em `a₁ + 5`, ou seja, **antes** da
  segunda chegada seguinte (`a₃ ≥ a₁ + 6`).
- Por indução, nunca há três clientes simultâneos: o estado 3 exigiria que alguém tivesse esperado,
  o que por sua vez exigiria já estar no estado 3.

**Verificação empírica:** o estado máximo atingido foi 2 em todas as sementes testadas
(`7, 13, 42, 1234, 99991`), sempre com 0 perdas.

---

## Verificações de consistência

| Checagem | G/G/1/5 | G/G/2/5 |
|---|---|---|
| Σ tempos acumulados = tempo global | ✅ (delta 0,00) | ✅ (delta 0,00) |
| Aleatórios consumidos = 100.000 | ✅ | ✅ |
| Σ probabilidades = 100 % | ✅ | ✅ |

Gerador: 100.000 valores em `[0, 1)` — mín. 0,000022 · máx. 0,999999 · **média 0,501115**
(esperado ≈ 0,5).

---

## Comparativo

| Métrica | G/G/1/5 | G/G/2/5 |
|---|---:|---:|
| Tempo global | 211.834,74 | 199.953,67 |
| P(fila vazia) | 0,0014 % | 2,0693 % |
| P(fila cheia, estado 5) | 51,5468 % | 0,0000 % |
| Perda de clientes | 5.883 | 0 |
| ρ (utilização) | 1,125 (saturado) | 0,5625 (folgado) |
