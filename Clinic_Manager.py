# -*- coding: utf-8 -*-
"""
Created on Thu Jun 4 23:21:44 2020

@author: Aniruddh Acharya
"""

import sqlite3
from tkinter import *
from PIL import Image,ImageTk
import datetime
from tkinter import messagebox, Toplevel, ttk
from Transaction import add_entry, query_transactions
from Attachment import attach_file, retrieve_file

#Linking The database
conn=sqlite3.connect('Clinic_Database.db')
cursor=conn.cursor()


#Defining tkinter object
root = Tk()

root.title("Patient Data Manager")
root.iconbitmap("shree_brahmi.ico")
root.attributes("-fullscreen",True)


global datestringAddedOn
global datestringUpdated
today = datetime.date.today()
date = str(today.day)+"/"+str(today.month)+"/"+str(today.year)
datestringAddedOn="\n Added on: "+str(date)+"\n"
datestringUpdated="\n last updated: "+str(date)+"\n"



#Function to view the entries in the database
def view_patients():
    conn=sqlite3.connect('Clinic_Database.db')
    cursor=conn.cursor()
    
    view=Toplevel()
    view.title('Viewing Database')
    view.iconbitmap("shree_brahmi.ico")
    view.attributes("-fullscreen",True)
    
    try:
        cursor.execute("SELECT * FROM PatientData") 
        records=cursor.fetchall()
    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"SQLite error: {e}")
       
    view_frame=Frame(view)
    view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
    
    view_list = ttk.Treeview(view_frame, height=30, yscrollcommand=view_scrollbar.set)
    
    view_scrollbar.config(command=view_list.yview)
    view_scrollbar.pack(side=RIGHT,fill=Y)
    
    view_list['columns']=("File Number","Name","Phone Number","Age","Gender")
       
    view_list.column("#0",width=120,minwidth=50)
    view_list.column("File Number",width=120,minwidth=50)
    view_list.column("Name",width=320,minwidth=100)
    view_list.column("Phone Number",width=200,minwidth=50)
    view_list.column("Age",width=120,minwidth=40)
    view_list.column("Gender",width=120,minwidth=40)
    
    
    view_list.heading("#0",text="Sl No.",anchor=W)
    view_list.heading("File Number",text="File No.",anchor=W)
    view_list.heading("Name",text="Name",anchor=W)
    view_list.heading("Phone Number",text="Phone Number",anchor=W)
    view_list.heading("Age",text="Age",anchor=W)
    view_list.heading("Gender",text="Gender",anchor=W)
    
    i=1
    for record in records:
       view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],record[2],record[3],record[4]))
       i+=1
    
    view_frame.pack(pady=20,padx=20)
    
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
        conn=sqlite3.connect('Clinic_Database.db')
        cursor=conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM PatientData") 
            records=cursor.fetchall()
        except sqlite3.Error as e:
                        messagebox.showerror("Error", f"SQLite error: {e}")
        
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
            cursor.execute("INSERT INTO PatientData values(:fileno,:name,:phoneno,:age,:gender,:symptoms,:findings,:treatment)",
              { 'fileno':fileno.get(),
               'name':name.get(),
               'phoneno':phoneno.get(),
               'age':age.get(),
               'gender':gender.get(),
               'symptoms':datestringAddedOn,
               'findings':datestringAddedOn,
               'treatment':datestringAddedOn
               } )

            fileno.delete(0,END)
            phoneno.delete(0,END)
            name.delete(0,END)
            age.delete(0,END)
            gender.delete(0,END)
    
            messagebox.showinfo("Added","The Patient's entry has been successfully added to the database!")
       
            add.destroy();
            
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
        conn=sqlite3.connect('Clinic_Database.db')
        cursor=conn.cursor()
        
        try:
            cursor.execute("DELETE from PatientData WHERE File_Number LIKE '"+ fileno.get()+"'")
            messagebox.showinfo("Deleted","The Patient's entry has been successfully Deleted!")
        
            dele.destroy();
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
            return

        fileno.delete(0,END)

    
    fileno_label=Label(dele,text="File Number",font='18')
    
    fileno_label.grid(row=1,column=0,padx=10,pady=5,ipadx=20)
        
    fileno=Entry(dele,width=30)
    
    fileno.grid(row=1,column=1,padx=10,pady=5,ipadx=30)
    
    delete_button=Button(dele,text="Delete Entry",font='verdana 14 bold',command=delete)
    delete_button.grid(row=4,columnspan=2,pady=5,ipadx=120)


