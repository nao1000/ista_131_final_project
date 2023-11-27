"""
    File: ChampionsERA.py
    Name: Nathan Oswald
    Section Leader: Chase Hult
    Date: November 27th, 2023
    Course: ISTA 131
    Assignment: Final
    Description: This program creates the second figure that shows which type of team has won the WS from
                1905-2015. The winners can be in one of five categories: Balanced, Leaning (Pitching or Batting), or
                Strongly Favoring (Pitching or Batting). The balanced teams are also broken down to see how they
                stack up overall.
    Credit: https://matplotlib.org/stable/gallery/pie_and_polar_charts/bar_of_pie.html#sphx-glr-gallery-pie-and-polar-charts-bar-of-pie-py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import ConnectionPatch

def ChampionsERA_OPS():
    """
    This function does as described above.
    """
    df = pd.read_csv("WinnersWithOPSandERA.csv", dtype ={"Year":str, "Team":str,"ERA":float,
                                                         "OPS":float, "OPSrank":int, "ERArank":int})

    ## storing team types
    dict2 = {'Balanced': 0, 'Leans to Pitching': 0, "Leans to Batting": 0, "Strongly Favors Pitching":0,
             "Strongly Favors Batting":0}
    withinteams = []
    for row in df.index:

        ## balanced teams have ranks within 2
        if abs(df.loc[row, "OPSrank"]  - df.loc[row, "ERArank"]) <= 2:
            dict2['Balanced'] += 1
            withinteams.append(df.loc[row,"OPS":].values) ## save them for later

        ## leaning has either OPS or ERA rank be more than 2 up to 5 spots different
        elif df.loc[row, "OPSrank"]  - df.loc[row, "ERArank"] > 2 and df.loc[row, "OPSrank"]  - df.loc[row, "ERArank"] <= 5:
            dict2['Leans to Batting'] += 1
        elif df.loc[row, "ERArank"]  - df.loc[row, "OPSrank"] > 2 and df.loc[row, "ERArank"]  - df.loc[row, "OPSrank"] <= 5:
            dict2['Leans to Pitching'] += 1

        ## strongly is more than 5 difference
        elif df.loc[row, "OPSrank"]  - df.loc[row, "ERArank"] > 5:
            dict2['Strongly Favors Batting'] += 1
        else:
            dict2['Strongly Favors Pitching'] += 1

    ## 110 winners
    total=110
    perc = []  ##percent of which type one
    label = [] ##type that won
    for key, value in dict2.items():
        label.append(key)
        perc.append(round(value/total * 100, 1))

    ## plotting a pie chart with a bar as well
    ## a lot of the code is credited to the Matplot website page
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)
    explode = [0.1,0,0,0,0]
    angle = 45 * perc[0]
    wedges, *_ = ax1.pie(perc,startangle =angle ,labels=label,explode=explode, autopct='%1.1f%%',
                         textprops={'fontsize': 14})

    ## overall rankings I made as the average of the OPS and ERA rank
    overall_dict = {"Top 3": 0, "Top 4 to 7" : 0, "Top 8 to 10": 0}
    for team in withinteams:
        if (team[1] + team[3])/2 < 4:
            overall_dict['Top 3'] += 1
        elif (team[1] + team[3])/2 < 8:
            overall_dict['Top 4 to 7'] += 1
        else:
            overall_dict['Top 8 to 10'] += 1

    label2 =[] ##top x-y
    perc2= [] ##percent of top x-y
    for key, value in overall_dict.items():
        label2.append(key)
        perc2.append(value/sum(overall_dict.values()))

    ## more matplot credit
    bottom = 1
    width = .2
    for j, (height, label) in enumerate(reversed([*zip(perc2, label2)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                     alpha=0.1 + 0.25 * j)
        ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

    ax2.set_title('Overall Ranking of "Balanced" World Series Winners')
    ax2.legend()
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(perc2)

    # draw top connecting line (matplot)
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(4)
    ax2.add_artist(con)

    # draw bottom connecting line (matplot)
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(4)