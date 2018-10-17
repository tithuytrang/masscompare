import pandas

from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox  
def file_open(title_name):
    root = Tk()
    root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = title_name,filetypes = (("csv files","*.csv"),("all files","*.*")))
    root.destroy()
    return root.filename

def select_dir():
    root = Tk()
    root.directory = tkFileDialog.askdirectory()
    root.destroy()
    return root.directory



def LC_read():
    try:
        file1 = file_open('Select LC (time - intensity) file')
        LC = pandas.read_csv(file1, header=None)
        global LC, file1
    except:
        tkMessageBox.showwarning(
            "Open file",
            "Cannot open this file\n(%s)" % file
        )
        return
#    LC_sort = LC.sort_values(2,ascending=False)
    
#    LC_top = []
#    for index, row in LC_sort.iterrows():
#        if float(row[2]) <= 50:
#            new = LC_sort.drop(index)
#        else:
#            newitem = row[0],row[2]
#            LC_top.append(newitem)


#LC_sort.to_dict(orient='index')

def LC_peak_get():
    LC_peak = []
    for index, row in LC.iterrows():
        try:
            if LC[2][index] >= LC[2][index-1] and LC[2][index] > LC[2][index+1]:
                new = str(row[0]), str(row[2])
                LC_peak.append(new)
        except KeyError:
            pass
    global LC_peak

def LC_peak_cut():
    LC_peakcut = []
    for time, intensity in LC_peak:
        if float(intensity) >= 10:
            new =  time, intensity
            LC_peakcut.append(new)
    global LC_peakcut

def MS_read():
    file2 = file_open('Select MS (start, end time, mass mono) file')
    LC_mass = pandas.read_csv(file2)
    MS_time = []
    for index, row in LC_mass.iterrows():
        newitem2 = row[0],row[5],row[6]
        MS_time.append(newitem2)
    global MS_time, file2

def result_1():
    result1 = []
    for time, intensity in LC_peakcut:
        for mass, start, end in MS_time:
            if float(start) <= float(time) and float(time) <= float(end):
                newitem3 = str(time), mass, intensity
                result1.append(newitem3)
    global result1

def MS_info_read():
    file3 = file_open('Select MS info file from Conoserver')
    Mass_info = pandas.read_csv(file3)
    MS_peptide = []
    for index, row in Mass_info.iterrows():
        newitem4 = row[0], row[3]
        MS_peptide.append(newitem4)
    global MS_peptide, file3

def result_2():    
    result2 = []
    for time, mass, intensity in result1:
        for peakmass, peptide in MS_peptide:
            if mass == peakmass:
                newitem5 = time, peptide
                result2.append(newitem5)
    global result2

def final():
    final = {}
    for time, peptide in result2:
        final.update({time:[]})
    
    for key, value in final.items():
        for time, peptide in result2:
            if key == time:
                head, sep, tail = peptide.partition(' (')
                if head not in value:
                    value.append(head)
    
    for key, value in final.items():
        for time, intensity in LC_peakcut:
            if str(key) == str(time):
                value.insert(0,str(intensity))
    
    for key, value in final.items():
        newn = '/'.join(value[1:])
        final[key] = value[0], newn
    
    global final
    

def export(): 
    finalresult = pandas.Series(final).to_frame()
    finalresult = pandas.DataFrame.from_dict(final, orient='index')
    directory = select_dir()
    finalresult.to_csv(directory + '/result.csv',index=True)

def confirm1(filename):
    if tkMessageBox.askyesno("Confirm", filename + " selected, are you sure ?"):
        pass
    else:
        LC_read()
        
def confirm2(filename):
    if tkMessageBox.askyesno("Confirm", filename + " selected, are you sure ?"):
        pass
    else:
        MS_read()        
    
def confirm3(filename):
    if tkMessageBox.askyesno("Confirm", filename + " selected, are you sure ?"):
        pass
    else:
        MS_info_read()   

def about():
    tkMessageBox.showinfo(
            "Info",
            """Made by Trang Truong - personal purpose only
Beta test version 17.10.18"""
        )
    
def exit_():
    root.destroy()

def insert(word):    
    w = Label(root, text=word)
    w.pack()

def begin():
    LC_read()
#    confirm1(file1)
    LC_peak_get()
    LC_peak_cut()
    MS_read()
#    confirm2(file2)
    result_1()
    MS_info_read()
#    confirm3(file3)
    result_2()
    final()
    export()

root = Tk()

# create a menu
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=begin)
filemenu.add_command(label="Open...", command=begin)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about)


mainloop()
