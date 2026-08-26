A = 1_103_515_245
C = 12_345
M = 2 ** 31
SEED = 7
QTD_ALEATORIOS = 100_000
PRIMEIRA_CHEGADA = 3.0


def next_random():
    global previous, count
    if count <= 0:
        return None
    count -= 1
    previous = (A * previous + C) % M
    return previous / M


def entre(a, b):
    u = next_random()
    return None if u is None else a + (b - a) * u


def agenda(tipo, tempo):
    escalonador.append((tempo, tipo))


def acumula(tempo_evento):
    global tempo_global
    times[fila] += tempo_evento - tempo_global
    tempo_global = tempo_evento


def chegada(tempo_evento):
    global fila, perdas
    acumula(tempo_evento)
    if fila < capacidade:
        fila += 1
        if fila <= servidores:
            dt = entre(atend_min, atend_max)
            if dt is not None:
                agenda("SAIDA", tempo_global + dt)
    else:
        perdas += 1
    dt = entre(chegada_min, chegada_max)
    if dt is not None:
        agenda("CHEGADA", tempo_global + dt)


def saida(tempo_evento):
    global fila
    acumula(tempo_evento)
    fila -= 1
    if fila >= servidores:
        dt = entre(atend_min, atend_max)
        if dt is not None:
            agenda("SAIDA", tempo_global + dt)


def simula(c, k, ch_min, ch_max, at_min, at_max):
    global previous, count, tempo_global, fila, perdas, times, escalonador
    global servidores, capacidade, chegada_min, chegada_max, atend_min, atend_max

    previous, count = SEED, QTD_ALEATORIOS
    tempo_global, fila, perdas = 0.0, 0, 0
    times = [0.0] * (k + 1)
    escalonador = []
    servidores, capacidade = c, k
    chegada_min, chegada_max = ch_min, ch_max
    atend_min, atend_max = at_min, at_max

    agenda("CHEGADA", PRIMEIRA_CHEGADA)

    while count > 0 and escalonador:
        tempo_evento, tipo = min(escalonador)
        escalonador.remove((tempo_evento, tipo))
        if tipo == "CHEGADA":
            chegada(tempo_evento)
        else:
            saida(tempo_evento)


def relatorio(titulo):
    linhas = ["=" * 62, titulo, "=" * 62, "",
              "Estado      Tempo acumulado      Probabilidade", "-" * 62]
    for i, t in enumerate(times):
        linhas.append(f"{i:>4}        {t:>15.4f}      {t / tempo_global * 100:>11.6f} %")
    linhas += ["-" * 62,
               f"{'TOTAL':>4}        {sum(times):>15.4f}      {100.0:>11.6f} %", "",
               f"Tempo global da simulação ..... {tempo_global:.4f}",
               f"Número de perda de clientes ... {perdas}", ""]
    return "\n".join(linhas)


saida_final = []
for c in (1, 2):
    simula(c, 5, 3.0, 5.0, 4.0, 5.0)
    texto = relatorio(f"G/G/{c}/5, chegadas entre 3...5, atendimento entre 4...5")
    print(texto)
    saida_final.append(texto)

with open("resultados.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(saida_final))
