from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px             # Plotly Express
import chart_studio.plotly as py        # Plotly Chart Studio
import cufflinks as cf                  # Cufflinks to bridge Plotly with Pandas
import plotly.offline
import plotly.graph_objs as go


# Merging DataFrame when loading in 2 Dataframes (Columns must have same name to combine)
def mergedf(df1, df2):
    samecol = [x for x in list(df1.columns) if x in list(df2.columns)]
    combinedf = df1.merge(df2, on=samecol, how='outer') # on=samecol has to be there or else a similar column name will have <same col>_y new columns, if the second column in the on-key has a different value, that row of table1 and table2 wont show
    return combinedf


# Creating New DataFrames to merge for export ----------------------------------Author: Meng Rong and Bao Huan
def activecasesDF(df):    
    '''
    Creates a new DataFrame from "Kaggle" DF
    
    "Current Active Cases" Structure:
    Date    ||      ICU     ||      General Ward        ||      In Isolation      ||      (new added column)
    
    Adds a new column:
    Current Active Cases = (ICU + General Ward + Isolation)
    '''
    activecasesdf = df[["Date", "Intensive Care Unit (ICU)", "General Wards MOH report", "In Isolation MOH report"]].copy()
    activecasesdf["Current Active Cases"] = df["Intensive Care Unit (ICU)"] + df["General Wards MOH report"] + df["In Isolation MOH report"]
    return activecasesdf

def percentO2DF(df):
    '''
    Creates a new DataFrame from "Kaggle" DF:

    "PercentO2" Structure:
    Date    ||      ICU     ||      General Ward        ||      Require O2 Supplementation      ||      (new added column)
    
    Adds a new column:
    Percentage req O2 Supplementation  = (O2 Count / (ICU + General Ward)  * 100
    '''
    percentO2df = df[["Date", "Intensive Care Unit (ICU)", "General Wards MOH report", "Requires Oxygen Supplementation"]].copy()
    percentO2df["Percentage Oxygen Supplementation"] = (df["Requires Oxygen Supplementation"] / (df["Intensive Care Unit (ICU)"] + df["General Wards MOH report"])  * 100).round(2)
    return percentO2df

def icuByAgeDF(df):       
    '''
    Creates a new DataFrame from "Hospital" DF:

    "icuByAge" Structure:
    Date    ||      (1st Age Group + ICU Keyword))    || (2nd Age Group + ICU keyword)      ||      ....
                            Count of cases                      Count of cases
    
    Adds multiple column:
    (Age Group + ICU Keyword) ....
    '''    
    # Regex for the ICU people, might have multiple inputs of ICU, in this case of the new file there is only 1
    icuRegex = "(Critically ill and Intubated in ICU)+"

    # Single out all the Rows that are related to ICU and make a pivot table dataframe to get individual age groups as a column
    tempdf = df.loc[df['clinical_status'].str.contains(pat=icuRegex, regex=True)]
    newdf = pd.pivot_table(tempdf, values="count_of_case", index="Date", columns="age_groups")
    
    # Rename the columns into (Age Group + ICU) at the end. Thus, e.g. "70 years old and above ICU"
    for value in list(newdf.columns):
        newdf = newdf.rename(columns={value: value+" in ICU"})
    
    newdf = newdf.reset_index().rename_axis(None, axis=1)       # Reset the index and Remove the name of axis of the row made by pivot table
    newdf = newdf.fillna(0)
    return newdf

def localsByAgeDF(df):
    '''
    Creates a new DataFrame from "LocalCasesByAgeGroup" DF:

    "localsByAge" Structure:
    Date    ||      (1st Age Group + Local Cases Keyword))    || (2nd Age Group + Local Cases keyword)      ||      ....

    Adds multiple column:
    (Age Group + Local Cases Keyword) ....
    '''
    newdf = pd.pivot_table(df, values="count_of_case", index="Date", columns="age_group")
    for value in list(newdf.columns):
        newdf = newdf.rename(columns={value: value+" Local Cases"})
    
    newdf = newdf.reset_index().rename_axis(None, axis=1)
    newdf = newdf.fillna(0)
    return newdf


