import io
import streamlit as st
import pdfrw
from datetime import datetime

st.title("PDF Form Filler")

# Date input
date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())
formatted_date = date.strftime("%m-%d-%Y")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # Load the PDF template
    template_pdf = pdfrw.PdfReader(uploaded_file)
    
    field_name = 'date'  # Field name in your PDF form

    # Fill in the date field
    for page in template_pdf.pages:
        annotations = page.get('/Annots', [])
        st.write("Type of annotations:", type(annotations))  # Debug line
        if annotations is not None:
            st.write("Annotations on this page:", annotations)  # Debug line
            for annotation in annotations:
                st.write("Annotation object:", annotation)  # Debug line
                if annotation.get('/T') == f'({field_name})':
                    annotation.update(pdfrw.PdfDict(V=f'{formatted_date}'))

    # Write to a bytes buffer
    output_pdf = io.BytesIO()
    pdfrw.PdfWriter().write(output_pdf, template_pdf)
    output_pdf.seek(0)

    # Download button
    st.download_button(
        label="Download Filled PDF",
        data=output_pdf,
        file_name="filled_form.pdf",
        mime="application/pdf"
    )

