import sys
from pathlib import Path

A = 1_103_515_245
C = 12_345
M = 2 ** 31


def escalar(txt):
    txt = txt.strip()
    if len(txt) >= 2 and txt[0] == txt[-1] and txt[0] in "'\"":
        return txt[1:-1]
    for conversao in (int, float):
        try:
            return conversao(txt)
        except ValueError:
            pass
    if txt.lower() in ("true", "false"):
        return txt.lower() == "true"
    return None if txt.lower() in ("null", "~", "") else txt


def divide(txt):
    partes, nivel, atual = [], 0, ""
    for ch in txt:
        nivel += (ch in "[{") - (ch in "]}")
        if ch == "," and nivel == 0:
            partes.append(atual)
            atual = ""
        else:
            atual += ch
    return partes + ([atual] if atual.strip() else [])


def valor(txt):
    txt = txt.strip()
    if txt.startswith("{") and txt.endswith("}"):
        return {k.strip(): valor(v) for k, _, v in (p.partition(":") for p in divide(txt[1:-1]))}
    if txt.startswith("[") and txt.endswith("]"):
        return [valor(p) for p in divide(txt[1:-1])]
    return escalar(txt)


def bloco(linhas, i, recuo):
    if linhas[i][1] == "-" or linhas[i][1].startswith("- "):
        sequencia = []
        while i < len(linhas) and linhas[i][0] == recuo and linhas[i][1].split(" ")[0] == "-":
            cabeca, item, i = linhas[i][1][1:].strip(), [], i + 1
            corpo = []
            while i < len(linhas) and linhas[i][0] > recuo:
                corpo.append(linhas[i])
                i += 1
            if cabeca:
                item = [(corpo[0][0] if corpo else recuo + 2, cabeca)] + corpo
            else:
                item = corpo
            if not item:
                sequencia.append(None)
            elif len(item) == 1 and ":" not in item[0][1]:
                sequencia.append(valor(item[0][1]))
            else:
                sequencia.append(bloco(item, 0, item[0][0])[0])
        return sequencia, i
    mapa = {}
    while i < len(linhas) and linhas[i][0] == recuo:
        chave, _, resto = linhas[i][1].partition(":")
        i += 1
        if resto.strip():
            mapa[chave.strip()] = valor(resto)
        elif i < len(linhas) and linhas[i][0] > recuo:
            mapa[chave.strip()], i = bloco(linhas, i, linhas[i][0])
        else:
            mapa[chave.strip()] = None
    return mapa, i


def carrega_modelo(caminho):
    linhas = []
    for linha in Path(caminho).read_text(encoding="utf-8").splitlines():
        corpo = linha.split("#", 1)[0].rstrip()
        if corpo.strip():
            linhas.append((len(corpo) - len(corpo.lstrip()), corpo.strip()))
    return bloco(linhas, 0, linhas[0][0])[0] if linhas else {}


class Fila:
    def __init__(self, nome, cfg):
        self.nome = nome
        self.servidores = int(cfg.get("servers", 1))
        capacidade = cfg.get("capacity")
        self.capacidade = float("inf") if capacidade is None else int(capacidade)
        self.atendimento = (cfg["minService"], cfg["maxService"])
        self.chegada = (cfg["minArrival"], cfg["maxArrival"]) if "minArrival" in cfg else None
        self.clientes = 0
        self.perdas = 0
        self.tempos = [0.0] * (self.capacidade + 1 if self.capacidade != float("inf") else 1)

    def marca(self, dt):
        while len(self.tempos) <= self.clientes:
            self.tempos.append(0.0)
        self.tempos[self.clientes] += dt

    def descricao(self):
        limite = "" if self.capacidade == float("inf") else f"/{self.capacidade}"
        texto = f"{self.nome} | G/G/{self.servidores}{limite}"
        if self.chegada:
            texto += f", chegadas entre {self.chegada[0]:g}...{self.chegada[1]:g}"
        return texto + f", atendimento entre {self.atendimento[0]:g}...{self.atendimento[1]:g}"


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


