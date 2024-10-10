import streamlit as st
from docx import Document
import os

def create_word_doc(template_path, date, time, option):
    # Load the Word document template
    doc = Document(template_path)

    # Check and replace text in paragraphs
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            # Replace Date and Time Placeholders
            if 'DatePlaceholder' in run.text:
                run.text = run.text.replace('DatePlaceholder', date)
            if 'TimePlaceholder' in run.text:
                run.text = run.text.replace('TimePlaceholder', time)
            # Replace FrontPagePlaceholder with the selected option
            if 'FrontPagePlaceholder' in run.text:
                run.text = run.text.replace('FrontPagePlaceholder', option)

    # Save the modified document
    doc_file = 'airway_bundle_form.docx'
    doc.save(doc_file)
    return doc_file

# Streamlit app
st.title("Fill in Template Document")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'input'

# Input page
if st.session_state.page == 'input':
    # User inputs
    date = st.text_input("Enter your date")
    time = st.text_input("Enter your time")
    option = st.selectbox("Select an option", [
        "Select an option", 
        "On admission", 
        "During rounds", 
        "After Rounds", 
        "Just prior to intubation", 
        "After intubation", 
        "Prior to Extubation"
    ])

    if st.button("Next"):
        if date and time and option != "Select an option":
            # Store user input in session state
            st.session_state.date = date
            st.session_state.time = time
            st.session_state.option = option
            st.session_state.page = 'download'  # Navigate to download page
        else:
            st.warning("Please fill in all fields and select an option.")

# Download page
elif st.session_state.page == 'download':
    # Path to your template file
    template_path = 'airway_bundlex.docx'  # Ensure this is the correct path

    # Debugging output
    st.write(f"Using template: {template_path}")
    st.write(f"Date entered: {st.session_state.date}")
    st.write(f"Time entered: {st.session_state.time}")
    st.write(f"Option selected: {st.session_state.option}")

    try:
        doc_file = create_word_doc(template_path, st.session_state.date, st.session_state.time, st.session_state.option)
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

    if st.button("Go Back"):
        st.session_state.page = 'input'  # Navigate back to input page


