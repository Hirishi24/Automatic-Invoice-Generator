import pywhatkit
from PIL import Image
from fpdf import FPDF
import os

# Define a function to create handwriting image from text
def text_to_handwriting_image(text, image_path, rgb=(0, 0, 255)):
    pywhatkit.text_to_handwriting(text, save_to=image_path, rgb=rgb)

# Define a function to convert an image to A4 PDF page
def image_to_a4_pdf(image_path, pdf, a4_width=595, a4_height=842):
    image = Image.open(image_path).convert("RGB")

    # Resize image to fit A4 with some padding
    image.thumbnail((a4_width - 40, a4_height - 40))
    bg = Image.new("RGB", (a4_width, a4_height), "white")
    x = (a4_width - image.width) // 2
    y = (a4_height - image.height) // 2
    bg.paste(image, (x, y))

    # Save temporary image
    temp_file = "a4_image_temp.jpg"
    bg.save(temp_file)

    # Add to PDF
    pdf.add_page()
    pdf.image(temp_file, x=0, y=0, w=a4_width, h=a4_height)
    os.remove(temp_file)

# Text from Page 1
page1_text = """
Name: H. Devisree
Reg. No.: AP2311001510
Sec: CSE – ‘X’
Subject: AEC

1) Briefly explain the concept of design thinking.

Design thinking is a human-centered approach to problem-solving that emphasizes empathy, creativity, and iterative reasoning. It is used to tackle complex problems by deeply understanding the people for whom we are designing solutions. The process encourages innovation by combining what is desirable from a human point of view with what is technologically feasible and economically viable.

The design thinking process consists of five key stages:
1) Empathize: The first step involves understanding the users and their needs through observation, interaction, and research. It helps designers gain insights into users' experiences and emotions.
2) Define: Based on the findings from the empathy phase, the problem is clearly articulated. A well-defined problem statement focuses on the users and provides direction for the next steps.
3) Ideate: Think of as many ideas as possible to solve the problem. No idea is too crazy — just be creative and open-minded.
4) Prototype: Make a simple version of your best idea. It doesn’t have to be perfect — just something to show how it might work.
5) Test: Try out your prototype with real users. See what works, what doesn’t, and use their feedback to make it better.
"""

# Text from Page 2
page2_text = """
2) Concept of Six Thinking Hats

The Six Thinking Hats technique, developed by Edward de Bono, is a powerful thinking framework used for group discussions and individual thinking. It helps individuals focus on one perspective at a time, reducing confusion and conflict and enabling better decision-making.

Each "hat" is a metaphor for a mode of thinking. The idea is that by "wearing" a hat, you adopt a specific role or mindset:

1. White Hat – Neutral and Objective
   - Focus: Facts, data, and information
   - Ask: What do we know? What do we need to find out?
   - Avoid emotions and assumptions

2. Red Hat – Emotions and Feelings
   - Focus: Intuition, gut feelings, and emotional reactions
   - No need to justify feelings
   - Encourages people to express emotions that might otherwise be hidden

3. Black Hat – Caution and Critical Thinking
   - Focus: Risks, dangers, and weaknesses in an idea
   - Asks: What could go wrong? What are the obstacles?

4. Yellow Hat – Optimism and Positivity
   - Focus: Benefits, feasibility, and value
   - Encourages a positive view even if the idea is new or unusual

5. Green Hat – Creativity and New Ideas
   - Focus: Alternatives, innovation, and possibilities
   - Encourages thinking outside the box

6. Blue Hat – Control and Process
   - Focus: Managing the thinking process
   - Organizes the use of other hats
   - Decides the order of hats and summarizes outcomes
"""

# Generate handwriting images
text_to_handwriting_image(page1_text, "page1.png")
text_to_handwriting_image(page2_text, "page2.png")

# Create PDF
pdf = FPDF(unit="pt", format="A4")
image_to_a4_pdf("page1.png", pdf)
image_to_a4_pdf("page2.png", pdf)
pdf.output("handwriting_output.pdf")
print("✅ PDF generated as handwriting_output.pdf")

# Clean up handwriting images
os.remove("page1.png")
os.remove("page2.png")
