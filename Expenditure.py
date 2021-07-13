# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:17:04 2020

@author: Aniruddh Acharya
"""

import sqlite3
from tkinter import *
from PIL import ImageTk, Image
import datetime
from tkinter import messagebox
import xlwings as xw

def add_entry():
 
    conn=sqlite3.connect('Patient_Database.db')
    c=conn.cursor()
       
    add=Tk()
    add.title('Adding Entry')
    add.iconbitmap("shree_brahmi.ico")
    
    global datestring
    today = datetime.date.today()
    datestring=str(today.day)+"/"+str(today.month)+"/"+str(today.year)
    
    def edit():
        
        global ed       
        ed=Toplevel()
        ed.title('Adding Entry')
        ed.iconbitmap("shree_brahmi.ico")
        
        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
        
        record_id=fileno_editor.get()
        
        
        name_label=Label(ed,text="Name",font='Helvetica 16 bold')
        fileno_label=Label(ed,text="File Number",font='Helvetica 16 bold')
        date_label=Label(ed,text="Date",font='Helvetica 16 bold')
        ie=IntVar()
        oc=IntVar()
        tp=IntVar()
        ie.set(0)
        oc.set(0)
        tp.set(0)
        amount_label=Label(ed,text="Amount",font='Helvetica 16 bold')
        description_label=Label(ed,text="Description",font='Helvetica 16 bold')
        
        fileno_label.grid(row=0,column=0,ipady=3)
        name_label.grid(row=1,column=0,padx=10)
        date_label.grid(row=2,column=0,padx=10)
        amount_label.grid(row=7,column=0,padx=10)
        description_label.grid(row=8,column=0,padx=10)
        
        
        name=Entry(ed,width=50)
        fileno=Entry(ed,width=20) 
        date=Entry(ed,width=20) 
        amount=Entry(ed,width=30)
        description=Text(ed,width=50,height=5)
        
        name.grid(row=1,column=1,padx=20,ipady=3)
        fileno.grid(row=0,column=1)
        date.grid(row=2,column=1)
        Radiobutton(ed,text="Income", variable=ie, value=0).grid(row=3,column=0,padx=1)
        Radiobutton(ed,text="Expense", variable=ie, value=1).grid(row=3,column=1,padx=1)   
        Radiobutton(ed,text="None", variable=oc, value=0).grid(row=4,column=0,padx=1)
        Radiobutton(ed,text="Opex", variable=oc, value=1).grid(row=4,column=1,padx=1)
        Radiobutton(ed,text="Capex", variable=oc, value=2).grid(row=4,column=2,padx=1)
        Radiobutton(ed,text="Medicine", variable=oc, value=3).grid(row=4,column=3,padx=1)
        Radiobutton(ed,text="Cash", variable=tp, value=0).grid(row=5,column=0,padx=1)
        Radiobutton(ed,text="UPI", variable=tp, value=1).grid(row=5,column=1,padx=1)
        Radiobutton(ed,text="NEFT", variable=tp, value=2).grid(row=5,column=2,padx=1)
        Radiobutton(ed,text="Cc/Dc", variable=tp, value=3).grid(row=5,column=3,padx=1)
        amount.grid(row=7,column=1)
        description.grid(row=8,column=1,columnspan=2,ipady=10,padx=5,pady=3)
        
        
        c.execute("SELECT * FROM PatientData WHERE File_Number LIKE '"+ record_id+"'") 
        records=c.fetchall()
        
        for record in records:
            fileno.insert(0,record[0]) 
            name.insert(0,record[1])
        date.insert(0,datestring)
        description.insert(1.0," ")
            
        def update():
            conn=sqlite3.connect('Patient_Database.db')
            c=conn.cursor()
            
            iec=' '
            occ=' '
            tpc=' '
            if ie.get()==0:
                iec="Income"
            elif ie.get()==1:
                iec="Expense"
            if oc.get()==0:
                occ="None"
            elif oc.get()==1:
                occ="Opex"
            elif oc.get()==2:
                occ="Capex"
            elif oc.get()==3:
                occ="Medicine"
            if tp.get()==0:
                tpc="Cash"
            elif tp.get()==1:
                tpc="UPI"
            elif tp.get()==2:
                tpc="Net Banking"
            elif tp.get()==3:
                tpc="Credit/Debit"
            
            
            c.execute("INSERT INTO ExpenditureData values(:fileno,:name,:date,:incomeexpense,:opexcapex,:typepayment,:amount,:description)",
                  { 'fileno':fileno.get(),
                   'name':name.get(),
                   'date':datestring,
                   'incomeexpense':str(iec),
                   'opexcapex':str(occ),
                   'typepayment':str(tpc),
                   'amount':int(amount.get()),
                   'description':str(description.get("1.0","end-1c"))
                   } )
            messagebox.showinfo("Updated","The Entry has been successfully Added!")
            ed.destroy()
                        
            conn.commit()
            conn.close()
    
           
        fileno_editor.delete(0,END)  
        save_button=Button(ed,text="Save",font='verdana 12 bold',command=update)
        save_button.grid(row=9,column=0,columnspan=2,pady=10,ipadx=170)
        
        exit_button=Button(ed, text="Quit",font='verdana 12 bold', command=ed.destroy)
        exit_button.grid(row=9,column=2,columnspan=2,pady=10,ipadx=170)        
                
        conn.commit()
        conn.close()
          
    
    fileno_label=Label(add,text="File Number",font='16')
    fileno_label.grid(row=1,column=0,padx=10,ipadx=20)
    global fileno_editor    
    fileno_editor=Entry(add,width=30)
    fileno_editor.grid(row=1,column=1,padx=10,ipadx=30)
    
    update_button=Button(add,text="Update Entry",font='verdana 12 bold',command=edit)
    update_button.grid(row=4,columnspan=2,pady=10,ipadx=100)  
    
    conn.commit()
    conn.close()





def search_entry():
    
    sea=Toplevel()
    sea.title('Searching Patient')
    sea.iconbitmap("shree_brahmi.ico")
    global records
    
    headings=['File Number','Name','Date',' Income/Expense ', ' Opex/Capex ',' Amount ',' Description ']
    
    
    def search_date():
        
        sead=Toplevel()
        sead.title('Searching Entry')
        sead.iconbitmap("shree_brahmi.ico")  
        
        sead.attributes("-fullscreen",True)
    
        
        def generate():

            excelworkbook=xw.Book('Report.xlsx')
            excelsheet=excelworkbook.sheets['Report1']
            excelsheet.range("A2").value=records
        

        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
            
        c.execute("SELECT * FROM ExpenditureData WHERE Date LIKE '%"+ str(date_search.get())+"%'") 
        records=c.fetchall()

        view_frame=Frame(sead)
        view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
        view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
        view_scrollbar.config(command=view_list.yview)
        view_scrollbar.pack(side=RIGHT,fill=Y)
        
        view_list['columns']=("File Number","Name","Amount","Date","Income/Expense","Opex/Capex","Payment Type","Description")
           
        view_list.column("#0",width=60,minwidth=50)
        view_list.column("File Number",width=120,minwidth=50)
        view_list.column("Name",width=200,minwidth=100)
        view_list.column("Amount",width=100,minwidth=100)
        view_list.column("Date",width=80,minwidth=50)
        view_list.column("Income/Expense",width=100,minwidth=40)
        view_list.column("Opex/Capex",width=100,minwidth=40)
        view_list.column("Payment Type",width=100,minwidth=40)
        view_list.column("Description",width=250,minwidth=40)
                
        
        
        
        view_list.heading("#0",text="Sl No.",anchor=W)
        view_list.heading("File Number",text="File No.",anchor=W)
        view_list.heading("Name",text="Name",anchor=W)
        view_list.heading("Amount",text="Amount",anchor=W)
        view_list.heading("Date",text="Date",anchor=W)
        view_list.heading("Income/Expense",text="Income/Expense",anchor=W)
        view_list.heading("Opex/Capex",text="Opex/Capex",anchor=W)
        view_list.heading("Payment Type",text="Payment Type",anchor=W)
        view_list.heading("Description",text="Description",anchor=W)
        
        i=1
        for record in records:
           view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],("₹ "+str(record[6])),record[2],record[3],record[4],record[5],record[7]))
           i+=1
        
        view_frame.pack(pady=20,padx=20)
        
        view_list.pack()
        conn.commit()
        conn.close()
        
        reportbutton=Button(sead,text="Generate Report",font='verdana 14 bold',command=generate)
        reportbutton.pack(pady=5)
        
        exit_button=Button(sead, text="Quit",font='verdana 12 bold', command=sead.destroy)
        exit_button.pack(pady=5)

        
        
    def search_fileno():
        
        seaf=Toplevel()
        seaf.title('Searching Entry')
        seaf.iconbitmap("shree_brahmi.ico")
           
        seaf.attributes("-fullscreen",True)
    
        
        def generate():            

            excelworkbook=xw.Book('Report.xlsx')
            excelsheet=excelworkbook.sheets['Report1']
            excelsheet.range("A2").value=records        

        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
            
        c.execute("SELECT * FROM ExpenditureData WHERE File_Number LIKE '"+ str(fileno_search.get())+"'")
        records=c.fetchall()

        
        view_frame=Frame(seaf)
        view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
        view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
        view_scrollbar.config(command=view_list.yview)
        view_scrollbar.pack(side=RIGHT,fill=Y)
        
        view_list['columns']=("File Number","Name","Amount","Date","Income/Expense","Opex/Capex","Payment Type","Description")
           
        view_list.column("#0",width=60,minwidth=50)
        view_list.column("File Number",width=120,minwidth=50)
        view_list.column("Name",width=200,minwidth=100)
        view_list.column("Amount",width=100,minwidth=100)
        view_list.column("Date",width=80,minwidth=50)
        view_list.column("Income/Expense",width=100,minwidth=40)
        view_list.column("Opex/Capex",width=100,minwidth=40)
        view_list.column("Payment Type",width=100,minwidth=40)
        view_list.column("Description",width=250,minwidth=40)
                
        
        
        
        view_list.heading("#0",text="Sl No.",anchor=W)
        view_list.heading("File Number",text="File No.",anchor=W)
        view_list.heading("Name",text="Name",anchor=W)
        view_list.heading("Amount",text="Amount",anchor=W)
        view_list.heading("Date",text="Date",anchor=W)
        view_list.heading("Income/Expense",text="Income/Expense",anchor=W)
        view_list.heading("Opex/Capex",text="Opex/Capex",anchor=W)
        view_list.heading("Payment Type",text="Payment Type",anchor=W)
        view_list.heading("Description",text="Description",anchor=W)
        
        i=1
        for record in records:
           view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],("₹ "+str(record[6])),record[2],record[3],record[4],record[5],record[7]))
           i+=1
        
        view_frame.pack(pady=20,padx=20)
        
        view_list.pack()
        
        conn.commit()
        conn.close()
        
        reportbutton=Button(seaf,text="Generate Report",font='verdana 14 bold',command=generate)
        reportbutton.pack(pady=5)
        
        exit_button=Button(seaf, text="Quit",font='verdana 12 bold', command=seaf.destroy)
        exit_button.pack(pady=5)
        
        
    date_label=Label(sea,text="Date",font='16')
    date_label.grid(row=0,column=0,padx=10,pady=3,ipadx=20)        
    date_search=Entry(sea,width=30)
    date_search.grid(row=0,column=1,padx=10,pady=3,ipadx=30)
    
    
    date_searchbutton=Button(sea,text="Search Entries",font='verdana 14 bold',command=search_date)
    date_searchbutton.grid(row=1,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
    fileno_label=Label(sea,text="File Number",font='16')
    fileno_label.grid(row=2,column=0,padx=10,pady=3,ipadx=20)        
    fileno_search=Entry(sea,width=20)
    fileno_search.grid(row=2,column=1,padx=10,pady=3,ipadx=30)
    
    
    fileno_searchbutton=Button(sea,text="Search Entries",font='verdana 14 bold',command=search_fileno)
    fileno_searchbutton.grid(row=3,column=0,padx=50,pady=7,ipadx=20,columnspan=2)


    
    
    
def view_entries():
    conn=sqlite3.connect('Patient_Database.db')
    c=conn.cursor()
    
    view=Toplevel()
    view.title('Viewing Database')
    view.iconbitmap("shree_brahmi.ico")    
    view.attributes("-fullscreen",True)
    
    c.execute("SELECT * FROM ExpenditureData") 
    records=c.fetchall()

    view_frame=Frame(view)
    view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
    
    view_list = ttk.Treeview(view_frame, height=30, yscrollcommand=view_scrollbar.set)
    
    view_scrollbar.config(command=view_list.yview)
    view_scrollbar.pack(side=RIGHT,fill=Y)
    
    view_list['columns']=("File Number","Name","Amount","Date","Income/Expense","Opex/Capex","Payment Type","Description")
       
    view_list.column("#0",width=60,minwidth=50)
    view_list.column("File Number",width=120,minwidth=50)
    view_list.column("Name",width=200,minwidth=100)
    view_list.column("Amount",width=100,minwidth=100)
    view_list.column("Date",width=80,minwidth=50)
    view_list.column("Income/Expense",width=100,minwidth=40)
    view_list.column("Opex/Capex",width=100,minwidth=40)
    view_list.column("Payment Type",width=100,minwidth=40)
    view_list.column("Description",width=250,minwidth=40)
            
    
    
    
    view_list.heading("#0",text="Sl No.",anchor=W)
    view_list.heading("File Number",text="File No.",anchor=W)
    view_list.heading("Name",text="Name",anchor=W)
    view_list.heading("Amount",text="Amount",anchor=W)
    view_list.heading("Date",text="Date",anchor=W)
    view_list.heading("Income/Expense",text="Income/Expense",anchor=W)
    view_list.heading("Opex/Capex",text="Opex/Capex",anchor=W)
    view_list.heading("Payment Type",text="Payment Type",anchor=W)
    view_list.heading("Description",text="Description",anchor=W)
    
    i=1
    for record in records:
       view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],("₹ "+str(record[6])),record[2],record[3],record[4],record[5],record[7]))
       i+=1
    
    view_frame.pack(pady=20,padx=20)
    
    view_list.pack()

    exit_button=Button(view, text="Quit",font='verdana 12 bold', command=view.destroy)
    exit_button.pack()
        
    conn.commit()
    conn.close()
    
