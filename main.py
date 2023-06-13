from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import customtkinter
import time

# create database

conn = sqlite3.connect("mypharmacy.db")
curs = conn.cursor()

curs.execute("""CREATE TABLE IF NOT EXISTS Information (
                        Ref_no text,
                        Company_name text,
                        Type_of_med text,
                        Med_name text,
                        Lot_no text,
                        Issue_dt text,
                        Exp_dt text,
                        Uses text,
                        Side_effect text,
                        Precaution text,
                        Dosage text,
                        Price text,
                        Quantity text
                )""")
curs.execute("""CREATE TABLE IF NOT EXISTS pharma(
                        Ref_no integer,
                        Med_name text
                )""")

curs.execute("""CREATE TABLE IF NOT EXISTS patients(
                        patient_id INT NOT NULL,
                        patient_name VARCHAR(50) NOT NULL,
                        dob  text NOT NULL,
                        gender VARCHAR(10) NOT NULL,
                        contact_no VARCHAR(20) NOT NULL,
                        email VARCHAR(50) NOT NULL,
                        emergency_contact VARCHAR(20) NOT NULL,
                        street VARCHAR(50) NOT NULL,
                        city VARCHAR(50) NOT NULL,
                        allergies VARCHAR(100),
                        medications VARCHAR(100),
                        dosage VARCHAR(100),
                        price DECIMAL(10, 2) NOT NULL,
                        Name VARCHAR(50) NOT NULL,
                        Gender_kin VARCHAR(10) NOT NULL,
                        Relation VARCHAR(20) NOT NULL,
                        phone text NOT NULL,
                        Email_kin VARCHAR(50) NOT NULL,
                        Id_Number VARCHAR(20) NOT NULL,
                        mailing_address text NOT NULL,
                        emergency_contact_person text NOT NULL,
                        emergency_contact_kin VARCHAR(20) NOT NULL,
                        emergency_contact_email VARCHAR(20) NOT NULL,
                        language text NOT NULL
                 )""")

