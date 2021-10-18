# References
# That answer of Chuck666 did the trick: https://stackoverflow.com/a/60949800/4352930
# https://www.youtube.com/watch?v=PgLjwl6Br0k&list=LL&index=1&t=1425s&ab_channel=RamonWilliams
# https://www.youtube.com/watch?v=WdhNkabUAVU&ab_channel=softwareManiac
# https://www.semicolonworld.com/question/42826/switch-between-two-frames-in-tkinter#comment-21

# Imported Modules
from datetime import datetime
from itertools import count
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import Message, Widget, filedialog , messagebox , ttk
from tkinter.constants import BOTTOM, DISABLED, FALSE, NORMAL, TRUE, X
import numpy
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.indexing import check_bool_indexer

# Self-made Modules
import seaborn as sns #bh code
import matplotlib.pyplot as plt #bh code
from matplotlib.figure import Figure #bh code
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #bh code
from matplotlib.widgets import CheckButtons #bh code
#import CovidStatistics as cvdstats #mengrong code module


# Always place Functions first before __main__ code
#--- Functions -------------------------------------------------------------------------------------------------------------

#Fixed Colour Problem -----------------Author: Sow Ying
def fixed_map(option):
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]


# Function to change frame -------------Author: Sow Ying
def raise_frame(frame):
    frame.tkraise()


# Browsing Data File -------------Author: Sow Ying
def file_dialog():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("xlsx files","*.xlsx"),("All Files","*.*")))
    label_file["text"] = filename
    return None
    

# Raw data into DataFrame -------------Author: Sow Ying
def load_excel_data():
    global df1
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        df1 = pd.read_excel(excel_filename)
        df = df1.applymap(str)
        reversed_df = df.iloc[::-1]

    except ValueError:
        tk.messagebox.showerror(message="Invalid File")
        return None
    except FileNotFoundError:
         tk.messagebox.showerror(message="No Such file found")
         return None

    clear_data()

    latestCaseNum = reversed_df.at[reversed_df.index[0],'Cumulative Confirmed']

    CasesNumLabel = ttk.Label(MainFrame, text='Confrimed Cases (as of now):' ,font=('Courier',10,'bold'), background="#242424",foreground="white")
    CasesNumLabel.place(rely=0.72, relx=0.62)

    CasesNum = ttk.Label(MainFrame, text=latestCaseNum ,font=('Courier',30,'bold'), background="#242424",foreground="white")
    CasesNum.place(rely=0.76, relx=0.62)

    newcolumn = reversed_df[['Date','Daily Confirmed','Cumulative Confirmed','Daily Imported','Daily Local transmission']]
    newcolumn1 = reversed_df[['Date','Daily Confirmed','Cumulative Confirmed','Daily Imported','Daily Local transmission']].copy()
    CleanNewcolumn = newcolumn1.dropna(subset=['Date']) #Drop only if NaN in specific column (as asked in the question)

    treeView1["column"] = list(CleanNewcolumn.columns)
    treeView1["show"] = "headings"
    for column in treeView1["column"]:
        treeView1.heading(column, text=column)

    df_row = CleanNewcolumn.to_numpy().tolist()
    for row in df_row:
        treeView1.insert("","end",values=row)
    return None


# Clear Treeview table -------------Author: Sow Ying
def clear_data():
    treeView1.delete(*treeView1.get_children())


# Search Function on Treeview table -------------Author: Sow Ying
def search_excel_data(isClicked):

    INPUT = searchInput.get("1.0", "end-1c")

    if (isClicked == 1) :
        load_excel_data()

    if (INPUT == "") and (isClicked == 1) :
          tk.messagebox.showerror(message="Please enter something...")
    
    itemsonTreeView = treeView1.get_children()
    treeView1.tag_configure('searchrow', background='#527584',foreground='white')

    for eachItem in itemsonTreeView:

        if (searchvar1.get() == 1) & (INPUT != "") & (isClicked == 1):

            if INPUT in treeView1.item(eachItem)['values'][0]:

                print(treeView1.item(eachItem)['values'][0])
                search_varr = treeView1.item(eachItem)['values']
                treeView1.delete(eachItem)
            
                treeView1.insert("",0, values=search_varr, tags=('searchrow',))

        elif (searchvar2.get() == 1) & (INPUT != "") & (isClicked == 1):

            if INPUT in treeView1.item(eachItem)['values'][1]:

                print(treeView1.item(eachItem)['values'][1])
                search_varr = treeView1.item(eachItem)['values']
                treeView1.delete(eachItem)
            
                treeView1.insert("",0, values=search_varr, tags=('searchrow',))

        elif (searchvar3.get() == 1) & (INPUT != "") & (isClicked == 1):

            if INPUT in treeView1.item(eachItem)['values'][2]:

                print(treeView1.item(eachItem)['values'][2])
                search_varr = treeView1.item(eachItem)['values']
                treeView1.delete(eachItem)
            
                treeView1.insert("",0, values=search_varr, tags=('searchrow',))

        elif (searchvar4.get() == 1) & (INPUT != "") & (isClicked == 1):

            if INPUT in treeView1.item(eachItem)['values'][3]:

                print(treeView1.item(eachItem)['values'][3])
                search_varr = treeView1.item(eachItem)['values']
                treeView1.delete(eachItem)
            
                treeView1.insert("",0, values=search_varr, tags=('searchrow',))

        elif (searchvar5.get() == 1) & (INPUT != "") & (isClicked == 1):

            if INPUT in treeView1.item(eachItem)['values'][4]:

                print(treeView1.item(eachItem)['values'][4])
                search_varr = treeView1.item(eachItem)['values']
                treeView1.delete(eachItem)
            
                treeView1.insert("",0, values=search_varr, tags=('searchrow',))

        else:
            pass


