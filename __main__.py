import agentAmplada
import agentAEstrella
import agentMinMax
import joc
import sys
import os

sys.path.append(os.getcwd())


def main():
    rana = agentAmplada.Rana("Luis")
    lab = joc.Laberint([rana], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
