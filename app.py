import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime

# Function to fill the Word template with form inputs
def fill_word_template(template_path, data):
    doc = Document(template_path)

    # Replace placeholders in the document with form data
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if f'{{{{{key}}}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{{{key}}}}}', str(value))

    # Save the updated document in memory
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer

# Function to determine ETT size based on age and unit
def calculate_ett_size(age, age_unit):
    if age_unit == "Days":
        return '3.0' if age <= 30 else '3.5'
    elif age_unit == "Weeks":
        if age <= 6:
            return '3.5'
        elif age <= 104:  # Up to 2 years
            return '4.0'
        else:
            return '6.0'  # Above 2 years (cuffed)
    elif age_unit == "Months":
        if age <= 12:
            return '4.0'
        elif age <= 24:
            return '4.5'
        elif age <= 36:
            return '5.0'
        else:
            return '5.5'  # For ages greater than 36 months
    elif age_unit == "Years":
        if age <= 2:
            return '4.5'
        elif age <= 10:
            return '5.0'
        else:
            return '6.0'
    return ''  # Default if no valid input

# Function to validate if the input is a valid integer or decimal number
def validate_weight(weight_str):
    try:
        # Check if it's a valid float number or integer
        if weight_str:
            float(weight_str)  # Check if the value is a number (float or int)
            return True
        else:
            return False
    except ValueError:
        return False

# Streamlit form for the Airway Bundle Checklist
st.title("Airway Bundle Checklist")

# Function to create a boxed section
def box_section(title):
    return f"""
    <div style="border: 1px solid #0072B8; border-radius: 5px; padding: 10px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #0072B8;">{title}</h4>
    </div>
    """

# Create a form
with st.form("airway_form"):
    # Front Page Section
    st.markdown(box_section("Front Page Completed"), unsafe_allow_html=True)
    front_page_completed = st.checkbox("On admission")
    during_rounds = st.checkbox("During rounds")
    after_rounds = st.checkbox("After rounds")
    just_prior_intubation = st.checkbox("Just prior to intubation")
    after_intubation = st.checkbox("After intubation")
    prior_to_extubation = st.checkbox("Prior to extubation")

    # Person who completed the form
    completed_by = st.text_input("Who completed the form? (Name or Role)")

    # Patient Information
    st.markdown(box_section("Patient Information"), unsafe_allow_html=True)
    
    cols = st.columns(2)

    with cols[0]:
        date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())
        
        # Replace number input with dropdown for age
        age_options = [
            "Premature", "Newborn", "1 month old", "2 month old", "3 month old", "4 month old", "5 month old", 
            "6 month old", "7 month old", "8 month old", "9 month old", "10 month old", "11 month old", 
            "12 month old", "1 year old", "2 year old", "3 year old", "4 year old", "5 year old", 
            "6 year old", "7 year old", "8 year old", "9 year old", "10 year old", "11 year old", 
            "12 year old", "13 year old", "14 year old", "15 year old", "16 year old", "17 year old", 
            "18 year old"
        ]
        age = st.selectbox("Select Patient Age", age_options)
        

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())
        
        # Weight input with text input validation
        weight_str = st.text_input("Enter Patient Weight (Kilograms)", value="")
        
        # Validate the weight input
        if weight_str and not validate_weight(weight_str):
            st.error("Please enter a valid number for the weight (e.g., 12.5 or 12).")

    # Initialize ETT Type based on age
    if 'ett_type' not in st.session_state:
        st.session_state.ett_type = ""

    # Extract age in months or years for ETT size calculation
    age_value, age_unit = "", ""
    if age:
        if "month" in age:
            age_value = int(age.split()[0])
            age_unit = "Months"
        elif "year" in age:
            age_value = int(age.split()[0])
            age_unit = "Years"
        elif age == "Premature":
            age_value = 0
            age_unit = "Days"
        elif age == "Newborn":
            age_value = 0
            age_unit = "Days"

    # Change ETT Type based on age input
    if age_value > 0 and (age_unit in ["Months", "Years"] or (age_unit == "Days" and age_value > 30)):
        st.session_state.ett_type = "Cuffed"
    else:
        st.session_state.ett_type = "Uncuffed"

    # Calculate ETT Size based on age and unit
    ett_size = ""
    if age_value > 0:
        ett_size = calculate_ett_size(age_value, age_unit)

    # Intubation plan section
    st.markdown(box_section("Intubation Plan"), unsafe_allow_html=True)

    # Multi-select for "Who will intubate?" and "Who will bag-mask?"
    who_intubate = st.multiselect("Who will intubate?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other'])

    who_bag_mask = st.multiselect("Who will bag-mask?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'RT', 'Other'])

    # Create a layout for intubation method
    intubation_method = st.selectbox("How will we intubate? (Method)", ["Oral", "Nasal"])

    # Create a layout for ETT Type and ETT Size
    cols = st.columns(2)

    with cols[0]:
        ett_type = st.selectbox("ETT Type", ["", "Cuffed", "Uncuffed"], index=["", "Cuffed", "Uncuffed"].index(st.session_state.ett_type))

    with cols[1]:
        # ETT Size Selection
        ett_options = ['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0']
        
        # Set index to 0 for blank or find the index of calculated size if applicable
        default_index = 0 if ett_size == "" else ett_options.index(ett_size)
        ett_size = st.selectbox("ETT Size", ett_options, index=default_index)

    # Timing of Intubation section
    st.markdown(box_section("Timing of Intubation"), unsafe_allow_html=True)
    intubation_timing = st.text_input("Describe timing of airway management")

    # Submit button
    submit = st.form_submit_button("Submit")

    # Process submission
    if submit:
        # Store form data into a dictionary to replace placeholders
        form_data = {
            "date": date,
            "time": time,
            "weight": weight_str,  # Save the weight as the string (allowing decimal numbers if entered)
            "age": age,
            "ett_type": st.session_state.ett_type,
            "who_intubate": ", ".join(who_intubate),
            "who_bag_mask": ", ".join(who_bag_mask),
            "ett_size": ett_size,
            "intubation_timing": intubation_timing,
            "front_page_completed": ", ".join([k for k, v in {"On admission": front_page_completed, "During rounds": during_rounds, "After rounds": after_rounds, "Just prior to intubation": just_prior_intubation, "After intubation": after_intubation, "Prior to extubation": prior_to_extubation}.items() if v]),
            "completed_by": completed_by
        }
        
        # Path to the provided Word template
        template_path = 'AirwayBundleChecklist_7-2020.docx'

        # Fill the Word template with form data
        filled_doc = fill_word_template(template_path, form_data)
        
        # Provide download link for the filled Word document
        st.success("Form submitted successfully!")
        st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")


