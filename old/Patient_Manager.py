# -*- coding: utf-8 -*-
"""
Created on Thu Jun 4 23:21:44 2020

@author: Aniruddh Acharya
"""

import sqlite3
from tkinter import *
from PIL import Image,ImageTk
import datetime
from tkinter import messagebox
from Expenditure import add_entry
from Expenditure import search_entry
from Expenditure import view_entries
from Attachment import attach_file
from Attachment import retrieve_file

#Linking The database
conn=sqlite3.connect('Patient_Database.db')
c=conn.cursor()


#Defining tkinter object
root = Tk()
root.geometry("1920x1000")
root.title("Patient Data Manager")
root.iconbitmap("shree_brahmi.ico")
root.attributes("-fullscreen",True)


global datestring1
global datestring
today = datetime.date.today()
date = str(today.day)+"/"+str(today.month)+"/"+str(today.year)
datestring1="\n Added on: "+str(date)+"\n"
datestring="\n last updated: "+str(date)+"\n"





#Function to view the entries in the database
def view_database():
    conn=sqlite3.connect('Patient_Database.db')
    c=conn.cursor()
    
    view=Toplevel()
    view.title('Viewing Database')
    view.iconbitmap("shree_brahmi.ico")
    view.attributes("-fullscreen",True)
    
    c.execute("SELECT * FROM PatientData") 
    records=c.fetchall()

    print_records='_______________\n'
    for record in records:
        print_records+='\n File Number: '+str(record[0])+"\n Name: "+str(record[1])+"\n Phone Number:  "+str(record[2])+"\n Age: "+str(record[3])+"\n Gender:  "+str(record[4])+"\n\n Symptoms: "+str(record[5])+"\n\n Findings: "+str(record[6])+"\n\n Treatment: "+str(record[7])+"\n_______________\n  "
    
    view_frame=Frame(view)
    view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
    view_list = Listbox(view_frame, width=220, height=45, yscrollcommand=view_scrollbar.set)
    view_scrollbar.config(command=view_list.yview)
    view_scrollbar.pack(side=RIGHT,fill=Y)
    view_frame.pack()
    
    for c in print_records.split('\n'):
       view_list.insert(END,c)
       
    view_list.pack()

    exit_button=Button(view, text="Quit",font='verdana 12 bold', command=view.destroy)
    exit_button.pack()
        
    conn.commit()
    conn.close()
    
    
 

    
#Function to add entries to the database
def add_patient():
    
    add=Toplevel()
    add.title('Adding Patient')
    add.iconbitmap("shree_brahmi.ico")
    
    def submit():
        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
        
        c.execute("SELECT * FROM PatientData") 
        records=c.fetchall()
        
        flag=0
        for record in records:
            if record[0]==fileno.get():
                flag=1
            elif len(fileno.get())==0:
                flag=2
            elif len(name.get())==0:
                flag=3
            elif len(age.get())==0:
                flag=4
            elif len(gender.get())==0:
                flag=5
        
        if flag==1:
            messagebox.showerror("Error","The Patient's entry already exists!")
        elif flag==2:
            messagebox.showerror("Error","The Patient's entry has no File Number!")
        elif flag==3:
            messagebox.showerror("Error","The Patient's entry has no Name!")
        elif flag==4:
            messagebox.showerror("Error","The Patient's entry has no Age!")
        elif flag==5:
            messagebox.showerror("Error","The Patient's entry has no Gender!")
        
        elif flag==0:
            c.execute("INSERT INTO PatientData values(:fileno,:name,:phoneno,:age,:gender,:symptoms,:findings,:treatment)",
              { 'fileno':fileno.get(),
               'name':name.get(),
               'phoneno':phoneno.get(),
               'age':age.get(),
               'gender':gender.get(),
               'symptoms':datestring1,
               'findings':datestring1,
               'treatment':datestring1
               } )

            fileno.delete(0,END)
            phoneno.delete(0,END)
            name.delete(0,END)
            age.delete(0,END)
            gender.delete(0,END)
    
            messagebox.showinfo("Added","The Patient's entry has been successfully added to the database!")
       
            
        conn.commit()
        conn.close()

    name_label=Label(add,text="Name",font='20')
    phoneno_label=Label(add,text="Phone Number",font='20')
    fileno_label=Label(add,text="File Number",font='20')
    age_label=Label(add,text="Age",font='20')
    gender_label=Label(add,text="Gender",font='20')
    
    name_label.grid(row=1,column=0,padx=10)
    phoneno_label.grid(row=2,column=0)
    fileno_label.grid(row=0,column=0)
    age_label.grid(row=3,column=0)
    gender_label.grid(row=4,column=0)
    
        
    name=Entry(add,width=60)
    phoneno=Entry(add,width=40)
    fileno=Entry(add,width=20)
    age=Entry(add,width=20)
    gender=Entry(add,width=20)
    
    name.grid(row=1,column=1,padx=20)
    phoneno.grid(row=2,column=1)
    fileno.grid(row=0,column=1)
    age.grid(row=3,column=1)
    gender.grid(row=4,column=1)
    
    submit_button=Button(add,text="Add Patient",font='verdana 14 bold',command=submit)
    submit_button.grid(row=6,columnspan=4,pady=10,ipadx=130)
    
  

 
    
    
