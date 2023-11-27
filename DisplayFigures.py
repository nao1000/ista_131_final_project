"""
    File: DisplayFigures.py
    Name: Nathan Oswald
    Section Leader: Chase Hult
    Date: November 27th, 2023
    Course: ISTA 131
    Assignment: Final
    Description: This program imports all the figure-making programs and shows them all.
"""
import matplotlib.pyplot as plt

from ERAvsOPS import ERAvsOPS
from ChampionsERA_OPS import ChampionsERA_OPS
from pitchersPer9 import pitchersPer9

def main():
    ERAvsOPS()
    ChampionsERA_OPS()
    pitchersPer9()
    plt.show()

if __name__ == '__main__':
    main()