admin = sqlite3.connect('Admin.db')
cursor = admin.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS adm(
                        User_ID text,
                        Password text
                )""")


class Pharmacy:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1400x695")
        # self.root.resizable(False, False)
        self.ref_variable = StringVar()
        self.addmed_variable = StringVar()

        # MEDICINE DEPARTMENT VARIABLE

        self.refno_var = StringVar()
        self.companyname_var = StringVar()
        self.typemed_var = StringVar()
        self.medicine_var = StringVar()
        self.lotno_var = StringVar()
        self.issuedt_var = StringVar()
        self.expdt_var = StringVar()
        self.uses_var = StringVar()
        self.sideeffect_var = StringVar()
        self.warning_var = StringVar()
        self.dosage_var = StringVar()
        self.price_var = StringVar()
        self.quantity_var = StringVar()

        self.search_by = StringVar()
        self.search_txt = StringVar()

        # TITLE

        label_title = Label(self.root, text="Pharmacy management system", relief=RIDGE, fg="white", bg="black", bd=3,
                            font=('times new roman', 30, 'bold'))
        label_title.place(x=0, y=0, width=1370, height=75)

        # topframe
        top_frame = Frame(self.root, bg="#2f473d", relief=RIDGE, padx=20)
        top_frame.place(x=0, y=75, width=1370, height=370)

        # Downframe

        down_frame = Frame(self.root, bg='#2f473d', relief=RIDGE)
        down_frame.place(x=0, y=492, width=1365, height=200)

        # rightframe

        medinfo_frame = LabelFrame(top_frame, bg='#2f473d', relief=RIDGE, padx=20, text="Medicine Information",
                                   font=("arial", 13, "bold"), fg="white")
        medinfo_frame.place(x=500, y=0, width=820, height=350)

        # leftframe

        new_medframe = LabelFrame(top_frame, bg='#2f473d', relief=RIDGE, text="New Medicine",
                                  font=("arial", 13, "bold"), fg="white")
        new_medframe.place(x=0, y=5, width=452, height=350)

        # down button frame

        down_buttonframe = Frame(self.root, bg='#2f473d', relief=RIDGE, padx=20)
        down_buttonframe.place(x=0, y=432, width=1365, height=60)

        newframe_buttons = Frame(new_medframe, bg='#2f473d', relief=RIDGE)
        newframe_buttons.place(x=260, y=100, width=170, height=170)

        # Buttons on the med info frame

        add_button = Button(medinfo_frame, text="Add Medicine", font=("arial", 12, "bold"), command=self.addmedicine,
                            width=14, fg="white",
                            bg="#2f473d", bd=3, relief=RIDGE, activebackground="green", activeforeground="black")
        add_button.grid(row=4, column=3)

        update_button = Button(medinfo_frame, text="Update", font=("arial", 12, "bold"), width=14, fg="white",
                               bg="#2f473d", bd=3, relief=RIDGE, command=self.Update_new, activebackground="green",
                               activeforeground="black")
        update_button.place(x=440, y=180)

        delete_button = Button(medinfo_frame, text="Delete", font=("arial", 12, "bold"), command=self.delete,
                               width=14, fg="white",
                               bg="#2f473d", bd=3, relief=RIDGE, activebackground="green", activeforeground="black")
        delete_button.place(x=620, y=180)

        reset_button = Button(medinfo_frame, text="Reset", font=("arial", 12, "bold"), width=14, fg="white",
                              command=self.clear_new,
                              bg="#2f473d", bd=3, relief=RIDGE, activebackground="green", activeforeground="black")
        reset_button.place(x=440, y=250)

        def exit():
            self.root.destroy()
            WelcomeScreen()

        exit_button = Button(medinfo_frame, text="Exit", font=("arial", 12, "bold"), width=14, fg="white", bg="#2f473d",
                             bd=3, relief=RIDGE, activebackground="red", activeforeground="black", command=exit)
        exit_button.place(x=620, y=250)

        ###################Entry box and labels in med info frame############

        ref_label = Label(medinfo_frame, text="Reference No. :", padx=2, pady=4, font=("times new roman", 13, "bold"),
                          bg="#2f473d")
        ref_label.grid(row=0, column=0, sticky=W)

        def refresh(e):
            curs.execute("SELECT Ref_no FROM pharma")
            data = [row[0] for row in curs.fetchall()]
            self.ref_combo['values'] = data
            ref_no = self.refno_var.get()
            if ref_no:
                curs.execute("SELECT Med_name FROM pharma WHERE Ref_no=?", (ref_no,))
                data = curs.fetchone()
                if data:
                    self.medicine_var.set(data[0])
                else:
                    self.medicine_var.set("")
            else:
                self.medicine_var.set("")

        self.ref_combo = ttk.Combobox(medinfo_frame, textvariable=self.refno_var, width=23, font=(
            "times new roman", 13, "bold"), state="readonly")
        self.ref_combo.bind("<Button-1>", refresh)
        self.ref_combo.grid(row=0, column=1)

        company_label = Label(medinfo_frame, text="Company Name :", padx=2, pady=4,
                              font=("times new roman", 13, "bold"), bg="#2f473d")
        company_label.grid(row=1, column=0, sticky=W)
        self.company_entry = Entry(medinfo_frame, textvariable=self.companyname_var, width=24,
                                   font=("times new roman", 13, "bold"), fg="black",
                                   bg="white")
        self.company_entry.grid(row=1, column=1)

        medicine_type_label = Label(medinfo_frame, text="Type Of Medicine :. :", padx=2, pady=4,
                                    font=("times new roman", 13, "bold"), bg="#2f473d")
        medicine_type_label.grid(row=2, column=0, sticky=W)
        self.medicine_type_combo = ttk.Combobox(medinfo_frame, textvariable=self.typemed_var, width=23,
                                                font=("times new roman", 13, 'bold'), state="readonly")
        self.medicine_type_combo["values"] = (
            'Select', 'Tablet', 'Capsule', "Injection", "Ayurvedic", "Drops", "Inhales")
        self.medicine_type_combo.grid(row=2, column=1)
        self.medicine_type_combo.current(0)

        medicine_name_namelabel = Label(medinfo_frame, text="Medicine Name. :", padx=2, pady=4,
                                        font=("times new roman", 13, "bold"), bg="#2f473d")
        medicine_name_namelabel.grid(row=3, column=0, sticky=W)
        curs.execute("SELECT Med_name FROM pharma")
        data2 = [row[0] for row in curs.fetchall()]
        self.medicine_name_combo = ttk.Combobox(medinfo_frame, values=data2, textvariable=self.medicine_var, width=23,
                                                font=("times new roman", 13, 'bold'), state="readonly")
        self.medicine_name_combo.grid(row=3, column=1)

        lot_label = Label(medinfo_frame, text=" Lot No. :", padx=2, pady=4, font=("times new roman", 13, "bold"),
                          bg="#2f473d")
        lot_label.grid(row=4, column=0)
        self.lot_entry = Entry(medinfo_frame, width=24, textvariable=self.lotno_var,
                               font=("times new roman", 13, " bold"), fg="black", bg="white")
        self.lot_entry.grid(row=4, column=1)

        issue_label = Label(medinfo_frame, text=" Issue Date :", padx=2, pady=4, font=("times new roman", 13, "bold"),
                            bg="#2f473d")
        issue_label.grid(row=5, column=0)
        self.issue_entry = Entry(medinfo_frame, width=24, textvariable=self.issuedt_var,
                                 font=("times new roman", 13, "bold"), fg="black", bg="white")
        self.issue_entry.grid(row=5, column=1)

        exp_label = Label(medinfo_frame, text=" Expiry Date :", padx=2, pady=4, font=("times new roman", 13, "bold"),
                          bg="#2f473d")
        exp_label.grid(row=6, column=0)
        self.exp_entry = Entry(medinfo_frame, textvariable=self.expdt_var, width=24,
                               font=("times new roman", 13, " bold"), fg="black", bg="white")
        self.exp_entry.grid(row=6, column=1)

        use_label = Label(medinfo_frame, text=" Uses :", padx=2, pady=4, font=("times new roman", 13, "bold"),
                          bg="#2f473d")
        use_label.grid(row=7, column=0)
        self.use_entry = Entry(medinfo_frame, textvariable=self.uses_var, width=24,
                               font=("times new roman", 13, " bold"), fg="black", bg="white")
        self.use_entry.grid(row=7, column=1)

        sideeffect_label = Label(medinfo_frame, text=" Side Effect :", padx=2, pady=4,
                                 font=("times new roman", 13, "bold"), bg="#2f473d")
        sideeffect_label.grid(row=8, column=0)
        self.sideeffect_entry = Entry(medinfo_frame, textvariable=self.sideeffect_var, width=24,
                                      font=("times new roman", 13, " bold"), fg="black",
                                      bg="white")
        self.sideeffect_entry.grid(row=8, column=1)

        warn_label = Label(medinfo_frame, text=" Prec & warning:", padx=2, pady=4,
                           font=("times new roman", 13, "bold"), bg="#2f473d")
        warn_label.grid(row=9, column=0)
        self.warn_entry = Entry(medinfo_frame, textvariable=self.warning_var, width=24,
                                font=("times new roman", 13, " bold"), fg="black", bg="white")
        self.warn_entry.grid(row=9, column=1)

        dosage_label = Label(medinfo_frame, text=" Dosage :", padx=2, pady=4, font=("times new roman", 13, "bold"),
                             bg="#2f473d")
        dosage_label.grid(row=0, column=2)
        self.dosage_entry = Entry(medinfo_frame, textvariable=self.dosage_var, width=24,
                                  font=("times new roman", 13, " bold"), fg="black",
                                  bg="white")
        self.dosage_entry.grid(row=0, column=3)

        price_label = Label(medinfo_frame, text=" Tablet Price :", padx=2, pady=4,
                            font=("times new roman", 13, "bold"), bg="#2f473d")
        price_label.grid(row=1, column=2)
        self.price_entry = Entry(medinfo_frame, textvariable=self.price_var, width=24,
                                 font=("times new roman", 13, " bold"), fg="black",
                                 bg="white")
        self.price_entry.grid(row=1, column=3)

        qt_label = Label(medinfo_frame, text=" Tablet Quantity :", padx=2, pady=4,
                         font=("times new roman", 13, "bold"), bg="#2f473d")
        qt_label.grid(row=2, column=2)
        self.qt_entry = Entry(medinfo_frame, width=24, textvariable=self.quantity_var,
                              font=("times new roman", 13, " bold"), fg="black", bg="white")
        self.qt_entry.grid(row=2, column=3)

        ################frame displaying the medicine################
        side_frame = Frame(new_medframe, bd=5, relief=RIDGE, bg="#2f473d")
        side_frame.place(x=0, y=70, width=250, height=250)

        sc_x = ttk.Scrollbar(side_frame, orient=HORIZONTAL)
        sc_y = ttk.Scrollbar(side_frame, orient=VERTICAL)
        self.medicine_table = ttk.Treeview(side_frame, column=("ref", "medname"), xscrollcommand=sc_x.set,
                                           yscrollcommand=sc_y.set)
        sc_x.pack(side=BOTTOM, fill=X)
        sc_y.pack(side=RIGHT, fill=Y)

        sc_x.config(command=self.medicine_table.xview)
        sc_y.config(command=self.medicine_table.yview)

        self.medicine_table.heading("ref", text="Ref")
        self.medicine_table.heading("medname", text="Medicine Name")

        self.medicine_table["show"] = "headings"
        self.medicine_table.pack(fill=BOTH, expand=1)

        self.medicine_table.column("ref", width=100)
        self.medicine_table.column("medname", width=100)

        self.medicine_table.bind("<ButtonRelease-1>", self.medget_cursor)
        self.fetch_datamed()

        ##################buttons in new medicine department###################
        add_button = Button(newframe_buttons, text="Add", font=("arial", 13, "bold"), command=self.AddMed, width=13,
                            activeforeground="white", fg="white", bg="#2f473d", activebackground="green")
        add_button.grid(row=0, column=0)

        update_button = Button(newframe_buttons, text="update", command=self.update_med, bg="#2f473d",
                               font=("arial", 13, "bold"), width=13, fg="white", relief=RIDGE,
                               activebackground="green", activeforeground="white")
        update_button.grid(row=1, column=0)

        delete_button = Button(newframe_buttons, text="Delete", bg="#2f473d", command=self.Delete_med,
                               font=("arial", 13, "bold"), width=13, fg="white", relief=RIDGE,
                               activebackground="red", activeforeground="white")
        delete_button.grid(row=2, column=0)

        clear_button = Button(newframe_buttons, text="Clear", bg="#2f473d", font=("arial", 13, "bold"), width=13,
                              command=self.clear_med, fg="white", relief=RIDGE, activebackground="light grey",
                              activeforeground="white")
        clear_button.grid(row=3, column=0)

        ####################entry and label for new med frane###################33#
        no_label = Label(new_medframe, text="Reference No:", font=("times new roman", 11, "bold"), bg="#2f473d")
        no_label.place(x=0, y=10)
        self.no_entry = Entry(new_medframe, textvariable=self.ref_variable, relief=RIDGE, width=36,
                              font=("times new roman", 11, "bold"), bg="white", foreground='black')
        self.no_entry.place(x=120, y=10)

        med_label = Label(new_medframe, text="Med name:", font=("times new roman", 11, "bold"), bg="#2f473d")
        med_label.place(x=0, y=40)
        self.med_entry = Entry(new_medframe, textvariable=self.addmed_variable, relief=RIDGE, width=36,
                               font=("times new roman", 11, "bold"), bg="white", foreground='black')
        self.med_entry.place(x=120, y=40)

        ################search and show buttons and labels ###################
        search_by = Label(down_buttonframe, text="Search By", font=("arial", 15, "bold"), fg="black", bg="#2f473d",
                          bd=3,
                          padx=3)
        search_by.grid(row=0, column=5, sticky=W)

        self.search_combo = ttk.Combobox(down_buttonframe, width=12, font=("", 13, "bold"), state="readonly",
                                         textvariable=self.search_by)
        self.search_combo["values"] = ("Select Options", "Ref No.")
        self.search_combo.grid(row=0, column=6)
        self.search_combo.current(0)

        entry_button = Entry(down_buttonframe, font=("arial", 15, "bold"), fg="black", bg="white", bd=3, width=12,
                             relief=RIDGE, textvariable=self.search_txt)
        entry_button.grid(row=0, column=7)

        ##################button for search###################
        search_button = Button(down_buttonframe, text="Search", command=self.search_data, font=("arial", 13, "bold"),
                               width=10, fg="white", bg="#2f473d", relief=RIDGE, activebackground="black",
                               activeforeground="white")
        search_button.grid(row=0, column=8)
        show_button = Button(down_buttonframe, text="Show All", command=self.fetch_new,
                             font=("times new roman", 13, "bold"), fg="white", bg="#2f473d", width=10, relief=RIDGE,
                             activebackground="black", activeforeground="white")
        show_button.grid(row=0, column=9)

        pass_button = Button(down_buttonframe, text="Users",
                             font=("times new roman", 13, "bold"), command=password, fg="white", bg="purple", width=10,
                             relief=RIDGE,
                             activebackground="black", activeforeground="white")
        pass_button.grid(row=0, column=10, padx=100)

        search_button = customtkinter.CTkButton(master=self.root, bg_color="#2f473d",
                                                fg_color="blue",  # <- tuple color for light and dark theme
                                                text="Patients Details", command=self.search)
        search_button.place(x=1200, y=25)

        ########################down frame with table############
        scroll_frame = Frame(down_frame, bd=2, bg="brown")
        scroll_frame.place(x=0, y=0, width=1370, height=205)

        scroll_x = ttk.Scrollbar(scroll_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(scroll_frame, orient=VERTICAL)
        self.info_table = ttk.Treeview(scroll_frame,
                                       column=("ref no", "comp name", "type", "med name", "lot no", "issue", "exp",
                                               "uses", "side effect", "warning", "dosage", "price", "product"),
                                       xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.info_table.xview)
        scroll_y.config(command=self.info_table.yview)

        self.info_table.heading("ref no", text="Ref No.")
        self.info_table.heading("comp name", text="Company Name")
        self.info_table.heading("type", text="Type Of Medicine")
        self.info_table.heading("med name", text="Medicine Name")
        self.info_table.heading("lot no", text="Lot No.")
        self.info_table.heading("issue", text="Issue Date")
        self.info_table.heading("exp", text="Expiry Date")
        self.info_table.heading("uses", text="Uses")
        self.info_table.heading("side effect", text="Side Effects")
        self.info_table.heading("warning", text="Prec & Warning")
        self.info_table.heading("dosage", text="Dosage")
        self.info_table.heading("price", text="Medicine Price")
        self.info_table.heading("product", text="Product Qt.")

        self.info_table["show"] = "headings"
        self.info_table.pack(fill=BOTH, expand=1)

        self.info_table.column("ref no", width=100)
        self.info_table.column("comp name", width=100)
        self.info_table.column("type", width=100)
        self.info_table.column("med name", width=100)
        self.info_table.column("lot no", width=100)
        self.info_table.column("issue", width=100)
        self.info_table.column("exp", width=100)
        self.info_table.column("uses", width=100)
        self.info_table.column("side effect", width=100)
        self.info_table.column("warning", width=100)
        self.info_table.column("dosage", width=100)
        self.info_table.column("price", width=100)
        self.info_table.column("product", width=100)

        self.fetch_datamed()
        self.fetch_new()
        self.info_table.bind("<ButtonRelease-1>", self.get_cursor)

    ########################################med depart###########################

    def AddMed(self):
        if self.ref_variable.get() == "" or self.addmed_variable.get() == "":
            messagebox.showerror("Error", "All fields required")
        else:
            curs.execute("SELECT * FROM pharma WHERE Ref_no=?", (self.ref_variable.get(),))
            rows = curs.fetchall()
            if rows:
                messagebox.showerror("Error", "Ref_no already exists")
            else:
                curs.execute("INSERT INTO pharma(Ref_no, Med_name) VALUES (?, ?)",
                             (self.ref_variable.get(), self.addmed_variable.get()))
                conn.commit()
                self.fetch_datamed()
                self.medget_cursor()
                messagebox.showinfo("Success", "MEDICINE ADDED")

    def fetch_datamed(self):
        curs.execute("select * from pharma")
        rows = curs.fetchall()

        if len(rows) != 0:
            self.medicine_table.delete(*self.medicine_table.get_children())

            for i in rows:
                self.medicine_table.insert("", END, values=i)
            conn.commit()

    def medget_cursor(self, event=""):
        cursor_row = self.medicine_table.focus()
        content = self.medicine_table.item(cursor_row)
        row = content["values"]
        self.ref_variable.set(row[0])
        self.addmed_variable.set(row[1])

    def update_med(self):
        if self.ref_variable.get() == "" or self.addmed_variable.get() == "":

            messagebox.showerror("Error", "Ref No. and med name is required")
        else:
            try:
                curs.execute("update pharma set Med_name=? where Ref_no=?", (
                    self.addmed_variable.get(),
                    self.ref_variable.get(),
                ))

                conn.commit()
                messagebox.showinfo("Update", "Successfully Updated", parent=self.root)
                self.fetch_datamed()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to:{str(e)}", parent=self.root)

    def Delete_med(self):
        sql = "delete from pharma where Ref_no=?"
        val = (self.ref_variable.get(),)
        curs.execute(sql, val)
        conn.commit()
        self.fetch_datamed()

    def clear_med(self):
        self.ref_variable.set("")
        self.addmed_variable.set("")

    ###########################################################################333

    def addmedicine(self):
        if self.refno_var.get() == "" or self.lotno_var.get() == "" or self.typemed_var.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            curs.execute(
                "Insert into Information(REF_NO,COMPANY_NAME,TYPE_OF_MED,Med_name,LOT_NO,ISSUE_DT,EXP_DT,USES,SIDE_EFFECT,PRECAUTION,DOSAGE,PRICE,QUANTITY) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (

                    self.refno_var.get(),
                    self.companyname_var.get(),
                    self.typemed_var.get(),
                    self.medicine_var.get(),
                    self.lotno_var.get(),
                    self.issuedt_var.get(),
                    self.expdt_var.get(),
                    self.uses_var.get(),
                    self.sideeffect_var.get(),
                    self.warning_var.get(),
                    self.dosage_var.get(),
                    self.price_var.get(),
                    self.quantity_var.get(),
                ))
            conn.commit()
            self.fetch_new()

            messagebox.showinfo("Success", "Successfully added")

    def fetch_new(self):
        curs.execute("select * from Information")
        row = curs.fetchall()

        if len(row) != 0:
            self.info_table.delete(*self.info_table.get_children())

            for i in row:
                self.info_table.insert("", END, values=i)

            conn.commit()

    def get_cursor(self, ev=""):
        curs_row = self.info_table.focus()
        content = self.info_table.item(curs_row)
        row = content["values"]
        self.refno_var.set(row[0])
        self.companyname_var.set(row[1])
        self.typemed_var.set(row[2])
        self.medicine_var.set(row[3])
        self.lotno_var.set(row[4])
        self.issuedt_var.set(row[5])
        self.expdt_var.set(row[6])
        self.uses_var.set(row[7])
        self.sideeffect_var.set(row[8])
        self.warning_var.set(row[9])
        self.dosage_var.set(row[10])
        self.price_var.set(row[11])
        self.quantity_var.set(row[12])

    def Update_new(self):
        if self.refno_var.get() == "" or self.lotno_var.get() == "" or self.typemed_var.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            curs.execute(
                "update Information set Company_name=?,Type_of_med=?,Med_name=?,Lot_no=?,Issue_dt=?,Exp_dt=?,Uses=?, "
                "Side_effect=? ,Precaution=?,  Dosage=?, Price=? ,Quantity=?  where Ref_no=?",
                (
                    self.companyname_var.get(),
                    self.typemed_var.get(),
                    self.medicine_var.get(),
                    self.lotno_var.get(),
                    self.issuedt_var.get(),
                    self.expdt_var.get(),
                    self.uses_var.get(),
                    self.sideeffect_var.get(),
                    self.warning_var.get(),
                    self.dosage_var.get(),
                    self.price_var.get(),
                    self.quantity_var.get(),
                    self.refno_var.get(),
                ))
            conn.commit()
            self.fetch_new()
            messagebox.showinfo("UPDATE", "Record has been updated successfully")

    def clear_new(self):
        self.refno_var.set("")
        self.companyname_var.set("")
        self.typemed_var.set("")
        self.medicine_var.set("")
        self.lotno_var.set("")
        self.issuedt_var.set("")
        self.expdt_var.set("")
        self.uses_var.set("")
        self.sideeffect_var.set("")
        self.warning_var.set("")
        self.dosage_var.set("")
        self.price_var.set("")
        self.quantity_var.set("")

    def search_data(self):
        try:
            selected = self.search_combo.get()
            if selected == "Select Options":
                messagebox.showerror("Error", "You have to choose an option")
            else:
                curs.execute("SELECT * FROM Information WHERE Ref_no=?", (self.search_txt.get(),))
                row = curs.fetchone()
                if row is not None:
                    self.info_table.delete(*self.info_table.get_children())
                    self.info_table.insert("", END, values=row)
                    conn.commit()
                else:
                    messagebox.showinfo("Information", "No data found!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete(self):
        sql = "delete from Information where Ref_no=?"
        val = (self.refno_var.get(),)
        curs.execute(sql, val)
        conn.commit()
        self.fetch_new()

        messagebox.showinfo("Update", "Record has been deleted")

    def search(self):
        window = Tk()
        window.geometry("1470x720+0+0")
        scroll_frame = Frame(window, bg="#2f473d")
        scroll_frame.place(x=0, y=10, width=1370, height=600)

        button_frame = Frame(window, bg="#2f473d", bd=4, relief=RIDGE)
        button_frame.place(x=20, y=650, width=1300, height=50)

        scroll_x = ttk.Scrollbar(scroll_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(scroll_frame, orient=VERTICAL)

        self.patients = ttk.Treeview(scroll_frame,
                                     column=("patient_id", "patient_name", "dob", "gender", "contact_no", "email",
                                             "emergency_contact",
                                             "street", "city", "allergies", "medications", "dosage", "price", "Name",
                                             "Gender_kin", "Relation", "phone", "Email_kin", "Id_Number",
                                             "mailing_address",
                                             "emergency_contact_person", "emergency_contact_kin",
                                             "emergency_contact_email", "language"),
                                     xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.patients.xview)
        scroll_y.config(command=self.patients.yview)

        self.patients.heading("patient_id", text="Patient Id.")
        self.patients.heading("patient_name", text="Patient Name")
        self.patients.heading("dob", text="DOB")
        self.patients.heading("gender", text="Gender patient")
        self.patients.heading("contact_no", text="Contacts.")
        self.patients.heading("email", text="Email")
        self.patients.heading("emergency_contact", text="Emergency Contact")
        self.patients.heading("street", text="Street")
        self.patients.heading("city", text="City")
        self.patients.heading("allergies", text="Allergies")
        self.patients.heading("medications", text="Medicine")
        self.patients.heading("dosage", text="Dosage")
        self.patients.heading("price", text="Med Price")
        self.patients.heading("Name", text="Next of kin")
        self.patients.heading("Gender_kin", text="Gender_kin")
        self.patients.heading("Relation", text="Relation")
        self.patients.heading("phone", text="Contacts_kin")
        self.patients.heading("Email_kin", text="Email_kin")
        self.patients.heading("Id_Number", text="Id_kin")
        self.patients.heading("mailing_address", text="Mailing_address")
        self.patients.heading("emergency_contact_person", text="Emergency_contact_person")
        self.patients.heading("emergency_contact_kin", text="Emergency_contact_Kin")
        self.patients.heading("emergency_contact_email", text="emergency_contact_kin")
        self.patients.heading("language", text="Language")

        self.patients["show"] = "headings"
        self.patients.pack(fill=BOTH, expand=1)

        self.patients.column("patient_id", width=50)
        self.patients.column("patient_name", width=100)
        self.patients.column("dob", width=100)
        self.patients.column("gender", width=100)
        self.patients.column("contact_no", width=100)
        self.patients.column("email", width=100)
        self.patients.column("emergency_contact", width=100)
        self.patients.column("street", width=100)
        self.patients.column("city", width=100)
        self.patients.column("allergies", width=100)
        self.patients.column("medications", width=100)
        self.patients.column("dosage", width=100)
        self.patients.column("price", width=100)
        self.patients.column("Name", width=50)
        self.patients.column("Gender_kin", width=100)
        self.patients.column("Relation", width=100)
        self.patients.column("phone", width=100)
        self.patients.column("Email_kin", width=100)
        self.patients.column("Id_Number", width=100)
        self.patients.column("mailing_address", width=100)
        self.patients.column("emergency_contact_person", width=100)
        self.patients.column("emergency_contact_kin", width=100)
        self.patients.column("emergency_contact_email", width=100)
        self.patients.column("language", width=100)

        self.patients_fetch()

        close_button = Button(button_frame, text="close patients window", bd=6, relief=RIDGE, command=window.destroy,
                              font=("arial", 13, "bold"), width=30,
                              activeforeground="white", fg="white", bg="#2f473d",
                              activebackground="red")
        close_button.grid(row=0, column=0, padx=(500, 450))

    def patients_fetch(self):
        curs.execute("select * from patients ")
        row = curs.fetchall()

        if len(row) != 0:
            self.patients.delete(*self.patients.get_children())

            for i in row:
                self.patients.insert("", END, values=i)

            conn.commit()


class PatientsDashboard:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Patients Registration Dashboard")
        self.master.geometry("1400x760")

        self.title_label = Label(self.master, bg="#43233F", text="Welcome to Patients Registration Dashboard",
                                 font=("Arial", 20))
        self.title_label.place(x=0, y=0, width=1360, height=50)

        self.main_frame = LabelFrame(self.master, bg='#2f473d', text="Patients Information", labelanchor=N,
                                     font=("arial", 13, "bold"))
        self.main_frame.place(x=0, y=50, width=1360, height=650)

        self.title_label = Label(self.main_frame, bg='#2f473d', text="Patients Details",
                                 font=("Arial"))
        self.title_label.place(x=200, y=30, width=130, height=20)

        self.search_bar = LabelFrame(self.master, bg='#2f473d')
        self.search_bar.place(y=50, x=0, width=1360, height=50)

        frame_patient = customtkinter.CTkFrame(master=self.main_frame,
                                               width=800,
                                               height=700,
                                               corner_radius=10)
        frame_patient.place(x=50, y=50)

        frame = customtkinter.CTkFrame(master=self.main_frame,
                                       width=500,
                                       height=500,
                                       corner_radius=10)
        frame.place(x=600, y=50)

        # Patient ID field
        patient_id_lbl = Label(frame_patient, text='Patient ID:', font=("arial"))
        patient_id_lbl.grid(row=0, column=0, padx=15, sticky="w", pady=(0, 15))

        patient_id_ent = Entry(frame_patient, width=23, font=("arial"))
        patient_id_ent.grid(row=0, column=1, padx=15, pady=(0, 15))

        # Patient name field
        patient_name_lbl = Label(frame_patient, text='Patient Name:', font=("arial"))
        patient_name_lbl.grid(row=1, column=0, padx=15, sticky="w", pady=(0, 15))

        patient_name_ent = Entry(frame_patient, width=23, font=("arial"))
        patient_name_ent.grid(row=1, column=1, padx=15, pady=(0, 15))

        # Date of birth field
        dob_lbl = Label(frame_patient, text='Date of Birth:', font=("arial"))
        dob_lbl.grid(row=2, column=0, padx=15, sticky="w", pady=(0, 15))

        dob_ent = Entry(frame_patient, width=23, font=("arial"))
        dob_ent.grid(row=2, column=1, padx=15, pady=(0, 15))

        # Gender field
        patient_gender_lbl = Label(frame_patient, text='Gender:', font=("arial"))
        patient_gender_lbl.grid(row=3, column=0, padx=15, sticky="w", pady=(0, 15))

        patient_gender_ent = ttk.Combobox(frame_patient, width=21, font=("arial"),
                                          state='readonly')
        patient_gender_ent['values'] = ('Select Gender', 'Male', 'Female', 'Others')
        patient_gender_ent.current(0)
        patient_gender_ent.grid(row=3, column=1, padx=15, pady=(0, 15))

        # Contact information fields
        contact_lbl = Label(frame_patient, text='Contact Information:', font=("arial"))
        contact_lbl.grid(row=4, column=0, padx=15, sticky="w", pady=(0, 15))
        contact_no_ent = Entry(frame_patient, width=23, font=("arial"))
        contact_no_ent.grid(row=4, column=1, padx=15, sticky="w", pady=(0, 15))

        email_lbl = Label(frame_patient, text='Email Address:', font=("arial"))
        email_lbl.grid(row=6, column=0, padx=15, sticky="w", pady=(0, 15))

        email_ent = Entry(frame_patient, width=23, font=("arial"))
        email_ent.grid(row=6, column=1, padx=15, pady=(0, 15))

        # Emergency contact information fields
        emergency_lbl = Label(frame_patient, text='Emergency Contact Information:', font=("arial"))
        emergency_lbl.grid(row=7, column=0, padx=15, sticky="w", pady=(0, 15))
        emergency_contact_ent = Entry(frame_patient, width=23, font=("arial"))
        emergency_contact_ent.grid(row=7, column=1, padx=15, pady=(0, 15))

        street_lbl = Label(frame_patient, text='Street:', font=("arial"))
        street_lbl.grid(row=11, column=0, padx=15, sticky="w", pady=(0, 15))

        street_ent = Entry(frame_patient, width=23, font=("arial"))
        street_ent.grid(row=11, column=1, padx=15, pady=(0, 15))

        city_lbl = Label(frame_patient, text='City:', font=("arial"))
        city_lbl.grid(row=12, column=0, padx=15, sticky="w", pady=(0, 15))

        city_ent = Entry(frame_patient, width=23, font=("arial"))
        city_ent.grid(row=12, column=1, padx=15, pady=(0, 15))

        allergies_lbl = Label(frame_patient, text='Allergies:', font=("arial"))
        allergies_lbl.grid(row=17, column=0, padx=15, sticky="w", pady=(0, 15))

        allergies_ent = Entry(frame_patient, width=23, font=("arial"))
        allergies_ent.grid(row=17, column=1, padx=15, pady=(0, 15))

        medications_lbl = Label(frame_patient, text='Medicine:', font=("arial"))
        medications_lbl.grid(row=18, column=0, padx=15, sticky="w", pady=(0, 15))

        medications_ent = Entry(frame_patient, width=23, font=("arial"))
        medications_ent.grid(row=18, column=1, padx=15, pady=(0, 15))

        diagnosis_lbl = Label(frame_patient, text='Dosage:', font=("arial"))
        diagnosis_lbl.grid(row=19, column=0, padx=15, sticky="w", pady=(0, 15))

        diagnosis_ent = Entry(frame_patient, width=23, font=("arial"))
        diagnosis_ent.grid(row=19, column=1, padx=15, pady=(0, 15))

        medicine_price_lbl = Label(frame_patient, text='Price:', font=("arial"))
        medicine_price_lbl.grid(row=20, column=0, padx=15, sticky="w", pady=(0, 15))

        price_ent = ttk.Entry(frame_patient, width=23, font=("arial"))
        price_ent.grid(row=20, column=1, padx=15, pady=(0, 15))

        title_label = tk.Label(frame, text="Next of Kin Details")
        title_label.grid(row=0, column=0, padx=100, pady=10)

        name_label = tk.Label(frame, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        name_entry = tk.Entry(frame, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        gender_lbl = Label(frame, text='Gender:')
        gender_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        gender_ent = ttk.Combobox(frame, width=30, state='readonly')
        gender_ent['values'] = ('Select Gender', 'Male', 'Female', 'Others')
        gender_ent.current(0)
        gender_ent.grid(row=2, column=1, padx=10, pady=10)

        relation_label = tk.Label(frame, text="Relation:")
        relation_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        relation_entry = tk.Entry(frame, width=30)
        relation_entry.grid(row=3, column=1, padx=10, pady=10)

        phone_label = tk.Label(frame, text="Phone:")
        phone_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        phone_entry = tk.Entry(frame, width=30)
        phone_entry.grid(row=4, column=1, padx=10, pady=10)

        email_label = tk.Label(frame, text="Email:")
        email_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        email_entry = tk.Entry(frame, width=30)
        email_entry.grid(row=5, column=1, padx=10, pady=10)

        id_number = tk.Label(frame, text="Id Number:")
        id_number.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        id_number = tk.Entry(frame, width=30)
        id_number.grid(row=6, column=1, padx=10, pady=10)

        mailing_address_label = tk.Label(frame, text="Mailing Address:")
        mailing_address_label.grid(row=11, column=0, padx=10, pady=10, sticky="w")

        mailing_address_entry = tk.Entry(frame, width=30)
        mailing_address_entry.grid(row=11, column=1, padx=10, pady=10)

        emergency_contact_label = tk.Label(frame, text="Emergency Contact Person:")
        emergency_contact_label.grid(row=12, column=0, padx=10, pady=10, sticky="w")

        emergency_contact_entry = tk.Entry(frame, width=30)
        emergency_contact_entry.grid(row=12, column=1, padx=10, pady=10)

        emergency_contact_phone_label = tk.Label(frame, text="Emergency Contact Phone Number:")
        emergency_contact_phone_label.grid(row=13, column=0, padx=10, pady=10, sticky="w")

        emergency_contact_phone_entry = tk.Entry(frame, width=30)
        emergency_contact_phone_entry.grid(row=13, column=1, padx=10, pady=10)

        emergency_contact_email_label = tk.Label(frame, text="Emergency Contact Email:")
        emergency_contact_email_label.grid(row=14, column=0, padx=10, pady=10, sticky="w")

        emergency_contact_email_entry = tk.Entry(frame, width=30)
        emergency_contact_email_entry.grid(row=14, column=1, padx=10, pady=10)

        preferred_language_label = tk.Label(frame, text="Preferred Language for Communication with Next of Kin:")
        preferred_language_label.grid(row=17, column=0, padx=10, pady=10, sticky="w")

        preferred_language_entry = tk.Entry(frame, width=30)
        preferred_language_entry.grid(row=17, column=1, padx=10, pady=10)

        customtkinter.set_appearance_mode("dark")  # Other: "Light", "System" (only macOS)

        button = customtkinter.CTkButton(master=self.search_bar, bg_color="#2f473d",
                                         fg_color=("black", "grey"),  # <- tuple color for light and dark theme
                                         text="Log Out", command=self.exit)
        button.place(x=30, y=15)

        def search():
            window = Tk()
            window.geometry("1370x350+0+90")
            window.overrideredirect(True)
            search_button.configure(state=DISABLED)

            scroll_frame = Frame(window, bg="#2f473d")
            scroll_frame.place(x=0, y=10, width=1370, height=250)

            button_frame = Frame(window, bg="#2f473d", bd=7, relief=RIDGE)
            button_frame.place(x=20, y=270, width=1300, height=70)

            def selected():
                for selected_item in self.info_table.selection():
                    item = self.info_table.item(selected_item)
                    vals = item['values']

                    curs.execute("SELECT  Med_name,Dosage,Price FROM Information WHERE Ref_no LIKE '%" + vals[0] + "%'")
                    details = curs.fetchall()

                    medlist = []
                    for items in details:
                        medlist.append(items)

                    for x in medlist:
                        medications_ent.delete(0, END)
                        diagnosis_ent.delete(0, END)
                        price_ent.delete(0, END)

                        medications_ent.insert(0, x[0])
                        diagnosis_ent.insert(0, x[1])
                        price_ent.insert(0, x[2])

            def fetch_new(self):
                curs.execute("select * from Information")
                row = curs.fetchall()

                if len(row) != 0:
                    self.info_table.delete(*self.info_table.get_children())

                    for i in row:
                        self.info_table.insert("", END, values=i)

                    conn.commit()

            scroll_x = ttk.Scrollbar(scroll_frame, orient=HORIZONTAL)
            scroll_y = ttk.Scrollbar(scroll_frame, orient=VERTICAL)
            self.info_table = ttk.Treeview(scroll_frame,
                                           column=("ref no", "comp name", "type", "med name", "lot no", "issue", "exp",
                                                   "uses", "side effect", "warning", "dosage", "price", "product"),
                                           xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)

            scroll_x.config(command=self.info_table.xview)
            scroll_y.config(command=self.info_table.yview)

            self.info_table.heading("ref no", text="Ref No.")
            self.info_table.heading("comp name", text="Company Name")
            self.info_table.heading("type", text="Type Of Medicine")
            self.info_table.heading("med name", text="Medicine Name")
            self.info_table.heading("lot no", text="Lot No.")
            self.info_table.heading("issue", text="Issue Date")
            self.info_table.heading("exp", text="Expiry Date")
            self.info_table.heading("uses", text="Uses")
            self.info_table.heading("side effect", text="Side Effects")
            self.info_table.heading("warning", text="Prec & Warning")
            self.info_table.heading("dosage", text="Dosage")
            self.info_table.heading("price", text="Medicine Price")
            self.info_table.heading("product", text="Product Qt.")

            self.info_table["show"] = "headings"
            self.info_table.pack(fill=BOTH, expand=1)

            self.info_table.column("ref no", width=50)
            self.info_table.column("comp name", width=100)
            self.info_table.column("type", width=100)
            self.info_table.column("med name", width=100)
            self.info_table.column("lot no", width=100)
            self.info_table.column("issue", width=100)
            self.info_table.column("exp", width=100)
            self.info_table.column("uses", width=100)
            self.info_table.column("side effect", width=100)
            self.info_table.column("warning", width=100)
            self.info_table.column("dosage", width=100)
            self.info_table.column("price", width=100)
            self.info_table.column("product", width=100)

            add_button = Button(button_frame, text="Select Medicine", font=("arial", 13, "bold"), width=13,
                                activeforeground="white", fg="white", command=selected, bg="#2f473d",
                                activebackground="green")
            add_button.grid(row=0, column=0, padx=(500, 450), pady=10)

            def iExit():
                search_button.configure(state=ACTIVE)
                window.destroy()

            close_button = Button(button_frame, text="Close", font=("arial", 13, "bold"), width=13,
                                  activeforeground="white", fg="white", bg="#2f473d", command=iExit,
                                  activebackground="green")
            close_button.grid(row=0, column=1, pady=10)

            # get_cursor()

            fetch_new(self)

        search_button = customtkinter.CTkButton(master=self.search_bar, bg_color="#2f473d",
                                                fg_color=("blue"),  # <- tuple color for light and dark theme
                                                text="Medicine Details", command=search)
        search_button.place(x=1200, y=15)

        def addpatient():
            if patient_id_ent.get() == "" or patient_name_ent.get() == "" or emergency_contact_ent.get() == "":
                messagebox.showerror("Error", "All fields are required")
            else:
                curs.execute("INSERT INTO  patients  (patient_id, patient_name, dob, gender, contact_no, email,"
                             "emergency_contact, street, city, allergies, medications, dosage, price,Name, Gender_kin,"
                             "Relation ,phone,Email_kin,"
                             "Id_Number,mailing_address,emergency_contact_person,emergency_contact_kin,"
                             "emergency_contact_email, language) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,"
                             "?,?,?,?,?,?,?,?,?,?)", (patient_id_ent.get(), patient_name_ent.get(), dob_ent.get(),
                                                      patient_gender_ent.get(), contact_no_ent.get(), email_ent.get(),
                                                      emergency_contact_ent.get(), street_ent.get(), city_ent.get(),
                                                      allergies_ent.get(), medications_ent.get(), diagnosis_ent.get(),
                                                      price_ent.get(), name_entry.get(),
                                                      gender_ent.get(), relation_entry.get(), phone_entry.get(),
                                                      email_entry.get(),
                                                      id_number.get(), mailing_address_entry.get(),
                                                      emergency_contact_entry.get(),
                                                      emergency_contact_ent.get(), emergency_contact_email_entry.get(),
                                                      preferred_language_entry.get(),))

                conn.commit()
                messagebox.showinfo("Success", "Successfully added")

        def update():
            if patient_id_ent.get() == "" or patient_name_ent.get() == "" or emergency_contact_ent.get() == "":
                messagebox.showerror("Error", "All fields are required")
            else:
                curs.execute(
                    "update patients set patient_name=?,dob=?,gender=?,contact_no=?,email=?,emergency_contact=?,"
                    "street=?, city=? ,allergies=?,  medications=?, dosage=? ,price=?  where patient_id=?",
                    (
                        patient_name_ent.get(),
                        dob_ent.get(),
                        patient_gender_ent.get(),
                        contact_no_ent.get(),
                        email_ent.get(),
                        emergency_contact_ent.get(),
                        street_ent.get(),
                        city_ent.get(),
                        allergies_ent.get(),
                        medications_ent.get(),
                        diagnosis_ent.get(),
                        price_ent.get(),
                        patient_id_ent.get(),

                    ))
                conn.commit()

                messagebox.showinfo("Success", "Successfully updated patients details")

        def Delete_patient():
            sql = "delete from patients where patient_id=?"
            val = (patient_id_ent.get(),)
            curs.execute(sql, val)
            messagebox.showwarning("Deleted", "Record have been deleted successfully")
            conn.commit()

        # Add butt self.fetch_new()on for Add
        add_button = customtkinter.CTkButton(self.main_frame, width=90, command=addpatient, height=50,
                                             bg_color="#2f473d",
                                             fg_color="black",
                                             text="Add")
        add_button.place(x=600, y=570)

        # Add button for Update
        update_button = customtkinter.CTkButton(self.main_frame, command=update, width=90, height=50,
                                                bg_color="#2f473d",
                                                fg_color="blue",
                                                text="Update")
        update_button.place(x=800, y=570)

        # Add button for Delete
        delete_button = customtkinter.CTkButton(self.main_frame, command=Delete_patient, width=90, height=50,
                                                bg_color="#2f473d",
                                                fg_color="Red",
                                                text="Delete")
        delete_button.place(x=1000, y=570)

        def clear():
            patient_id_ent.delete(0, END)
            patient_name_ent.delete(0, END)
            patient_name_ent.delete(0, END)
            dob_ent.delete(0, END)
            patient_gender_ent.delete(0, END)
            contact_no_ent.delete(0, END)
            email_ent.delete(0, END)
            emergency_contact_ent.delete(0, END)
            street_ent.delete(0, END)
            city_ent.delete(0, END)
            allergies_ent.delete(0, END)
            medications_ent.delete(0, END)
            diagnosis_ent.delete(0, END)
            price_ent.delete(0, END)
            patient_id_ent.delete(0, END)
            name_entry.delete(0, END)
            name_entry.delete(0, END)
            gender_ent.delete(0, END)
            relation_entry.delete(0, END)
            phone_entry.delete(0, END),
            email_entry.delete(0, END),
            id_number.delete(0, END)
            mailing_address_entry.delete(0, END),
            emergency_contact_entry.delete(0, END),
            emergency_contact_ent.delete(0, END)
            emergency_contact_email_entry.delete(0, END)
            preferred_language_entry.delete(0, END)



        # Add button for Search
        clear_button = customtkinter.CTkButton(self.main_frame, width=90,command=clear, height=50, bg_color="#2f473d",
                                               fg_color="green",
                                               text="Clear")
        clear_button.place(x=1200, y=570)

        self.master.mainloop()

    def exit(self):
        self.master.destroy()

        WelcomeScreen()


class password:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("450x450+500+50")

        self.username = StringVar()
        self.password = StringVar()

        new_user = LabelFrame(self.window, bg='purple', relief=RIDGE, text="New user",
                                  font=("arial", 13, "bold"), fg="white")
        new_user.place(x=0, y=5, width=452, height=350)

        newframe_buttons = Frame(new_user, bg='purple', relief=RIDGE)
        newframe_buttons.place(x=260, y=100, width=170, height=170)

        no_label = Label(new_user, text="User Name:", font=("times new roman", 11, "bold"), bg="purple")
        no_label.place(x=0, y=10)

        side_frame = Frame(new_user, bd=5, relief=RIDGE, bg="purple")
        side_frame.place(x=0, y=70, width=250, height=250)

        sc_x = ttk.Scrollbar(side_frame, orient=HORIZONTAL)
        sc_y = ttk.Scrollbar(side_frame, orient=VERTICAL)
        self.password_table = ttk.Treeview(side_frame, column=("Username", "Password"), xscrollcommand=sc_x.set,
                                           yscrollcommand=sc_y.set)
        sc_x.pack(side=BOTTOM, fill=X)
        sc_y.pack(side=RIGHT, fill=Y)

        sc_x.config(command=self.password_table.xview)
        sc_y.config(command=self.password_table.yview)

        self.password_table.heading("Username", text="Username")
        self.password_table.heading("Password", text="Password")

        self.password_table["show"] = "headings"
        self.password_table.pack(fill=BOTH, expand=1)

        self.password_table.column("Username", width=100)
        self.password_table.column("Password", width=100)

        self.password_table.bind("<ButtonRelease-1>", self.userget_cursor)
        self.fetch_user()

        ##################buttons in new medicine department###################
        add_button = Button(newframe_buttons, text="Add", font=("arial", 13, "bold"), command=self.adduser, width=13,
                            activeforeground="white", fg="white", bg="purple", activebackground="green")
        add_button.grid(row=0, column=0)

        update_button = Button(newframe_buttons, text="update", command=self.update_user, bg="purple",
                               font=("arial", 13, "bold"), width=13, fg="white", relief=RIDGE,
                               activebackground="green", activeforeground="white")
        update_button.grid(row=1, column=0)

        delete_button = Button(newframe_buttons, text="Delete", bg="purple", command=self.delete_user,
                               font=("arial", 13, "bold"), width=13, fg="white", relief=RIDGE,
                               activebackground="red", activeforeground="white")
        delete_button.grid(row=2, column=0)

        clear_button = Button(newframe_buttons, text="Clear", bg="purple", font=("arial", 13, "bold"), width=13,
                              command=self.clearent, fg="white", relief=RIDGE, activebackground="light grey",
                              activeforeground="white")
        clear_button.grid(row=3, column=0)

        self.no_entry = Entry(new_user, textvariable=self.username, relief=RIDGE, width=36,
                              font=("times new roman", 11, "bold"), bg="white", foreground='black')
        self.no_entry.place(x=120, y=10)

        med_label = Label(new_user, text="Password:", font=("times new roman", 11, "bold"), bg="purple")
        med_label.place(x=0, y=40)
        self.passwo_entry = Entry(new_user, textvariable=self.password, relief=RIDGE, width=36,
                                  font=("times new roman", 11, "bold"), bg="white", foreground='black')
        self.passwo_entry.place(x=120, y=40)

        button_frame = Frame(self.window, bg="purple", bd=4, relief=RIDGE)
        button_frame.place(x=20, y=380, width=400, height=50)

        close_button = Button(button_frame, text="close password window", bd=3, relief=RIDGE,
                              command=self.window.destroy,
                              font=("arial", 13, "bold"), width=30,
                              activeforeground="white", fg="white", bg="purple",
                              activebackground="red")
        close_button.grid(row=0, column=0, ipadx=20)

        self.window.mainloop()

    def adduser(self):
        if self.no_entry.get() == "" or self.passwo_entry.get() == "":
            messagebox.showerror("Error", "All fields required")
        else:
            cursor.execute("SELECT * FROM adm WHERE User_ID=?", (self.no_entry.get(),))
            rows = cursor.fetchall()
            if rows:
                messagebox.showerror("Error", "User_ID already exists")
            else:
                cursor.execute("INSERT INTO adm(User_ID, Password) VALUES (?, ?)",
                               (self.no_entry.get(), self.passwo_entry.get()))
                admin.commit()
                messagebox.showinfo("Success", "User added")
                self.fetch_user()
                self.userget_cursor()

    def fetch_user(self):
        cursor.execute("select * from adm ")
        rows = cursor.fetchall()

        if len(rows) != 0:
            self.password_table.delete(*self.password_table.get_children())

            for i in rows:
                self.password_table.insert("", END, values=i)
            admin.commit()

    def userget_cursor(self, event=""):
        cursor_row = self.password_table.focus()
        content = self.password_table.item(cursor_row)
        row = content["values"]
        # for items in content:
        #     row.append(items)

        self.no_entry.delete(0, END)
        self.passwo_entry.delete(0, END)

        self.no_entry.insert(0, row[0])
        self.passwo_entry.insert(END, row[1])

    def update_user(self):
        if self.no_entry.get() == "" or self.passwo_entry.get() == "":

            messagebox.showerror("Error", "Username. and med name is required")
        else:
            try:
                cursor.execute("update adm set Password=? where User_ID=?", (
                    self.passwo_entry.get(),
                    self.no_entry.get(),
                ))

                admin.commit()
                messagebox.showinfo("Update", "Successfully Updated", parent=self.window)
                self.fetch_user()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to:{str(e)}", parent=self.window)

    def delete_user(self):
        sql = "delete from adm where User_ID=?"
        val = (self.no_entry.get(),)
        cursor.execute(sql, val)
        admin.commit()
        self.fetch_user()

    def clearent(self):
        self.no_entry.delete(0, END)
        self.passwo_entry.delete(0, END)


class WelcomeScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("1360x760")

        self.Label = Label(self.root, fg='green', text="WELCOME TO PHARMARCY MANAGEMENT SYSTEM", font=("times", 17),
                           bg="#d8dddd").place(x=400, y=40)

        mainframe = LabelFrame(self.root, text=":::LOGIN AS:::", background="#2f473d", labelanchor=N)
        mainframe.place(x=300, y=100, height=360, width=760)

        self.bgg = PhotoImage(
            file=r"pattern.png")
        lbl_bgg = Label(mainframe, image=self.bgg)
        lbl_bgg.place(x=0, y=0, width=1350, height=750)

        self.login_pharmacy_button = Button(mainframe, text="ADMIN", font=("arial", 12, "bold"), width=130, height=32,
                                            fg="white",
                                            bg="#2f473d", bd=6, relief=RIDGE, command=self.open_pharmacy_dashboard,
                                            activebackground="green",
                                            activeforeground="black")
        self.login_pharmacy_button.place(x=320, y=20)
        self.logo = PhotoImage(file='user.png')
        self.login_pharmacy_button.config(image=self.logo, compound=LEFT)
        self.small_logo = self.logo.subsample(1, 1)
        self.login_pharmacy_button.config(image=self.small_logo)


        self.login_patients_button = Button(mainframe, text="USER", font=("arial", 12, "bold"), width=130, height=32,
                                            fg="white",
                                            bg="#2f473d", bd=6, relief=RIDGE, command=self.open_patients_dashboard,
                                            activebackground="green",
                                            activeforeground="black")
        self.login_patients_button.place(x=320, y=100)
        self.logo2 = PhotoImage(file='bt4.png')
        self.login_patients_button.config(image=self.logo2, compound=LEFT)
        self.small_logo2 = self.logo2.subsample(1, 1)
        self.login_patients_button.config(image=self.small_logo2)

        login_out_button = customtkinter.CTkButton(self.root, corner_radius=30, command=exit, width=100,
                                                   height=50,bg_color="#35373a",
                                                   fg_color="GREEN", text="CLOSE APPLICATION")
        login_out_button.place(x=1150, y=650)


        self.fm3 = Frame(self.root, bg='#35373a', width=350, height=30)
        self.fm3.place(x=1000, y=50)

        def clock():
            h = str(time.strftime("%H"))
            m = str(time.strftime("%M"))
            s = str(time.strftime("%S"))

            if int(h) >= 12 and int(m) >= 0:
                self.lb7_hr.config(text="PM")

            self.lb1_hr.config(text=h)
            self.lb3_hr.config(text=m)
            self.lb5_hr.config(text=s)

            self.lb1_hr.after(200, clock)

        self.lb1_hr = Label(self.fm3, text='12', font=('times new roman', 20, 'bold'), bg='#fc1c1c', fg='white')
        self.lb1_hr.place(x=60, y=0, width=60, height=30)

        self.lb3_hr = Label(self.fm3, text='05', font=('times new roman', 20, 'bold'), bg='#0ee38b', fg='white')
        self.lb3_hr.place(x=130, y=0, width=60, height=30)

        self.lb5_hr = Label(self.fm3, text='37', font=('times new roman', 20, 'bold'), bg='#2b1dff', fg='white')
        self.lb5_hr.place(x=200, y=0, width=60, height=30)

        self.lb7_hr = Label(self.fm3, text='AM', font=('times new roman', 17, 'bold'), bg='black', fg='white')
        self.lb7_hr.place(x=280, y=0, width=60, height=30)

        clock()

        self.root.mainloop()


    def exit(self):
        self.root.destroy()

    def open_pharmacy_dashboard(self):
        self.login_pharmacy_button.destroy()
        self.login_patients_button.destroy()
        self.root.destroy()
        Loginadmin()

    def open_patients_dashboard(self):
        self.login_patients_button.destroy()
        self.login_pharmacy_button.destroy()
        self.root.destroy()
        # PatientsDashboard()
        Loginuser()


class Loginuser:
    def __init__(self):
        self.login = tk.Tk()
        self.login.title("login")
        self.login.geometry("1350x700")
        # self.login.resizable(False, False)

        customtkinter.set_appearance_mode("light")

        self.bgg = PhotoImage(
            file=r"pattern.png")
        lbl_bgg = Label(self.login, image=self.bgg)
        lbl_bgg.place(x=0, y=0, width=1350, height=700)

        frame_patient = customtkinter.CTkFrame(master=self.login,
                                               width=500,
                                               height=300,
                                               corner_radius=30)
        frame_patient.place(x=400, y=50)

        Label(frame_patient, fg='green', text="Login with user Password", font=("times", 17), bg="#d8dddd").place(x=150,
                                                                                                                  y=10)

        Label(frame_patient, text="Username:", fg="green", bg="#d8dddd", font=("times", 16)).place(x=50,
                                                                                                   y=100)
        Label(frame_patient, text="Password:", fg='green', bg="#d8dddd", font=("times", 16)).place(x=50,
                                                                                                   y=150)

        self.username = Entry(frame_patient, width=23)
        self.username.place(x=170, y=100)

        self.password = Entry(frame_patient, width=23, show="*")
        self.password.place(x=170, y=150)

        def login():

            # Execute a query to retrieve the username and password for the entered username
            cursor.execute("SELECT * FROM adm WHERE User_ID=?", (self.username.get(),))
            row = cursor.fetchone()

            # If a row is returned and the password matches, login is successful
            if row is not None and row[1] == self.password.get():
                self.login.destroy()
                PatientsDashboard()


            else:
                messagebox.showinfo("Incorrect username or password")
                Loginadmin(frame_patient)

        login_button = customtkinter.CTkButton(frame_patient, corner_radius=30, command=login, width=150, height=50,
                                               fg_color="green",
                                               text="Login")
        login_button.place(x=150, y=200)

        def log_out():
            self.login.destroy()
            WelcomeScreen()

        login_out_button = customtkinter.CTkButton(frame_patient, corner_radius=30, command=log_out, width=100,
                                                   height=50,
                                                   fg_color="red", text="EXIT")
        login_out_button.place(x=10, y=200)

        self.login.mainloop()


class Loginadmin:
    def __init__(self):
        self.login = tk.Tk()
        self.login.title("login")
        self.login.geometry("1350x700")
        # self.login.resizable(False, False)

        customtkinter.set_appearance_mode("light")

        self.bgg = PhotoImage(
            file=r"pattern.png")
        lbl_bgg = Label(self.login, image=self.bgg)
        lbl_bgg.place(x=0, y=0, width=1350, height=700)

        frame_patient = customtkinter.CTkFrame(master=self.login,
                                               width=500,
                                               height=300,
                                               corner_radius=30)
        frame_patient.place(x=400, y=50)

        Label(frame_patient, fg='green', text="ADMINISTRATOR", font=("times", 17), bg="#d8dddd").place(x=150, y=10)

        Label(frame_patient, text="Username:", fg="green", bg="#d8dddd", font=("times", 16)).place(x=50,
                                                                                                   y=100)
        Label(frame_patient, text="Password:", fg='green', bg="#d8dddd", font=("times", 16)).place(x=50,
                                                                                                   y=150)

        self.username = Entry(frame_patient, width=23)
        self.username.place(x=170, y=100)

        self.password = Entry(frame_patient, width=23, show="*")
        self.password.place(x=170, y=150)

        def login1():

            if self.username.get() == "" and self.password.get() == "":
                messagebox.showinfo("", "blank not allowed")
                Loginadmin(frame_patient)

            elif self.username.get() == "admin" and self.password.get() == "admin":
                Pharmacy(self.login)


            else:
                messagebox.showinfo("", "incorrect user name and password")
                Loginadmin(frame_patient)

        login_button = customtkinter.CTkButton(frame_patient, corner_radius=30, command=login1, width=150, height=50,
                                               fg_color="green",
                                               text="Login")
        login_button.place(x=150, y=200)

        def log_out():
            self.login.destroy()
            WelcomeScreen()

        login_out_button = customtkinter.CTkButton(frame_patient, corner_radius=30, command=log_out, width=100,
                                                   height=50,
                                                   fg_color="red", text="EXIT")
        login_out_button.place(x=10, y=200)

        self.login.mainloop()


class SlashScreen:
    def __init__(self):
        w = Tk()

        # Using piece of code from old splash screen
        width_of_window = 427
        height_of_window = 250
        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        # w.configure(bg='#ED1B76')
        w.overrideredirect(1)  # for hiding titlebar

        # new window to open
        def new_win():
            WelcomeScreen()

        Frame(w, width=560, height=250, bg='#272727').place(x=0, y=0)
        label1 = Label(w, text='Pharmarcy Management \n System', fg='white', bg='#272727')  # decorate it
        label1.configure(
            font=("Game Of Squids", 20, "bold"))  # You need to install this font in your PC or try another one
        label1.place(x=5, y=80)

        label2 = Label(w, text='Loading...', fg='white', bg='#272727')  # decorate it
        label2.configure(font=("Calibri", 11))
        label2.place(x=10, y=215)

        # making animation

        image_a = PhotoImage(file="c2.png")
        image_b = PhotoImage(file="c1.png")

        for i in range(5):  # 5loops
            l1 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
            l2 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            w.update_idletasks()
            time.sleep(0.189)

            l1 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
            l3 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            w.update_idletasks()
            time.sleep(0.189)

            l1 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
            l4 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            w.update_idletasks()
            time.sleep(0.189)

            l1 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
            w.update_idletasks()
            time.sleep(0.189)

        w.destroy()

        new_win()

        w.mainloop()


if __name__ == "__main__":
    welcome_screen = SlashScreen()
