
from fpdf import FPDF
from datetime import datetime
import os

class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        current_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.cell(0, 10, f'Generated: {current_date}  |  Page {self.page_no()}', 0, 0, 'R')

def fabric_summary(data):
    fabric_data = {}
    for item in data:
        fabric_id = item[10]
        achieved_length_m = item[6]
        if isinstance(achieved_length_m, float):
            fabric_data[fabric_id] = fabric_data.get(fabric_id, 0) + achieved_length_m
    for fabric_id in fabric_data:
        fabric_data[fabric_id] = round(fabric_data[fabric_id], 1)
    return fabric_data

def customer_order_summary(data):
    customer_order_data = {}
    for item in data:
        customer_order_id = item[11]
        qty = item[12]
        customer_order_data[customer_order_id] = customer_order_data.get(customer_order_id, 0) + qty
    for customer_order_id in customer_order_data:
        customer_order_data[customer_order_id] = round(customer_order_data[customer_order_id], 1)
    return customer_order_data

def generate_summary_page(pdf, data):
    # Implementation for generating the summary page
    pass

def generate_report_pdf(data, summary_only=True):
    pdf = CustomPDF(format=(210, 297))
    pdf.core_fonts_encoding = 'UTF-8'
    pdf.add_page(orientation='P')
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVuBold', '', 'DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.add_font('DejaVuCond', '', 'DejaVuSansCondensed.ttf', uni=True)

    # Implementation for generating the PDF content

    filename = f"{data[0][0]}.pdf"
    output_dir = 'temp'
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)
    return filepath
