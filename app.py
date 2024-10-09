import io
import streamlit as st
import pdfrw
from datetime import datetime

# Streamlit app title
st.title("PDF Form Filler")

# Date input
date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())
formatted_date = date.strftime("%m-%d-%Y")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # Load the PDF template
    template_pdf = pdfrw.PdfReader(uploaded_file)
    
    # Define the field name in your PDF form where the date should go
    field_name = 'date'  # Adjust to the actual field name in your PDF

    # Fill in the date field
    for page in template_pdf.pages:
        annotations = page.get('/Annots', [])
        st.write("Annotations on this page:", annotations)  # Debug line
        if annotations:
            for annotation in annotations:
                st.write("Annotation object:", annotation)  # Debug line
                if annotation.get('/T') == f'({field_name})':
                    annotation.update(pdfrw.PdfDict(V=f'{formatted_date}'))

    # Write to a bytes buffer
    output_pdf = io.BytesIO()
    pdfrw.PdfWriter().