# Function for checkbutton selecting column for x & y - axis  -------------Author: Bao Huan
def selection():
    x_axis =""
    y_axis = ""
    if statvar1.get() == 1:
        x_axis = "Date"
    if statvar2.get() == 1:
        y_axis = "Daily Confirmed"
    elif statvar3.get() == 1:
        y_axis = "Cumulative Confirmed"
    elif statvar4.get()==1:
        y_axis = "Daily Imported"
    elif statvar5.get()==1:
        y_axis = "Daily Local transmission"
    else: 
        pass
    print(x_axis, y_axis)
    return [x_axis, y_axis]


# Function for launching Line Graph based on selected checkbox  -------------Author: Bao Huan
def viewLineGraph(): 
    """Using Seaborn method to display a linegraph"""
    #using seaborn
    #filepath = label_file["text"]
    '''excel_filename = r"{}".format(filepath)
    df = pd.read_excel(excel_filename)'''
    
    #year = pd.DatetimeIndex(df['Date']).year
    #sns.lineplot()
    y = selection()
    plt.plot(y[0], y[1],data=df1)
    #sns.barplot()
    #sns.barplot(x="Date", y='Daily Confirmed', data=df)
    #sns.barplot(x=year, y='Daily Confirmed', data=df)
    plt.title("Covid19 Cases", color='Blue')
    plt.show()
    '''except:
        tk.messagebox.showerror(message="File is not loaded")'''
        

# Function for launching Line Graph based on selected checkbox  -------------Author: Bao Huan
def view_countplot():
    try:
        filepath = label_file["text"]
        excel_filename = r"{}".format(filepath)
        df = pd.read_excel(excel_filename)
        year = pd.DatetimeIndex(df['Date']).year
        
        sns.lineplot(x=year, y='Daily Confirmed', data=df)
        plt.xlabel("Year")
        plt.ylabel("Total cases")
        plt.title("Covid19 Cases by year")
        plt.legend
        plt.show()
    except:
        tk.messagebox.showerror(message="File is not loaded")



# Exporting Selected DataFrame -------------Author: Yong Javen
def export_excel():
    pass
    # compilated_list=[]
    
    # itemsonTreeView = treeView1.get_children()
    # #treeView1.tag_configure('exportrow', background='#527584',foreground='white')

    # for eachItem in itemsonTreeView:    
    #     new=[]
    #     if (exportvar1.get() == 1) & (isClicked == 1):
    #         fields = treeView1.item(eachItem)['values'][0]
    #         selected_item = treeView1.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar2.get() == 1) & (isClicked == 1):
    #         fields = treeView1.item(eachItem)['values'][1]
    #         selected_item = treeView1.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar3.get() == 1) & (isClicked == 1):
    #         fields = treeView1.item(eachItem)['values'][2]
    #         selected_item = treeView1.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar4.get() == 1) & (isClicked == 1):
    #         fields = treeView1.item(eachItem)['values'][3]
    #         selected_item = treeView1.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar5.get() == 1) & (isClicked == 1):
    #         fields = treeView1.item(eachItem)['values'][4]
    #         selected_item = treeView1.item(eachItem)['values']
    #         new.append(fields)
    #     compilated_list.append(new)

    # exported_data = pd.DataFrame(compilated_list)
    # exported_data.to_csv('Exported.csv', index=False)



