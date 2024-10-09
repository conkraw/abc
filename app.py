import streamlit as st
from docx import Document
import os

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

        # Check for checkbox and replace based on the selected option
        if option != "Select an option":
            # Look for the option in the paragraph
            if option in paragraph.text:
                # Split the paragraph text to find and replace the checkbox
                parts = paragraph.text.split(option)
                checkbox_index = paragraph.text.index(option) - 2  # Index of checkbox

                if paragraph.text[checkbox_index:checkbox_index + 2] == ' ':
                    st.write(f"Found checkbox for '{option}' in paragraph: {paragraph.text}")

                    # Create a new text for the checkbox with an "x"
                    new_checkbox = 'x'
                    # Rebuild the paragraph text
                    new_paragraph_text = parts[0][:checkbox_index] + new_checkbox + option + ''.join(parts[1:])
                    paragraph.clear()  # Clear existing runs
                    # Add the modified text back to the paragraph
                    paragraph.add_run(new_paragraph_text)

    # Save the modified document
    doc_file = 'airway_bundle_form.docx'
    doc.save(doc_file)
    return doc_file



# Streamlit app
st.title("Fill in Template Document")

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



