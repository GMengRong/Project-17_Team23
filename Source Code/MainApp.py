# Imported Modules
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import Message, Widget, filedialog , messagebox , ttk
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, FALSE, LEFT, NORMAL, RIGHT, TRUE, VERTICAL, X, Y
import webbrowser

# Self-made Modules
import CovidStatistics as cvdstats
import SearchModule as sm
import LoadModule as lm
import ExportModule as em


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Internal Functions:
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Fixed Colour Problem ------------------------------------------- (Author: Sow Ying)
def fixed_map(option):
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]


# Function to change frame ------------------------------------------- (Author: Sow Ying)
def raise_frame(frame):
    frame.tkraise()


# Function to show data in TreeView ------------------------------------------- (Author: Sow Ying)
def reload_TreeView():
    '''
    Reload every value in the Treeview
    Step 1: Retrieve DataFrame from Master in DataFrame Dictionary
    Step 2: Clear existing rows in Treeview Table
    Step 3: Load the values in the Master Dataframe into TreeView
    '''
    # Retrieve DataFrame from Master Key in Dictionary
    string_df = dfDict["Master"].applymap(str)
    reversed_df = string_df.iloc[::-1]                  #Reverse the order of index

    # Clear Existing Treeview table
    treeView1.delete(*treeView1.get_children())         #Destroy all the existing widgets in the treeview

    #Insert Data into Tree View
    treeView1["column"] = list(reversed_df.columns)     
    treeView1["show"] = "headings"
    for column in treeView1["column"]:
        treeView1.heading(column, text=column)
    df_row = reversed_df.to_numpy().tolist()
    for row in df_row:
        treeView1.insert("","end",values=row)


# Refresh View For TreeView after searching / Clearing export buttons ------------- (Author: Sow Ying)
def refresh():
    '''
    Reload whole MainPage
    Step 1: Deselect All Export Checkboxes
    Step 2: Reload all original values in the TreeView
    Step 3: Create Search Option variables in the drop down button
    '''
    # Clear "checked" status Export Button
    deselectAllCheckbox(exportCheckButtonVar)

    # Reload all original values in the TreeView
    reload_TreeView()

    # Making Search Option Menu ---------------- (Author:Sow Ying)
    string_df = dfDict["Master"].applymap(str)
    reversed_df = string_df.iloc[::-1]
    global columnname
    columnname = list(reversed_df.columns)
  
    global searchvariable
    searchvariable = tk.StringVar(searchFrame)
    searchvariable.set(columnname[0])

    searchopt = tk.OptionMenu(searchFrame, searchvariable, *columnname)
    searchopt.config(width=85, font=('Courier', 8))
    searchopt.place(rely=0.5, relx=0.01)
    
    #Calculating Overview ---------------- (Author: Javen)
    CurrentPhase = dfDict["Master"]["Phase"].iat[-1]
    LatestCaseNum = dfDict["Master"]["Cumulative Confirmed"].iat[-1]
    LatestDeathNum = dfDict["Master"]["Cumulative Deaths"].iat[-1]
    MortalityRate = (float(LatestDeathNum) / float(LatestCaseNum)) * 100
    
    #Printing Overview ---------------- (Author: Javen)
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


# Press all select export checkbuttons ------------- (Author: Meng Rong)
def selectAllCheckbox(CheckButtonVar):
    '''
    param:
    CheckButtonVar - List of all instantiated checkbox button are held

    Function:
    Select and check all the CheckBoxButton passed in the list parameter
    '''
    for x in CheckButtonVar:
        x.select()


# Press all deselect export checkbuttons ------------- (Author: Meng Rong)
def deselectAllCheckbox(CheckButtonVar):
    '''
    param:
    CheckButtonVar - List of all instantiated checkbox button are held

    Function:
    Deselect and check all the CheckBoxButton passed in the list parameter
    '''
    for x in CheckButtonVar:
        x.deselect()


