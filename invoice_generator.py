from fpdf import FPDF
import qrcode
import csv
import os
import platform
import subprocess
from datetime import datetime
import pytz
from num2words import num2words

counter_file = "bill_counter.txt"

if not os.path.exists(counter_file):
    with open(counter_file, "w") as f:
        f.write("1")

with open(counter_file, "r") as f:
    bill_num = int(f.read().strip())

invoice_number = f"INV-{bill_num:04d}"
pdf_path = f"invoice_{invoice_number}.pdf"

with open(counter_file, "w") as f:
    f.write(str(bill_num + 1))

# === Step 2: Get Today's Date ===
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
invoice_date = now.strftime("%d-%b-%Y ")  # e.g. 14-Apr-2025 10:45 AM
issued_time = now.strftime("%I:%M %p IST")


# === Step 3: Define PDF Structure ===
class InvoicePDF(FPDF):
    def header(self):
        # Watermark-style logo (faded transparent logo.png)
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        self.image(logo_path, x=30, y=60, w=150)


        # Overlaid header text
        self.set_y(15)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, "Customer Invoice ", ln=True, align='C')
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, "DEVI SREE RETAIL PVT. LIMITED", ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, "BANGLORE, KARNATAKA", ln=True, align='C')
        self.cell(0, 5, "EST. 2013", ln=True, align='C')
        self.ln(5)

        # Invoice metadata
        self.set_font('Arial', '', 10)
        self.cell(0, 8, f"Invoice No.: {invoice_number}", ln=True)
        self.cell(0, 8, f"Invoice Date: {invoice_date}", ln=True)
        self.cell(0, 8, f"Issued At: {issued_time}", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15) 
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

# === Step 4: Create PDF ===
pdf = InvoicePDF()
pdf.add_page()
pdf.set_font("Arial", size=10)

# === Seller & Buyer Info ===
pdf.cell(0, 10, "Seller: Devi Sree Retail Private Limited", ln=True)
pdf.cell(0, 6, "GSTIN: 29ABCDE1234F2Z5", ln=True)
pdf.cell(0, 6, "Address: 1-2-3, MG Road, Bangalore, Karnataka - 560001", ln=True)
pdf.ln(5)
pdf.cell(0, 6, "Buyer: Akash Harsha Saladi", ln=True)
pdf.cell(0, 6, "Address: 45-12-34, Agraharam Street, Guntur, Andhra Pradesh - 522002", ln=True)
pdf.ln(5)

# === Table Headers ===
pdf.set_fill_color(200, 220, 255)
headers = ["Description", "HSN", "Qty", "Rate(RS)", "Disc%", "GST%", "Total(RS)"]
col_widths = [55, 20, 15, 25, 20, 20, 30]
for i in range(len(headers)):
    pdf.cell(col_widths[i], 8, headers[i], 1, 0, 'C', 1)
pdf.ln()

# === Read CSV and Fill Table ===
csv_path = os.path.join(os.path.dirname(__file__), "invoice_data.csv")
subtotal = 0

with open(csv_path, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            desc = row['Description']
            hsn = row['HSN Code']
            qty = int(row['Qty'])
            price = float(row['Unit Price'])
            disc = float(row['Discount (%)'])
            gst = float(row['Tax Rate (%)'])

            total_price = qty * price * (1 - disc / 100)
            gst_amount = total_price * gst / 100
            total = total_price + gst_amount
            subtotal += total

            values = [desc, hsn, str(qty), f"{price:.2f}", f"{disc:.0f}", f"{gst:.0f}", f"{total:.2f}"]
            for i in range(len(values)):
                pdf.cell(col_widths[i], 8, values[i], 1)
            pdf.ln()
        except Exception as e:
            print(f"Skipping row due to error: {e}")

# === Totals Section ===
pdf.ln(5)
pdf.set_font("Arial", 'B', 11)
pdf.cell(0, 10, f"Grand Total: Rs. {subtotal:.2f}", ln=True)

pdf.set_font("Arial", '', 10)
amount_words = num2words(subtotal, to='currency', lang='en_IN')
amount_words = amount_words.replace('euro', 'rupees').replace('cents', 'paise').title()
pdf.cell(0, 6, f"Amount in words: {amount_words}", ln=True)




# Generate dynamic UPI QR
upi_id = "devisreehonne@oksbi"
payee_name = "Devi Sree Retail Pvt. Ltd."
upi_uri = (
    f"upi://pay?pa={upi_id}&pn={payee_name.replace(' ', '%20')}"
    f"&am={subtotal:.2f}&cu=INR"
)

qr_img = qrcode.make(upi_uri)
qr_img_path = "payment_qr.png"
qr_img.save(qr_img_path)

# Insert QR code image in invoice
pdf.ln(10)
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "Scan to Pay:", ln=True)
pdf.image(qr_img_path, x=80, w=50)
pdf.set_font("Arial", '', 10)
pdf.ln(10)
pdf.cell(0, 6, f"UPI ID: {upi_id}", ln=True, align='C')


# === Step 5: Save PDF ===
pdf.output(pdf_path)

# === Step 6: Auto-open the PDF ===
if platform.system() == 'Windows':
    os.startfile(pdf_path)
elif platform.system() == 'Darwin':
    subprocess.run(['open', pdf_path])
else:
    subprocess.run(['xdg-open', pdf_path])


print(f"Invoice generated and opened: {pdf_path}")
