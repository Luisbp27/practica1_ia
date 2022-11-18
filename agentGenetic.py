from ia_2022 import entorn
import joc
from entorn import AccionsRana
from entorn import Direccio
from queue import PriorityQueue
import random
import operator

ESPERAR = 0.5
BOTAR = 6
MOURE = 1


class Individu:
    max_individus = 20
    moviments = {(AccionsRana.MOURE, Direccio.DALT): (0, -1), (AccionsRana.MOURE, Direccio.BAIX): (0, +1),
                (AccionsRana.MOURE, Direccio.ESQUERRE): (-1, 0), (AccionsRana.MOURE, Direccio.DRETA): (+1, 0),
                (AccionsRana.BOTAR, Direccio.DALT): (0, -2), (AccionsRana.BOTAR, Direccio.BAIX): (0, +2), 
                (AccionsRana.BOTAR, Direccio.ESQUERRE): (-2, 0), (AccionsRana.BOTAR, Direccio.DRETA): (+2, 0),
                (AccionsRana.ESPERAR, None): (0, 0)}

    def __init__(self, nom, pos_pizza, pos_agent, parets, individu) -> None:
        self.__nom = nom
        self.__pos_pizza = pos_pizza
        self.__pos_agent = pos_agent
        self.__parets = parets
        self.__accions = individu

    def __hash__(self):
        return hash(tuple(self.__accions))

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return self.__accions == other.get_accions()

    def get_accions(self):
        return self.__accions

    @classmethod
    def crear_individu(self, ind):
        individu = []

        for i in range(ind.max_individus):
            individu.append(list(ind.moviments.values())[random.randint(0, 8)])

        return individu

    def fitness(self):
        posicio = self.__pos_agent[self.__nom]

        for i in range(len(self.__accions)):
            posicio = tuple(map(operator.add, posicio, self.__accions[i]))
            fitness = abs(self.__pos_pizza[0] - posicio[0]) + abs(self.__pos_pizza[1] - posicio[1])

        return fitness

class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__accions = None
        self.__botar = 0
        self.__meta = False

    def _cerca(self, pizza, agent, parets):
        """ "Mètode que realitza la cerca del primer camí fins a la porció de pizza, mitjançant una cerca genètica"""
        individus = PriorityQueue()
        fills = []
        generacio = 0

        # Generam la població inicial
        for i in range(20):
            accions = Individu.crear_individu()
            individu = Individu(self.nom, pizza, agent, parets, accions)

            puntuacio = individu.fitness()
            individus.put((individu, puntuacio))

        # Mentres no trobem solució
        while not Rana.__meta:
            # Cada 3 generacions, retornam una llista d'individus
            if generacio == 3:
                break

            # Generam tots els individus
            for i in range():
                pass

            # Afegim els fills a la cua de prioritat
            for i in range(len(fills)):
                individus.put((fills[i].fitness, fills[i]))

            # Seleccionam els millors 30 individus a la cua de prioritat (previament buidada)
            temp = individus
            individus = PriorityQueue()
            for i in range(30):
                individus.put(temp.get())

            # Cercam algun individu que ens doni la solucio, fitness = 0
            if list(individus.queue)[0][0] == 0:
                Rana.__meta = True

            generacio += 1

        return list(individus.queue)[0][1]

    def pinta(self, display):
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        
        if self.__accions is not None:
            if self.__botar <= 0:
                accio = self.__accions.pop(0)
            else:    
                self.__botar -= 1
                return

        else:
            individu = self._cerca()
            self.__accions = individu.get_accions()


        
