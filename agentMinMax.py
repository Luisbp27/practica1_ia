from ia_2022 import entorn
import joc
from entorn import AccionsRana
from entorn import Direccio
from entorn import ClauPercepcio


ESPERAR = 0.5
BOTAR = 6
MOURE = 1


class Estat:
    def __init__(self, nom, pos_pizza, pos_agent, parets, pare=None):
        self.__nom_agent = nom
        self.__pos_agent = pos_agent
        self.__pos_pizza = pos_pizza
        self.__parets = parets
        self.__pare = pare
        self.__nom_agent2 = None

    def __hash__(self):
        return hash(tuple(self.__pos_agent))

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
        """Mètode que retorna la posició actual de l'agent"""
        return self.__pos_agent

    def es_meta(self, nom) -> bool:
        """Mètode que verifica si un estat es o no meta, en funció de la posició de l'agent i de la posició final"""
        return (
            self.__pos_agent[nom][0] == self.__pos_pizza[0]
            and self.__pos_agent[nom][1] == self.__pos_pizza[1]
        )

    def es_valid(self):
        """Mètode que verifica si un estat es o no vàlid"""
        claus = list(self.__pos_agent.keys())
        self.get_altre_agent()

        # Comprovam que l'agent no estigui en una casella paret
        for paret in self.__parets:
            if (
                self.__pos_agent[self.__nom_agent2][0] == paret[0]
                and self.__pos_agent[self.__nom_agent2][1] == paret[1]
            ):
                return False
                # mirar si hi ha agent

        # Si un agent està a la mateixa fila i columna que l'altre, no és vàlid
        if (
            self.__pos_agent[claus[0]][0] == self.__pos_agent[claus[1]][0]
            and self.__pos_agent[claus[0]][1] == self.__pos_agent[claus[1]][1]
        ):
            return False

        # Comprovam que l'agent no estigui defora el tauler
        return (
            (self.__pos_agent[self.__nom_agent2][0] <= 7)
            and (self.__pos_agent[self.__nom_agent2][0] >= 0)
            and (self.__pos_agent[self.__nom_agent2][1] <= 7)
            and (self.__pos_agent[self.__nom_agent2][1] >= 0)
        )

    def get_altre_agent(self):
        """Mètode que ens indica qui és l'altre agent implicat"""
        claus = list(self.__pos_agent.keys())

        for i in range(2):
            if self.__nom_agent != claus[i]:
                self.__nom_agent2 = claus[i]

    def calcular_puntuacio(self, nom):
        """Mètode que calcula la distància entre l'agent i la pizza"""
        suma = 0

        for i in range(2):
            suma += abs(self.__pos_pizza[i] - self.__pos_agent[nom][i])

        return suma

    def calcular_puntuacio_agents(self, nom):
        """Mètode que compara les puntuacions dels dos agents"""
        claus = list(self.__pos_agent.keys())

        if nom == claus[0]:
            puntuacio = self.calcular_puntuacio(claus[1]) - self.calcular_puntuacio(
                claus[0]
            )
        else:
            puntuacio = self.calcular_puntuacio(claus[0]) - self.calcular_puntuacio(
                claus[1]
            )

        return puntuacio

    def genera_fills(self):
        """Mètode que genera tot l'abre d'accions"""
        self.get_altre_agent()
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
            coordenades = [
                sum(tup) for tup in zip(self.__pos_agent[self.__nom_agent], m)
            ]
            nueva = self.__pos_agent.copy()
            nueva[self.__nom_agent] = coordenades

            actual = Estat(
                self.__nom_agent2,
                self.__pos_pizza,
                nueva,
                self.__parets,
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
            coordenades = [
                sum(tup) for tup in zip(self.__pos_agent[self.__nom_agent], m)
            ]
            nou_agent = self.__pos_agent.copy()
            nou_agent[self.__nom_agent] = coordenades

            actual = Estat(
                self.__nom_agent2,
                self.__pos_pizza,
                nou_agent,
                self.__parets,
                (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))),
            )

            if actual.es_valid():
                fills.append(actual)

        return fills


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__botar = 0
        self.__meta = False

    def _cerca(self, estat: Estat, profunditat, torn_max=True):
        """Mètode que realitza la cerca del cami per arribar a l'estat meta; utilitzant l'algorisme de cerca Min i Max"""
        # Calculam les respectives puntuacions dels agents
        score = estat.calcular_puntuacio_agents(self.nom)

        if estat.es_meta(self.nom) or profunditat == 2:
            return score, estat

        # Generam els estats fills corresponents
        puntuacio_fills = [
            self._cerca(estat_fill, profunditat + 1, not torn_max)
            for estat_fill in estat.genera_fills()
        ]

        # Depenent de qui tengui el torn, maximizam o minimitzam el resultat
        if torn_max:
            return max(puntuacio_fills)
        else:
            return min(puntuacio_fills)

    def pinta(self, display):
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        estat: Estat = Estat(
            self.nom,
            percep[ClauPercepcio.OLOR],
            percep[ClauPercepcio.POSICIO],
            percep[ClauPercepcio.PARETS],
        )

        if not self.__meta:
            actual = self._cerca(estat, 0)[1]

        agent = percep[ClauPercepcio.POSICIO].keys()

        for a in agent:
            # Si l'agent està en la posició final
            if percep[ClauPercepcio.POSICIO][a] == percep[ClauPercepcio.OLOR]:
                self.__meta = True

        # Si qualque agent ha guanyat, no es mouen
        if self.__meta:
            return AccionsRana.ESPERAR

        accio = None

        while actual.pare is not None:
            pare, accio = actual.pare
            actual = pare

        # Si acaba de botar, ha d'esperar
        if self.__botar > 0:
            self.__botar -= 1
            return AccionsRana.ESPERAR

        # Si ha de botar o si ha de mourer-se a una casella adjacent
        else:
            if accio[0] == AccionsRana.BOTAR:
                self.__botar = 2

            return accio[0], accio[1]
