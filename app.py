import streamlit as st
from docx import Document
import os

# Function to replace placeholders in the template
def create_word_doc(template_path, date, time):
    doc = Document(template_path)

    # Replace placeholders in paragraphs
    for paragraph in doc.paragraphs:
        if 'DatePlaceholder' in paragraph.text:
            paragraph.text = paragraph.text.replace('DatePlaceholder', date)
        if 'TimePlaceholder' in paragraph.text:
            paragraph.text = paragraph.text.replace('TimePlaceholder', time)

    # Save the modified document
    doc_file = 'airway_bundle_form.docx'
    doc.save(doc_file)
    return doc_file

# Streamlit app
st.title("Fill in Template Document")

# User inputs
date = st.text_input("Enter your date")
time = st.text_input("Enter your time")

if st.button("Submit"):
    if date and time:
        # Path to your template file
        template_path = 'airway_bundle.docx'  # Ensure this is the correct path
        
        doc_file = create_word_doc(template_path, date, time)
        
        with open(doc_file, 'rb') as f:
            st.download_button(
                label="Download Word Document",
                data=f,
                file_name=doc_file,
                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        os.remove(doc_file)  # Clean up the file after download
    else:
        st.warning("Please fill in all fields.")
