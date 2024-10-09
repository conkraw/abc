import streamlit as st
from docx import Document
import os

# Function to replace placeholders in the template
def create_word_doc(template_path, date_input):
    doc = Document(template_path)
    
    for paragraph in doc.paragraphs:
        if '{{date}}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{{date}}', date_input)
    
    doc_file = 'airway_bundle_form.docx'
    doc.save(doc_file)
    return doc_file

# Streamlit app
st.title("Fill in Template Document")

# User input
date_input = st.text_input("Enter a date (e.g., 2024-10-09)")

if st.button("Submit"):
    if date_input:
        # Path to your template file
        template_path = 'airway_bundle.docx'  # Change this to the path of your template
        
        doc_file = create_word_doc(template_path, date_input)
        
        with open(doc_file, 'rb') as f:
            st.download_button(
                label="Download Word Document",
                data=f,
                file_name=doc_file,
                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        os.remove(doc_file)  # Clean up the file after download
    else:
        st.warning("Please enter a valid date.")
