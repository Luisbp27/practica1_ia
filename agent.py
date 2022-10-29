"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from tokenize import ContStr
from turtle import pos

from numpy import append
from ia_2022 import entorn
import joc
from entorn import AccionsRana

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

    def __eq__(self, other):
        return self.__pos_agent == other.info

    def es_meta(self) -> bool:
        return self.__pos_agent == self.__pos_pizza

    def es_valid(self, estat) -> bool:
        """Retorn vertader si la posició està dins el tauler"""
        pass

    def generaFills(self):
        fills = []

        def fn(accions):
            for moviment in accions.values():
                coordenades = [
                    sum(elem) for elem in zip(self.__pos_agent["Rana", moviment])
                ]
                f = self.heuristica()

                estat = Estat(
                    self.__pos_pizza,
                    {"Rana": coordenades},
                    self.__parets,
                    f,
                )

                if estat.es_valid():
                    fills.append(estat)

        # Cas 1: Quan l'agent només s'ha de moure 1 casella adjacent
        # Les posicions estan per (C, F)
        accions = {"OEST": (-1, 0), "NORD": (0, -1), "EST": (+1, 0), "SUD": (0, +1)}
        fn(accions)

        # Cas 2: Quan l'agent ha s'ha de moure 2 caselles (quan bota)
        accions = {"OEST": (-2, 0), "NORD": (0, -2), "EST": (+2, 0), "SUD": (0, +2)}
        fn(accions)

        return fills

    def calcular_f():
        # Aplicam la distància Manhattan
        heuristica = 0
        pes = 0

        return heuristica + pes


class Rana(joc.Rana):
    def __init__(self, nom, *args, **kwargs):
        super(Rana, self).__init__(nom, *args, **kwargs)
        self.__accions

    def pinta(self, display):
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        percepcions = percep.to_dict()
        claus = list(percepcions.keys())
        estat = Estat(percep[claus[0]], percep[claus[1]], percep[claus[2]])

        # [ 0, x, T ]
        # [ x, A, x ]
        # [ 0, x, 0 ]

        return AccionsRana.ESPERAR
