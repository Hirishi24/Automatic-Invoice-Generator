from pdf2docx import Converter  # Correct import statement

# Define the input PDF and output DOCX file paths
pdf_file = "overcart.pdf"
docx_file = "overcart.docx"

# Create a Converter object
cv = Converter(pdf_file)  # Use 'Converter' (uppercase C)

# Convert the PDF to DOCX
cv.convert(docx_file, start=0, end=None)  # Use None instead of none

# Close the Converter object (not strictly necessary, but good practice)
cv.close()

print("Conversion completed!")