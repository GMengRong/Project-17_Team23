#Load Function - by Sow Ying & Meng Rong

import tkinter as tk
from tkinter import Message, Widget, filedialog , messagebox , ttk
import pandas as pd
import os
import re       # Regex for Data pre-processing

# Load Main Raw Data into DataFrame -------------Author: Sow Ying (loading data) &  Meng Rong (cleaning data)
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

        # Rename "Date" Column to standardise for all DataFrames
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

   



