import joc
import agent
import sys

sys.path.append("/home/luisb/Documentos/GitHub/ia_2022")


def main():
    rana = agent.Rana("Miquel")
    lab = joc.Laberint([rana], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
