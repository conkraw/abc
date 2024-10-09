import io
import requests
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject

st.title("PDF Form Filler")

# URL of the PDF file in your GitHub repository
pdf_url = "airway_bundle.pdf"

# Text input for user
custom_text = st.text_input("Enter text to fill in PDF (e.g., '98%'):")
field_name = 'date'  # Change this to your desired text input field name

# Submit button
if st.button("Submit"):
    if custom_text:
        # Load the PDF template from GitHub
        response = requests.get(pdf_url)
        pdf_content = io.BytesIO(response.content)
        
        reader = PdfReader(pdf_content)
        writer = PdfWriter()

        # Loop through all pages to fill the specified text field
        for page in reader.pages:
            if '/Annots' in page:
                annotations = page['/Annots']
                for annot in annotations:
                    annot_obj = annot.get_object()

                    # Check if the field name matches
                    if annot_obj.get('/T') == NameObject(field_name):
                        annot_obj.update({
                            NameObject('/V'): TextStringObject(custom_text)  # Set the value
                        })

            writer.add_page(page)  # Add the modified page to the writer

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
    else:
        st.warning("Please enter text to fill in the PDF.")

