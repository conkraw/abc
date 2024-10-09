import io
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject

st.title("PDF Form Filler")

# Text input for user
custom_text = st.text_input("Enter text to fill in PDF (e.g., '98%'):")
field_name = 'date'  # Change this to your desired text input field name

# File uploader
#uploaded_file = st.file_uploader("Upload airway_bundle.pdf", type=["pdf"])
uploaded_file = "https://raw.githubusercontent.com/conkraw/abc/main/airway_bundle.pdf"

# Submit button
if st.button("Submit"):
    if uploaded_file is not None and custom_text:
        # Load the PDF template
        reader = PdfReader(uploaded_file)
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
        st.warning("Please upload a PDF and enter the text.")