def acumula(tempo_evento):
    global tempo_global
    dt = tempo_evento - tempo_global
    for fila in filas.values():
        fila.marca(dt)
    tempo_global = tempo_evento


def tempo_atendimento(fila):
    dt = entre(*fila.atendimento)
    return None if dt is None else tempo_global + dt


def destino_de(origem):
    rotas = roteamento[origem]
    if len(rotas) == 1:
        return rotas[0][0]
    u = next_random()
    if u is None:
        return None
    acumulado = 0.0
    for destino, p in rotas:
        acumulado += p
        if u < acumulado:
            return destino
    return rotas[-1][0]


def admite(fila):
    if fila.clientes < fila.capacidade:
        fila.clientes += 1
        if fila.clientes <= fila.servidores:
            agenda("SAIDA", fila.nome, tempo_atendimento(fila))
    else:
        fila.perdas += 1


def libera(fila):
    fila.clientes -= 1
    if fila.clientes >= fila.servidores:
        agenda("SAIDA", fila.nome, tempo_atendimento(fila))


def chegada(tempo_evento, origem):
    fila = filas[origem]
    acumula(tempo_evento)
    admite(fila)
    dt = entre(*fila.chegada)
    agenda("CHEGADA", origem, None if dt is None else tempo_global + dt)


def saida(tempo_evento, origem):
    acumula(tempo_evento)
    libera(filas[origem])
    destino = destino_de(origem)
    if destino is not None:
        admite(filas[destino])


def monta_roteamento(modelo, nomes):
    rotas = {nome: [] for nome in nomes}
    for aresta in modelo.get("network") or []:
        rotas[aresta["source"]].append((aresta["target"], float(aresta["probability"])))
    for nome, destinos in rotas.items():
        saida_sistema = 1.0 - sum(p for _, p in destinos)
        if saida_sistema > 1e-9 or not destinos:
            destinos.append((None, saida_sistema))
    return rotas


def simula(modelo, semente):
    global previous, count, tempo_global, filas, escalonador, roteamento

    previous = int(semente)
    count = int(modelo.get("rndnumbersPerSeed", 100_000))
    tempo_global = 0.0
    escalonador = []
    filas = {nome: Fila(nome, cfg) for nome, cfg in modelo["queues"].items()}
    roteamento = monta_roteamento(modelo, filas)

    for nome, instante in (modelo.get("arrivals") or {}).items():
        agenda("CHEGADA", nome, float(instante))

    tratadores = {"CHEGADA": chegada, "SAIDA": saida}
    while count > 0 and escalonador:
        evento = min(escalonador)
        escalonador.remove(evento)
        tratadores[evento[1]](evento[0], evento[2])


def relatorio(fila):
    linhas = ["=" * 62, fila.descricao(), "=" * 62, "",
              "Estado      Tempo acumulado      Probabilidade", "-" * 62]
    for i, t in enumerate(fila.tempos):
        linhas.append(f"{i:>4}        {t:>15.4f}      {t / tempo_global * 100:>11.6f} %")
    linhas += ["-" * 62,
               f"{'TOTAL':>4}        {sum(fila.tempos):>15.4f}      {100.0:>11.6f} %", "",
               f"Número de perda de clientes ... {fila.perdas}", ""]
    return "\n".join(linhas)


def main():
    if len(sys.argv) < 2:
        print("uso: python3 simulador.py <modelo.yml> [saida.txt]")
        return 1
    modelo = carrega_modelo(sys.argv[1])
    destino = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(sys.argv[1]).with_suffix(".txt")

    partes = []
    for semente in modelo.get("seeds") or [7]:
        simula(modelo, semente)
        partes.append(f"Semente ....................... {int(semente)}")
        partes += [relatorio(fila) for fila in filas.values()]
        partes.append(f"Tempo global da simulação ..... {tempo_global:.4f}\n")

    texto = "\n".join(partes)
    print(texto)
    destino.write_text(texto + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
