from pathlib import Path

A = 1_103_515_245
C = 12_345
M = 2 ** 31
SEED = 7
QTD_ALEATORIOS = 100_000
PRIMEIRA_CHEGADA = 2.5

REDE = {
    "F1": {"servidores": 2, "capacidade": 3, "atendimento": (4.0, 5.0), "chegada": (1.0, 5.0)},
    "F2": {"servidores": 1, "capacidade": 5, "atendimento": (1.0, 3.0)},
}

ROTEAMENTO = {
    "F1": [("F2", 1.0)],
    "F2": [(None, 1.0)],
}


class Fila:
    def __init__(self, nome, servidores, capacidade, atendimento, chegada=None):
        self.nome = nome
        self.servidores = servidores
        self.capacidade = capacidade
        self.atend_min, self.atend_max = atendimento
        self.chegada = chegada
        self.clientes = 0
        self.perdas = 0
        self.tempos = [0.0] * (capacidade + 1)

    def status(self):
        return self.clientes

    def entra(self):
        self.clientes += 1

    def sai(self):
        self.clientes -= 1

    def perde(self):
        self.perdas += 1


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


def agenda(tipo, origem, tempo):
    if tempo is not None:
        escalonador.append((tempo, tipo, origem))


def destino_de(origem):
    u = next_random()
    if u is None:
        return None
    acumulado = 0.0
    for destino, p in ROTEAMENTO[origem]:
        acumulado += p
        if u < acumulado:
            return destino
    return ROTEAMENTO[origem][-1][0]


def roteia(origem):
    rotas = ROTEAMENTO[origem]
    if len(rotas) == 1:
        return rotas[0][0]
    return destino_de(origem)


def acumula(tempo_evento):
    global tempo_global
    dt = tempo_evento - tempo_global
    for fila in filas.values():
        fila.tempos[fila.status()] += dt
    tempo_global = tempo_evento


def tempo_atendimento(fila):
    dt = entre(fila.atend_min, fila.atend_max)
    return None if dt is None else tempo_global + dt


def admite(fila, origem):
    if fila.status() < fila.capacidade:
        fila.entra()
        if fila.status() <= fila.servidores:
            tipo = "SAIDA" if roteia(fila.nome) is None else "PASSAGEM"
            agenda(tipo, fila.nome, tempo_atendimento(fila))
    else:
        fila.perde()


def libera(fila):
    fila.sai()
    if fila.status() >= fila.servidores:
        tipo = "SAIDA" if roteia(fila.nome) is None else "PASSAGEM"
        agenda(tipo, fila.nome, tempo_atendimento(fila))


def chegada(tempo_evento, origem):
    fila = filas[origem]
    acumula(tempo_evento)
    admite(fila, origem)
    dt = entre(*fila.chegada)
    agenda("CHEGADA", origem, None if dt is None else tempo_global + dt)


def passagem(tempo_evento, origem):
    fila = filas[origem]
    acumula(tempo_evento)
    libera(fila)
    destino = roteia(origem)
    if destino is not None:
        admite(filas[destino], destino)


def saida(tempo_evento, origem):
    acumula(tempo_evento)
    libera(filas[origem])


def simula():
    global previous, count, tempo_global, filas, escalonador

    previous, count = SEED, QTD_ALEATORIOS
    tempo_global = 0.0
    escalonador = []
    filas = {nome: Fila(nome, **cfg) for nome, cfg in REDE.items()}

    for nome, fila in filas.items():
        if fila.chegada:
            agenda("CHEGADA", nome, PRIMEIRA_CHEGADA)

    tratadores = {"CHEGADA": chegada, "PASSAGEM": passagem, "SAIDA": saida}
    while count > 0 and escalonador:
        tempo_evento, tipo, origem = min(escalonador)
        escalonador.remove((tempo_evento, tipo, origem))
        tratadores[tipo](tempo_evento, origem)


def relatorio(fila, titulo):
    linhas = ["=" * 62, titulo, "=" * 62, "",
              "Estado      Tempo acumulado      Probabilidade", "-" * 62]
    for i, t in enumerate(fila.tempos):
        linhas.append(f"{i:>4}        {t:>15.4f}      {t / tempo_global * 100:>11.6f} %")
    linhas += ["-" * 62,
               f"{'TOTAL':>4}        {sum(fila.tempos):>15.4f}      {100.0:>11.6f} %", "",
               f"Número de perda de clientes ... {fila.perdas}", ""]
    return "\n".join(linhas)


simula()

saida_final = [
    relatorio(filas["F1"], "Fila 1 | G/G/2/3, chegadas entre 1...5, atendimento entre 4...5"),
    relatorio(filas["F2"], "Fila 2 | G/G/1/5, atendimento entre 1...3"),
    f"Tempo global da simulação ..... {tempo_global:.4f}",
]
texto = "\n".join(saida_final)
print(texto)

with open(Path(__file__).with_name("resultados.txt"), "w", encoding="utf-8") as f:
    f.write(texto + "\n")