#--- Set Up --------------------------------------------------------- (__main__ code)
#initiallise
root = tk.Tk()
root.geometry("1280x720") # width x height
root.pack_propagate(False) #dont resize based on widget
root.resizable(0,0) #Window cant be resize

style = ttk.Style()
style.map("Treeview", 
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))

#Set Frame Pages
MainFrame = tk.Frame(root,bg='#242424')
MainFrame.place(height=720, width=1280)   

StatsFrame = tk.Frame(root,bg='#242424')
StatsFrame.place(height=720, width=1280)


#--- Main Page - Buttons --------------------------------------------- (__main__ code)
menuFrame = tk.LabelFrame(MainFrame,background="#636262")
menuFrame.place(height=50, width=990, relx=0.005 ,rely=0.005)  

MainTitle = ttk.Label(MainFrame, text='Covid-19 Analyser' , font=('Aquire',22,'bold'), background="#636262",foreground="white")
MainTitle.place(rely=0.01, relx=0.01)

#Refresh Button
RefreshButton = tk.Button(MainFrame, text="REFRESH",width=15,font=('Courier',10,'bold'),background="#242424",
                                                    foreground="white", command=lambda:load_excel_data())
RefreshButton.place(relx=0.85 ,rely=0.02)

#To Stats Page Button
toStatsBtn = tk.Button(MainFrame, text="VIEW STATISTICS",height =2, width = 26, font=('Courier',18,'bold'),
                                                        background="#636262",foreground="white", borderwidth=0,
                                                        command=lambda:raise_frame(StatsFrame))
toStatsBtn.place(rely=0.6, relx=0.62)


#--- Main Page - TreeView --------------------------------------------- (__main__ code)

#Frame for TreeView
viewFrame = tk.LabelFrame(MainFrame,background="#636262")
viewFrame.place(height=545, width=600, relx=0.005, rely=0.25)  

#Treeview Widget
treeView1 = ttk.Treeview(viewFrame)
treeView1.place(relheight=1, relwidth=1)

#Treeview scrollbar
treescrolly = tk.Scrollbar(viewFrame, orient="vertical", command=treeView1.yview)
treescrollx = tk.Scrollbar(viewFrame, orient="horizontal", command=treeView1.xview)
treeView1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")


#--- Main Page - Search --------------------------------------------- (__main__ code)

searchFrame = tk.LabelFrame(MainFrame,background="#636262")
searchFrame.place(height=80, width=990, relx=0.005,rely=0.1)

searchInput = tk.Text(searchFrame, height = 0.5, width = 80)
searchInput.place(rely=0.2, relx=0.01)

searchButton = tk.Button(searchFrame, text="SEARCH",width=15,font=('Courier',10,'bold'),background="#242424",
                                                    foreground="white", command=lambda:search_excel_data(1))
searchButton.place(rely=0.1, relx=0.7) 

searchvar1 = tk.IntVar()
searchvar2 = tk.IntVar()
searchvar3 = tk.IntVar()
searchvar4 = tk.IntVar()
searchvar5 = tk.IntVar()
searchvar6 = tk.IntVar()

