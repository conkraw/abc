import streamlit as st
from docx import Document
from lxml import etree
import os

# Function to replace placeholders in the template
from docx import Document
from lxml import etree

# Inside your create_word_doc function
def create_word_doc(template_path, date, time):
    doc = Document(template_path)

    # Define the namespace
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Check and replace text in paragraphs
    st.write("Checking paragraphs:")
    for paragraph in doc.paragraphs:
        st.write(f"Paragraph: {paragraph.text}")
        for run in paragraph.runs:
            if 'DatePlaceholder' in run.text:
                st.write(f"Found 'DatePlaceholder' in paragraph: {run.text}")
                run.text = run.text.replace('DatePlaceholder', date)
            if 'TimePlaceholder' in run.text:
                st.write(f"Found 'TimePlaceholder' in paragraph: {run.text}")
                run.text = run.text.replace('TimePlaceholder', time)

    # Check and replace text in content controls
    st.write("Checking content controls:")
    xml = doc.element.xml
    root = etree.fromstring(xml)

    sdt_elements = root.xpath('//w:sdt', namespaces=namespace)
    st.write("Number of content controls found:", len(sdt_elements))

    for sdt in sdt_elements:
        # Print the entire sdt element for debugging
        st.write("Content Control XML:", etree.tostring(sdt, pretty_print=True).decode())
    
        # Attempt to get the title of the content control
        title = sdt.find('.//w:sdtPr/w:title', namespaces=namespace)
        title_text = title.text if title is not None else "No Title"
        st.write(f"Content control title: '{title_text}'")  # Debug output
    
        sdt_content = sdt.find('.//w:sdtContent', namespaces=namespace)
        if sdt_content is not None:
            for text in sdt_content.xpath('.//w:t', namespaces=namespace):
                st.write(f"Content control text: '{text.text}'")  # Debug output
    
                # Replace based on the content control title
                if title_text == "DateControl":  # Adjust title as needed
                    st.write(f"Replacing in DateControl: '{text.text}'")
                    text.text = date  # Replace with date
                elif title_text == "TimeControl":  # Adjust title as needed
                    st.write(f"Replacing in TimeControl: '{text.text}'")
                    text.text = time  # Replace with time


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
        template_path = 'airway_bundlex.docx'  # Ensure this is the correct path

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