# For Analysis Graph Plotting-------------------------Author: Meng Rong
def analysis_bar_ActiveCases(df):
    '''
    Manipulates "Current Active Cases" DF:

    "Current Active Cases" Structure:
    Date    ||      ICU     ||      General Ward        ||      In Isolation      ||      (new added column)
    '''
    list1 = ["Intensive Care Unit (ICU)", "General Wards MOH report", "In Isolation MOH report"]
    fig = px.bar(df, x='Date', y=list1, text='Current Active Cases')
    fig.update_layout(title_text='Daily Active Cases bargraph')
    fig.show()


def analysis_scatter_percentO2(df):
    '''
    Manipulates "PercentO2" DF:

    "PercentO2" Structure:
    Date    ||      ICU     ||      General Ward        ||      Require O2 Supplementation      ||      (new added column)
    '''
    list1 = ["Intensive Care Unit (ICU)", "General Wards MOH report", "Requires Oxygen Supplementation"]
    internaldf = df.dropna(subset=["Percentage Oxygen Supplementation"])
    fig = px.scatter(internaldf, x="Date", y="Percentage Oxygen Supplementation", trendline="ols", hover_data=list1)
    fig.update_layout(title_text='Percentage Oxygen Supplement required by Hospitalised patients')
    fig.show()

def analysis_pie_ICU_AgeGroup(df):
    '''
    Manipulate "icuByAge" DF

    "icuByAge" Structure:
    Date    ||      (1st Age Group + ICU Keyword))    || (2nd Age Group + ICU keyword)      ||      ....
                            Count of cases                      Count of cases
    '''
    date = str(df.sort_values(by='Date').iloc[0,0].date())
    dict1 = {}

    # Store values into dict1
    # Key = Age Group Column Name
    # Value = Total count of all values in (Age Group) column
    colhead = [x for x in df.columns if x != "Date"]
    for value in colhead:
        dict1[value] = df[value].sum()

    # Show pie chart 
    labels = []
    values = []
    for k,v in dict1.items():
        labels.append(k)
        values.append(v)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=20)
    fig.update_layout(title_text='Total ICU based on Age Group from ' + date)
    fig.show()


def analysis_pie_TotalCases_AgeGroup(df):
    '''
    Manipulates "localsByAge" DF:

    "localsByAge" Structure:
    Date    ||      (1st Age Group + Local Cases keyword))    || (2nd Age Group + Local Cases keyword)      ||      ....
    '''
    date = str(df.sort_values(by='Date').iloc[0,0].date())
    dict1 = {}

    # Store values into dict1
    # Key = Age Group Column Name
    # Value = Total count of all values in (Age Group) column
    colhead = [x for x in df.columns if x != "Date"]
    for value in colhead:
        dict1[value] = df[value].sum()

    # 
    labels = []
    values = []
    for k,v in dict1.items():
        labels.append(k)
        values.append(v)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=20)
    fig.update_layout(title_text='Active Cases by Age Range from ' + date)
    fig.show()

    
def custom_animated_ActiveCases_AgeGroup(df):
    pass



# For Basic Graph Plotting ----------------------------------Author: Meng Rong
def basic_line_graph(df, y_axis):
    '''
    Creates a Line Graph of DataFrame:

    df = Cleaned Pandas DataFrame (with starting column, labelled as "Date")
    y_axis = Column name used for y-axis (list)
    '''
    fig = px.line(df, x="Date", y=y_axis)
    fig.show()

def basic_bar_graph(df, y_axis):
    '''
    Creates a Bar Graph of based on DataFrame:

    df = Cleaned Pandas DataFrame (with starting column, labelled as "Date")
    y_axis = Column name used for y-axis (list)
    '''
    fig = px.bar(df, x="Date", y=y_axis)
    fig.show()