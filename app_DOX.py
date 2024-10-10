import streamlit as st
from docx import Document
import os

def create_word_doc(template_path, date, time, option, intubation_method):
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
            # Replace IntubationMethodPlaceholder with the selected intubation method
            if 'IntubationMethodPlaceholder' in run.text:
                run.text = run.text.replace('IntubationMethodPlaceholder', intubation_method)

    # Save the modified document
    doc_file = 'airway_bundle_form.docx'
    doc.save(doc_file)
    return doc_file

# Streamlit app
st.title("Fill in Template Document")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'date'

# Date input page
if st.session_state.page == 'date':
    date = st.text_input("Enter your date")
    
    if st.button("Next"):
        if date:
            st.session_state.date = date
            st.session_state.page = 'time'  # Navigate to time input page
        else:
            st.warning("Please enter a date.")

# Time input page
elif st.session_state.page == 'time':
    time = st.text_input("Enter your time")
    
    if st.button("Next"):
        if time:
            st.session_state.time = time
            st.session_state.page = 'option'  # Navigate to option selection page
        else:
            st.warning("Please enter a time.")

# Option selection page
elif st.session_state.page == 'option':
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
        if option != "Select an option":
            st.session_state.option = option
            st.session_state.page = 'intubation_method'  # Navigate to intubation method selection page
        else:
            st.warning("Please select an option.")

# Intubation method selection page
elif st.session_state.page == 'intubation_method':
    intubation_method = st.selectbox("Select an intubation method", [
        "Select a method",
        "Endotracheal tube",
        "Laryngeal mask airway",
        "Bougie",
        "Other"
    ])

    if st.button("Next"):
        if intubation_method != "Select a method":
            st.session_state.intubation_method = intubation_method
            st.session_state.page = 'download'  # Navigate to download page
        else:
            st.warning("Please select an intubation method.")

# Download page
elif st.session_state.page == 'download':
    # Path to your template file
    template_path = 'airway_bundlex.docx'  # Ensure this is the correct path

    # Debugging output
    st.write(f"Using template: {template_path}")
    st.write(f"Date entered: {st.session_state.date}")
    st.write(f"Time entered: {st.session_state.time}")
    st.write(f"Option selected: {st.session_state.option}")
    st.write(f"Intubation method selected: {st.session_state.intubation_method}")

    try:
        doc_file = create_word_doc(template_path, st.session_state.date, st.session_state.time, st.session_state.option, st.session_state.intubation_method)
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
        st.session_state.page = 'intubation_method'  # Navigate back to intubation method selection page

