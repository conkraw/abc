import io
import streamlit as st
import pdfrw

st.title("PDF Form Filler")

# Text input for user
custom_text = st.text_input("Enter text to fill in PDF:")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # Load the PDF template
    template_pdf = pdfrw.PdfReader(uploaded_file)
    
    field_name = 'textFieldName'  # Change this to your PDF's text input field name

    # Fill in the specified text field
    for page in template_pdf.pages:
        annotations = page.get('/Annots', [])
        if annotations:
            for annotation in annotations:
                # Check if the annotation is a text field
                if annotation.get('/T') == f'({field_name})':
                    annotation.update(pdfrw.PdfDict(V=f'{custom_text}'))  # Set the value

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

