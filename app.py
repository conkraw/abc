import io
import streamlit as st
import pdfrw
from datetime import datetime

# Streamlit app title
st.title("PDF Form Filler")

# Date input
date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())
formatted_date = date.strftime("%m-%d-%Y")  # Format the date

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # Load the PDF template
    template_pdf = pdfrw.PdfReader(uploaded_file)
    
    # Define the field name in your PDF form where the date should go
    field_name = 'date'  # Change this to the actual field name in your PDF

    # Fill in the date field
    for page in template_pdf.pages:
        annotations = page.get('/Annots', [])
        for annotation in annotations:
            # Check if the field name matches and update its value
            if annotation.get('/T') == f'({field_name})':
                annotation.update(pdfrw.PdfDict(V=f'{formatted_date}'))  # Fill in the date

    # Write to a bytes buffer
    output_pdf = io.BytesIO()
    pdfrw.PdfWriter().write(output_pdf, template_pdf)
    output_pdf.seek(0)

    # Allow the user to download the modified PDF
    st.download_button(
        label="Download Filled PDF",
        data=output_pdf,
        file_name="filled_form.pdf",
        mime="application/pdf"
    )
