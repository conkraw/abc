import streamlit as st
from docx import Document
import os

# Function to replace placeholders in the template
def create_word_doc(template_path, date, time):
    doc = Document(template_path)

    # Debug: Print the current paragraphs
    for paragraph in doc.paragraphs:
        st.write(f"Original paragraph: {paragraph.text}")

    # Replace placeholders in paragraphs
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if 'DatePlaceholder' in run.text:
                run.text = run.text.replace('DatePlaceholder', date)
            if 'TimePlaceholder' in run.text:
                run.text = run.text.replace('TimePlaceholder', time)

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

        # Debugging output
        st.write(f"Using template: {template_path}")
        st.write(f"Date entered: {date}")
        st.write(f"Time entered: {time}")

        try:
            doc_file = create_word_doc(template_path, date, time)
            st.success("Document created successfully!")
            
            with open(doc_file, 'rb') as f:
                st.download_button(
                    label="Download Word Document",
                    data=f,
                    file_name=doc_file,
                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
            os.remove(doc_file)  # Clean up the file after download
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill in all fields.")
