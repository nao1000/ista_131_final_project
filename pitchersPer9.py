"""
    File: pitcherPer9.py
    Name: Nathan Oswald
    Section Leader: Chase Hult
    Date: November 27th, 2023
    Course: ISTA 131
    Assignment: Final
    Description: This program plots the third figure that shows how an average game for every year would like.
                 This is done by looking at the league average hits, homeruns, walks, and strikeouts
                 oer 9 innings (the length of a normal game).
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

def pitchersPer9():
    """
    This function does as described above.
    :return:
    """
    df = pd.read_csv("yearlyPitchingTotals(BR).csv", usecols = [0,26,27,28,29], index_col=0)

    ## simple plot of the df, added shadow behind the lines to look nicer
    ## this was an easy plot but one I can talk a good amount about
    df.plot(path_effects=[pe.SimpleLineShadow(shadow_color='black'), pe.Normal()])
    plt.title("League Game Average Hit, Homerun, Walk, and Strikeout Numbers Per Year",fontsize=20)
    plt.xlabel('Year', fontsize = 24)
    plt.ylabel('Amount of H/HR/W/SO per 9 Innings', fontsize = 24)

    ax = plt.gca()
    ax.set_xlim(1871, 2023)
    ax.set_facecolor('lightsteelblue')
    plt.legend(fontsize=15)