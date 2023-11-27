"""
    File: analyze.py
    Name: Nathan Oswald
    Section Leader: Chase Hult
    Date: November 27th, 2023
    Course: ISTA 131
    Assignment: Final
    Description: This program is used to clean up and create the csv files that are actually used
                 to produce the figures for the final.
"""
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime
import os
import matplotlib.pyplot as plt
import string
import statsmodels.api as sm
def trim_teamsCSV():
    """
    This takes the Teams.csv file from the dataset folder and condenses to the stats that
    I was considering using. Not all the stats were used, but this is how I created the
    "TeamsTrimmed.csv" file you'll see in one of the figure scripts.
    """
    df = pd.read_csv('datasets/Teams.csv',usecols=["yearID", "lgID", 'teamID', 'franchID',
                                                   "W", "L", "R", "AB", "H", "2B", "3B", "HR",
                                                   "BB", "SO", "HBP", "ER","ERA", "CG", "SHO", "BBA", "SOA"], dtype = str)

    trimmed_file = open("TeamsTrimmed.csv", 'w')
    trimmed_file.write("yearID,lgID,teamID,franchID,W,L,R,AB,H,2B,3B,HR,BB,SO,HBP,ER,ERA,CG,SHO,BBA,SOA\n")

    for i in range(len(df.index)):

        result = df.iloc[i,:].fillna('0')
        trimmed_file.write(",".join(result) + '\n')
    trimmed_file.close()


def OBP(abs, hits, bb, hbp):
    """
    This function calculates the on base % used for finding the OPS of a team.
    :param abs: total at bats
    :param hits: total hits
    :param bb: total walks
    :param hbp: total hit by pitches
    :return: the on base %
    """
    return (hits + bb + hbp) / (abs + bb + hbp)

def SLUG(AB, H, D, T, HR):
    """
    This function calculates the slugging % used for finding the OPS of a team
    :param AB: total at bats
    :param H: total hits
    :param D: total doubles
    :param T: total triples
    :param HR: total homeruns
    :return: slugging %
    """
    singles = H - D - T - HR ##want singles when it comes to slugging equation
    ## better hits are weighted more
    return (singles + D*2 + T*3 + HR*4) / AB

def WSwinners():
    """
    This function read through the SeriesPost.csv file and pulled out all the WorldSeries winners (which I then ended
    up deleting all the teams before 1905 because years when there was no WS).
    """
    winners = open('WSwinners.csv', 'w')
    df = pd.read_csv("datasets/SeriesPost.csv", header =0, usecols=[0,1,2])
    winners.write("Year,Winner\n")
    for i in range(len(df.index)):
        if df.iloc[i,1] =='WS':
            winners.write(f"{df.iloc[i,0]},{df.iloc[i, 2]}\n")
    winners.close()

def winnerAndRanking():
    """
    This function calculates the ERA and OPS of the world series winning teams and find where they rank amongst
    the league in those respective categories and creates a csv file storing them.
    """
    df = pd.read_csv("WSwinners.csv", header =0, index_col=0)
    winners = open("WinnersWithOPSandERA.csv", 'w')
    winners.write("Year,Team,OPS,OPSrank,ERA,ERArank\n")
    df2 = pd.read_csv("TeamsTrimmed.csv", usecols=[0,2,3,7,8,9,10,11,12,14,16])
    spotter  = 0
    curr_ops, curr_era = None, None
    eras, ops = [],[]
    current_winner, current_year = None,None
    for i in range(len(df.index)):
        current_year = df.index[i]
        current_winner = df.iloc[i,0]
        for k in range(spotter,len(df2.index)):

            ## check to make sure we are in the correct season still
            if df2.iloc[k,0] == current_year:
                obp = OBP(df2.iloc[k,3], df2.iloc[k,4], df2.iloc[k,8], df2.iloc[k,9])
                slg = SLUG(df2.iloc[k,3], df2.iloc[k,4], df2.iloc[k,5], df2.iloc[k,6], df2.iloc[k,7])

                ## when the WS winner is found, update
                if df2.iloc[k, 1] == current_winner or df2.iloc[k, 2] == current_winner:
                    curr_ops, curr_era = round(obp + slg, 3), df2.iloc[k,10]
                eras.append(df2.iloc[k,10])
                ops.append(round(obp + slg, 3))

            ##the next year is starting
            else:
                spotter = k ## keep track of where in the df2 we're at
                eras.sort()
                ops.sort()
                ops.reverse()
                ##era order is fine for league rankings, we want largest ops at the front though
                ## use .index() + 1 to get team rank in that category
                winners.write(f"{current_year},{current_winner},{curr_ops},{ops.index(curr_ops) + 1},"
                              f"{curr_era},{eras.index(curr_era) + 1}\n")

                ## resest
                curr_ops, curr_era = None, None
                eras, ops = [], []
                break
    ##2015 season
    eras.sort()
    ops.sort()
    ops.reverse()
    winners.write(f"{current_year},{current_winner},{curr_ops},{ops.index(curr_ops)+1},"
                  f"{curr_era},{eras.index(curr_era) + 1}\n")
    winners.close()

def turn_into_csv():
    """
    This program cleans up two copy and pastes I did. Originally, used this new data (very, very similar to orignial
    dataset) because it had some additional data I wanted. I didn't end up using the specific data, but it was easy
    to use this csv file, so I kept it. I will explain the csvs more in the README.
    """
    file1 = open('yearlyPitchingTotals(BR).txt', 'r')
    file2 = open('yearlyPitchingTotals(BR).csv', 'w')
    for line in file1:
        line = line.strip()
        line = line.split('\t')
        file2.write(','.join(line) + '\n')
    file1.close()
    file2.close()