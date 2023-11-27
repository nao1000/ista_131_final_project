"""
    File: ERAvsOPS.py
    Name: Nathan Oswald
    Section Leader: Chase Hult
    Date: November 27th, 2023
    Course: ISTA 131
    Assignment: Final
    Description: This program creates the first figure that models the linear relationship of ERA and OPS.
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


def ERAvsOPS():
    """
    This function does exactly as the description above says.
    """
    df = pd.read_csv("yearlyPitchingTotals(BR).csv", usecols=[0,5,24,29], index_col=0)
    df2 = pd.read_csv('yearlyBattingTotals(BR).csv', usecols=[0,19,20,21,22], index_col=0)

    ##Take the era data from the first df as indices and the ops data from the second df
    s = pd.Series(index=df.iloc[:,0].values, data=df2.iloc[:,3].values)


    ## era labels, their years, and the colors that associate with them
    eras = ["Pre-20th Cent. (1871-1899)", "Dead Ball (1900-1920)", "Lively Ball (1921-1945)", "Post-War (1946-1960)"
        , "Expansion (1961-1972)", "Pre-Steroid (1973-1993)", "Steroid (1994-2004)", "Modern (2005-2023)"]
    years = [(1871, 1899), (1900,1920), (1921, 1945), (1946,1960), (1961,1972), (1973, 1993), (1994, 2004), (2005, 2023)]
    colors = ["black", "red", "green", 'yellow', 'purple', "orange",'blue', 'magenta']

    spot = 0 ## keep track of series location

    ## reveres because I wrote the lists in the wrong order
    eras.reverse()
    years.reverse()
    colors.reverse()
    edge = "gold"
    for era, block, color in zip(eras,years, colors):
        ##plot each era accordingly
        plt.scatter(x = s.index[spot:spot+(block[1] - block[0]) + 1], y = s.values[spot:spot+(block[1] - block[0]) + 1],
                    label = era, color= color, s=65, edgecolors=edge)
        spot += block[1] - block[0] + 1

        ## silver represents before AL had universal DH
        if era == "Pre-Steroid (1973-1993)":
            edge = 'silver'


    plt.legend()

    ## get regression line
    x = s.index.values
    X = sm.add_constant(x)
    model = sm.OLS(s, X)
    result = model.fit()
    slope = result.params["x1"]
    intercept = result.params["const"]
    r_2 = result.rsquared


    ##some labeling
    ax = plt.gca()
    ax.set_xlim(2,6)
    ax.set_ylim(0.500,0.900)
    plt.axline(xy1=(0,intercept), slope=slope, color='springgreen')
    ax.set_facecolor('lightslategray')
    plt.ylabel("OPS (On-base% + Slugging%)", fontsize = 24)
    plt.xlabel("ERA (Earned Runs Average)",fontsize = 24)
    plt.title("ERA vs OPS by Year and Divided by Era", fontsize =24)