# Create Canvas and Scrollable Checkbox for StatsFrame and Export------------- (Author: Meng Rong)
def createScrollinFrame(mainframe, CheckBoxVar, CheckButtonVar):
    '''
    1. Creates a Tkinter Canvas to attached the scrollbar to the variable "mainframe" being passed in
    2. Create a Second Frame to hold the Canvas
    3. Launch the createCheckButton Function
    '''
    # Create Canvas
    x_canvas = tk.Canvas(mainframe, bg='#636262',bd=0,highlightthickness=0)
    x_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    x_scrollbar = tk.Scrollbar(x_canvas, orient=VERTICAL, command=x_canvas.yview)
    x_scrollbar.pack(side=RIGHT, fill=Y)
    x_canvas.configure(yscrollcommand=x_scrollbar.set)
    x_canvas.bind('<Configure>', lambda e: x_canvas.configure(scrollregion=x_canvas.bbox("all")))

    # Create a second frame in canvas
    x_second_frame = tk.Frame(x_canvas, bg='#636262')
    x_canvas.create_window((0,0), window=x_second_frame, anchor="nw")
    createCheckButtons(x_second_frame, CheckBoxVar, CheckButtonVar)


# Used in createScrollinFrame to create the checkbuttons------------- (Author: Meng Rong)
def createCheckButtons(secondframe, CheckBoxVar, CheckButtonVar):
    '''
    1. Create CheckButtons based on the number of column headers in the Master DataFrame
    2. Store the variables made while creating the CheckButtonss into list "CheckBoxVar, CheckButtonVar" being parsed in to the function
    '''
    for no in range(len(allColumns)):
        CheckBoxVar.append(tk.IntVar())
        x = tk.Checkbutton(secondframe, text=allColumns[no], variable=CheckBoxVar[no], onvalue=1, offvalue=0, background="#636262", foreground='white',selectcolor="#636262")
        x.grid(row=no, column=0, sticky='nw')
        CheckButtonVar.append(x)


# Function to get all checked Checkboxed in list yaxis_CheckBoxVar --------------------- (Author: Meng Rong)
def selectedCheckBox(CheckBoxVar):
    axislist = []
    for item in range(len(CheckBoxVar)):
        if CheckBoxVar[item].get() == 1:
            axislist.append(allColumns[item])
    return axislist


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
-----------
Launch App 
-----------
Step 1: Analyse and process Datasets
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Dictionary containing Dataset initiatlise
dfDict = {}   #Dictionary of all DF objects loaded into the program, (Key: Name of File w/o .Ext (str), Value: DataFrame)

# Dictionary Contents: (Initial 4 after loading dataset files)
# 1. "Master" (to be used for Export and viewed by Treeview)
# 2. "Kaggle"
# 3. "Hospital"
# 4. "LocalCasesByAgeGroup"
dfDict = lm.load_excel_data()

# DataFrames added from Analysis functions: 
# 5. "Current Active Cases"
# 6. "PercentO2"
# 7. "icuByAge"
# 8. "localsByAge"
dfDict["Current Active Cases"] = cvdstats.activecasesDF(dfDict["Kaggle"])
dfDict["PercentO2"] = cvdstats.percentO2DF(dfDict["Kaggle"])
dfDict["icuByAge"] = cvdstats.icuByAgeDF(dfDict["Hospital"])
dfDict["localsByAge"] = cvdstats.localsByAgeDF(dfDict["LocalCasesByAgeGroup"])

# Merge columns in new DataFrame with Master to be able to export analysed data
dfDict["Master"] = cvdstats.mergedf(dfDict["Master"], dfDict["Current Active Cases"])   # Add 1 new column
dfDict["Master"] = cvdstats.mergedf(dfDict["Master"], dfDict["PercentO2"])              # Add 1 new column
dfDict["Master"] = cvdstats.mergedf(dfDict["Master"], dfDict["icuByAge"])               # Add 4 new columns (Depends on new age group)
dfDict["Master"] = cvdstats.mergedf(dfDict["Master"], dfDict["localsByAge"])            # Add 6 new columns (Depends on new age group)

# Stores all the column title in the Master DataFrame into a list
allColumns = list(dfDict['Master'].columns)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Step 2: Create all GUI Object in Main Frame
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Start Build Tkinter Objects
root = tk.Tk()
root.geometry("1280x720")       # Width x height
root.pack_propagate(False)      # Dont resize based on widget
root.resizable(0,0)             # Window cant be resize

