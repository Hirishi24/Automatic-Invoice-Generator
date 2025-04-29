import cv2
from pyzbar.pyzbar import decode
import csv
import os

# Product ID catalog
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

# Create CSV if not present
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "HSN Code", "Qty", "Unit Price", "Discount (%)", "Tax Rate (%)"])

print("Starting webcam scanner... (Press 'q' to quit)")
cap = cv2.VideoCapture(1)

while True:
    success, frame = cap.read()
    if not success:
        break

    for barcode in decode(frame):
        pid = barcode.data.decode('utf-8').strip()
        x, y, w, h = barcode.rect

        if pid in products:
            name, hsn, price, tax = products[pid]
            cv2.putText(frame, f" Added: {name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Write to CSV (Qty = 1, Discount = 0)
            with open(csv_file, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, hsn, 1, price, 0, tax])
        else:
            cv2.putText(frame, f" Unknown Product: {pid}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Draw rectangle around barcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

    cv2.imshow("Barcode Scanner", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
