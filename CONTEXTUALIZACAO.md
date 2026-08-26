# M4 | Desenvolvimento de Simulador para uma Fila

**Disciplina:** Simulação e Métodos Analíticos
**Unidade de Aprendizagem:** UA2 | Fundamentos de Simulação por Computador
**Módulo:** M4 | Desenvolvimento de Simulador para uma Fila
**Professor:** Afonso Sales, Ph.D.

---

## Contextualização

Este módulo é uma oportunidade para aplicar conhecimentos teóricos em um problema concreto e
desafiador, típico dos sistemas computacionais e operacionais modernos. A fila, enquanto
estrutura de dados, é um conceito fundamental, mas seu estudo ganha nova dimensão quando
consideramos a **simulação de eventos discretos** que ocorrem no mundo real.

> A fila será estudada não apenas como uma entidade abstrata, mas **como uma ferramenta** para
> modelar e analisar sistemas complexos, como o fluxo de clientes em um banco, o processamento
> de tarefas em um sistema operacional ou a gestão de filas em aeroportos.

### Questão norteadora

> **Como se pode modelar e simular o comportamento de uma fila em um sistema computacional de
> forma eficiente e que pareça representar a realidade?**

Partindo dessa indagação, serão desenvolvidas habilidades para criar um simulador que não apenas
represente a realidade de forma fidedigna, mas também ofereça *insights* para a otimização de
processos.

---

## Construção conceitual e atuação investigativa

O simulador a ser desenvolvido visa **capturar e analisar os tempos acumulados em cada estado da
fila**, proporcionando uma visão clara e quantificável dos diferentes cenários que uma fila pode
apresentar.

A grande vantagem do método é traduzir esses tempos acumulados em **probabilidades para cada
estado da fila**, em relação ao tempo global (total) da simulação. Isso simplifica a análise de
sistemas complexos de filas e fornece insights para tomada de decisões e estratégias de otimização.

---

## Desenvolvendo um simulador para uma fila

Estrutura simples de código — não é necessário organizar em classes. Podem ser usadas **variáveis
globais diretamente na `main()`** e funções simples de apoio. Linguagem livre (usualmente Java ou
Python). A ideia é construir progressivamente, começando com um código básico e aprimorando.

### Etapa 1 — Implementação do gerador de números pseudoaleatórios

Implementar um gerador pelo **Método Congruente Linear** (assunto do M2 — Geração de Números
Pseudoaleatórios). O gerador é a base para simular a chegada e o atendimento de clientes, então
seus parâmetros devem ser bem escolhidos e a implementação bem feita, garantindo a qualidade da
simulação.

- Escolher valores apropriados para os parâmetros **a**, **c** e **M**, e o valor inicial da
  semente (*seed*).
- Testar a qualidade dos números gerados via gráfico de dispersão (Excel, por exemplo), como no M2.
- Desenvolver `NextRandom()`, que gera números **normalizados entre 0 e 1**, armazenando sempre o
  último número gerado da sequência para facilitar a próxima chamada.

```java
double NextRandom() {
   previous = ((a * previous) + c) % M;
   return (double) previous/M;
}
```

### Etapa 2 — Loop principal da simulação

Diretamente na `main()`, implementar um laço que executa a simulação por um determinado período.
Critério de parada: **quantidade de números pseudoaleatórios consumidos**. Inicializa-se o contador
`count` (ex.: 100.000) e, a cada número solicitado, decrementa-se o contador; ao acabar, para-se o
laço.

```java
int count = 100000;
...
while (count > 0) {
   evento = NextEvent();

   if (evento == tipo_chegada) {
      CHEGADA(evento)
   } else if (evento == tipo_saida) {
      SAIDA(evento)
   }
}
```

O processo é simples: solicita-se o **primeiro evento do escalonador** (o agendado com menor tempo
de simulação a ser executado), verifica-se se é do tipo "chegada" ou "saída" e chama-se o
procedimento correspondente.

### Etapa 3 — Tratamento dos eventos de chegada e saída

