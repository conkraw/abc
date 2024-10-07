import streamlit as st

st.title("Testing SPO2 Input")

with st.form("test_form"):
    when_intubate = st.multiselect(
        "When will we intubate?",
        ['Prior to procedure', 'Mental Status Changes', 'Hypoxemia Refractory to CPAP'],
        key="when_intubate"
    )

    if "Hypoxemia Refractory to CPAP" in when_intubate:
        spo2_input = st.text_input("SPO2 Less Than?:", key="spo2_input")

    submit = st.form_submit_button("Submit")

if submit:
    st.write("Form submitted!")
