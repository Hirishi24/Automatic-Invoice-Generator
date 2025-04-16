# Automatic-Invoice-Generator
🧾 Automatic Invoice Generator using Python
A Python-based automation project that generates professional, GST-compliant PDF invoices based on product/item details entered via CSV or GUI. The invoices follow an Amazon-style layout with clean formatting, tax calculation, and disclaimers.

👨‍💻 Developed By
Akash Harsha S (AP23110011490)

Devi Sree H (AP23110011510)

📌 Project Description
This tool reads item-wise billing data from a CSV file (or GUI form), applies necessary calculations like quantity, discount, CGST + SGST (from tax rate), and then generates a formatted PDF invoice. The layout is inspired by Amazon’s GST invoice format.

🚀 Features
✅ Reads input from CSV file

✅ GUI Form (Tkinter) for easier data entry

✅ Calculates Discount, CGST, SGST, Subtotal, and Grand Total

✅ Outputs professional PDF invoice (with template)

✅ Adds invoice date, number, disclaimer, and business info

✅ Amazon-style layout with legal GST structure

✅ Footer disclaimer added only to Page 1

✅ QR code link to GitHub included in final slides

🧠 Technologies Used
Python 3.x

FPDF (for PDF generation)

CSV module

Tkinter (for GUI input form)

Matplotlib (for reference pie chart)

OS, subprocess, datetime modules

📂 File Structure
bash
Copy
Edit
├── invoice_data.csv             # Input data file
├── invoice_generator.py        # Main Python script for PDF generation
├── csv_entry_gui.py            # GUI to add invoice items to CSV
├── invoice_template.png        # Background image template for invoice (optional)
├── pie_chart_reference.png     # Resource pie chart (used in presentation)
├── README.md                   # This file
🖼 Sample Output
<p align="center"> <img src="path-to-screenshot.png" alt="Sample Invoice Output" width="600"> </p>
📚 References
Python Official Docs

FPDF Library Docs

Amazon Invoice Sample (format guide)

Stack Overflow

SlidesGo (presentation template)

🔮 Future Enhancements
Integrate database (SQLite/MySQL)

Add email functionality to send invoice

Export as desktop app (PyInstaller)

Include QR code for UPI payments

Store multiple invoice histories

📎 License
This project is for educational/demo purposes.

