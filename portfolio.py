import streamlit as st
from datetime import datetime

st.title("🇳🇵 .com.np Domain Registration Cover Letter Generator")
with st.sidebar:
    st.image("kailashprofile.jpeg", width=500)
    st.markdown("""
    ### Introduction
    This application helps you generate a cover letter for registering a .com.np domain.
    
    ### Instructions
    1. Fill in your details in the form.
    2. Click on "Generate Letter".
    3. Download the generated letter.
                
    ### Note
    - Ensure all information is accurate.
    """)
# Simple form
st.subheader("Enter Your Details")

full_name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Contact Number")
citizenship = st.text_input("Citizenship Number")
domain = st.text_input("Domain Name (without .com.np)")

# Generate button
if st.button("Generate Letter"):
    
    # Check if all fields are filled
    if full_name and email and phone and citizenship and domain:
        
        # Get today's date
        date = datetime.now().strftime("%Y/%m/%d")
        
        # Create the letter
        letter = f"""Date: {date}

To
The Domain Registration Team
Mercantile Communications Pvt. Ltd.
Kathmandu, Nepal

Subject: Request for Registration of Domain Name {domain}.com.np

Respected Sir/Madam,

I kindly request the registration of the domain name {domain}.com.np under the .com.np domain extension.
The requested domain name is based on my personal name and will be used for professional and personal purposes, including portfolio presentation, educational content, and maintaining an online presence. The domain name does not violate any existing trademark or intellectual property rights and complies with the policies and regulations of .np domain registration.

I have attached a copy of my citizenship certificate for identity verification, as required by the domain registration guidelines.

I would be grateful if you could process my domain registration request at your earliest convenience.

Thank you for your support and cooperation.

Yours sincerely,

Full Name: {full_name}
Email Address: {email}
Contact Number: {phone}
Citizenship Number: {citizenship}"""
        
        # Show success message
        st.success("Letter Generated!")
        
        # Show the letter
        st.subheader("Your Letter")
        st.text_area("", letter, height=410)
        
        # Download button
        st.download_button(
            "Download Letter",
            letter,
            f"{domain}_registration_letter.txt"
        )
    
    else:
        # Show error if fields are empty
        st.error("Please fill all fields")
