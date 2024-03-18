# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:17:04 2020

@author: Aniruddh Acharya
"""

import json
import sqlite3
from tkinter import *
import traceback
from PIL import ImageTk, Image
import datetime
from tkinter import ttk
from tkinter import messagebox
import xlwings as xw

global datestring

today = datetime.date.today()
datestring=str(today.day)+"/"+str(today.month)+"/"+str(today.year)

def add_entry():
       
    add=Toplevel()
    add.title('Adding Entry')
    add.iconbitmap("shree_brahmi.ico")
    global fileno_editor    
    
    def edit():

        record_id=fileno_editor.get() 

        if not record_id.isnumeric():
            messagebox.showerror("Error","Please Enter Valid File Number")
            add.destroy()
            return
              
        global ed       
        ed=Toplevel()
        ed.title('Adding Entry')
        ed.iconbitmap("shree_brahmi.ico")
        
        conn=sqlite3.connect('Clinic_Database.db')
        cursor=conn.cursor()
        
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
        Radiobutton(ed,text="Consultation", variable=oc, value=3).grid(row=4,column=3,padx=1)
        Radiobutton(ed,text="Cash", variable=tp, value=0).grid(row=5,column=0,padx=1)
        Radiobutton(ed,text="UPI", variable=tp, value=1).grid(row=5,column=1,padx=1)
        Radiobutton(ed,text="NEFT", variable=tp, value=2).grid(row=5,column=2,padx=1)
        Radiobutton(ed,text="Cc/Dc", variable=tp, value=3).grid(row=5,column=3,padx=1)
        amount.grid(row=7,column=1)
        description.grid(row=8,column=1,columnspan=2,ipady=10,padx=5,pady=3)
        
        try:
            cursor.execute("SELECT * FROM PatientData WHERE File_Number LIKE '"+ record_id+"'") 
            records=cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
        
        for record in records:
            fileno.insert(0,record[0]) 
            name.insert(0,record[1])
        date.insert(0,datestring)
        description.insert(1.0," ")
        
        def exitf():
            ed.destroy()
            add.destroy()
        
        
        def add_bill():
            global addBillPage       
            addBillPage=Toplevel()
            addBillPage.title('Creating Bill')
            addBillPage.iconbitmap("shree_brahmi.ico")

            med_name_label=Label(addBillPage,text="Medicine Name",font='Helvetica 14')
            med_name_input=Entry(addBillPage,width=50)
            med_cost_label=Label(addBillPage,text="Cost",font='Helvetica 14')
            med_cost_input=Entry(addBillPage,width=20)
            med_quantity_label=Label(addBillPage,text="Quantity",font='Helvetica 14')
            med_quantity_var = ''  
            med_quantity_input = Spinbox(addBillPage, from_=1, to=1000, textvariable=med_quantity_var)
            total_cost_label=Label(addBillPage,text="Total Cost: ₹ 0",font='Helvetica 16')

            med_name_label.grid(row=0,column=0,padx=10,ipady=3)
            med_name_input.grid(row=0,column=1,padx=10,ipady=3)
            med_cost_label.grid(row=0,column=2,padx=10,ipady=3)
            med_cost_input.grid(row=0,column=3,padx=10,ipady=3)
            med_quantity_label.grid(row=0,column=4,padx=10,ipady=3)
            med_quantity_input.grid(row=0,column=5,padx=10,ipady=3)
            

            bill=[]
            itemNo,billTotal=1,0
            
            def add_bill_entry():
                nonlocal itemNo, billTotal

                try:
                    cost = float(med_cost_input.get())
                    quantity = int(med_quantity_input.get())
                except ValueError as e:
                    error_message = f"Error: {str(e)}\n\n{traceback.format_exc()}"
                    messagebox.showerror("Error", "Cost and Quantity must be valid numbers.")
                    addBillPage.attributes('-topmost', 1)
                    addBillPage.attributes('-topmost', 0)
                    return

                bill_entry = [med_name_input.get(), cost, quantity]
                view_list.insert(parent='',index='end',iid=itemNo, text=itemNo, values=(bill_entry[0],("₹ "+str(bill_entry[1])),bill_entry[2]))
                bill.append(bill_entry)
                itemNo+=1
                item_total=int(bill_entry[1])*int(bill_entry[2])
                billTotal+=item_total
                total_cost_label.config(text=f"Total Cost: ₹ {billTotal}")

            def clear_bill_entries():
                nonlocal itemNo, billTotal, bill

                bill = []
                itemNo=1
                billTotal=0
                total_cost_label.config(text=f"Total Cost: ₹ {billTotal}")
                view_list.delete(*view_list.get_children())

            def save_bill() :
                
                conn=sqlite3.connect('Clinic_Database.db')
                cursor=conn.cursor()

                if bill:
                # Serialize the 'bill' array to a JSON string
                    bill_json = json.dumps(bill)

                    try:
                        # Insert the bill into the table
                        cursor.execute("INSERT INTO Bills (File_Number, Bill_Data, Date) VALUES (:File_Number, :Bill_Data, :Date)",
                                       {"File_Number":fileno.get(),
                                        "Bill_Data":bill_json,
                                        "Date":datestring})
                        conn.commit()

                        messagebox.showinfo("Success", "Bill added successfully!")

                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"SQLite error: {e}")

                    finally:
                        conn.close()
                        addBillPage.destroy()
                        ed.attributes('-topmost', 1)
                        ed.attributes('-topmost', 0)
                else:
                    messagebox.showwarning("Warning", "The bill is empty. Please add items to the bill.")
           

            add_bill_button=Button(addBillPage,text="Add Entry",font='Helvetica 16 bold',width=40, command=add_bill_entry)
            add_bill_button.grid(row=1,columnspan=4,padx=5,pady=10,ipady=2)  

            clear_bill_button=Button(addBillPage,text="Clear Entries",font='Helvetica 16 bold',width=15, command=clear_bill_entries)
            clear_bill_button.grid(row=1,column=4,columnspan=2,padx=5,pady=10,ipady=2)  

            view_frame=Frame(addBillPage)
            view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
            view_list = ttk.Treeview(view_frame, height=15, yscrollcommand=view_scrollbar.set)

            view_scrollbar.config(command=view_list.yview)
            view_scrollbar.pack(side=RIGHT,fill=Y)
            
            view_list['columns']=("Name","Cost","Quantity")
            
            view_list.column("#0", width=80, minwidth=50)
            view_list.column("Name", width=250, minwidth=200)
            view_list.column("Cost", width=120, minwidth=100)
            view_list.column("Quantity", width=100, minwidth=100)
         
            view_list.heading("#0",text="Sl No.",anchor=W)
            view_list.heading("Name",text="Name",anchor=W)
            view_list.heading("Cost",text="Cost",anchor=W)
            view_list.heading("Quantity",text="Quantity",anchor=W)
            
            view_frame.grid(row=2,columnspan=6,pady=5,padx=50,ipady=3,ipadx=1)
            view_list.pack()

            total_cost_label.grid(row=3,column=4,padx=10,ipady=3)

            save_bill_button=Button(addBillPage,text="Save Bill Details",font='Helvetica 18 bold',width=50, command=save_bill)
            save_bill_button.grid(row=5,columnspan=6,padx=10,pady=15,ipady=1) 
            
            
        def update():
            
            conn=sqlite3.connect('Clinic_Database.db')
            cursor=conn.cursor()

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
            
            try:
                cursor.execute("INSERT INTO TransactionData (File_Number,Name,Date,\"Income/Expense\",\"Opex/Capex\",\"Type_Payment\",Amount,Description) VALUES (:fileno,:name,:date,:incomeexpense,:opexcapex,:typepayment,:amount,:description)",
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
            except sqlite3.Error as e:
                        messagebox.showerror("Error", f"SQLite error: {e}")
                        return
            
            ed.destroy()
            add.destroy()
            
            conn.commit()
            conn.close()

        fileno_editor.delete(0,END)
        add_bill_button=Button(ed,text="Add Medicine Bill",font='Helvetica 16 bold', command=add_bill)
        add_bill_button.grid(row=8,column=3,padx=10,pady=1)  
        save_button=Button(ed,text="Save",font='verdana 12 bold',command=update)
        save_button.grid(row=9,column=0,columnspan=2,pady=10,padx=10,ipadx=170)
        
        exit_button=Button(ed, text="Quit",font='verdana 12 bold', command=exitf)
        exit_button.grid(row=9,column=2,columnspan=2,pady=10,padx=10,ipadx=170)        
                
        conn.commit()
        conn.close()
          
    
    fileno_label=Label(add,text="File Number",font='16')
    fileno_label.grid(row=1,column=0,padx=10,ipadx=20)
    fileno_editor=Entry(add,width=30)
    fileno_editor.grid(row=1,column=1,padx=10,ipadx=30)
    
    update_button=Button(add,text="Update Entry",font='verdana 12 bold',command=edit)
    update_button.grid(row=4,columnspan=2,pady=10,ipadx=100)

def query_transactions():
    
    queryTrans=Toplevel()
    queryTrans.title('Querying Entry')
    queryTrans.iconbitmap("shree_brahmi.ico")
    
    global date_search_entry, fileno_search_entry, date_search1_entry, date_search2_entry, cursor

    conn=sqlite3.connect('Clinic_Database.db')
    cursor=conn.cursor()

    def show_query_option_frame():
        if query_option.get() == 0:  # Date
            date_frame.pack()
            file_frame.pack_forget()
            time_span_frame.pack_forget()
        elif query_option.get() == 1:  # File Number
            date_frame.pack_forget()
            file_frame.pack()
            time_span_frame.pack_forget()
        elif query_option.get() == 2:  # Time Span
            date_frame.pack_forget()
            file_frame.pack_forget()
            time_span_frame.pack()

    table_option=IntVar()
    table_option.set(0)
    query_option=IntVar()
    query_option.set(0)

    option_frame=Frame(queryTrans)
    option_frame.pack(fill=BOTH, expand=True)

    button_frame=Frame(queryTrans)
    button_frame.pack(fill=BOTH, expand=True)

    
    # Create Option Frames
    date_frame = Frame(button_frame)
    file_frame = Frame(button_frame)
    time_span_frame = Frame(button_frame)

    heading_label = Label(option_frame, text="Table - ", font=('Helvetica', 18, 'bold'))
    heading_label.grid(row=0, column=0, padx=10, ipady=3)
    Radiobutton(option_frame, text="Transactions", variable=table_option, value=0, font=('Helvetica', 16)).grid(row=0, column=2, padx=10)
    Radiobutton(option_frame, text="Bills", variable=table_option, value=1, font=('Helvetica', 16)).grid(row=0, column=4, padx=10)

    heading_label = Label(option_frame, text="Query Based on:", font=('Helvetica', 14))
    heading_label.grid(row=3, column=1, padx=10, pady=10)
    
    Radiobutton(option_frame,text="Date", variable=query_option, value=0, command=show_query_option_frame, font=('Helvetica', 12, 'bold')).grid(row=4,column=1,padx=5, pady=5)
    
    Radiobutton(option_frame,text="File Number", variable=query_option, value=1, command=show_query_option_frame, font=('Helvetica', 12, 'bold')).grid(row=4,column=2,padx=5, pady=5)
   
    Radiobutton(option_frame,text="Time Span", variable=query_option, value=2, command=show_query_option_frame, font=('Helvetica', 12, 'bold')).grid(row=4,column=3,padx=5, pady=5)

    Label(date_frame, text="Enter Date:", font=('Helvetica', 12)).pack(side=LEFT, padx=10)
    date_search_entry = Entry(date_frame, font=('Helvetica', 12))
    date_search_entry.pack(side=LEFT, padx=10, pady=10)
    format_label=Label(date_frame,text="(D/M/YYYY)",font='12')
    format_label.pack()

    Label(file_frame, text="Enter File Number:", font=('Helvetica', 12)).pack(side=LEFT, padx=10)
    fileno_search_entry = Entry(file_frame, font=('Helvetica', 12))
    fileno_search_entry.pack(side=LEFT, padx=10, pady=10)

    Label(time_span_frame, text="Start Date:", font=('Helvetica', 12)).pack(side=LEFT, padx=10)
    date_search1_entry = Entry(time_span_frame, font=('Helvetica', 12))
    date_search1_entry.pack(side=LEFT, padx=10, pady=10)
    Label(time_span_frame, text="End Date:", font=('Helvetica', 12)).pack(side=LEFT, padx=10)
    date_search2_entry = Entry(time_span_frame, font=('Helvetica', 12))
    date_search2_entry.pack(side=LEFT, padx=10, pady=10)
    
    format_label=Label(time_span_frame,text="(D/M/YYYY)",font='12')
    format_label.pack()

    def run_query():
        selected_table = table_option.get()
        selected_query = query_option.get()

        if selected_table == 0:  # Transactions
            if selected_query == 0:  # Date
                search_by_date()
            elif selected_query == 1:  # File Number
                search_by_file_number()
            elif selected_query == 2:  # Time Span
                search_by_time_span()
        elif selected_table == 1:  # Bills
            if selected_query == 0:  # Date
                search_bill_date()
            elif selected_query == 1:  # File Number
                search_bill_file_number()
            elif selected_query == 2:  # Time Span
                search_bill_time_span()

    Button(button_frame, text="Query Entries", font=('Helvetica', 16, 'bold'), command=run_query ).pack(padx=5, pady=10)

    # Initially show the date frame
    show_query_option_frame()

    def generate_report(records,type):
        if type == 'T':
            excelworkbook = xw.Book('Transaction_Report.xlsx')
            excelsheet = excelworkbook.sheets['Report']
        elif type == 'B':
            excelworkbook = xw.Book('Bill_Invoice.xlsx')
            excelsheet = excelworkbook.sheets['Invoice']
        excelsheet.range("A2").value = records
        messagebox.showinfo("Generated", "Report has been Successfully Generated. Minimise the Application to view it.")

    def search_by_date():
        try:
            cursor.execute("SELECT * FROM TransactionData WHERE Date LIKE ?", ('%' + date_search_entry.get() + '%',))
            records = cursor.fetchall()
            display_transaction_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")

    def search_by_file_number():
        try:
            cursor.execute("SELECT * FROM TransactionData WHERE File_Number LIKE ?", (fileno_search_entry.get(),))
            records = cursor.fetchall()
            display_transaction_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")

    def search_by_time_span():
        try:
            start_date = datetime.datetime.strptime(date_search1_entry.get(), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(date_search2_entry.get(), '%d/%m/%Y')
            cursor.execute("SELECT * FROM TransactionData")
            all_records = cursor.fetchall()
            records = [record for record in all_records if start_date <= datetime.datetime.strptime(record[2], '%d/%m/%Y') <= end_date]
            display_transaction_records(records)
        except ValueError:
            messagebox.showerror("Error", "Invalid Dates")
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

        view_list['columns'] = ("File Number", "Name", "Amount", "Date", "Income/Expense", "Opex/Capex", "Payment Type", "Description")

        for column in ("#0", "File Number", "Name", "Amount", "Date", "Income/Expense", "Opex/Capex", "Payment Type", "Description"):
            view_list.column(column, width=100, minwidth=50)
            view_list.heading(column, text=column)

        i = 1
        for record in records:
            view_list.insert(parent='', index='end', iid=i, text=i, values=(record[0], record[1], ("₹ " + str(record[6])), record[2], record[3], record[4], record[5], record[7]))
            i += 1

        view_list.pack(fill=BOTH, expand=True)

        report_button = Button(view_page, text="Generate Report", font='verdana 14 bold', command=lambda: generate_report(records[:-2],'T'))
        report_button.pack(pady=5)

        exit_button = Button(view_page, text="Quit", font='verdana 12 bold', command=view_page.destroy)
        exit_button.pack(pady=5)

    def search_bill_date():
        conn = sqlite3.connect('Clinic_Database.db')
        cursor = conn.cursor()
        
        try:
            if(date_search_entry.get()==""): 
                cursor.execute("SELECT * FROM Bills")
                records=cursor.fetchall()
                display_bill_records(records)
            else:    
                cursor.execute("SELECT * FROM Bills WHERE Date LIKE ?", ('%' + date_search_entry.get() + '%',))
                records = cursor.fetchall()
                display_bill_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
            return None
        
        conn.close()
        return records

    def search_bill_file_number():
        conn = sqlite3.connect('Clinic_Database.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM Bills WHERE File_Number LIKE '%"+ str(fileno_search_entry.get())+"%'") 
            records = cursor.fetchall()
            display_bill_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
            return None
        
        conn.close()
        return records

    def search_bill_time_span():
        conn = sqlite3.connect('Clinic_Database.db')
        cursor = conn.cursor()
        
        try:
            start_date = datetime.datetime.strptime(date_search1_entry.get(), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(date_search2_entry.get(), '%d/%m/%Y')
            cursor.execute("SELECT * FROM Bills")
            all_records = cursor.fetchall()
            records=[]
            for record in all_records:
                if  datetime.datetime.strptime(record[3],'%d/%m/%Y')>=datetime.datetime.strptime(date_search1_entry.get(),'%d/%m/%Y') and datetime.datetime.strptime(record[3],'%d/%m/%Y')<=datetime.datetime.strptime(date_search2_entry.get(),'%d/%m/%Y'):
                    records.append(record)
            display_bill_records(records)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
            return
        
        conn.close()
        return
    
    def display_bill_records(records):
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

        view_list['columns'] = ("File Number","Name","Cost","Quantity","Date")

        for column in ("#0", "File Number","Name","Cost","Quantity","Date"):
            view_list.column(column, width=100, minwidth=50)
            view_list.heading(column, text=column)
        
        all_bill_items=[]
        for record in records:
            for item in json.loads(record[2]):
                billItem=[record[0],record[1],item[0],item[1],item[2],record[3]]
                all_bill_items.append(billItem)
        i=1
        for record in all_bill_items:
            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[1],record[2],record[3],record[4],record[5]))
            i+=1

        view_list.pack(fill=BOTH, expand=True)

        report_button = Button(view_page, text="Generate Report", font='verdana 14 bold', command=lambda: generate_report(records, 'B'))
        report_button.pack(pady=5)

        exit_button = Button(view_page, text="Quit", font='verdana 12 bold', command=view_page.destroy)
        exit_button.pack(pady=5)

# def view_bills():

#     viewBillPage=Toplevel()
#     viewBillPage.title('Querying Bills')
#     viewBillPage.iconbitmap("shree_brahmi.ico")

#     date_label=Label(viewBillPage,text="Date",font='16')
#     date_label.grid(row=0,column=0,padx=10,pady=3,ipadx=20)        
#     date_search=Entry(viewBillPage,width=30)
#     date_search.grid(row=0,column=1,padx=10,pady=3,ipadx=30)
    
#     def search_bill_date():
        
#         searchBillDate=Toplevel()
#         searchBillDate.title('Searching Entry')
#         searchBillDate.iconbitmap("shree_brahmi.ico")  
        
#         searchBillDate.attributes("-fullscreen",True)
        
#         def exitf():
#             searchBillDate.destroy()
#             viewBillPage.attributes('-topmost', 1)
#             viewBillPage.attributes('-topmost', 0)
            
#         def generate():
#             excelworkbook=xw.Book('Bill_invoice.xlsx')
#             excelsheet=excelworkbook.sheets['Report1']
#             excelsheet.range("A2").value=all_bill_items
#             messagebox.showinfo("Generated","Report has been Successfully Generated. Minimise the Application to view it.")


#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
            
#         try:
#             if(date_search.get()==""): 
#                 cursor.execute("SELECT * FROM Bills")
#                 records=cursor.fetchall()
#             else:
#                 date_search_valid = datetime.datetime.strptime(date_search.get(), '%d/%m/%Y')
#                 cursor.execute("SELECT * FROM Bills WHERE Date LIKE '%"+ str(date_search_valid)+"%'") 
#                 records=cursor.fetchall()
#         except sqlite3.Error as e:
#             messagebox.showerror("Error", f"SQLite error: {e}")
#             exitf()
#             return
        
#         all_bill_items=[]
#         for record in records:
#             for item in json.loads(record[2]):
#                 billItem=[record[0],record[1],item[0],item[1],item[2],record[3]]
#                 all_bill_items.append(billItem)

#         view_frame=Frame(searchBillDate)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
#         view_list['columns']=("File Number","Name","Cost","Quantity","Date")
           
#         view_list.column("#0",width=60,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=400,minwidth=100)
#         view_list.column("Cost",width=80,minwidth=50)
#         view_list.column("Quantity",width=80,minwidth=50)
#         view_list.column("Date",width=80,minwidth=50)      
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Cost",text="Cost",anchor=W)
#         view_list.heading("Quantity",text="Quantity",anchor=W)
#         view_list.heading("Date",text="Date",anchor=W)
        
#         i=1
#         for record in all_bill_items:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[1],record[2],record[3],record[4],record[5]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
#         conn.commit()
#         conn.close()
        
#         reportbutton=Button(searchBillDate,text="Generate Report",font='verdana 14 bold',command=generate)
#         reportbutton.pack(pady=5)
        
#         exit_button=Button(searchBillDate, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack(pady=5)

#     def search_bill_fileNo():
        
#         searchBillFileNo=Toplevel()
#         searchBillFileNo.title('Searching Entry')
#         searchBillFileNo.iconbitmap("shree_brahmi.ico")  
        
#         searchBillFileNo.attributes("-fullscreen",True)
        
#         def exitf():
#             searchBillFileNo.destroy()
#             viewBillPage.attributes('-topmost', 1)
#             viewBillPage.attributes('-topmost', 0)
            
#         def generate():

#             excelworkbook=xw.Book('Bill_invoice.xlsx')
#             excelsheet=excelworkbook.sheets['Invoice']
#             excelsheet.range("A2").value=all_bill_items
#             messagebox.showinfo("Generated","Report has been Successfully Generated. Minimise the Application to view it.")

#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
            
#         try:
#             cursor.execute("SELECT * FROM Bills WHERE File_Number LIKE '%"+ str(fileno_search.get())+"%'") 
#             records=cursor.fetchall()
#         except sqlite3.Error as e:
#             messagebox.showerror("Error", f"SQLite error: {e}")
#             exitf()
#             return

#         all_bill_items=[]
#         for record in records:
#             for item in json.loads(record[2]):
#                 billItem=[record[0],record[1],item[0],item[1],item[2],record[3]]
#                 all_bill_items.append(billItem)

#         view_frame=Frame(searchBillFileNo)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
        
#         view_list['columns']=("File Number","Name","Cost","Quantity","Date")
           
#         view_list.column("#0",width=60,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=400,minwidth=100)
#         view_list.column("Cost",width=80,minwidth=50)
#         view_list.column("Quantity",width=80,minwidth=50)
#         view_list.column("Date",width=80,minwidth=50)      
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Cost",text="Cost",anchor=W)
#         view_list.heading("Quantity",text="Quantity",anchor=W)
#         view_list.heading("Date",text="Date",anchor=W)
        
#         i=1
#         for record in all_bill_items:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[1],record[2],record[3],record[4],record[5]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
#         conn.commit()
#         conn.close()
        
#         reportbutton=Button(searchBillFileNo,text="Generate Report",font='verdana 14 bold',command=generate)
#         reportbutton.pack(pady=5)
        
#         exit_button=Button(searchBillFileNo, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack(pady=5)

#     def search_bill_set_date():
    
#         searchBillSetDate=Toplevel()
#         searchBillSetDate.title('Searching Entry')
#         searchBillSetDate.iconbitmap("shree_brahmi.ico")  
        
#         searchBillSetDate.attributes("-fullscreen",True)
        
#         def exitf():
#             searchBillSetDate.destroy()
#             viewBillPage.attributes('-topmost', 1)
#             viewBillPage.attributes('-topmost', 0)
            
#         def generate():

#             excelworkbook=xw.Book('Bill_invoice.xlsx')
#             excelsheet=excelworkbook.sheets['Sheet1']
#             excelsheet.range("A2").value=all_bill_items
#             messagebox.showinfo("Generated","Report has been Successfully Generated. Minimise the Application to view it.")

#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
            
#         try:
#             datetime.datetime.strptime(date_search1.get(), '%d/%m/%Y')
#             datetime.datetime.strptime(date_search2.get(), '%d/%m/%Y')
#         except ValueError:    
#             messagebox.showerror("Error","The Dates are invalid!")
#             return 
        
#         if(date_search1.get()=="" or date_search2.get()=="" or  datetime.datetime.strptime(date_search1.get(),'%d/%m/%Y') > datetime.datetime.strptime(date_search2.get(),'%d/%m/%Y')): 
#             messagebox.showerror("Error","The Dates are invalid!")
#             return
        
                      
#         try:
#             cursor.execute("SELECT * FROM Bills")
#             allrecords=cursor.fetchall()
#             records=[]
#         except sqlite3.Error as e:
#             messagebox.showerror("Error", f"SQLite error: {e}")
        
       
#         for record in allrecords:
#             if  datetime.datetime.strptime(record[3],'%d/%m/%Y')>=datetime.datetime.strptime(date_search1.get(),'%d/%m/%Y') and datetime.datetime.strptime(record[3],'%d/%m/%Y')<=datetime.datetime.strptime(date_search2.get(),'%d/%m/%Y'):
#                 records.append(record)


#         all_bill_items=[]
#         for record in records:
#             for item in json.loads(record[2]):
#                 billItem=[record[0],record[1],item[0],item[1],item[2],record[3]]
#                 all_bill_items.append(billItem)

#         view_frame=Frame(searchBillSetDate)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
        
#         view_list['columns']=("File Number","Name","Cost","Quantity","Date")
           
#         view_list.column("#0",width=60,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=400,minwidth=100)
#         view_list.column("Cost",width=80,minwidth=50)
#         view_list.column("Quantity",width=80,minwidth=50)
#         view_list.column("Date",width=80,minwidth=50)      
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Cost",text="Cost",anchor=W)
#         view_list.heading("Quantity",text="Quantity",anchor=W)
#         view_list.heading("Date",text="Date",anchor=W)
        
#         i=1
#         for record in all_bill_items:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[1],record[2],record[3],record[4],record[5]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
#         conn.commit()
#         conn.close()
    
#         reportbutton=Button(searchBillSetDate,text="Generate Report",font='verdana 14 bold',command=generate)
#         reportbutton.pack(pady=5)
        
#         exit_button=Button(searchBillSetDate, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack(pady=5)

    
#     date_searchbutton=Button(viewBillPage,text="Search Entries",font='verdana 14 bold',command=search_bill_date)
#     date_searchbutton.grid(row=1,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
#     fileno_label=Label(viewBillPage,text="File Number",font='16')
#     fileno_label.grid(row=2,column=0,padx=10,pady=3,ipadx=20)        
#     fileno_search=Entry(viewBillPage,width=20)
#     fileno_search.grid(row=2,column=1,padx=10,pady=3,ipadx=30)
    
    
#     fileno_searchbutton=Button(viewBillPage,text="Search Entries",font='verdana 14 bold',command=search_bill_fileNo)
#     fileno_searchbutton.grid(row=3,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
#     date_label1=Label(viewBillPage,text="From",font='16')
#     date_label1.grid(row=4,column=0,padx=10,pady=3,ipadx=20)        
#     date_search1=Entry(viewBillPage,width=30)
#     date_search1.grid(row=4,column=1,padx=10,pady=3,ipadx=30)
#     format_label=Label(viewBillPage,text="(DD/MM/YYYY)",font='14')
#     format_label.grid(row=5,column=1,padx=10,pady=3,ipadx=20)
    
#     date_label2=Label(viewBillPage,text="To",font='16')
#     date_label2.grid(row=6,column=0,padx=10,pady=3,ipadx=20)        
#     date_search2=Entry(viewBillPage,width=30)
#     date_search2.grid(row=6,column=1,padx=10,pady=3,ipadx=30)
    
    
#     date_searchbutton=Button(viewBillPage,text="Search Entries",font='verdana 14 bold',command=search_bill_set_date)
#     date_searchbutton.grid(row=7,column=0,padx=50,pady=7,ipadx=20,columnspan=2)


# def search_entry():
    
#     sea=Toplevel()
#     sea.title('Searching Patient')
#     sea.iconbitmap("shree_brahmi.ico")
#     global records
    
#     headings=['File Number','Name','Date',' Income/Expense ', ' Opex/Capex ',' Amount ',' Description ']
    
    
#     def search_date():
        
#         sead=Toplevel()
#         sead.title('Searching Entry')
#         sead.iconbitmap("shree_brahmi.ico")  
        
#         sead.attributes("-fullscreen",True)
        
        
#         def exitf():
#             sead.destroy()
#             sea.destroy()
    
        
#         def generate():

#             excelworkbook=xw.Book('Report.xlsx')
#             excelsheet=excelworkbook.sheets['Report1']
#             excelsheet.range("A2").value=records
#             messagebox.showinfo("Generated","Report has been Successfully Generated. Minimise the Application to view it.")
        

#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
            
#         try:
#             cursor.execute("SELECT * FROM TransactionData WHERE Date LIKE '%"+ str(date_search.get())+"%'") 
#             records=cursor.fetchall()
#         except sqlite3.Error as e:
#             messagebox.showerror("Error", f"SQLite error: {e}")
#             exitf()
#             return

#         view_frame=Frame(sead)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
#         view_list['columns']=("File Number","Name","Amount","Date","Income/Expense","Opex/Capex","Payment Type","Description")
           
#         view_list.column("#0",width=60,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=200,minwidth=100)
#         view_list.column("Amount",width=100,minwidth=100)
#         view_list.column("Date",width=80,minwidth=50)
#         view_list.column("Income/Expense",width=100,minwidth=40)
#         view_list.column("Opex/Capex",width=100,minwidth=40)
#         view_list.column("Payment Type",width=100,minwidth=40)
#         view_list.column("Description",width=250,minwidth=40)       
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Amount",text="Amount",anchor=W)
#         view_list.heading("Date",text="Date",anchor=W)
#         view_list.heading("Income/Expense",text="Income/Expense",anchor=W)
#         view_list.heading("Opex/Capex",text="Opex/Capex",anchor=W)
#         view_list.heading("Payment Type",text="Payment Type",anchor=W)
#         view_list.heading("Description",text="Description",anchor=W)
        
#         i=1
#         for record in records:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],("₹ "+str(record[6])),record[2],record[3],record[4],record[5],record[7]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
#         conn.commit()
#         conn.close()
        
#         reportbutton=Button(sead,text="Generate Report",font='verdana 14 bold',command=generate)
#         reportbutton.pack(pady=5)
        
#         exit_button=Button(sead, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack(pady=5)
        
        
#     def search_fileno():
        
#         seaf=Toplevel()
#         seaf.title('Searching Entry')
#         seaf.iconbitmap("shree_brahmi.ico")
           
#         seaf.attributes("-fullscreen",True)
    
        
#         def exitf():
#             seaf.destroy()
#             sea.destroy()
        
#         def generate():            

#             excelworkbook=xw.Book('Report.xlsx')
#             excelsheet=excelworkbook.sheets['Report1']
#             excelsheet.range("A2").value=records  
#             messagebox.showinfo("Generated","Report has been Successfully Generated. Minimise the Application to view it.")      

#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()

#         try:    
#             cursor.execute("SELECT * FROM TransactionData WHERE File_Number LIKE '"+ str(fileno_search.get())+"'")
#             records=cursor.fetchall()
#         except sqlite3.Error as e:
#                         messagebox.showerror("Error", f"SQLite error: {e}")

        
#         view_frame=Frame(seaf)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
#         view_list['columns']=("File Number","Name","Amount","Date","Income/Expense","Opex/Capex","Payment Type","Description")
           
#         view_list.column("#0",width=60,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=200,minwidth=100)
#         view_list.column("Amount",width=100,minwidth=100)
#         view_list.column("Date",width=80,minwidth=50)
#         view_list.column("Income/Expense",width=100,minwidth=40)
#         view_list.column("Opex/Capex",width=100,minwidth=40)
#         view_list.column("Payment Type",width=100,minwidth=40)
#         view_list.column("Description",width=250,minwidth=40)
                        
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Amount",text="Amount",anchor=W)
#         view_list.heading("Date",text="Date",anchor=W)
#         view_list.heading("Income/Expense",text="Income/Expense",anchor=W)
#         view_list.heading("Opex/Capex",text="Opex/Capex",anchor=W)
#         view_list.heading("Payment Type",text="Payment Type",anchor=W)
#         view_list.heading("Description",text="Description",anchor=W)
        
#         i=1
#         for record in records:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],("₹ "+str(record[6])),record[2],record[3],record[4],record[5],record[7]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
        
#         conn.commit()
#         conn.close()
        
#         reportbutton=Button(seaf,text="Generate Report",font='verdana 14 bold',command=generate)
#         reportbutton.pack(pady=5)
        
#         exit_button=Button(seaf, text="Quit",font='verdana 12 bold', command=exitf)
#         exit_button.pack(pady=5)
        
    
#     def search_set_date():
        
#         seasd=Toplevel()
#         seasd.title('Searching Entry')
#         seasd.iconbitmap("shree_brahmi.ico")  
        
#         seasd.attributes("-fullscreen",True)
    
        
#         def generate():

#             excelworkbook=xw.Book('Report.xlsx')
#             excelsheet=excelworkbook.sheets['Report1']
#             excelsheet.range("A2").value=records
#             messagebox.showinfo("Generated","Report has been Successfully Generated. Minimise the Application to view it.")
        
        
#         conn=sqlite3.connect('Clinic_Database.db')
#         cursor=conn.cursor()
        
#         try:
#             datetime.datetime.strptime(date_search1.get(), '%d/%m/%Y')
#             datetime.datetime.strptime(date_search2.get(), '%d/%m/%Y')
#         except ValueError:    
#             messagebox.showerror("Error","The Dates are invalid!")
#             return 
        
#         if(date_search1.get()=="" or date_search2.get()=="" or  datetime.datetime.strptime(date_search1.get(),'%d/%m/%Y') > datetime.datetime.strptime(date_search2.get(),'%d/%m/%Y')): #is_date(date_search1.get()) or is_date(date_search2.get()) or
#             messagebox.showerror("Error","The Dates are invalid!")
#             return
        
                      
#         try:
#             cursor.execute("SELECT * FROM TransactionData")
#             allrecords=cursor.fetchall()
#             records=[]
#         except sqlite3.Error as e:
#                         messagebox.showerror("Error", f"SQLite error: {e}")
        
       
#         for record in allrecords:
#             if  datetime.datetime.strptime(record[2],'%d/%m/%Y')>=datetime.datetime.strptime(date_search1.get(),'%d/%m/%Y') and datetime.datetime.strptime(record[2],'%d/%m/%Y')<=datetime.datetime.strptime(date_search2.get(),'%d/%m/%Y'):
#                 records.append(record)
       
                                  
#         view_frame=Frame(seasd)
#         view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
        
#         view_list = ttk.Treeview(view_frame, height=27, yscrollcommand=view_scrollbar.set)
        
#         view_scrollbar.config(command=view_list.yview)
#         view_scrollbar.pack(side=RIGHT,fill=Y)
        
#         view_list['columns']=("File Number","Name","Amount","Date","Income/Expense","Opex/Capex","Payment Type","Description")
           
#         view_list.column("#0",width=60,minwidth=50)
#         view_list.column("File Number",width=120,minwidth=50)
#         view_list.column("Name",width=200,minwidth=100)
#         view_list.column("Amount",width=100,minwidth=100)
#         view_list.column("Date",width=80,minwidth=50)
#         view_list.column("Income/Expense",width=100,minwidth=40)
#         view_list.column("Opex/Capex",width=100,minwidth=40)
#         view_list.column("Payment Type",width=100,minwidth=40)
#         view_list.column("Description",width=250,minwidth=40)
                
        
#         view_list.heading("#0",text="Sl No.",anchor=W)
#         view_list.heading("File Number",text="File No.",anchor=W)
#         view_list.heading("Name",text="Name",anchor=W)
#         view_list.heading("Amount",text="Amount",anchor=W)
#         view_list.heading("Date",text="Date",anchor=W)
#         view_list.heading("Income/Expense",text="Income/Expense",anchor=W)
#         view_list.heading("Opex/Capex",text="Opex/Capex",anchor=W)
#         view_list.heading("Payment Type",text="Payment Type",anchor=W)
#         view_list.heading("Description",text="Description",anchor=W)
        
#         i=1
#         for record in records:
#            view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],("₹ "+str(record[6])),record[2],record[3],record[4],record[5],record[7]))
#            i+=1
        
#         view_frame.pack(pady=20,padx=20)
        
#         view_list.pack()
#         conn.commit()
#         conn.close()
        
#         reportbutton=Button(seasd,text="Generate Report",font='verdana 14 bold',command=generate)
#         reportbutton.pack(pady=5)
        
#         exit_button=Button(seasd, text="Quit",font='verdana 12 bold', command=seasd.destroy)
#         exit_button.pack(pady=5)
        
        
#     date_label=Label(sea,text="Date",font='16')
#     date_label.grid(row=0,column=0,padx=10,pady=3,ipadx=20)        
#     date_search=Entry(sea,width=30)
#     date_search.grid(row=0,column=1,padx=10,pady=3,ipadx=30)
    
    
#     date_searchbutton=Button(sea,text="Search Entries",font='verdana 14 bold',command=search_date)
#     date_searchbutton.grid(row=1,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
#     fileno_label=Label(sea,text="File Number",font='16')
#     fileno_label.grid(row=2,column=0,padx=10,pady=3,ipadx=20)        
#     fileno_search=Entry(sea,width=20)
#     fileno_search.grid(row=2,column=1,padx=10,pady=3,ipadx=30)
    
    
#     fileno_searchbutton=Button(sea,text="Search Entries",font='verdana 14 bold',command=search_fileno)
#     fileno_searchbutton.grid(row=3,column=0,padx=50,pady=7,ipadx=20,columnspan=2)
    
#     date_label1=Label(sea,text="From",font='16')
#     date_label1.grid(row=4,column=0,padx=10,pady=3,ipadx=20)        
#     date_search1=Entry(sea,width=30)
#     date_search1.grid(row=4,column=1,padx=10,pady=3,ipadx=30)
#     format_label=Label(sea,text="(DD/MM/YYYY)",font='14')
#     format_label.grid(row=5,column=1,padx=10,pady=3,ipadx=20)
    
#     date_label2=Label(sea,text="To",font='16')
#     date_label2.grid(row=6,column=0,padx=10,pady=3,ipadx=20)        
#     date_search2=Entry(sea,width=30)
#     date_search2.grid(row=6,column=1,padx=10,pady=3,ipadx=30)
    
    
#     date_searchbutton=Button(sea,text="Search Entries",font='verdana 14 bold',command=search_set_date)
#     date_searchbutton.grid(row=7,column=0,padx=50,pady=7,ipadx=20,columnspan=2)

    
    
# def view_entries():
#     conn=sqlite3.connect('Clinic_Database.db')
#     cursor=conn.cursor()
    
#     view=Toplevel()
#     view.title('Viewing Database')
#     view.iconbitmap("shree_brahmi.ico")    
#     view.attributes("-fullscreen",True)
    
#     try:
#         cursor.execute("SELECT * FROM TransactionData") 
#         records=cursor.fetchall()
#     except sqlite3.Error as e:
#         messagebox.showerror("Error", f"SQLite error: {e}")

#     view_frame=Frame(view)
#     view_scrollbar=Scrollbar(view_frame, orient=VERTICAL)
    
#     view_list = ttk.Treeview(view_frame, height=30, yscrollcommand=view_scrollbar.set)
    
#     view_scrollbar.config(command=view_list.yview)
#     view_scrollbar.pack(side=RIGHT,fill=Y)
    
#     view_list['columns']=("File Number","Name","Amount","Date","Income/Expense","Opex/Capex","Payment Type","Description")
       
#     view_list.column("#0",width=60,minwidth=50)
#     view_list.column("File Number",width=120,minwidth=50)
#     view_list.column("Name",width=200,minwidth=100)
#     view_list.column("Amount",width=100,minwidth=100)
#     view_list.column("Date",width=80,minwidth=50)
#     view_list.column("Income/Expense",width=100,minwidth=40)
#     view_list.column("Opex/Capex",width=100,minwidth=40)
#     view_list.column("Payment Type",width=100,minwidth=40)
#     view_list.column("Description",width=250,minwidth=40)    
    
    
#     view_list.heading("#0",text="Sl No.",anchor=W)
#     view_list.heading("File Number",text="File No.",anchor=W)
#     view_list.heading("Name",text="Name",anchor=W)
#     view_list.heading("Amount",text="Amount",anchor=W)
#     view_list.heading("Date",text="Date",anchor=W)
#     view_list.heading("Income/Expense",text="Income/Expense",anchor=W)
#     view_list.heading("Opex/Capex",text="Opex/Capex",anchor=W)
#     view_list.heading("Payment Type",text="Payment Type",anchor=W)
#     view_list.heading("Description",text="Description",anchor=W)
    
#     i=1
#     for record in records:
#        view_list.insert(parent='',index='end', iid=i, text=i, values=(record[0],record[1],("₹ "+str(record[6])),record[2],record[3],record[4],record[5],record[7]))
#        i+=1
    
#     view_frame.pack(pady=20,padx=20)
    
#     view_list.pack()

#     exit_button=Button(view, text="Quit",font='verdana 12 bold', command=view.destroy)
#     exit_button.pack()
        
#     conn.commit()
#     conn.close()



