"""
    File: analyze.py
    Name: Nathan Oswald
    Section Leader: Chase Hult
    Date: November 27th, 2023
    Course: ISTA 131
    Assignment: Final
    Description: This program is going to go through the datasets, cleaning up some CSV files
                 adding data to some, and creating some databases to help in the process.
"""
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime
import os
import matplotlib.pyplot as plt



def kill_dbs():
    if os.path.exists('finalDB'):

        os.remove('finalDB')
def created_id_name_db():
    df = pd.read_csv('datasets/Master.csv', usecols = ["playerID", "nameFirst", 'nameLast', 'debut'], parse_dates=['debut'], index_col=0)
    conn = sqlite3.connect('finalDB.db')
    conn.row_factory =sqlite3.Row
    c = conn.cursor()

    cut_off_data = datetime(1950, 1, 1)
    create_db = "CREATE TABLE playerID (id TEXT PRIMARY KEY, name TEXT);"
    c.execute(create_db)
    for i in range(len(df.index)):
        if df.iloc[i, 2] >= cut_off_data:
            id_name = (df.index[i], df.iloc[i, 0] + ' ' + df.iloc[i, 1])
            insert_s = 'INSERT INTO playerID VALUES (?,?);'
            c.execute(insert_s, id_name)
    conn.commit()
    conn.close()


def active_teams():
    df = pd.read_csv('datasets/TeamsFranchises.csv', usecols=[0,1,2])
    conn =sqlite3.connect('finalDB.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    create_db = "CREATE TABLE active_teams (id TEXT PRIMARY KEY, name TEXT);"
    c.execute(create_db)
    for i in range(len(df.index)):
        if df.iloc[i, 2] == "Y":
            id_name = df.iloc[i,0]
            team_name = df.iloc[i,1]
            insert_s = 'INSERT INTO active_teams VALUES (?,?);'
            c.execute(insert_s, (id_name, team_name))
    conn.commit()
    conn.close()

def trim_teamsCSV():
    conn = sqlite3.connect('finalDB.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    select_q = "SELECT id FROM active_teams;"
    teamIDs = []
    for id in c.execute(select_q):
        teamIDs.append(id[0])

    df = pd.read_csv('datasets/Teams.csv',usecols=["yearID", "lgID", 'franchID',
                                                   "W", "L", "R", "AB", "H", "2B", "3B", "HR",
                                                   "BB", "SO", "HBP", "ER","ERA", "CG", "SHO", "BBA", "SOA"], dtype = str)

    trimmed_file = open("TeamsTrimmed.csv", 'w')
    trimmed_file.write("yearID,lgID,franchID,W,L,R,AB,H,2B,3B,HR,BB,SO,HBP,ER,ERA,CG,SHO,BBA,SOA\n")

    cut_off_data = datetime(1950, 1, 1)
    for i in range(len(df.index)):
        if df.iloc[i,2] in teamIDs and datetime(int(df.iloc[i, 0]), 1 ,1) >= cut_off_data:
            result = df.iloc[i,:].fillna('0')
            trimmed_file.write(",".join(result) + '\n')
    trimmed_file.close()

def yearly_batting():
    df = pd.read_csv('TeamsTrimmed.csv', usecols=[0, 6,7,8,9,10,11,13])
    batting = open('BattingStatsYearly.csv', 'w')
    batting.write("Year,SLUGGING%, OBP, OPS\n")
    current_year = 1950
    stats = [0,0,0,0,0,0,0] ##ABS hits, doubles, triples, homers, Walks, HBP
    for i in range(len(df.index)):
        if df.iloc[i,0] == current_year:
            for k in range(1,8):
                stats[k-1] += float(df.iloc[i,k])

        else:
            obs = OBP(stats[1], stats[5], stats[6], stats[0])
            slug = SLUG(stats[1], stats[2], stats[3], stats[4], stats[0])
            OPS = obs+slug
            batting.write(f"{current_year}, {obs}, {slug}, {OPS}\n")
            current_year = df.iloc[i, 0]
            stats = [0,0,0,0,0,0,0]
            for k in range(1,8):
                stats[k-1] += float(df.iloc[i,k])
    obs = OBP(stats[1], stats[5], stats[6], stats[0])
    slug = SLUG(stats[1], stats[2], stats[3], stats[4], stats[0])
    OPS = obs + slug
    batting.write(f"{current_year}, {obs}, {slug}, {OPS}")
    batting.close()

def OBP(hits, bb, hbp, abs):
    return (hits + bb + hbp) / (abs + bb + hbp)

def SLUG(H, D, T, HR, AB):
    singles = H - D - T - HR
    return (singles + D*2 + T*3 + HR*4) / AB

def yearly_pitching():
    df = pd.read_csv('TeamsTrimmed.csv', usecols=[0, 16, 15])

    pitching = open("PitchingStatsYearly.csv", "w")
    pitching.write("Year,ERA,complete_game\n")
    current_year = 1950
    stats = [0,0]
    teamcount = 0
    for i in range(len(df.index)):
        if df.iloc[i,0] == current_year:
            teamcount+=1
            for k in range(1,3):
                stats[k-1] += float(df.iloc[i,k])

        else:

            pitching.write(f"{current_year},{stats[0]/teamcount},{stats[1]}\n")
            current_year = df.iloc[i, 0]
            stats = [0,0]
            teamcount = 1
            for k in range(1,3):
                stats[k-1] += float(df.iloc[i,k])
    pitching.write(f"{current_year},{stats[0]/teamcount},{stats[1]}\n")
    pitching.close()







#created_id_name_db()
#active_teams()
##trim_teamsCSV()
##yearly_batting()
##yearly_pitching()

df = pd.read_csv("PitchingStatsYearly.csv", index_col=0)
df2 = pd.read_csv("BattingStatsYearly.csv", index_col=0)
df.iloc[:,0].plot()
plt.figure()
df2.iloc[:,2].plot()
plt.show()

#kill_dbs()