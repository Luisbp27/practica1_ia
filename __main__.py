import agentAmplada
import agentAEstrella
import agentMinMax
import agentGenetic
import joc
import sys
import os

sys.path.append(os.getcwd())


def main():
    menu()
    eleccio = int(input())

    match eleccio:
        case 0:
            raise SystemExit
        case 1:
            rana = agentAmplada.Rana("Luis")
            lab = joc.Laberint([rana], parets=True)
        case 2:
            rana = agentAEstrella.Rana("Luis")
            lab = joc.Laberint([rana], parets=True)
        case 3:
            rana = agentMinMax.Rana("Luis")
            rana2 = agentMinMax.Rana("Victor")
            lab = joc.Laberint([rana, rana2], parets=True)
        case 4:
            rana = agentGenetic.Rana("Luis")
            lab = joc.Laberint([rana], parets=True)

    lab.comencar()


def menu():
    print("\n Elegeix l'algorisme de cerca que vols utilitzar: ")
    print("0. Sortir")
    print("1. Amplada")
    print("2. A*")
    print("3. Min i Max")
    print("4. Genètic")


if __name__ == "__main__":
    main()
