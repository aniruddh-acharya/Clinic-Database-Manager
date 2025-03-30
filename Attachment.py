# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 19:04:19 2021

@author: Aniruddh Acharya
"""

import sqlite3
from tkinter import messagebox
import PIL
from tkinter import *
from tkinter import filedialog
import datetime
from tkinter import ttk
import os

global datestring
today = datetime.date.today()
datestring=str(today.day)+"/"+str(today.month)+"/"+str(today.year)

def attach_file():
 
    att=Tk()
    att.title('Saving Attachment')
    att.iconbitmap("shree_brahmi.ico")
    
    def find():
        conn=sqlite3.connect('Clinic_Database.db')
        cursor=conn.cursor()
        att.filename=filedialog.askopenfilename(initialdir="C:/", title="Select A File",filetypes=(("All files","*.*"),("png files","*.png"),("jpg files","*.jpg"),("jpeg files","*.jpeg"),("pdf files","*.pdf")))
       
        split_tup = os.path.splitext(att.filename)
        file_extension = split_tup[1]
        
        ftype=0;
        if(file_extension==".pdf"):
            ftype=1
        if(file_extension==".doc" or file_extension==".docx"):
            ftype=2
        if(file_extension==".xls" or file_extension==".xlsx" or file_extension==".csv"):
            ftype=3
        if(file_extension==".mp4"):
            ftype=4
        if(file_extension==".mkv"):
            ftype=5
        if(file_extension==".avi"):
            ftype=6
        if(file_extension==".mpeg"):
            ftype=7
            
        
        with open(att.filename, "rb") as file:
            blob=file.read()
        
        cursor.execute("SELECT Name FROM PatientData WHERE File_Number LIKE '%"+ str(fileno.get())+"%' LIMIT 1")
        records=cursor.fetchall()
        name=records[0][0]
        
        cursor.execute("SELECT * FROM Attachment")
        records=cursor.fetchall()
        sl_no=len(records)+1
        
        cursor.execute("INSERT INTO Attachment (Sl_No,File_Number,Name,File,Description,Date,Format) VALUES (?,?,?,?,?,?,?)",(sl_no,fileno.get(),name,blob,description.get(),datestring,ftype))
        cursor.close()
        conn.commit()
        
        messagebox.showinfo("Added","The File has been Successfuly added to the database!")
        att.destroy()
                
    
    fileno_label=Label(att,text="File Number",font='20')
    fileno_label.grid(row=0,column=0)
    
    desc_label=Label(att,text="Description",font='20')
    desc_label.grid(row=1,column=0)
    
    fileno=Entry(att,width=20)
    fileno.grid(row=0,column=1)
    
    description=Entry(att,width=50)
    description.grid(row=1,column=1)
    
    find_button=Button(att,text="Attach Document",font='verdana 14 bold',command=find)
    find_button.grid(row=2,columnspan=4,pady=10,ipadx=100,padx=10)
    
    
    
def retrieve_file():

    conn=sqlite3.connect('Clinic_Database.db')
    cursor=conn.cursor()
    
    def open_document():
        sel=ret_table.selection()[0]
        blob=records[int(sel)-1][3]
        
        if(records[int(sel)-1][6]==1):
            with open("attachments\\document.pdf",'wb')as f:
                f.write(blob)
                os.startfile("attachments\\document.pdf")
                    
        elif(records[int(sel)-1][6]==2):
            with open("attachments\\document.docx",'wb')as f:
                f.write(blob)
                os.startfile("document.docx")
                
        elif(records[int(sel)-1][6]==3):
            with open("attachments\\document.xlsx",'wb')as f:
                f.write(blob)
                os.startfile("attachments\\document.xlsx")
        
        elif(records[int(sel)-1][6]==4):
            with open("attachments\\document.mp4",'wb')as f:
                f.write(blob)
                os.startfile("attachments\\document.mp4")
        
        elif(records[int(sel)-1][6]==5):
            with open("attachments\\document.mkv",'wb')as f:
                f.write(blob)
                os.startfile("attachments\\document.mkv")
        
        elif(records[int(sel)-1][6]==6):
            with open("attachments\\document.avi",'wb')as f:
                f.write(blob)
                os.startfile("attachments\\document.avi")
        
        elif(records[int(sel)-1][6]==7):
            with open("attachments\\document.mpeg",'wb')as f:
                f.write(blob)
                os.startfile("attachments\\document.mpeg")
        
        else:
            with open("attachments\\image.png",'wb')as f:
                f.write(blob)
                os.startfile("attachments\\image.png")

    
    def filter_document():
        for x in ret_table.get_children():
            ret_table.delete(x)
            
        cursor.execute("SELECT * FROM Attachment WHERE Name LIKE '%"+ str(filter_entry.get())+"%'") 

        records=cursor.fetchall()

        for record in records:
            ret_table.insert(parent='',index='end', iid=record[0], text=record[0], values=(record[1],record[2],record[4],record[5],record[6]))
    
        
    ret=Tk()
    ret.title('Retrieve Document')
    ret.iconbitmap("shree_brahmi.ico")
    ret.attributes("-fullscreen",True)
    
    ret_frame=Frame(ret)
    ret_frame.pack(pady=20,padx=20)
    
    
    ret_scroll=Scrollbar(ret_frame)
    
    ret_table=ttk.Treeview(ret_frame, height=22, yscrollcommand=ret_scroll.set)
    
    ret_scroll.pack(side=RIGHT, fill=Y)
    ret_scroll.config(command=ret_table.yview)
    
    ret_table['columns']=("File Number","Name","Description","Date","Format")
       
    ret_table.column("#0",width=120,minwidth=30)
    ret_table.column("File Number",width=120,minwidth=25)
    ret_table.column("Name",width=200,minwidth=50)
    ret_table.column("Description",width=350,minwidth=25)
    ret_table.column("Date",width=120,minwidth=25)
    ret_table.column("Format",width=0,minwidth=0)
    
    
    
    ret_table.heading("#0",text="Sl No.",anchor=W)
    ret_table.heading("File Number",text="File No.",anchor=W)
    ret_table.heading("Name",text="Name",anchor=W)
    ret_table.heading("Description",text="Description",anchor=W)
    ret_table.heading("Date",text="Date",anchor=W)
    ret_table.heading("Format",text="Format",anchor=W)
    
    
    ret_table.pack()
    
    cursor.execute("SELECT * FROM Attachment") 

    records=cursor.fetchall()

    for record in records:
        ret_table.insert(parent='',index='end', iid=record[0], text=record[0], values=(record[1],record[2],record[4],record[5],record[6]))
    
    
    filter_entry=Entry(ret,width=30)
    filter_entry.pack(pady=3,ipadx=100,padx=10)
    
    search_button=Button(ret,text="Search",font='verdana 12 bold',command=filter_document)
    search_button.pack(pady=3,ipadx=30,padx=5)
    
    open_button=Button(ret,text="Open Document",font='verdana 16 bold ',command=open_document)
    open_button.pack(pady=5,ipadx=30,padx=10) 
    
    exit_button=Button(ret, text="QUIT",font='verdana 16 bold', command=ret.destroy)
    exit_button.pack(pady=15,ipadx=30,padx=10)
    