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

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return self.__pos_agent == other.get_pos_agent()

    @property
    def info(self):
        return self.__pos_agent

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def get_pos_agent(self):
        """Mètode que retorna la posició actual de l'agent"""
        return self.__pos_agent

    def es_meta(self, nom: str) -> bool:
        """Mètode que verifica si un estat es o no meta, en funció de la posició de l'agent i de la posició final"""
        return (
            self.__pos_agent[nom][0] == self.__pos_pizza[0]
            and self.__pos_agent[nom][1] == self.__pos_pizza[1]
        )

    def es_valid(self):
        """Mètode que verifica si un estat es o no vàlid"""
        # Comprovam que l'agent no estigui en una casella paret
        for paret in self.__parets:
            if (
                self.__pos_agent["Rana"][0] == paret[0]
                and self.__pos_agent["Rana"][1] == paret[1]
            ):
                return False

        # Comprovam que l'agent no estigui defora el tauler
        return (
            (self.__pos_agent["Rana"][0] <= 7)
            and (self.__pos_agent["Rana"][0] >= 0)
            and (self.__pos_agent["Rana"][1] <= 7)
            and (self.__pos_agent["Rana"][1] >= 0)
        )

    def calcular_heuristica(self):
        sum = 0

        for i in range(2):
            sum += abs(self.__pos_pizza[i] - self.__pos_agent["Rana"][i])

        return sum

    def genera_fills(self):
        """Mètode que genera tot l'abre d'accions"""
        fills = []

        moviments = {
            "ESQUERRE": (-1, 0),
            "DRETA": (+1, 0),
            "DALT": (0, -1),
            "BAIX": (0, +1),
        }
        claus = list(moviments.keys())

        # Cas 1: Desplaçament a una casella adjacent, no diagonal
        for i, m in enumerate(moviments.values()):
            coordenades = [sum(tup) for tup in zip(self.__pos_agent["Rana"], m)]
            moviment = {"Rana": coordenades}

            actual = Estat(
                self.__pos_pizza,
                moviment,
                self.__parets,
                self.calcular_heuristica(),
                (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))),
            )

            if actual.es_valid():
                fills.append(actual)

        # Cas 2: Desplaçament a dues caselles adjacents, no diagonal (botar paret)
        moviments = {
            "ESQUERRE": (-2, 0),
            "DRETA": (+2, 0),
            "DALT": (0, -2),
            "BAIX": (0, +2),
        }
        for i, m in enumerate(moviments.values()):
            coordenades = [sum(tup) for tup in zip(self.__pos_agent["Rana"], m)]
            moviment = {"Rana": coordenades}

            actual = Estat(
                self.__pos_pizza,
                moviment,
                self.__parets,
                self.calcular_heuristica(),
                (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))),
            )

            if actual.es_valid():
                fills.append(actual)

        return fills

    def evaluar(self, estat):
        if estat.es_meta():
            return self.__puntuacio


class Rana(joc.Rana):
    def __init__(self, nom, *args, **kwargs):
        super(Rana, self).__init__(nom, *args, **kwargs)

        self.__accions = None
        self.__botar = 0
        self.__puntuacio = 0
        self.__nom = nom

    def _cerca(self, estat: Estat, torn_max, nom: str):
        """Mètode que realitza la cerca del cami òptim per arribar a l'estat meta; utilitzant l'algorisme de cerca Min i Max"""
        score = estat.evaluar(estat)
        if score:
            return score

        puntuacio_fills = [
            self._cerca(estat, not torn_max, nom) for estat in estat.genera_fills()
        ]
        if torn_max:
            return max(puntuacio_fills)
        else:
            return min(puntuacio_fills)

    def pinta(self, display):
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        percepcions = percep.to_dict()
        claus = list(percepcions.keys())
        # percep[claus[0]] = pizza, percep[claus[1]] = rana, percep[claus[2]] = paretes
        estat: Estat = Estat(percep[claus[0]], percep[claus[1]], percep[claus[2]])

        # Si no tenim accions, les cercam
        if self.__accions is None:
            self._cerca(estat=estat, torn_max=True)
            print(self.__accions)

        # Si tenim les accions
        if self.__accions:
            # Si acaba de botar, ha d'esperar
            if self.__botar > 0:
                self.__botar -= 1
                return AccionsRana.ESPERAR

            # Si ha de botar o si ha de mourer-se a una casella adjacent
            else:
                accio = self.__accions.pop()

                if accio[0] == AccionsRana.BOTAR:
                    self.__botar = 2

                return accio[0], accio[1]

        # Sino esperam
        else:
            return AccionsRana.ESPERAR
