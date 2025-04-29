from tkinter import *
from tkinter import ttk, messagebox
import csv
import os
import subprocess
import platform
import cv2
from pyzbar.pyzbar import decode
import winsound
import time



# Product catalog (ID → name, HSN, price, tax%)
products = {
    "101": ("HP Pavillion Laptop", "85044016", 60666, 18),
    "102": ("Wireless Mouse", "84716060", 400, 18),
    "103": ("Bluetooth Headphones", "85183000", 1500, 18),
    "104": ("Smartphone (128GB)", "85171200", 18000, 18),
    "105": ("USB-C Charger", "85044010", 850, 18),
    "106": ("LED Monitor 24-inch", "85285200", 8999, 18),
    "107": ("Canon Inkjet Printer", "84433210", 5799, 18),
    "108": ("Office Chair", "94033010", 4990, 18),
    "109": ("Steel Water Bottle 1L", "73239390", 499, 12),
    "110": ("Pendrive 64GB", "85235100", 749, 18),
    "111": ("External HDD 1TB", "84717020", 4399, 18),
    "112": ("Wireless Keyboard", "84716050", 1299, 18),
    "113": ("Laptop Bag 15.6 inch", "42021220", 999, 18),
    "114": ("Bluetooth Speaker", "85182100", 1799, 18),
    "115": ("Gaming Mousepad", "40169990", 399, 18),
    "116": ("LED Strip Light", "94051010", 599, 18),
    "117": ("Cleaning Cloth", "63071010", 199, 5),
    "118": ("Smartwatch AMOLED", "91021200", 3499, 18),
    "119": ("Wi-Fi Router", "85176290", 2699, 18),
    "120": ("Tripod Stand", "96200000", 799, 18),
    "121": ("Ring Light", "94051090", 1499, 18),
    "122": ("Table Lamp", "94052010", 899, 12),
    "123": ("HDMI Cable", "85444299", 299, 18),
    "124": ("Power Bank 10000mAh", "85076000", 1299, 18)
}

csv_file = r"C:\Users\akash\Hirishi Python\AutoInvoiceProject\invoice_data.csv"

# Write header if needed
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "HSN Code", "Qty", "Unit Price", "Discount (%)", "Tax Rate (%)"])

def save_to_csv():
    pid = entry_pid.get().strip()
    qty = entry_qty.get()
    discount = entry_discount.get()

    if pid not in products:
        messagebox.showerror("Invalid", f"Product ID {pid} not found.")
        return
    if not qty:
        messagebox.showerror("Missing", "Enter quantity.")
        return

    try:
        qty = int(qty)
        discount = float(discount) if discount else 0
    except:
        messagebox.showerror("Invalid", "Qty must be int. Discount must be %.")
        return

    name, hsn, price, tax = products[pid]
    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, hsn, qty, price, discount, tax])

    refresh_listbox()
    entry_pid.delete(0, END)
    entry_qty.delete(0, END)
    entry_discount.delete(0, END)

def generate_invoice():
    try:
        if platform.system() == 'Windows':
            subprocess.run(["python", "C:\\Users\\akash\\Hirishi Python\\AutoInvoiceProject\\invoice_generator.py"], check=True)
        else:
            subprocess.run(["python3", "invoice_generator.py"], check=True)
        messagebox.showinfo("Invoice", "Invoice generated!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_selected_row():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0] + 1
    with open(csv_file, newline='') as f:
        rows = list(csv.reader(f))
    if index < len(rows):
        del rows[index]
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        refresh_listbox()

def refresh_listbox():
    listbox.delete(0, END)
    try:
        with open(csv_file, newline='') as f:
            rows = list(csv.reader(f))[1:]
            for row in rows:
                listbox.insert(END, f"{row[0]} | Qty: {row[2]} | ₹{row[3]}")
    except:
        pass

import threading

def scan_thread():
    cap = cv2.VideoCapture(0)
    last_scan_time = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for code in decode(frame):
            pid = code.data.decode('utf-8').strip()
            now = time.time()
            last_time = last_scan_time.get(pid, 0)

            if pid in products and (now - last_time > 2):
                last_scan_time[pid] = now
                name, hsn, price, tax = products[pid]

                # Read existing rows
                with open(csv_file, newline='') as f:
                    rows = list(csv.reader(f))

                header = rows[0]
                data = rows[1:]
                updated = False

                # Try to update qty if product exists
                for row in data:
                    if row[0] == name:
                        row[2] = str(int(row[2]) + 1)  # increase Qty
                        updated = True
                        break

                if not updated:
                    data.append([name, hsn, 1, price, 0, tax])

                # Write back to CSV
                with open(csv_file, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)

                root.after(0, refresh_listbox)
                winsound.Beep(1000, 200)
                cv2.putText(frame, f"Added: {name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            elif pid not in products:
                cv2.putText(frame, "Unknown ID", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow("Scan Mode - Press Q to close", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_scan_mode():
    threading.Thread(target=scan_thread).start()



# GUI setup
root = Tk()
root.title("Devi Sree Retail - Invoice GUI")
root.geometry("500x550")

Label(root, text="Product ID (e.g. 101):").pack()
entry_pid = Entry(root, width=20)
entry_pid.pack()

Label(root, text="Quantity:").pack()
entry_qty = Entry(root, width=20)
entry_qty.pack()

Label(root, text="Discount (%):").pack()
entry_discount = Entry(root, width=20)
entry_discount.pack()

Button(root, text="Add Item", command=save_to_csv).pack(pady=8)
Button(root, text=" Generate Invoice", command=generate_invoice, bg="green", fg="white").pack(pady=4)
Button(root, text=" Scan Mode (Camera)", command=start_scan_mode, bg="blue", fg="white").pack(pady=4)

Label(root, text="Invoice Items:").pack(pady=(15, 2))
listbox = Listbox(root, width=60, height=10)
listbox.pack()

Button(root, text="🗑 Delete Selected", command=delete_selected_row, bg="red", fg="white").pack(pady=5)

refresh_listbox()
root.mainloop()