Conforme o módulo **Modelagem Orientada a Eventos (Algoritmo de Simulação)**, os procedimentos
`CHEGADA` e `SAIDA` fazem todo o tratamento que simula a entrada e saída de clientes da fila.
Gerenciam a adição e remoção de clientes usando o intervalo de tempo estabelecido para chegada e
atendimento, através dos números pseudoaleatórios do gerador — dando a sensação de que a dinâmica
não é estática.

### Etapa 4 — Cálculo de tempos acumulados e probabilidades

Após sair do laço principal, calcular e mostrar a **distribuição de probabilidade dos estados da
fila** (vazia, com 1 cliente, 2 clientes etc.).

Basta dividir cada tempo acumulado dos estados pelo **tempo global (total)** da simulação. Também é
interessante mostrar o tempo "puro" acumulado de cada estado — esses dados são cruciais para
entender a dinâmica da fila e identificar gargalos. `K` representa a capacidade de clientes da fila.

```java
for (int i=0; i<K+1; i++) {
   print i + ": " + times[i] + " (" +
           times[i]/TempoGlobal + "\%)\n";
}
```

### Etapa 5 — Análise e interpretação dos resultados

Com a distribuição de probabilidades, é possível compreender como a fila se comporta sob diferentes
condições, alterando a configuração simulada para novas análises. Isso ajuda a entender a eficiência
do sistema e possíveis melhorias.

A partir dessas probabilidades também é possível calcular **índices de desempenho** (vazão,
utilização, população e tempo de resposta) — detalhados no módulo **Cálculo dos Índices de
Desempenho**.

---

## Aplicação

A avaliação é organizada em duas partes: uma atividade gamificada e outra prática.

### Parte 1 | Entrega | Fila simples [FEEDBACK]

Módulo dedicado a aprimorar e terminar o **simulador de uma fila simples** — primeira etapa do
trabalho.

Além do **código-fonte**, entregar o **resultado da simulação** das seguintes filas:

- **`G/G/1/5`**, chegadas entre **3...5**, atendimento entre **4...5**
- **`G/G/2/5`**, chegadas entre **3...5**, atendimento entre **4...5**

> ℹ️ O arquivo modelo `.docx` traz, nos rótulos das respostas, `2...5` / `3...5` — divergente do
> enunciado. **Vale o enunciado** (`3...5` / `4...5`), confirmado pelo professor. Ao preencher o
> Word, corrigir os rótulos.

Condições para ambas as simulações:

- Fila inicialmente **vazia**
- **Primeiro cliente chegando no tempo 3,0**
- Simulação com **100.000 números aleatórios** — ao usar o 100.000º aleatório, a simulação encerra

Reportar:

- **Distribuição de probabilidades** dos estados da fila
- **Tempos acumulados** para os estados da fila
- **Número de perda de clientes** (caso tenha havido perda)
- **Tempo global da simulação**

### Observações da entrega

- Esta entrega **não vale nota**. Não há problema se o simulador tiver erros.
- O professor dará **feedback** ao simulador enviado — retorno essencial para que o **simulador
  final (módulo 9)** esteja correto.
- Baixar o arquivo modelo editável (Word) no CARD "M4 | Arquivo Modelo", responder às questões e
  enviar **em PDF** no CARD "M4 | Entrega | Fila simples".
- Status atualizado para "concluído" após a correção do professor.

---

## Estrutura do arquivo modelo (.docx)

```
Disciplina: SIMULAÇÃO E MÉTODOS ANALÍTICOS
Unidade de Aprendizagem: UA2 | FUNDAMENTOS DE SIMULAÇÃO POR COMPUTADOR
Módulo de Aprendizagem: M4 | DESENVOLVIMENTO DE SIMULADOR PARA UMA FILA
Estudantes:

Entrega | Fila Simples
Registre neste espaço sua resposta!

Link para o código fonte do grupo:

G/G/1/5, chegadas entre 2...5, atendimento entre 3...5:
G/G/2/5, chegadas entre 2...5, atendimento entre 3...5:
```