style = ttk.Style()
style.map("Treeview", 
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))

# Set Frame Pages
MainFrame = tk.Frame(root,bg='#242424')
MainFrame.place(height=720, width=1280)   

StatsFrame = tk.Frame(root,bg='#242424')
StatsFrame.place(height=720, width=1280)


#--- Main Frame ------------------------------------------- (Author: Sow Ying)
menuFrame = tk.LabelFrame(MainFrame,background="#636262")
menuFrame.place(height=50, width=1270, relx=0.005 ,rely=0.005)  

MainTitle = ttk.Label(MainFrame, text='Covid-19 Analyser' , font=('Aquire',22,'bold'), background="#636262",foreground="white")
MainTitle.place(rely=0.01, relx=0.01)

#Refresh Button
RefreshButton = tk.Button(MainFrame, text="REFRESH",width=15,font=('Courier',10,'bold'),background="#242424",
                                                    foreground="white", command=lambda:refresh())
RefreshButton.place(relx=0.85 ,rely=0.02)

#To Stats Page Button
toStatsBtn = tk.Button(MainFrame, text="VIEW STATISTICS",height =4, width = 30, font=('Courier',16,'bold'),
                                                        background="#636262",foreground="white", borderwidth=0,
                                                        command=lambda:raise_frame(StatsFrame))
toStatsBtn.place(rely=0.61, relx=0.68)

#Open Webpage
openURL =  tk.Button(MainFrame, text="Phase - More Info",height =1, width = 20, font=('Courier',12,'bold'),
                                                        background="#636262",foreground="white", borderwidth=0,
                                                        command=lambda:webbrowser.open("https://www.moh.gov.sg/covid-19-phase-advisory"))
openURL.place(rely=0.93, relx=0.6)

openURL2 =  tk.Button(MainFrame, text="Follow App on Github",height =1, width = 20, font=('Courier',12,'bold'),
                                                        background="#636262",foreground="white", borderwidth=0,
                                                        command=lambda:webbrowser.open("https://github.com/Xynorimas/Project-17_Team23"))
openURL2.place(rely=0.93, relx=0.8)


#--- Main Page - TreeView --------------------------------- (Author: Sow Ying)
#Frame for TreeView
viewFrame = tk.LabelFrame(MainFrame,background="#636262")
viewFrame.place(height=400, width=850, relx=0.005, rely=0.2)  

#Treeview Widget
treeView1 = ttk.Treeview(viewFrame)
treeView1.place(relheight=1, relwidth=1)

#Treeview scrollbar
treescrolly = tk.Scrollbar(viewFrame, orient="vertical", command=treeView1.yview)
treescrollx = tk.Scrollbar(viewFrame, orient="horizontal", command=treeView1.xview)
treeView1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")


#--- Main Page - Search --------------------------------------------- (Author: Sow Ying)
searchFrame = tk.LabelFrame(MainFrame,background="#636262")
searchFrame.place(height=80, width=850, relx=0.005,rely=0.08)

searchInput = tk.Text(searchFrame, height = 0.5, width = 80)
searchInput.place(rely=0.1, relx=0.01)

searchButton = tk.Button(searchFrame, text="SEARCH",width=15,font=('Courier',10,'bold'),background="#242424",
                                                    foreground="white",command=lambda:sm.search(1,searchvariable,columnname,searchInput,reload_TreeView,treeView1))
searchButton.place(rely=0.1, relx=0.8)


#--- Main Page - Export --------------------------------------------- (Author: Javen and Su Qin)
exportVarList = []
exportCheckButtonVar = []

exportFrame = tk.LabelFrame(MainFrame, background="#242424")
exportFrame.place(relheight=0.5, width=400, rely=0.08, relx=0.68) 

checkboxFrame = tk.LabelFrame(exportFrame, background="#242424")
checkboxFrame.place(relheight=0.85, width=400) 

createScrollinFrame(checkboxFrame, exportVarList, exportCheckButtonVar)

selectAllExportButton = exportButton = tk.Button(exportFrame, text='Select all', width=15,font=('Courier',10,'bold'),background="#636262",
                                                    foreground="white", command=lambda:selectAllCheckbox(exportCheckButtonVar))
