"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""

from ia_2022 import entorn
import joc
from entorn import AccionsRana
from entorn import Direccio
from queue import PriorityQueue

ESPERAR = 0.5
BOTAR = 6
MOURE = 1


class Estat:
    def __init__(self, pos_pizza, pos_agent, parets, pes=0, pare=None):
        self.__pos_pizza = pos_pizza
        self.__pos_agent = pos_agent
        self.__parets = parets
        self.__pes = pes
        self.__pare = pare

    def __hash__(self):
        return hash(tuple(self.__pos_agent))

    @property
    def info(self):
        return self.__pos_agent

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return self.__pos_agent == other.get_pos_agent()

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def get_pos_agent(self):
        return self.__pos_agent

    def es_meta(self) -> bool:
        return (
            self.__pos_agent["Rana"][0] == self.__pos_pizza[0]
            and self.__pos_agent["Rana"][1] == self.__pos_pizza[1]
        )

    def es_valid(self):
        """Retorn vertader si la posició està dins el tauler"""
        # mirar si hi ha parets

        for pared in self.__parets:
            if (
                self.__pos_agent["Rana"][0] == pared[0]
                and self.__pos_agent["Rana"][1] == pared[1]
            ):
                return False

        # mirar si esta dins el tauler
        return (
            (self.__pos_agent["Rana"][0] <= 7)
            and (self.__pos_agent["Rana"][0] >= 0)
            and (self.__pos_agent["Rana"][1] <= 7)
            and (self.__pos_agent["Rana"][1] >= 0)
        )

    def calcular_f(self):
        sum = 0
        for i in range(2):
            sum += abs(self.__pos_pizza[i] - self.__pos_agent["Rana"][i])
        return self.__pes + sum

    def generaFills(self):
        movs = {"ESQUERRE": (-1, 0), "DRETA": (+1, 0), "DALT": (0, -1), "BAIX": (0, +1)}
        claus = list(movs.keys())
        fills = []

        """
        Cas 1: Moviments de desplaçament a caselles adjacents.
        """
        for i, m in enumerate(movs.values()):
            coords = [sum(tup) for tup in zip(self.__pos_agent["Rana"], m)]
            coord = {"Rana": coords}
            # coords=[(0,0)]
            cost = self.__pes + MOURE
            actual = Estat(
                self.__pos_pizza,
                coord,
                self.__parets,
                cost,
                (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))),
            )
            if actual.es_valid():
                fills.append(actual)

        """
        Cas 2: Moviments de desplaçament de 2 caselles en caselles
        """
        movs = {"ESQUERRE": (-2, 0), "DRETA": (+2, 0), "DALT": (0, -2), "BAIX": (0, +2)}
        for i, m in enumerate(movs.values()):
            coords = [sum(tup) for tup in zip(self.__pos_agent["Rana"], m)]
            coord = {"Rana": coords}
            cost = self.__pes + BOTAR

            actual = Estat(
                self.__pos_pizza,
                coord,
                self.__parets,
                cost,
                (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))),
            )

            if actual.es_valid():
                fills.append(actual)

        return fills


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__accions = None
        self.__tancats = None
        self.__oberts = None
        self.__botar = 0

    def _cerca(self, estat: Estat):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat.calcular_f(), estat))
        actual = None

        while not self.__oberts.empty():
            # si un retorn no t'interessa li posam _S
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if not actual.es_valid():
                self.__tancats.add(actual)
                continue

            estats_fills = actual.generaFills()

            if actual.es_meta():
                break

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calcular_f(), estat_f))

            self.__tancats.add(actual)

        if actual.es_meta():
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare
                accions.append(accio)
                iterador = pare

            self.__accions = accions

    def pinta(self, display):
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        percepcions = percep.to_dict()
        claus = list(percepcions.keys())
        # percep[claus[0]] = pizza, percep[claus[1]] = rana, percep[claus[2]] = paredes
        estat: Estat = Estat(percep[claus[0]], percep[claus[1]], percep[claus[2]])

        if self.__accions is None:
            self._cerca(estat=estat)
            print(self.__accions)

        if self.__accions:
            if self.__botar > 0:
                self.__botar -= 1
                return AccionsRana.ESPERAR

            else:
                accio = self.__accions.pop()

                if accio[0] == AccionsRana.BOTAR:
                    self.__botar = 2

                return accio[0], accio[1]
        else:
            return AccionsRana.ESPERAR
