import agentAmplada
import agentAEstrella
import joc
import sys
import os

sys.path.append(os.getcwd())


def main():
    rana = agentAEstrella.Rana("Rana")
    lab = joc.Laberint([rana], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