exportButton.place(rely=0.9, relx=0.1)

exportButton = tk.Button(exportFrame, text='Export', width=15,font=('Courier',10,'bold'),background="#636262",
                                                    foreground="white", command=lambda:em.export_excel(dfDict["Master"], selectedCheckBox(exportVarList)))
exportButton.place(rely=0.9, relx=0.6)


#--- Main Page - Overview  ------------------------------------------- (Author: Javen and Su Qin)
OverviewFrame = tk.LabelFrame(MainFrame,background="#636262")
OverviewFrame.place(height=100, width=1270, rely=0.77, relx=0.005)

OverviewCases = ttk.Label(OverviewFrame,font=('Courier',13,'bold'),background="#636262", foreground="white")
OverviewCases.place(rely=0.2, relx=0.01) #rely height, relx length
CaseNum = ttk.Label(OverviewFrame, font=('Courier',20,'bold'),background="#636262", foreground="white")
CaseNum.place(rely=0.5, relx=0.01)
OverviewDeaths = ttk.Label(OverviewFrame, font=('Courier',13,'bold'),background="#636262", foreground="white")
OverviewDeaths.place(rely=0.2,relx=0.26)
DeathNum = ttk.Label(OverviewFrame, font=('Courier',20,'bold'),background="#636262", foreground="white")
DeathNum.place(rely=0.5,relx=0.26)
OverviewMortality = ttk.Label(OverviewFrame, font=('Courier',13,'bold'),background="#636262", foreground="white")
OverviewMortality.place(rely=0.2,relx=0.51)
MortalityNum = ttk.Label(OverviewFrame, font=('Courier',20,'bold'),background="#636262", foreground="white")
MortalityNum.place(rely=0.5,relx=0.51)
OverviewPhase = ttk.Label(OverviewFrame, font=('Courier',13,'bold'),background="#636262", foreground="white")
OverviewPhase.place(rely=0.2,relx=0.68)
PhaseName = ttk.Label(OverviewFrame, font=('Courier',20,'bold'),background="#636262", foreground="white")
PhaseName.place(rely=0.5,relx=0.68)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Step 3: Create all GUI Object in Stats Page
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# List to hold the CheckButtons variables to plot basic graphs based on the Column Headers
yaxis_CheckBoxVar = []
yaxis_CheckButtonVar = []

#To go back Main Page Button
toMainBtn2 = tk.Button(StatsFrame, text="Back",height=1, width=10, command=lambda:raise_frame(MainFrame))
toMainBtn2.place(rely=0, relx=0)


# Basic Graph Y-axis Frame - Stats Page (Creation of "(X)" Area) ---------------- (Author: Meng Rong and Bao Huan)
# x x x x x x x x x x x x x x x x x x x
# x                 X                 x
# x                 X        (X)      x
# x                 X                 x
# x ----------------------------------x
# x                                   x
# x                                   x
# x                                   x
# x x x x x x x x x x x x x x x x x x x
yAxisFrame = tk.Frame(StatsFrame,background="#636262")
yAxisFrame.place(relwidth=0.35, relheight=0.4, rely=0.1, relx=0.5) 
yAxisTitle = ttk.Label(StatsFrame, text='Y-Axis', font=('Aquire',12,'bold'), background="#636262",foreground="white")
yAxisTitle.place(rely=0.07, relx=0.5)

# Create the Canvas and Checkbox Buttons for the Graph Y-axis
createScrollinFrame(yAxisFrame, yaxis_CheckBoxVar, yaxis_CheckButtonVar)

# Plot Basic Graphs Frame
basicGraphFrame = tk.LabelFrame(StatsFrame, background="#242424", text="Plot Basic Graph", font=('Aquire',12,'bold'), foreground="white")
basicGraphFrame.place(relheight=0.4, relwidth=0.12, rely=0.1, relx=0.86)

# Plot Basic Graphs Button
viewLinegraphbtn = tk.Button(basicGraphFrame, text="LINEGRAPH", width=15, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:cvdstats.basic_line_graph(dfDict["Master"], selectedCheckBox(yaxis_CheckBoxVar)))
viewLinegraphbtn.place(rely=0.1, relx=0.05)

