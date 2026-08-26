"""
Simulador de fila simples por eventos discretos — M4

Modelo: G/G/c/K
    G  -> distribuição geral (uniforme) para os tempos entre chegadas
    G  -> distribuição geral (uniforme) para os tempos de atendimento
    c  -> número de servidores
    K  -> capacidade total da fila (clientes em atendimento + aguardando)

Gerador de números pseudoaleatórios: Método da Congruência Linear (mesmo do M2)
    X(n+1) = (a * Xn + c) mod M
    U(i)   = X(i) / M   ->  normalizado em [0, 1)

Critério de parada: consumo de 100.000 números pseudoaleatórios. Ao utilizar o
100.000º aleatório a simulação se encerra (NextRandom() deixa de fornecer números
e nenhum evento novo é agendado).
"""

# ----------------------------------------------------------------- parâmetros
# Gerador (glibc / GCC) — mesmos valores validados no M2
A = 1_103_515_245       # multiplicador
C = 12_345              # incremento
M = 2 ** 31             # módulo (2.147.483.648)
SEED = 7                # semente (X0)

QTD_ALEATORIOS = 100_000    # critério de parada
PRIMEIRA_CHEGADA = 3.0      # primeiro cliente chega no tempo 3,0

# ------------------------------------------------------- variáveis globais
previous = SEED         # último número gerado da sequência
count = 0               # aleatórios restantes

tempo_global = 0.0      # relógio da simulação
fila = 0                # clientes no sistema (atendimento + espera)
perdas = 0              # clientes perdidos (fila cheia)
times = []              # tempo acumulado em cada estado da fila
escalonador = []        # eventos agendados: (tempo, tipo)

servidores = 1          # c
capacidade = 5          # K
chegada_min = 3.0       # intervalo entre chegadas
chegada_max = 5.0
atend_min = 4.0         # intervalo de atendimento
atend_max = 5.0


# ------------------------------------------------------------------ gerador
def next_random():
    """Retorna o próximo pseudoaleatório em [0, 1), ou None se acabaram."""
    global previous, count
    if count <= 0:
        return None
    count -= 1
    previous = (A * previous + C) % M
    return previous / M


def entre(a, b):
    """Sorteia um valor uniforme no intervalo [a, b]. None se acabaram os aleatórios."""
    u = next_random()
    if u is None:
        return None
    return a + (b - a) * u


# -------------------------------------------------------------- escalonador
def agenda(tipo, tempo):
    """Agenda um evento no escalonador."""
    escalonador.append((tempo, tipo))


def next_event():
    """Retira e devolve o evento de menor tempo do escalonador."""
    menor = min(escalonador)
    escalonador.remove(menor)
    return menor


def acumula_tempo(tempo_evento):
    """Contabiliza o tempo decorrido no estado atual da fila."""
    global tempo_global
    times[fila] += tempo_evento - tempo_global
    tempo_global = tempo_evento


# ---------------------------------------------------------------- eventos
def CHEGADA(tempo_evento):
    global fila, perdas

    acumula_tempo(tempo_evento)

    if fila < capacidade:
        fila += 1
        if fila <= servidores:              # há servidor livre -> atende agora
            dt = entre(atend_min, atend_max)
            if dt is not None:
                agenda("SAIDA", tempo_global + dt)
    else:
        perdas += 1                         # fila cheia -> cliente perdido

    dt = entre(chegada_min, chegada_max)    # agenda a próxima chegada
    if dt is not None:
        agenda("CHEGADA", tempo_global + dt)


def SAIDA(tempo_evento):
    global fila

    acumula_tempo(tempo_evento)

    fila -= 1
    if fila >= servidores:                  # ainda há cliente esperando
        dt = entre(atend_min, atend_max)
        if dt is not None:
            agenda("SAIDA", tempo_global + dt)


# -------------------------------------------------------------- simulação
def simula(c, k, ch_min, ch_max, at_min, at_max):
    """Executa uma simulação completa e devolve os resultados."""
    global previous, count, tempo_global, fila, perdas, times, escalonador
    global servidores, capacidade, chegada_min, chegada_max, atend_min, atend_max

    # reinicializa o estado global
    previous = SEED
    count = QTD_ALEATORIOS
    tempo_global = 0.0
    fila = 0
    perdas = 0
    times = [0.0] * (k + 1)
    escalonador = []

    servidores, capacidade = c, k
    chegada_min, chegada_max = ch_min, ch_max
    atend_min, atend_max = at_min, at_max

    # primeiro cliente chega no tempo 3,0 (não consome aleatório)
    agenda("CHEGADA", PRIMEIRA_CHEGADA)

    # ------------------------------------------------- laço principal (main)
    while count > 0 and escalonador:
        tempo_evento, tipo = next_event()

        if tipo == "CHEGADA":
            CHEGADA(tempo_evento)
        elif tipo == "SAIDA":
            SAIDA(tempo_evento)

    return {
        "times": list(times),
        "tempo_global": tempo_global,
        "perdas": perdas,
        "aleatorios_usados": QTD_ALEATORIOS - count,
    }


# ------------------------------------------------------------------ saída
def relatorio(titulo, cfg, r):
    linhas = []
    add = linhas.append

    add("=" * 62)
    add(titulo)
    add("=" * 62)
    add(f"Gerador ....... X0={SEED} | a={A} | c={C} | M={M}")
    add(f"Aleatórios .... {r['aleatorios_usados']}")
    add(f"Chegadas ...... entre {cfg['ch_min']:.1f} e {cfg['ch_max']:.1f}")
    add(f"Atendimento ... entre {cfg['at_min']:.1f} e {cfg['at_max']:.1f}")
    add("")
    add("Estado      Tempo acumulado      Probabilidade")
    add("-" * 62)

    tg = r["tempo_global"]
    for i, t in enumerate(r["times"]):
        p = (t / tg * 100) if tg else 0.0
        add(f"{i:>4}        {t:>15.4f}      {p:>11.6f} %")

    add("-" * 62)
    add(f"{'TOTAL':>4}        {sum(r['times']):>15.4f}      {100.0:>11.6f} %")
    add("")
    add(f"Tempo global da simulação ..... {tg:.4f}")
    add(f"Número de perda de clientes ... {r['perdas']}")
    add("")
    return "\n".join(linhas)


def main():
    filas = [
        ("G/G/1/5, chegadas entre 3...5, atendimento entre 4...5",
         {"c": 1, "k": 5, "ch_min": 3.0, "ch_max": 5.0, "at_min": 4.0, "at_max": 5.0}),
        ("G/G/2/5, chegadas entre 3...5, atendimento entre 4...5",
         {"c": 2, "k": 5, "ch_min": 3.0, "ch_max": 5.0, "at_min": 4.0, "at_max": 5.0}),
    ]

    saida = []
    for titulo, cfg in filas:
        r = simula(cfg["c"], cfg["k"], cfg["ch_min"], cfg["ch_max"],
                   cfg["at_min"], cfg["at_max"])
        texto = relatorio(titulo, cfg, r)
        print(texto)
        saida.append(texto)

    with open("resultados.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(saida))

    print("Resultados salvos em: resultados.txt")


if __name__ == "__main__":
    main()
