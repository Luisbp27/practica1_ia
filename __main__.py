import agentAmplada
import agentAEstrella
import agentMinMax
import joc
import sys
import os

sys.path.append(os.getcwd())


def main():
    rana = agentMinMax.Rana("Rana")
    rana2 = agentMinMax.Rana("Victor")
    lab = joc.Laberint([rana, rana2], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
