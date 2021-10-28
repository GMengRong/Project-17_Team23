#Load Function - by Chow Sow Ying

import tkinter as tk
from tkinter import Message, Widget, filedialog , messagebox , ttk
import numpy
import pandas as pd
import os

import re       # Regex for Data pre-processing


# might not be needed
# Browsing Data File -------------Author: Sow Ying
def file_dialog(FileLabel_V):
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("xlsx files","*.xlsx"),("All Files","*.*")))
    FileLabel_V["text"] = filename
    return None


# Load Main Raw Data into DataFrame -------------Author: Sow Ying & Meng Rong
def load_excel_data():
    try:
        tempdict = {}

        # Load main dataset
        basedir = os.path.dirname(__file__)
        excel_filename = os.path.join(basedir, 'Dataset/Covid-19 SG.xlsx')
        df = pd.read_excel(excel_filename)
        df["Date"] = pd.to_datetime(df["Date"])
        
        # Drop Irrelevant Columns -- cleaning
        vaccineRegex = "([vV]accine|[vV]accinated|[vV]accination|[dD]ose|[dD]osage)+"
        excludedColumns = ['Linked community cases', 'Unlinked community cases']
        excludedVacList = []
        for column in df.columns.tolist():
            if re.search(vaccineRegex, column):
                excludedVacList.append(column)
        excludedColumns.extend(excludedVacList)
        df = df.drop(excludedColumns, axis=1)

        # Drop NA's found in Date columns to remove the empty rows after last entry -- cleaning
        df = df.dropna(subset=['Date'])

        # Impute "False Positives Found" column with 0 -- cleaning
        df['False Positives Found'] = df['False Positives Found'].fillna(0)

        # Cleaning Discrepancies/Dirty Data (unable to clean so dropped to prevent error) -- cleaning
        df = df.drop(['Discharged to Isolation','Still Hospitalised'], axis=1)
        

        # Load other datasets (no cleaning required)
        secondFile = os.path.join(basedir, 'Dataset/patients-needing-oxygen-supplementation-icu-care-or-died-by-age-groups.csv')
        thirdFile = os.path.join(basedir, 'Dataset/number-of-community-cases-by-age.csv')
        df2 = pd.read_csv(secondFile)
        df3 = pd.read_csv(thirdFile)

        df2 = df2.rename(columns={df2.columns[0]: "Date"})
        df2["Date"] = pd.to_datetime(df2["Date"])
        df3 = df3.rename(columns={df3.columns[0]: "Date"})
        df3["Date"] = pd.to_datetime(df3["Date"])
        
        
        # Save into dictionary - Easy to remember Key names, DataFrame as Value
        tempdict["Master"] = df
        tempdict["Kaggle"] = df
        tempdict["Hospital"] = df2
        tempdict["LocalCasesByAgeGroup"] = df3

        return tempdict

    except ValueError:
        tk.messagebox.showerror(message="Invalid File")
        return None
    except FileNotFoundError:
         tk.messagebox.showerror(message="Dataset file not found")
         return None



    #Load Overview-Author:Javen
    CurrentPhase = reversed_df.at[reversed_df.index[0],'Phase']
    LatestCaseNum = reversed_df.at[reversed_df.index[0],'Cumulative Confirmed']
    LatestDeathNum = reversed_df.at[reversed_df.index[0],'Cumulative Deaths']
    MortalityRate = (LatestDeathNum / LatestCaseNum) * 100
    

    #Printing Overview-Author:Javen
    OverviewCases.config(text='Total Accumulated Cases:')
    OverviewCases.pack
    CaseNum.config(text=LatestCaseNum)
    CaseNum.pack
    OverviewDeaths.config(text='Total Accumulated Death:')
    OverviewDeaths.pack
    DeathNum.config(text=LatestDeathNum)
    DeathNum.pack
    OverviewMortality.config(text='Mortality Rate:')
    OverviewMortality.pack
    MortalityNum.config(text="%.2f" %  MortalityRate +"%")
    MortalityNum.pack
    OverviewPhase.config(text='Current Phase:')
    OverviewPhase.pack
    PhaseName.config(text=CurrentPhase)
    PhaseName.pack
  

# Combined with refresh function
# def load_treeview(df):
#     #Load Column Names
#     columnname = list(df.columns)

#     # Updating the buttons
#     searchc1["text"] = columnname[0]
#     searchc2["text"] = columnname[1]
#     searchc3["text"] = columnname[2]
#     searchc4["text"] = columnname[3]
#     searchc5["text"] = columnname[4]
    
#     exportc1["text"] = columnname[0]
#     exportc2["text"] = columnname[1]
#     exportc3["text"] = columnname[2]
#     exportc4["text"] = columnname[3]
#     exportc5["text"] = columnname[4]

#     #Load into Tree View
#     treeView1["column"] = list(df.columns)
#     treeView1["show"] = "headings"
#     for column in treeView1["column"]:
#         treeView1.heading(column, text=column)

#     df_row = df.to_numpy().tolist()
#     for row in df_row:
#         treeView1.insert("","end",values=row)
#     return None

   



