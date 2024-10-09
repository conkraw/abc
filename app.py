import io
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject

st.title("PDF Form Filler")

# Text input for user
custom_text = st.text_input("Enter text to fill in PDF (e.g., '98%'):")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # Load the PDF template
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()

    # Debugging: Print out all annotation names and their details
    for page in reader.pages:
        if '/Annots' in page:
            annotations = page['/Annots']
            for annot in annotations:
                annot_obj = annot.get_object()
                st.write(f"Annotation object: {annot_obj}")  # Print the annotation object
                st.write(f"Field name: {annot_obj.get('/T')}")  # Print the field name

    if custom_text:
        field_name = 'spo2'  # Change this to your desired text input field name

        # Loop through all pages to fill the specified text field
        for page in reader.pages:
            writer.add_page(page)  # Add the page to the writer
            if '/Annots' in page:
                annotations = page['/Annots']
                for annot in annotations:
                    annot_obj = annot.get_object()
                    
                    # Check if the field name matches
                    if annot_obj.get('/T') == NameObject(field_name):
                        annot_obj.update({
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

