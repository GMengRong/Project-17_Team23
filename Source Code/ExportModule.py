# Exporting Selected DataFrame -------------Author: Yong Javen

from os import name

def export_excel(df, selectedColumn):
    exported_data = df[selectedColumn].copy()
    exported_data.to_csv('Exported.csv', index=False)

    # compilated_list=[]
    
    # itemsonTreeView = treeView_v.get_children()

    #treeView1.tag_configure('exportrow', background='#527584',foreground='white')

    # for eachItem in itemsonTreeView:    
    #     new=[]
    #     if (exportvar_1.get() == 1) & (isClicked == 1):
    #         fields = treeView_v.item(eachItem)['values'][0]
    #         selected_item = treeView_v.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar_2.get() == 1) & (isClicked == 1):
    #         fields = treeView_v.item(eachItem)['values'][1]
    #         selected_item = treeView_v.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar_3.get() == 1) & (isClicked == 1):
    #         fields = treeView_v.item(eachItem)['values'][2]
    #         selected_item = treeView_v.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar_4.get() == 1) & (isClicked == 1):
    #         fields = treeView_v.item(eachItem)['values'][3]
    #         selected_item = treeView_v.item(eachItem)['values']
    #         new.append(fields)
    #     if (exportvar_5.get() == 1) & (isClicked == 1):
    #         fields = treeView_v.item(eachItem)['values'][4]
    #         selected_item = treeView_v.item(eachItem)['values']
    #         new.append(fields)
    #     compilated_list.append(new)

    # exported_data = pd.DataFrame(compilated_list)
    # exported_data.to_csv('Exported.csv', index=False)