def search_patient(): 
    searchPatient=Toplevel()
    searchPatient.title('Searching Entry')
    searchPatient.iconbitmap("shree_brahmi.ico")
    
    global name_search_entry, fileno_search_entry, phoneno_search_entry, cursor

    conn=sqlite3.connect('Clinic_Database.db')
    cursor=conn.cursor()

    def show_query_option_frame():
        if query_option.get() == 0:  # Date
            name_frame.pack()
            file_frame.pack_forget()
            phone_no_frame.pack_forget()
        elif query_option.get() == 1:  # File Number
            name_frame.pack_forget()
            file_frame.pack()
            phone_no_frame.pack_forget()
        elif query_option.get() == 2:  # Time Span
            name_frame.pack_forget()
            file_frame.pack_forget()
            phone_no_frame.pack()

    table_option=IntVar()
    table_option.set(0)
    query_option=IntVar()
    query_option.set(0)

    option_frame=Frame(searchPatient)
    option_frame.pack(fill=BOTH, expand=True)

    button_frame=Frame(searchPatient)
    button_frame.pack(fill=BOTH, expand=True)

    
    # Create Option Frames
    name_frame = Frame(button_frame)
    file_frame = Frame(button_frame)
    phone_no_frame = Frame(button_frame)

    heading_label = Label(option_frame, text="Query Based on:", font=('Helvetica', 14))
    heading_label.grid(row=3, column=1, padx=10, pady=10)
    
    Radiobutton(option_frame,text="Name", variable=query_option, value=0, command=show_query_option_frame, font=('Helvetica', 12, 'bold')).grid(row=4,column=1,padx=5, pady=5)
    
    Radiobutton(option_frame,text="File Number", variable=query_option, value=1, command=show_query_option_frame, font=('Helvetica', 12, 'bold')).grid(row=4,column=2,padx=5, pady=5)
   
    Radiobutton(option_frame,text="Phone No.", variable=query_option, value=2, command=show_query_option_frame, font=('Helvetica', 12, 'bold')).grid(row=4,column=3,padx=5, pady=5)

    Label(name_frame, text="Enter Name:", font=('Helvetica', 12)).pack(side=LEFT, padx=10)
    name_search_entry = Entry(name_frame, font=('Helvetica', 12))
    name_search_entry.pack(side=LEFT, padx=10, pady=10)

    Label(file_frame, text="Enter File Number:", font=('Helvetica', 12)).pack(side=LEFT, padx=10)
    fileno_search_entry = Entry(file_frame, font=('Helvetica', 12))
    fileno_search_entry.pack(side=LEFT, padx=10, pady=10)

    Label(phone_no_frame, text="Enter Phone Number:", font=('Helvetica', 12)).pack(side=LEFT, padx=10)
    phoneno_search_entry = Entry(phone_no_frame, font=('Helvetica', 12))
    phoneno_search_entry.pack(side=LEFT, padx=10, pady=10)


    def run_query():
        selected_query = query_option.get()

        if selected_query == 0:  # Date
            search_by_name()
        elif selected_query == 1:  # File Number
            search_by_file_number()
        elif selected_query == 2:  # Time Span
            search_by_phone()
    

    Button(button_frame, text="Query Entries", font=('Helvetica', 14, 'bold'), command=run_query ).pack(padx=5, pady=10)

    # Initially show the date frame
    show_query_option_frame()

    def search_by_name():
        try:
            cursor.execute("SELECT * FROM PatientData WHERE Name LIKE '"+ str(name_search_entry.get())+"%'") 
            records = cursor.fetchall()
            display_transaction_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")

    def search_by_file_number():
        try:
            cursor.execute("SELECT * FROM PatientData WHERE File_Number LIKE '"+ str(fileno_search_entry.get())+"%'") 
            records = cursor.fetchall()
            display_transaction_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")

    def search_by_phone():
        try:
            cursor.execute("SELECT * FROM PatientData WHERE Phone_Number LIKE '"+ str(phoneno_search_entry.get())+"%'") 
            records = cursor.fetchall()
            display_transaction_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")

    def display_transaction_records(records):

        view_page=Toplevel()
        view_page.title('Querying Entries')
        view_page.iconbitmap("shree_brahmi.ico")    
        view_page.attributes("-fullscreen",True)

        view_frame = Frame(view_page)
        view_frame.pack(pady=20, padx=20)

        view_scrollbar = Scrollbar(view_frame, orient=VERTICAL)
        view_scrollbar.pack(side=RIGHT, fill=Y)

        view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        view_scrollbar.config(command=view_list.yview)

        view_list['columns']=("File Number","Name","Phone Number","Age","Gender")

        for column in ("File Number","Name","Phone Number","Age","Gender"):
            view_list.column(column, width=100, minwidth=50)
            view_list.heading(column, text=column)

        i = 1
        for record in records:
            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],record[2],record[3],record[4]))
            i += 1

        view_list.pack(fill=BOTH, expand=True)

        exit_button = Button(view_page, text="Quit", font='verdana 12 bold', command=view_page.destroy)
        exit_button.pack(pady=5)

 
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
        ed_frame=Frame(ed)
        ed_frame.pack(pady=10)
        
        conn=sqlite3.connect('Clinic_Database.db')
        cursor=conn.cursor()
        
        record_id=fileno_editor.get()
        
        
        name_label=Label(ed_frame,text="Name",font='Helvetica 16 bold')
        phoneno_label=Label(ed_frame,text="Phone Number",font='Helvetica 16 bold')
        fileno_label=Label(ed_frame,text="File Number",font='Helvetica 16 bold')
        age_label=Label(ed_frame,text="Age",font='Helvetica 16 bold')
        gender_label=Label(ed_frame,text="Gender",font='Helvetica 16 bold')
        symptoms_label=Label(ed_frame,text="Symptoms",font='Helvetica 16 bold')
        findings_label=Label(ed_frame,text="Findings",font='Helvetica 16 bold')
        treatment_label=Label(ed_frame,text="Treatment",font='Helvetica 16 bold')
        
        fileno_label.grid(row=0,column=0,ipady=3)
        name_label.grid(row=1,column=0,padx=10)
        phoneno_label.grid(row=2,column=0) 
        age_label.grid(row=3,column=0) 
        gender_label.grid(row=4,column=0) 
        symptoms_label.grid(row=5,column=0)
        findings_label.grid(row=5,column=1)
        treatment_label.grid(row=5,column=2)
        
        
        name=Entry(ed_frame,width=30)
        phoneno=Entry(ed_frame,width=30)
        fileno=Entry(ed_frame,width=20)
        age=Entry(ed_frame,width=20)
        gender=Entry(ed_frame,width=20)
        symptoms=Text(ed_frame,width=43,height=27)
        findings=Text(ed_frame,width=43,height=27)
        treatment=Text(ed_frame,width=43,height=27)    
        
        name.grid(row=1,column=1,padx=20,ipady=3)
        phoneno.grid(row=2,column=1)
        fileno.grid(row=0,column=1)
        age.grid(row=3,column=1)
        gender.grid(row=4,column=1)
        symptoms.grid(row=6,column=0,columnspan=1,ipadx=30,ipady=10,padx=5,pady=3)
        findings.grid(row=6,column=1,columnspan=1,ipadx=30,ipady=10,padx=5,pady=3)
        treatment.grid(row=6,column=2,columnspan=1,ipadx=30,ipady=10,padx=5,pady=3)
        
        try:
            cursor.execute("SELECT * FROM PatientData WHERE File_Number LIKE '"+ record_id+"'") 
            records=cursor.fetchall()
        except sqlite3.Error as e:
                        messagebox.showerror("Error", f"SQLite error: {e}")

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
            conn=sqlite3.connect('Clinic_Database.db')
            cursor=conn.cursor()
            
            symptom_string=datestringUpdated+str(symptoms.get("1.0","end-1c"))
            findings_string=datestringUpdated+str(findings.get("1.0","end-1c"))
            treatment_string=datestringUpdated+str(treatment.get("1.0","end-1c"))
            
            try:
                cursor.execute('''UPDATE PatientData SET
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
                
                ed.destroy();
                upd.destroy();
                
                conn.commit()
                conn.close()

            except sqlite3.Error as e:
                        messagebox.showerror("Error", f"SQLite error: {e}")

        def quit_page():
            response= messagebox.askyesno("Saving","Do you want to save?")
            if response:
                update()
                ed.destroy()
            else:
                ed.destroy();    
            upd.destroy();
            
            
        fileno_editor.delete(0,END)  
        save_button=Button(ed_frame,text="Save",font='verdana 12 bold',command=update)
        save_button.grid(row=7,column=0,columnspan=2,pady=10,ipadx=170)
        
        exit_button=Button(ed_frame, text="Quit",font='verdana 12 bold', command=quit_page)
        exit_button.grid(row=7,column=2,columnspan=2,pady=10,ipadx=170)        
        
        conn.commit()
        conn.close()
          
    
    fileno_label=Label(upd,text="File Number",font='16')
    fileno_label.grid(row=1,column=0,padx=10,pady=5,ipadx=20)
    global fileno_editor    
    fileno_editor=Entry(upd,width=30)
    fileno_editor.grid(row=1,column=1,padx=10,pady=5,ipadx=30)
    
    update_button=Button(upd,text="Update Entry",font='verdana 12 bold',command=edit)
    update_button.grid(row=4,columnspan=2,padx=10,pady=5,ipadx=100)  

def close_all_windows():
    # Iterate over all children of the root window and destroy Toplevel windows
    for window in root.winfo_children():
        if isinstance(window, Toplevel):
            window.destroy()
    root.destroy()

    
#Label and Button Layout design
logo=ImageTk.PhotoImage(Image.open('shree_brahmi.jpg'))
logolabel=Label(image=logo)
logolabel.pack(pady=10)


frame=LabelFrame(root, padx=20,pady=20)
frame.pack(padx=30,pady=15)

header=Label(frame,text='Hari Om', font="Verdana 10 bold",pady=2)
heading=Label(frame,text='Shree Brahmi Ayurveda', font="Verdana 20 bold italic", padx=60,pady=10,bg="yellow",fg="green")  
      
button_add = Button(frame, text="Add Patient ",font="Helvetica 12 bold", padx=27, pady=4,command=add_patient)
button_search = Button(frame, text="Search Patient",font="Helvetica 12 bold", padx=17, pady=4,command=search_patient)
button_delete = Button(frame, text="Delete Patient",font="Helvetica 12 bold", padx=20, pady=4,command=delete_patient)
button_view = Button(frame, text="View Patients",font="Helvetica 12 bold", padx=21, pady=4,command=view_patients)
button_update = Button(frame, text="Update Patient",font="Helvetica 12 bold", padx=16, pady=4,command=update_patient)
adde_button = Button(frame, text="Add Transaction",font="Helvetica 12 bold", padx=16, pady=4,command=add_entry)
view_button = Button(frame, text="Query Transactions",font="Helvetica 12 bold", padx=4, pady=4,command=query_transactions)
attach_button = Button(frame, text="Attach Document",font="Helvetica 12 bold", padx=14, pady=4,command=attach_file)
retrieve_button = Button(frame, text="Retrieve Document",font="Helvetica 12 bold", padx=6, pady=4,command=retrieve_file)
exit_button=Button(frame, text="Quit",font='verdana 16 bold', command=close_all_windows)


header.grid(row=0,columnspan=2)
heading.grid(row=1, column=0,pady=20,columnspan=2)  
button_add.grid(row=3, column=0,padx=50, pady=10)
button_search.grid(row=4, column=0,padx=50, pady=10)
button_view.grid(row=6, column=0,padx=50, pady=10)
button_update.grid(row=7, column=0,padx=50, pady=10)
adde_button.grid(row=3, column=1,padx=50, pady=10)
view_button.grid(row=4, column=1,padx=60, pady=10)
attach_button.grid(row=6, column=1,padx=30, pady=10)
retrieve_button.grid(row=7, column=1,padx=30, pady=10)
exit_button.grid(row=8, columnspan=2,padx=50, pady=10)


conn.commit()
conn.close()

root.mainloop()


# def search_patients():
    
#     sea=Toplevel()
#     sea.title('Searching Patient')
#     sea.iconbitmap("shree_brahmi.ico")
    
#     records=[]
    
#     def search_fileno():
                
#         seaf=Toplevel()
#         seaf.title('Searching Patient')
#         seaf.iconbitmap("shree_brahmi.ico")
#         seaf.attributes("-fullscreen",True)
        
        
#         def exitf():
#             seaf.destroy();
#             sea.destroy();
        
#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
        
#         try:
#             cursor.execute("SELECT * FROM PatientData WHERE File_Number LIKE '"+ str(fileno_search.get())+"%'") 
#             records=cursor.fetchall()
#         except sqlite3.Error as e:
#                         messagebox.showerror("Error", f"SQLite error: {e}")
        
#         view_frame=Frame(seaf)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=30, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
#         view_list['columns']=("File Number","Name","Phone Number","Age","Gender")
           
#         view_list.column("#0",width=120,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=320,minwidth=100)
#         view_list.column("Phone Number",width=200,minwidth=50)
#         view_list.column("Age",width=120,minwidth=40)
#         view_list.column("Gender",width=120,minwidth=40)
        
        
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Phone Number",text="Phone Number",anchor=W)
#         view_list.heading("Age",text="Age",anchor=W)
#         view_list.heading("Gender",text="Gender",anchor=W)
        
#         i=1
#         for record in records:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],record[2],record[3],record[4]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()        
        
        
#         exit_button=Button(seaf, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack()
        
#         conn.commit()
#         conn.close()

        
        
#     def search_name():
        
#         sean=Toplevel()
#         sean.title('Searching Patient')
#         sean.iconbitmap("shree_brahmi.ico")
#         sean.attributes("-fullscreen",True)
                
#         def exitf():
#             sean.destroy();
#             sea.destroy();
        
#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
        
#         try:
#             cursor.execute("SELECT * FROM PatientData WHERE Name LIKE '%"+ str(name_search.get())+"%' ") 
#             records=cursor.fetchall()
#         except sqlite3.Error as e:
#                         messagebox.showerror("Error", f"SQLite error: {e}")

#         view_frame=Frame(sean)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=30, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
#         view_list['columns']=("File Number","Name","Phone Number","Age","Gender")
           
#         view_list.column("#0",width=120,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=300,minwidth=100)
#         view_list.column("Phone Number",width=200,minwidth=50)
#         view_list.column("Age",width=120,minwidth=40)
#         view_list.column("Gender",width=120,minwidth=40)
          
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Phone Number",text="Phone Number",anchor=W)
#         view_list.heading("Age",text="Age",anchor=W)
#         view_list.heading("Gender",text="Gender",anchor=W)
        
#         i=1
#         for record in records:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],record[2],record[3],record[4]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
        
#         exit_button=Button(sean, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack()   

#         conn.commit()
#         conn.close()
            
        
      
#     def search_phoneno():    
        
#         seap=Toplevel()
#         seap.title('Searching Patient')
#         seap.iconbitmap("shree_brahmi.ico")
#         seap.attributes("-fullscreen",True)
        
#         def exitf():
#             seap.destroy();
#             sea.destroy();
        
#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
        
#         try:
#             cursor.execute("SELECT * FROM PatientData WHERE Phone_Number LIKE '%"+ str(phoneno_search.get())+"%'") 
#             records=cursor.fetchall()
#         except sqlite3.Error as e:
#                         messagebox.showerror("Error", f"SQLite error: {e}")
        
#         view_frame=Frame(seap)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=42, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
#         view_list['columns']=("File Number","Name","Phone Number","Age","Gender")
           
#         view_list.column("#0",width=120,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=300,minwidth=100)
#         view_list.column("Phone Number",width=200,minwidth=50)
#         view_list.column("Age",width=120,minwidth=40)
#         view_list.column("Gender",width=120,minwidth=40)
        
                
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Phone Number",text="Phone Number",anchor=W)
#         view_list.heading("Age",text="Age",anchor=W)
#         view_list.heading("Gender",text="Gender",anchor=W)
        
#         i=1
#         for record in records:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],record[2],record[3],record[4]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
        
#         exit_button=Button(seap, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack()
        
#         conn.commit()
#         conn.close()
       
    
#     fileno_label=Label(sea,text="File Number",font='16')
#     fileno_label.grid(row=0,column=0,padx=10,pady=3,ipadx=20)        
#     fileno_search=Entry(sea,width=30)
#     fileno_search.grid(row=0,column=1,padx=10,pady=3,ipadx=30)
    
#     filesearch=Button(sea,text="Search File",font='verdana 14 bold',command=search_fileno)
#     filesearch.grid(row=1,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
#     name_label=Label(sea,text="Name",font='16')
#     name_label.grid(row=2,column=0,padx=10,pady=3,ipadx=20)        
#     name_search=Entry(sea,width=30)
#     name_search.grid(row=2,column=1,padx=10,pady=3,ipadx=30)
    
#     namesearch=Button(sea,text="Search Name",font='verdana 14 bold',command=search_name)
#     namesearch.grid(row=3,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
#     phoneno_label=Label(sea,text="Phone Number",font='16')
#     phoneno_label.grid(row=4,column=0,padx=10,pady=3,ipadx=20)        
#     phoneno_search=Entry(sea,width=30)
#     phoneno_search.grid(row=4,column=1,padx=10,pady=3,ipadx=30)
    
#     phonesearch=Button(sea,text="Search Phone No.",font='verdana 14 bold',command=search_phoneno)
#     phonesearch.grid(row=5,column=0,padx=50,pady=7,ipadx=20,columnspan=2)