searchc1 = tk.Checkbutton(searchFrame, text='Date',variable=searchvar1, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262", command=lambda:search_excel_data(0))
searchc1.place(rely=0.5, relx=0.01)

searchc2 = tk.Checkbutton(searchFrame, text='Daily Confirmed',variable=searchvar2, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262", command=lambda:search_excel_data(0))
searchc2.place(rely=0.5, relx=0.07)

searchc3 = tk.Checkbutton(searchFrame, text='Cumulative Confirmed',variable=searchvar3, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262", command=lambda:search_excel_data(0))
searchc3.place(rely=0.5, relx=0.195)

searchc4 = tk.Checkbutton(searchFrame, text='Daily Imported',variable=searchvar4, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262", command=lambda:search_excel_data(0))
searchc4.place(rely=0.5, relx=0.35)

searchc5 = tk.Checkbutton(searchFrame, text='Daily Local transmission',variable=searchvar5, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262", command=lambda:search_excel_data(0))
searchc5.place(rely=0.5, relx=0.46)


#--- Main Page - Export --------------------------------------------- (__main__ code)

exportFrame = tk.LabelFrame(MainFrame, background="#242424")
exportFrame.place(height=200, width=370, rely=0.25, relx=0.62) 

exportvar1 = tk.IntVar()
exportvar2 = tk.IntVar()
exportvar3 = tk.IntVar()
exportvar4 = tk.IntVar()
exportvar5 = tk.IntVar()
exportvar6 = tk.IntVar()

exportc1 = tk.Checkbutton(exportFrame, text='Date',variable=exportvar1, onvalue=1, offvalue=0,background="#242424",foreground='white',selectcolor="#636262", command=lambda:export_excel())
exportc1.place(rely=0.05, relx=0.05)

exportc2 = tk.Checkbutton(exportFrame, text='Daily Confirmed',variable=exportvar2, onvalue=1, offvalue=0,background="#242424",foreground='white',selectcolor="#636262", command=lambda:export_excel())
exportc2.place(rely=0.25, relx=0.05)

exportc3 = tk.Checkbutton(exportFrame, text='Cumulative Confirmed',variable=exportvar3, onvalue=1, offvalue=0,background="#242424",foreground='white',selectcolor="#636262", command=lambda:export_excel())
exportc3.place(rely=0.45, relx=0.05)

exportc4 = tk.Checkbutton(exportFrame, text='Daily Imported',variable=exportvar4, onvalue=1, offvalue=0,background="#242424",foreground='white',selectcolor="#636262", command=lambda:export_excel())
exportc4.place(rely=0.65, relx=0.05)

exportc5 = tk.Checkbutton(exportFrame, text='Daily Local transmission',variable=exportvar5, onvalue=1,offvalue=0,background="#242424",foreground='white',selectcolor="#636262", command=lambda:export_excel())
exportc5.place(rely=0.85, relx=0.05)

exportButton = tk.Button(exportFrame, text="EXPORT", width=15,font=('Courier',10,'bold'),background="#636262",
                                                    foreground="white", command=lambda:export_excel()())
exportButton.place(rely=0.8, relx=0.6)

#--- Main Page - Open File --------------------------------------------- (__main__ code)

fileFrame = tk.LabelFrame(MainFrame,background="#242424")
fileFrame.place(height=90, width=370, rely=0.85, relx=0.62)

label_file = ttk.Label(fileFrame, text="No file selected",background="#242424",foreground="white")
label_file.place(rely=0, relx=0)

browseButton = tk.Button(fileFrame,  text="BROWSE", width=15,font=('Courier',10,'bold'),background="#636262",
                                                    foreground="white", command=lambda: file_dialog()) 
browseButton.place(rely=0.65, relx=0.55)

loadButton = tk.Button(fileFrame,  text="LOAD", width=15,font=('Courier',10,'bold'),background="#636262",
                                                    foreground="white", command=lambda:load_excel_data())
loadButton.place(rely=0.65, relx=0.10)


#--- Stats Page --------------------------------------------- (__main__ code)

#To Main Page Button
toMainBtn2 = tk.Button(StatsFrame, text="Back",height =1, width = 10, command=lambda:raise_frame(MainFrame))
toMainBtn2.place(rely=0, relx=0)

#BaoHuan code
#Button of stats
viewLinegraphbtn = tk.Button(StatsFrame, text="LINEGRAPH", width=15, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:cvdstats.lineplot_graph())
viewLinegraphbtn.place(rely=0.6, relx=0.62)

viewCountplotBtn = tk.Button(StatsFrame, text="COUNTPLOT", width=15, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white", command=lambda:view_countplot())
viewCountplotBtn.place(rely=0.7, relx=0.62)

customBtn = tk.Button(StatsFrame, text="CUSTOM", width=15, font=('courier', 10, 'bold'), background = "#242424",
                            foreground="white")
customBtn.place(rely=0.8, relx=0.62)

statvar1 = tk.IntVar()
statvar2 = tk.IntVar()
statvar3 = tk.IntVar()
statvar4 = tk.IntVar()
statvar5 = tk.IntVar()

statc1 = tk.Checkbutton(StatsFrame, text='Date', variable=statvar1, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262")
statc1.place(rely=0.1, relx=0.01)

statc2 = tk.Checkbutton(StatsFrame, text='Daily Confirmed',variable=statvar2, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262")
statc2.place(rely=0.2, relx=0.01)

statc3 = tk.Checkbutton(StatsFrame, text='Cumulative Confirmed', variable=statvar3, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262")
statc3.place(rely=0.3, relx=0.01)

statc4 = tk.Checkbutton(StatsFrame, text='Daily Imported', variable=statvar4, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262")
statc4.place(rely=0.4, relx=0.01)

statc5 = tk.Checkbutton(StatsFrame, text='Daily Local transmission', variable=statvar5, onvalue=1, offvalue=0, background="#636262",foreground='white',selectcolor="#636262")
statc5.place(rely=0.5, relx=0.01)

#--- Launch App ---------------------------------------------
raise_frame(MainFrame)
root.mainloop()