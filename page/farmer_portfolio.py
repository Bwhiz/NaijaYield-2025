import streamlit as st

st.title("Farm Portfolio")
    
# Coming soon message
st.markdown("## 🌱 Coming Soon!")

# Brief description focused on loan assessment
st.write("We're building a comprehensive dashboard to document your farm assets, crop yields, and financial data that loan providers can use to assess your creditworthiness.")

# Add some space
st.write("")

# Basic features list with loan assessment focus
st.write("**Future Features:**")
st.write("✓ Crop yield tracking with historical performance")
st.write("✓ Farm assets inventory and valuation")
st.write("✓ Financial metrics for loan eligibility")
st.write("✓ Creditworthiness indicators for lenders")
st.write("✓ Documentation center for loan applications")



# Simple notification signup
st.markdown("<div class='signup-form'>", unsafe_allow_html=True)
st.subheader("Get notified when we launch")

email = st.text_input("Email Address")
if st.button("Notify Me"):
    if email:
        st.success(f"Thank you! We'll notify {email} when NaijaHarvest launches.")
        # In a real app, you would save this email to your database
    else:
        st.error("Please enter a valid email address.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; color: #777; font-size: 0.9rem;">
    © 2025 NaijaYield. All rights reserved.
</div>
""", unsafe_allow_html=True)