viewCountplotBtn = tk.Button(basicGraphFrame, text="BARGRAPH", width=15, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:cvdstats.basic_bar_graph(dfDict['Master'], selectedCheckBox(yaxis_CheckBoxVar)))
viewCountplotBtn.place(rely=0.25, relx=0.05)


# Analysis Frame 1 - Stats Page (Creation of "(X)" Area) ---------------- (Author: Meng Rong and Bao Huan)
# x x x x x x x x x x x x x x x x x x x
# x                 X                 x
# x       (X)       X                 x
# x                 X                 x
# x ----------------------------------x
# x                                   x
# x                                   x
# x                                   x
# x x x x x x x x x x x x x x x x x x x
analysisFrame1 = tk.LabelFrame(StatsFrame, background="#242424", text="Active Cases in Singapore Today", font=('Aquire',12,'bold'), foreground="white")
analysisFrame1.place(relwidth=0.45, relheight=0.4, rely=0.1, relx=0.02)

Current_Active_Cases_Label = ttk.Label(analysisFrame1, text='Current\nActive Cases', justify=CENTER, font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
Current_Active_Cases_Label.grid(row=0, column=1, padx=10, pady=(30,0))
Current_Active_Cases = ttk.Label(analysisFrame1, text=dfDict["Current Active Cases"]["Current Active Cases"].iloc[-1] ,font=('Courier',18,'bold'), background="#242424",foreground="white")
Current_Active_Cases.grid(row=1, column=1)

Current_Active_Cases_Label = ttk.Label(analysisFrame1, text='In\nGeneral Ward', justify=CENTER,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
Current_Active_Cases_Label.grid(row=2, column=0, padx=10, pady=(30,0))
Current_Active_Cases = ttk.Label(analysisFrame1, text=dfDict["Current Active Cases"]["General Wards MOH report"].iloc[-1] ,font=('Courier',18,'bold'), background="#242424",foreground="white")
Current_Active_Cases.grid(row=3, column=0)

Current_Active_Cases_Label = ttk.Label(analysisFrame1, text='In\nICU', justify=CENTER,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
Current_Active_Cases_Label.grid(row=2, column=1, padx=10, pady=(30,0))
Current_Active_Cases = ttk.Label(analysisFrame1, text=dfDict["Current Active Cases"]["Intensive Care Unit (ICU)"].iloc[-1] ,font=('Courier',18,'bold'), background="#242424",foreground="white")
Current_Active_Cases.grid(row=3, column=1)

Current_Active_Cases_Label = ttk.Label(analysisFrame1, text='In\nIsolation', justify=CENTER,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
Current_Active_Cases_Label.grid(row=2, column=2, padx=10, pady=(30,0))
Current_Active_Cases = ttk.Label(analysisFrame1, text=dfDict["Current Active Cases"]["In Isolation MOH report"].iloc[-1] ,font=('Courier',18,'bold'), background="#242424",foreground="white")
Current_Active_Cases.grid(row=3, column=2)


# Analysis Frame 2 - Stats Page (Creation of "(X)" Area) ---------------- (Author: Meng Rong and Bao Huan)
# x x x x x x x x x x x x x x x x x x x
# x                 X                 x
# x                 X                 x
# x                 X                 x
# x ----------------------------------x
# x                                   x
# x                (X)                x
# x                                   x
# x x x x x x x x x x x x x x x x x x x
analysisFrame2 = tk.LabelFrame(StatsFrame, background="#242424", text="Total Cases by Age Group (Data from 22nd Sept Onwards)", font=('Aquire',12,'bold'), foreground="white")
analysisFrame2.place(relheight=0.40, relwidth=0.7, rely=0.55, relx=0.02)

#First row of frame grid
totalcases70plus_Label = ttk.Label(analysisFrame2, text='Cases Age 70+:' ,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
totalcases70plus_Label.grid(row=0, column=0, padx=10, pady=(35,0))
totalcases70plus = ttk.Label(analysisFrame2, text=dfDict["localsByAge"]["70 years old and above Local Cases"].sum() ,font=('Courier',18,'bold'), background="#242424",foreground="white")
totalcases70plus.grid(row=1, column=0)

totalcases61to70_Label = ttk.Label(analysisFrame2, text='Cases Age 60 - 69:' ,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
totalcases61to70_Label.grid(row=0, column=1, padx=10, pady=(35,0))
totalcases61to70 = ttk.Label(analysisFrame2, text=dfDict["localsByAge"]["60 - 69 years old Local Cases"].sum() ,font=('Courier',18,'bold'), background="#242424",foreground="white")
totalcases61to70.grid(row=1, column=1)

totalcases40to60_Label = ttk.Label(analysisFrame2, text='Cases Age 40 - 59:' ,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
totalcases40to60_Label.grid(row=0, column=2, padx=10, pady=(35,0))
totalcases40to60 = ttk.Label(analysisFrame2, text=dfDict["localsByAge"]["40 - 59 years old Local Cases"].sum() ,font=('Courier',18,'bold'), background="#242424",foreground="white")
totalcases40to60.grid(row=1, column=2)

#Second row of frame grid
totalcases19to39_Label = ttk.Label(analysisFrame2, text='Cases Age 20 - 39:' ,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
totalcases19to39_Label.grid(row=2, column=0, padx=10, pady=(35,0))
totalcases19to39 = ttk.Label(analysisFrame2, text=dfDict["localsByAge"]["20 - 39 years old Local Cases"].sum(),font=('Courier',18,'bold'), background="#242424",foreground="white")
totalcases19to39.grid(row=3, column=0)

totalcases12to18_Label = ttk.Label(analysisFrame2, text='Cases Age 12 - 19:' ,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
totalcases12to18_Label.grid(row=2, column=1, padx=10, pady=(35,0))
totalcases12to18 = ttk.Label(analysisFrame2, text=dfDict["localsByAge"]["12 - 19 years old Local Cases"].sum(),font=('Courier',18,'bold'), background="#242424",foreground="white")
totalcases12to18.grid(row=3, column=1)

totalcases0to11_Label = ttk.Label(analysisFrame2, text='Cases Age 0 - 11:' ,font=('Courier',18,'bold'), background="#242424",foreground="#87CEEB")
totalcases0to11_Label.grid(row=2, column=2, padx=10, pady=(35,0))
totalcases0to11 = ttk.Label(analysisFrame2, text=dfDict["localsByAge"]["0 - 11 years old Local Cases"].sum(),font=('Courier',18,'bold'), background="#242424",foreground="white")
totalcases0to11.grid(row=3, column=2)

# Analysis Graphs Label --------------------------------- (Author: BaoHuan & Meng Rong)
customGraphFrame = tk.LabelFrame(StatsFrame, background="#242424", text="Plot Custom Graph", font=('Aquire',12,'bold'), foreground="white")
customGraphFrame.place(relheight=0.40, relwidth=0.25, rely=0.55, relx=0.73)


# Plot Analyssis Graph Button --------------------------------- (Author: BaoHuan & Meng Rong)
customBtn1 = tk.Button(customGraphFrame, text="Current Active Cases", width=35, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:cvdstats.analysis_bar_ActiveCases(dfDict["Current Active Cases"]))
customBtn1.place(rely=0.15, relx=0.05)

customBtn2 = tk.Button(customGraphFrame, text="% O2 Supplementation", width=35, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:cvdstats.analysis_scatter_percentO2(dfDict["PercentO2"]))
customBtn2.place(rely=0.3, relx=0.05)

customBtn3 = tk.Button(customGraphFrame, text="ICU Cases by Age Range", width=35, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:cvdstats.analysis_pie_ICU_AgeGroup(dfDict['icuByAge']))
customBtn3.place(rely=0.45, relx=0.05)

customBtn4 = tk.Button(customGraphFrame, text="Local Cases by Age Range", width=35, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:cvdstats.analysis_pie_TotalCases_AgeGroup(dfDict['localsByAge']))
customBtn4.place(rely=0.6, relx=0.05)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Step 4: Show the GUI Interface
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
refresh()
raise_frame(MainFrame)
root.mainloop()