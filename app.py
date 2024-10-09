import io
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter

st.title("PDF Form Filler")

# Text input for user
custom_text = st.text_input("Enter text to fill in PDF:")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # Load the PDF template
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()

    field_name = 'textFieldName'  # Change this to your PDF's text input field name

    # Loop through all pages to fill the specified text field
    for page in reader.pages:
        writer.add_page(page)  # Add the page to the writer
        if '/Annots' in page:
            for annot in page['/Annots']:
                if annot.get('/T') == f'({field_name})':
                    annot.update({
                        NameObject('/V'): TextStringObject(custom_text)  # Set the value
                    })

    # Write to a bytes buffer
    output_pdf = io.BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)

    # Download button
    st.download_button(
        label="Download Filled PDF",
        data=output_pdf,
        file_name="filled_form.pdf",
        mime="application/pdf"
    )


