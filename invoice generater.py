from fpdf import FPDF
from datetime import datetime
import os

class InvoiceGenerator:
    def __init__(self, customer_name, customer_address, items, tax_rate=0):
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.items = items
        self.tax_rate = tax_rate
        self.invoice_number = self.generate_invoice_number()
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_invoice_number(self):
        # Generate a unique invoice number using the current timestamp
        return f"INV-{int(datetime.now().timestamp())}"

    def calculate_total(self):
        # Calculate subtotal, tax, and grand total
        subtotal = sum(item['quantity'] * item['price'] for item in self.items)
        tax = subtotal * (self.tax_rate / 100)
        grand_total = subtotal + tax
        return subtotal, tax, grand_total

    def generate_invoice(self, filename="invoice.pdf"):
        # Create PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add header
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
        pdf.set_font("Arial", size=12)

        # Add invoice number and date
        pdf.cell(200, 10, txt=f"Invoice Number: {self.invoice_number}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {self.date}", ln=True)

        # Add customer details
        pdf.cell(200, 10, txt=f"Customer Name: {self.customer_name}", ln=True)
        pdf.cell(200, 10, txt=f"Customer Address: {self.customer_address}", ln=True)

        # Add items table
        pdf.cell(200, 10, txt="Items:", ln=True)
        pdf.cell(100, 10, txt="Description", border=1)
        pdf.cell(30, 10, txt="Quantity", border=1)
        pdf.cell(30, 10, txt="Price", border=1)
        pdf.cell(30, 10, txt="Total", border=1, ln=True)

        for item in self.items:
            pdf.cell(100, 10, txt=item['description'], border=1)
            pdf.cell(30, 10, txt=str(item['quantity']), border=1)
            pdf.cell(30, 10, txt=f"${item['price']:.2f}", border=1)
            pdf.cell(30, 10, txt=f"${item['quantity'] * item['price']:.2f}", border=1, ln=True)

        # Calculate totals
        subtotal, tax, grand_total = self.calculate_total()

        # Add totals to the PDF
        pdf.cell(200, 10, txt=f"Subtotal: ${subtotal:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Tax ({self.tax_rate}%): ${tax:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Grand Total: ${grand_total:.2f}", ln=True)

        # Save the PDF
        pdf.output(filename)
        print(f"Invoice saved as {filename}")

        # Open the PDF automatically
        self.open_pdf(filename)

    def open_pdf(self, filename):
        # Open the PDF file with the default viewer
        if os.name == "nt":  # For Windows
            os.startfile(filename)
        elif os.name == "posix":  # For macOS or Linux
            os.system(f"open {filename}" if sys.platform == "darwin" else f"xdg-open {filename}")
        else:
            print(f"Unable to open PDF automatically. Please open {filename} manually.")

# Function to get user input
def get_user_input():
    # Input customer details
    customer_name = input("Enter customer name: ")
    customer_address = input("Enter customer address: ")

    # Input items
    items = []
    while True:
        description = input("Enter product/service description (or type 'done' to finish): ")
        if description.lower() == "done":
            break
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per unit: "))
        items.append({"description": description, "quantity": quantity, "price": price})

    # Input tax rate
    tax_rate = float(input("Enter tax rate (in %): "))

    return customer_name, customer_address, items, tax_rate

# Main program
if __name__ == "__main__":
    # Get user input
    customer_name, customer_address, items, tax_rate = get_user_input()

    # Generate invoice
    invoice = InvoiceGenerator(customer_name, customer_address, items, tax_rate)
    invoice.generate_invoice("invoice.pdf")