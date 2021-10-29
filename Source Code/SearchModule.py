import tkinter as tk

# Function to Search up data from the TreeView -------------Author: Sow Ying
def search(isClicked_v,searchvariable_v,columnname_v,searchInput_v,reload_TreeView,treeView1_v):

    global colindex
    searchedcol = searchvariable_v.get()

    for i, j in enumerate(columnname_v):
        if j == searchedcol:
            colindex = i
            print(colindex)

    INPUT = searchInput_v.get("1.0", "end-1c")

    if (INPUT == ""):
         tk.messagebox.showerror(message="Please enter something...")
         return 0

    if (isClicked_v == 1) :
         reload_TreeView()
    
    itemsonTreeView = treeView1_v.get_children()
    treeView1_v.tag_configure('searchrow', background='#527584',foreground='white')

    for eachItem in itemsonTreeView:

        if INPUT in treeView1_v.item(eachItem)['values'][colindex]:
            
             search_varr = treeView1_v.item(eachItem)['values'] 
             treeView1_v.delete(eachItem) #delete that rows
             treeView1_v.insert("",0, values=search_varr, tags=('searchrow',))

        elif INPUT not in treeView1_v.item(eachItem)['values']:

             treeView1_v.delete(eachItem) #delete that rows  

        else:
                pass
