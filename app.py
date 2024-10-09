import streamlit as st
from docx import Document
import os

# Function to replace placeholders in the template
def create_word_doc(template_path, date, time, option):
    doc = Document(template_path)

    # Check and replace text in paragraphs
    st.write("Checking paragraphs:")
    for paragraph in doc.paragraphs:
        st.write(f"Paragraph: {paragraph.text}")
        
        # Replace Date and Time Placeholders
        for run in paragraph.runs:
            if 'DatePlaceholder' in run.text:
                run.text = run.text.replace('DatePlaceholder', date)
            if 'TimePlaceholder' in run.text:
                run.text = run.text.replace('TimePlaceholder', time)
        
        # Check for checkbox replacement
        if option == "On Admission":
            if '' in paragraph.text:  # Assuming this is the checkbox character
                st.write(f"Found checkbox in paragraph: {paragraph.text}")
                paragraph.text = paragraph.text.replace('', ' x')  # Replace with checked box


    # Check and replace text in inline shapes (text boxes)
    st.write("Checking inline shapes (text boxes):")
    for shape in doc.inline_shapes:
        if shape.type == 1:  # Text box
            shape_text = shape.text
            st.write(f"Inline shape text: {shape_text}")
            if 'DatePlaceholder' in shape_text:
                st.write(f"Found 'DatePlaceholder' in shape: {shape_text}")
                shape.text = shape_text.replace('DatePlaceholder', date)
            if 'TimePlaceholder' in shape_text:
                st.write(f"Found 'TimePlaceholder' in shape: {shape_text}")
                shape.text = shape_text.replace('TimePlaceholder', time)

    # Save the modified document
    doc_file = 'airway_bundle_form.docx'
    doc.save(doc_file)
    return doc_file

# Streamlit app
st.title("Fill in Template Document")

# User inputs
date = st.text_input("Enter your date")
time = st.text_input("Enter your time")
option = st.selectbox("Select an option", ["Select an option", "On Admission", "During Rounds", "After Rounds", "Just Prior to Intubation", "After Intubation", "Prior to Extubation"])

if st.button("Submit"):
    if date and time and option != "Select an option":
        # Path to your template file
        template_path = 'airway_bundlex.docx'  # Ensure this is the correct path

        # Debugging output
        st.write(f"Using template: {template_path}")
        st.write(f"Date entered: {date}")
        st.write(f"Time entered: {time}")
        st.write(f"Selected option: {option}")

        try:
            doc_file = create_word_doc(template_path, date, time, option)
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



