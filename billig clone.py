from tkinter import *
import random
import os
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime

# ============main============================
class Bill_App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Automatic Invoice Generator")
        bg_color = "#badc57"
        title = Label(self.root, text="Automatic Invoice Generator", font=('times new roman', 30, 'bold'), pady=2, bd=12, bg="#badc57", fg="Black", relief=GROOVE)
        title.pack(fill=X)
        
        # ================variables=======================
        self.items = []
        self.total_price = 0
        self.tax_rate = 0.05  # 5% tax rate
        
        # ==============Customer==========================
        self.c_name = StringVar()
        self.c_phone = StringVar()
        self.bill_no = StringVar()
        x = random.randint(1000, 9999)
        self.bill_no.set(str(x))
        self.search_bill = StringVar()
        
        # =============customer retail details======================
        F1 = LabelFrame(self.root, text="Customer Details", font=('times new roman', 15, 'bold'), bd=10, fg="Black", bg="#badc57")
        F1.place(x=0, y=80, relwidth=1)
        
        cname_lbl = Label(F1, text="Customer Name:", bg=bg_color, font=('times new roman', 15, 'bold'))
        cname_lbl.grid(row=0, column=0, padx=20, pady=5)
        cname_txt = Entry(F1, width=15, textvariable=self.c_name, font='arial 15', bd=7, relief=GROOVE)
        cname_txt.grid(row=0, column=1, pady=5, padx=10)
        
        cphn_lbl = Label(F1, text="Customer Phone:", bg="#badc57", font=('times new roman', 15, 'bold'))
        cphn_lbl.grid(row=0, column=2, padx=20, pady=5)
        cphn_txt = Entry(F1, width=15, textvariable=self.c_phone, font='arial 15', bd=7, relief=GROOVE)
        cphn_txt.grid(row=0, column=3, pady=5, padx=10)
        
        c_bill_lbl = Label(F1, text="Bill Number:", bg="#badc57", font=('times new roman', 15, 'bold'))
        c_bill_lbl.grid(row=0, column=4, padx=20, pady=5)
        c_bill_txt = Entry(F1, width=15, textvariable=self.search_bill, font='arial 15', bd=7, relief=GROOVE)
        c_bill_txt.grid(row=0, column=5, pady=5, padx=10)
        
        bil_btn = Button(F1, text="Search", command=self.find_bill, width=10, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        bil_btn.grid(row=0, column=6, pady=5, padx=10)
        
        # ===================Dynamic Items====================================
        F2 = LabelFrame(self.root, text="Add Items", font=('times new roman', 15, 'bold'), bd=10, fg="Black", bg="#badc57")
        F2.place(x=5, y=180, width=325, height=380)
        
        item_name_lbl = Label(F2, text="Item Name", font=('times new roman', 16, 'bold'), bg="#badc57", fg="black")
        item_name_lbl.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.item_name_txt = Entry(F2, width=10, font=('times new roman', 16, 'bold'), bd=5, relief=GROOVE)
        self.item_name_txt.grid(row=0, column=1, padx=10, pady=10)
        
        item_price_lbl = Label(F2, text="Price", font=('times new roman', 16, 'bold'), bg="#badc57", fg="black")
        item_price_lbl.grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.item_price_txt = Entry(F2, width=10, font=('times new roman', 16, 'bold'), bd=5, relief=GROOVE)
        self.item_price_txt.grid(row=1, column=1, padx=10, pady=10)
        
        item_qty_lbl = Label(F2, text="Quantity", font=('times new roman', 16, 'bold'), bg="#badc57", fg="black")
        item_qty_lbl.grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.item_qty_txt = Entry(F2, width=10, font=('times new roman', 16, 'bold'), bd=5, relief=GROOVE)
        self.item_qty_txt.grid(row=2, column=1, padx=10, pady=10)
        
        add_item_btn = Button(F2, text="Add Item", command=self.add_item, width=10, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        add_item_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # =================BillArea======================
        F5 = Frame(self.root, bd=10, relief=GROOVE)
        F5.place(x=1010, y=180, width=350, height=380)
        
        bill_title = Label(F5, text="Bill Area", font='arial 15 bold', bd=7, relief=GROOVE)
        bill_title.pack(fill=X)
        scroll_y = Scrollbar(F5, orient=VERTICAL)
        self.txtarea = Text(F5, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)
        
        # =======================ButtonFrame=============
        F6 = LabelFrame(self.root, text="Bill Area", font=('times new roman', 14, 'bold'), bd=10, fg="Black", bg="#badc57")
        F6.place(x=0, y=560, relwidth=1, height=140)
        
        total_btn = Button(F6, command=self.total, text="Total", bg="#535C68", bd=2, fg="white", pady=15, width=12, font='arial 13 bold')
        total_btn.grid(row=0, column=0, padx=5, pady=5)
        
        generateBill_btn = Button(F6, command=self.bill_area, text="Generate Bill", bd=2, bg="#535C68", fg="white", pady=12, width=12, font='arial 13 bold')
        generateBill_btn.grid(row=0, column=1, padx=5, pady=5)
        
        clear_btn = Button(F6, command=self.clear_data, text="Clear", bg="#535C68", bd=2, fg="white", pady=15, width=12, font='arial 13 bold')
        clear_btn.grid(row=0, column=2, padx=5, pady=5)
        
        exit_btn = Button(F6, command=self.exit_app, text="Exit", bd=2, bg="#535C68", fg="white", pady=15, width=12, font='arial 13 bold')
        exit_btn.grid(row=0, column=3, padx=5, pady=5)
        
        self.welcome_bill()
    
    # ===============Add Item==============================
    def add_item(self):
        item_name = self.item_name_txt.get()
        item_price = self.item_price_txt.get()
        item_qty = self.item_qty_txt.get()
        
        if item_name and item_price and item_qty:
            try:
                item_price = float(item_price)
                item_qty = int(item_qty)
                self.items.append((item_name, item_price, item_qty))
                self.total_price += item_price * item_qty
                self.item_name_txt.delete(0, END)
                self.item_price_txt.delete(0, END)
                self.item_qty_txt.delete(0, END)
                messagebox.showinfo("Success", "Item added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid price or quantity")
        else:
            messagebox.showerror("Error", "All fields are required")
    
    # ===============Total Calculation==============================
   # ===============Total Calculation==============================
def total(self):
    self.total_price_with_tax = self.total_price + (self.total_price * self.tax_rate)
    messagebox.showinfo("Total", f"Total Amount (including tax): Rs. {self.total_price_with_tax:.2f}")

# ===============Welcome Bill==============================
def welcome_bill(self):
    self.txtarea.delete('1.0', END)
    self.txtarea.insert(END, "\tWelcome Webcode Retail\n")
    self.txtarea.insert(END, f"\n Bill Number: {self.bill_no.get()}")
    self.txtarea.insert(END, f"\n Customer Name: {self.c_name.get()}")
    self.txtarea.insert(END, f"\n Phone Number: {self.c_phone.get()}")
    self.txtarea.insert(END, f"\n================================")
    self.txtarea.insert(END, f"\n Products\t\tQTY\t\tPrice")

# ===============Bill Area==============================
def bill_area(self):
    if not self.items:
        messagebox.showerror("Error", "No items added")
        return
    
    self.welcome_bill()
    
    for item in self.items:
        self.txtarea.insert(END, f"\n {item[0]}\t\t{item[2]}\t\tRs. {item[1] * item[2]:.2f}")
    
    self.txtarea.insert(END, f"\n--------------------------------")
    self.txtarea.insert(END, f"\n Total Amount:\t\t\tRs. {self.total_price:.2f}")
    tax_amount = self.total_price * self.tax_rate
    self.txtarea.insert(END, f"\n Tax (5%):\t\t\tRs. {tax_amount:.2f}")
    self.txtarea.insert(END, f"\n Total Amount (including tax):\t\t\tRs. {self.total_price_with_tax:.2f}")
    self.txtarea.insert(END, f"\n--------------------------------")
    
    self.save_bill()

# ===============Save Bill==============================
def save_bill(self):
    op = messagebox.askyesno("Save Bill", "Do you want to save the bill?")
    if op > 0:
        bill_data = self.txtarea.get('1.0', END)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
        pdf.cell(200, 10, txt=bill_data, ln=True, align='L')
        pdf.output(f"bills/{self.bill_no.get()}.pdf")
        messagebox.showinfo("Saved", f"Bill no: {self.bill_no.get()} Saved Successfully")
    else:
        return

# ===============Clear Data==============================
def clear_data(self):
    op = messagebox.askyesno("Clear", "Do you really want to clear?")
    if op > 0:
        self.items = []
        self.total_price = 0
        self.c_name.set("")
        self.c_phone.set("")
        self.bill_no.set("")
        x = random.randint(1000, 9999)
        self.bill_no.set(str(x))
        self.search_bill.set("")
        self.item_name_txt.delete(0, END)
        self.item_price_txt.delete(0, END)
        self.item_qty_txt.delete(0, END)
        self.welcome_bill()

# ===============Exit App==============================
def exit_app(self):
    op = messagebox.askyesno("Exit", "Do you really want to exit?")
    if op > 0:
        self.root.destroy()
        root = Tk()
        obj = Bill_App(root)
        root.mainloop()
