from ia_2022 import entorn
import joc
from entorn import AccionsRana, Direccio, ClauPercepcio
import random

ESPERAR = 0.5
BOTAR = 6
MOURE = 1


class Estat:
    max_individus = 20
    moviments = {
        (AccionsRana.MOURE, Direccio.DALT): (0, -1),
        (AccionsRana.MOURE, Direccio.BAIX): (0, +1),
        (AccionsRana.MOURE, Direccio.ESQUERRE): (-1, 0),
        (AccionsRana.MOURE, Direccio.DRETA): (+1, 0),
        (AccionsRana.BOTAR, Direccio.DALT): (0, -2),
        (AccionsRana.BOTAR, Direccio.BAIX): (0, +2),
        (AccionsRana.BOTAR, Direccio.ESQUERRE): (-2, 0),
        (AccionsRana.BOTAR, Direccio.DRETA): (+2, 0),
        (AccionsRana.ESPERAR, None): (0, 0),
    }

    def __init__(self, nom, pos_pizza, pos_agent, parets) -> None:
        self.__nom = nom
        self.__pos_pizza = pos_pizza
        self.__pos_agent = pos_agent
        self.__parets = parets

    def __hash__(self):
        return hash(tuple(self.__accions))

    def __lt__(self, other):
        return False

    def crear_estat():
        pass

    def calcular_f(self):
        """Mètode que calcula la f(n)"""
        suma = 0

        for i in range(2):
            suma += abs(self.__pos_pizza[i] - self.__pos_agent[self.nom_agent][i])

        return suma + self.__pes


class Rana(joc.Rana):
    accions_generades = [(AccionsRana.BOTAR, direccio) for direccio in Direccio] + [
        (AccionsRana.MOURE, direccio) for direccio in Direccio
    ]

    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__accions = None
        self.__botar = 0

    def calcular_fitness(
        self, estat: Estat, individu: list[tuple[AccionsRana, Direccio]]
    ):
        for accio, direccio in individu:
            estat = estat.crear_estat(self.nom, accio, direccio)

        return estat.calcular_f()

    def generar_accions(self, percep: entorn.Percepcio):
        self.__accions = self._cerca(Estat.from_percep(percep, None), 50, 10, 25, 0.1)

    def _cerca(self, estat: Estat, tamany_poblacio, accions, creuaments, mutacio):
        individus = tamany_poblacio // 2

        # Cream una població aleatoria
        poblacio = []

        for _ in range(tamany_poblacio):
            for _ in range(accions):
                poblacio.append(random.choice(self.accions_generades))

        # Iteram fins a trobar un individu que arribi a la posició final
        while True:
            # Seleccionam la poblacio segons la funció fitness
            poblacio_fitness = sorted(
                ((i, self.calcular_fitness(estat, i)) for i in poblacio),
                key=lambda i: i[1],
            )[:individus]

            # Si obtenim una solucio, la retornam
            for i, fitness in poblacio_fitness:
                return individus[i] if fitness == 0 else None

            # Actuialitzam la poblacio
            poblacio = []
            for i in poblacio_fitness:
                poblacio.append(i)

            # Realitzam els respectius creuaments dels fills amb els pares
            for _ in range(creuaments):
                pare_1 = random.choice(poblacio)
                pare_2 = random.choice(poblacio)

                fill_1 = pare_1[: accions // 2] + pare_2[accions // 2 :]
                fill_2 = pare_2[: accions // 2] + pare_1[accions // 2 :]

                poblacio.append(fill_1)
                poblacio.append(fill_2)

            # Realitzam la respectiva mutació dels fills
            for i in poblacio:
                if random.random() < mutacio:
                    # Modificam un  individu aleatori de la població
                    i[random.randInt(0, len(poblacio) - 1)] - random.choice(
                        self.accions_generades
                    )

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

        # Si no tenim accions, les cercam
        if self.__accions is None:
            self._cerca(estat, 30, 8, 35, 0.15)
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