#Function to delete entries from the database    
def delete_patient():
    
    dele=Toplevel()
    dele.title('Deleting Patient')
    dele.iconbitmap("shree_brahmi.ico")
    
    def delete():
        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
        
        c.execute("DELETE from PatientData WHERE File_Number LIKE '"+ fileno.get()+"'")

        fileno.delete(0,END)
        
        messagebox.showinfo("Deleted","The Patient's entry has been successfully Deleted!")
        
        conn.commit()
        conn.close()

    
    fileno_label=Label(dele,text="File Number",font='18')
    
    fileno_label.grid(row=1,column=0,padx=10,ipadx=20)
        
    fileno=Entry(dele,width=30)
    
    fileno.grid(row=1,column=1,padx=10,ipadx=30)
    
    delete_button=Button(dele,text="Delete Entry",font='verdana 14 bold',command=delete)
    delete_button.grid(row=4,columnspan=2,pady=10,ipadx=120)

    



def search_patient():
    
    sea=Toplevel()
    sea.title('Searching Patient')
    sea.iconbitmap("shree_brahmi.ico")
    
    records=[]
    
    def search_fileno():
        
        seaf=Toplevel()
        seaf.title('Searching Patient')
        seaf.iconbitmap("shree_brahmi.ico")
        seaf.attributes("-fullscreen",True)
        
        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
        
        c.execute("SELECT * FROM PatientData WHERE File_Number LIKE '%"+ str(fileno_search.get())+"%'") 
        records=c.fetchall()

        print_records='_______________\n'
        for record in records:
            print_records+='\n File Number: '+str(record[0])+"\n Name: "+str(record[1])+"\n Phone Number:  "+str(record[2])+"\n\n Symptoms: "+str(record[3])+"\n\n Findings: "+str(record[4])+"\n\n Treatment: "+str(record[5])+"\n_______________\n  "
        
        view_frame=Frame(seaf)
        view_scrollbar_y=Scrollbar(view_frame, orient=VERTICAL)
        view_scrollbar_x=Scrollbar(view_frame, orient=HORIZONTAL)
        view_list = Listbox(view_frame, width=90, height=25, font='verdana 16', yscrollcommand=view_scrollbar_y.set,xscrollcommand=view_scrollbar_x.set)
        view_scrollbar_y.config(command=view_list.yview)
        view_scrollbar_x.config(command=view_list.xview)
        view_scrollbar_y.pack(side=RIGHT,fill=Y)
        view_scrollbar_x.pack(side=BOTTOM,fill=X)
        view_frame.pack()
        
        for c in print_records.split('\n'):
           view_list.insert(END,c)
        view_list.pack()
        
        exit_button=Button(seaf, text="Quit",font='verdana 12 bold', command=seaf.destroy)
        exit_button.pack()
        
        conn.commit()
        conn.close()

        
        
    def search_name():
        
        sean=Toplevel()
        sean.title('Searching Patient')
        sean.iconbitmap("shree_brahmi.ico")
        sean.attributes("-fullscreen",True)
        
        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
        
        c.execute("SELECT * FROM PatientData WHERE Name LIKE '%"+ str(name_search.get())+"%' ") 
        records=c.fetchall()

        print_records='_______________\n'
        for record in records:
            print_records+='\n File Number: '+str(record[0])+"\n Name: "+str(record[1])+"\n\n Phone Number:  "+str(record[2])+"\n\n Symptoms: "+str(record[3])+"\n Findings: "+str(record[4])+"\n\n Treatment: "+str(record[5])+"\n_______________\n  "
        
        view_frame=Frame(sean)
        view_scrollbar_y=Scrollbar(view_frame, orient=VERTICAL)
        view_scrollbar_x=Scrollbar(view_frame, orient=HORIZONTAL)
        view_list = Listbox(view_frame, width=90, height=25, font='verdana 16', yscrollcommand=view_scrollbar_y.set,xscrollcommand=view_scrollbar_x.set)
        view_scrollbar_y.config(command=view_list.yview)
        view_scrollbar_x.config(command=view_list.xview)
        view_scrollbar_y.pack(side=RIGHT,fill=Y)
        view_scrollbar_x.pack(side=BOTTOM,fill=X)
        view_frame.pack()
        
        
        for c in print_records.split('\n'):
           view_list.insert(END,c)
        view_list.pack()
        
        exit_button=Button(sean, text="Quit",font='verdana 12 bold', command=sean.destroy)
        exit_button.pack()
       
        conn.commit()
        conn.close()
            
        
      
    def search_phoneno():    
        
        seap=Toplevel()
        seap.title('Searching Patient')
        seap.iconbitmap("shree_brahmi.ico")
        seap.attributes("-fullscreen",True)
        
        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
        
        c.execute("SELECT * FROM PatientData WHERE Phone_Number LIKE '%"+ str(phoneno_search.get())+"%'") 
        records=c.fetchall()

        print_records='_______________\n'
        for record in records:
            print_records+='\n File Number: '+str(record[0])+"\n Name: "+str(record[1])+"\n\n Phone Number:  "+str(record[2])+"\n\n Symptoms: "+str(record[3])+"\n Findings: "+str(record[4])+"\n\n Treatment: "+str(record[5])+"\n_______________\n  "
        
        view_frame=Frame(seap)
        view_scrollbar_y=Scrollbar(view_frame, orient=VERTICAL)
        view_scrollbar_x=Scrollbar(view_frame, orient=HORIZONTAL)
        view_list = Listbox(view_frame, width=90, height=25, font='verdana 16', yscrollcommand=view_scrollbar_y.set,xscrollcommand=view_scrollbar_x.set)
        view_scrollbar_y.config(command=view_list.yview)
        view_scrollbar_x.config(command=view_list.xview)
        view_scrollbar_y.pack(side=RIGHT,fill=Y)
        view_scrollbar_x.pack(side=BOTTOM,fill=X)
        view_frame.pack()
        
        for c in print_records.split('\n'):
           view_list.insert(END,c)
        view_list.pack()
        
        exit_button=Button(seap, text="Quit",font='verdana 12 bold', command=seap.destroy)
        exit_button.pack()
        
        conn.commit()
        conn.close()
       
    
    fileno_label=Label(sea,text="File Number",font='16')
    fileno_label.grid(row=0,column=0,padx=10,pady=3,ipadx=20)        
    fileno_search=Entry(sea,width=30)
    fileno_search.grid(row=0,column=1,padx=10,pady=3,ipadx=30)
    
    filesearch=Button(sea,text="Search File",font='verdana 14 bold',command=search_fileno)
    filesearch.grid(row=1,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
    name_label=Label(sea,text="Name",font='16')
    name_label.grid(row=2,column=0,padx=10,pady=3,ipadx=20)        
    name_search=Entry(sea,width=30)
    name_search.grid(row=2,column=1,padx=10,pady=3,ipadx=30)
    
    namesearch=Button(sea,text="Search Name",font='verdana 14 bold',command=search_name)
    namesearch.grid(row=3,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
    phoneno_label=Label(sea,text="Phone Number",font='16')
    phoneno_label.grid(row=4,column=0,padx=10,pady=3,ipadx=20)        
    phoneno_search=Entry(sea,width=30)
    phoneno_search.grid(row=4,column=1,padx=10,pady=3,ipadx=30)
    
    phonesearch=Button(sea,text="Search Phone No.",font='verdana 14 bold',command=search_phoneno)
    phonesearch.grid(row=5,column=0,padx=50,pady=7,ipadx=20,columnspan=2)



    

 
#Function to Update entries in the database    
def update_patient():
    
    upd=Toplevel()
    upd.title('Updating Patient')
    upd.iconbitmap("shree_brahmi.ico")   
    
    def edit():
        
        global ed       
        ed=Toplevel()
        ed.title('Updating Patient')
        ed.iconbitmap("shree_brahmi.ico")
        ed.attributes("-fullscreen",True)
        
        conn=sqlite3.connect('Patient_Database.db')
        c=conn.cursor()
        
        record_id=fileno_editor.get()
        
        
        name_label=Label(ed,text="Name",font='Helvetica 16 bold')
        phoneno_label=Label(ed,text="Phone Number",font='Helvetica 16 bold')
        fileno_label=Label(ed,text="File Number",font='Helvetica 16 bold')
        age_label=Label(ed,text="Age",font='Helvetica 16 bold')
        gender_label=Label(ed,text="Gender",font='Helvetica 16 bold')
        symptoms_label=Label(ed,text="Symptoms",font='Helvetica 16 bold')
        findings_label=Label(ed,text="Findings",font='Helvetica 16 bold')
        treatment_label=Label(ed,text="Treatment",font='Helvetica 16 bold')
        
        fileno_label.grid(row=0,column=0,ipady=3)
        name_label.grid(row=1,column=0,padx=10)
        phoneno_label.grid(row=2,column=0) 
        age_label.grid(row=3,column=0) 
        gender_label.grid(row=4,column=0) 
        symptoms_label.grid(row=5,column=0)
        findings_label.grid(row=5,column=1)
        treatment_label.grid(row=5,column=2)
        
        
        name=Entry(ed,width=30)
        phoneno=Entry(ed,width=30)
        fileno=Entry(ed,width=20)
        age=Entry(ed,width=20)
        gender=Entry(ed,width=20)
        symptoms=Text(ed,width=47,height=30)
        findings=Text(ed,width=47,height=30)
        treatment=Text(ed,width=47,height=30)    
        
        name.grid(row=1,column=1,padx=20,ipady=3)
        phoneno.grid(row=2,column=1)
        fileno.grid(row=0,column=1)
        age.grid(row=3,column=1)
        gender.grid(row=4,column=1)
        symptoms.grid(row=6,column=0,columnspan=1,ipadx=30,ipady=10,padx=5,pady=3)
        findings.grid(row=6,column=1,columnspan=1,ipadx=30,ipady=10,padx=5,pady=3)
        treatment.grid(row=6,column=2,columnspan=1,ipadx=30,ipady=10,padx=5,pady=3)
        
        c.execute("SELECT * FROM PatientData WHERE File_Number LIKE '"+ record_id+"'") 
        records=c.fetchall()
        
        for record in records:
            fileno.insert(0,record[0]) 
            name.insert(0,record[1])
            phoneno.insert(0,record[2])
            age.insert(0,record[3])
            gender.insert(0,record[4])
            symptoms.insert(1.0,record[5])
            findings.insert(1.0,record[6])
            treatment.insert(1.0,record[7])
            
        def update():
            conn=sqlite3.connect('Patient_Database.db')
            c=conn.cursor()
            
            symptom_string=str(symptoms.get("1.0","end-1c"))+datestring
            findings_string=str(findings.get("1.0","end-1c"))+datestring
            treatment_string=str(treatment.get("1.0","end-1c"))+datestring
            
            c.execute('''UPDATE PatientData SET
                      Name=:name,
                      Phone_Number=:phoneno,
                      Age=:age,
                      Gender=:gender,
                      Symptoms=:symptoms,
                      Findings=:findings,
                      Treatment=:treatment
                      
                      WHERE File_Number LIKE :fileno
                      ''',
                      {
                       'name':name.get(),
                       'phoneno':phoneno.get(),
                       'age':age.get(),
                       'gender':gender.get(),
                       'symptoms':"\n"+str(symptom_string)+"\n",
                       'findings':findings_string,
                       'treatment':treatment_string,
                       'fileno':record_id
                      }
                      )
            
            messagebox.showinfo("Updated","The Patient's entry has been successfully Updated!")
            ed.destroy()
                        
            conn.commit()
            conn.close()

        def quit_page():
            response= messagebox.askyesno("Saving","Do you want to save?")
            if response:
                update()
                ed.destroy()
            else:
                ed.destroy()
            
        fileno_editor.delete(0,END)  
        save_button=Button(ed,text="Save",font='verdana 12 bold',command=update)
        save_button.grid(row=7,column=0,columnspan=2,pady=10,ipadx=170)
        
        exit_button=Button(ed, text="Quit",font='verdana 12 bold', command=quit_page)
        exit_button.grid(row=7,column=2,columnspan=2,pady=10,ipadx=170)        
                
        conn.commit()
        conn.close()
          
    
    fileno_label=Label(upd,text="File Number",font='16')
    fileno_label.grid(row=1,column=0,padx=10,ipadx=20)
    global fileno_editor    
    fileno_editor=Entry(upd,width=30)
    fileno_editor.grid(row=1,column=1,padx=10,ipadx=30)
    
    update_button=Button(upd,text="Update Entry",font='verdana 12 bold',command=edit)
    update_button.grid(row=4,columnspan=2,pady=10,ipadx=100)  

    
    
    
 
    
#Label and Button Layout design
logo=ImageTk.PhotoImage(Image.open('shree_brahmi.jpg'))
logolabel=Label(image=logo)
logolabel.pack()


frame=LabelFrame(root, padx=20,pady=20)
frame.pack(padx=30,pady=30)

header=Label(frame,text='Hari Om', font="Verdana 8 italic",pady=5)
heading=Label(frame,text='Shree Brahmi Ayurveda', font="Verdana 16 bold italic", padx=60,pady=10,bg="yellow",fg="green")  
      
button_add = Button(frame, text="Add Patient ",font="Helvetica 12 bold", padx=27, pady=4,command=add_patient)
button_search = Button(frame, text="Search Patient",font="Helvetica 12 bold", padx=17, pady=4,command=search_patient)
button_delete = Button(frame, text="Delete Patient",font="Helvetica 12 bold", padx=20, pady=4,command=delete_patient)
button_view = Button(frame, text="View Database",font="Helvetica 12 bold", padx=15, pady=4,command=view_database)
button_update = Button(frame, text="Update Patient",font="Helvetica 12 bold", padx=16, pady=4,command=update_patient)
adde_button = Button(frame, text="Add Expense",font="Helvetica 12 bold", padx=27, pady=4,command=add_entry)
search_button = Button(frame, text="Search Expense",font="Helvetica 12 bold", padx=15, pady=4,command=search_entry)
view_button = Button(frame, text="View Expense",font="Helvetica 12 bold", padx=22, pady=4,command=view_entries)
attach_button = Button(frame, text="Attach Document",font="Helvetica 12 bold", padx=11, pady=4,command=attach_file)
retrieve_button = Button(frame, text="Retrieve Document",font="Helvetica 12 bold", padx=4, pady=4,command=retrieve_file)
exit_button=Button(frame, text="Quit",font='verdana 16 bold', command=root.destroy)



header.grid(row=0,columnspan=2)
heading.grid(row=1, column=0,pady=20,columnspan=2)  
button_add.grid(row=3, column=0,padx=50, pady=10)
button_search.grid(row=4, column=0,padx=50, pady=10)
button_delete.grid(row=5, column=0,padx=50, pady=10)
button_view.grid(row=6, column=0,padx=50, pady=10)
button_update.grid(row=7, column=0,padx=50, pady=10)
adde_button.grid(row=3, column=1,padx=50, pady=10)
search_button.grid(row=4, column=1,padx=50, pady=10)
view_button.grid(row=5, column=1,padx=60, pady=10)
attach_button.grid(row=6, column=1,padx=30, pady=10)
retrieve_button.grid(row=7, column=1,padx=30, pady=10)
exit_button.grid(row=8, column=1,padx=50, pady=10)


conn.commit()
conn.close()

root.mainloop()
