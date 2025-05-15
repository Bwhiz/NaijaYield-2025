import streamlit as st

def add_custom_css():
    st.markdown("""
    <style>
        /* Main page styling */
        .main {
            background-color: #f7f9f9;
        }
        
        /* Header styling */
        .title-container {
            background-color: #2E7D32;
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Card styling */
        .card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        /* Tip styling */
        .tip-number {
            background-color: #2E7D32;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-weight: bold;
        }
        
        .tip-title {
            font-weight: bold;
            color: #2E7D32;
            font-size: 1.2rem;
            margin-bottom: 10px;
        }
        
        /* URL cards styling */
        .url-card {
            background-color: #f0f7f0;
            border-left: 5px solid #2E7D32;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            transition: all 0.3s;
        }
        
        .url-card:hover {
            background-color: #e0eee0;
            transform: scale(1.01);
        }
        
        .url-title {
            font-weight: bold;
            color: #2E7D32;
        }
        
        /* Buttons */
        .css-1cpxqw2 {
            background-color: #2E7D32;
            color: white;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            font-size: 0.8rem;
            color: #666;
            border-top: 1px solid #ddd;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .card {
                padding: 15px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Function to create URL cards
def url_card(title, url, description=""):
    card_html = f"""
    <div class="url-card">
        <div class="url-title">{title}</div>
        <p>{description}</p>
        <a href="{url}" target="_blank">Visit Website</a>
    </div>
    """
    return card_html

# Function to create tip cards
def tip_card(number, title, content):
    card_html = f"""
    <div class="card">
        <h3><span class="tip-number">{number}</span> {title}</h3>
        <p>{content}</p>
    </div>
    """
    return card_html

add_custom_css()

# Header
st.markdown("""
<div class="title-container">
    <h1>Improve Your Credit Score</h1>
    <p>Practical tips to help farmers build and improve their credit score for better loan access</p>
</div>
""", unsafe_allow_html=True)

# Introduction -->
with st.container():
    st.subheader("Why Your Credit Score Matters")
    st.write("Having a good credit score makes it easier to get loans, increases the amount you can borrow, and gives you access to better interest rates. For farmers, this can be the difference between growing your business or being stuck in the same cycle.")
    st.write("A credit score is a number (usually between 300 and 850) that shows how likely you are to repay borrowed money. In Nigeria, scores are calculated using your loan history, bill payments, and how much debt you owe.")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**High score (700–850)**: Shows lenders you are trustworthy")
    with col2:
        st.write("**Low score (below 600)**: May prevent you from accessing loans")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h2>Tips to Improve Your Score</h2>", unsafe_allow_html=True)
    
    # Credit Score Tips
    tips = [
        {
            "number": 1,
            "title": "Get Your Credit Report",
            "content": "Get your credit report from a credit bureau (e.g., CRC Credit Bureau, FirstCentral Credit Bureau) and study it to understand your current standing."
        },
        {
            "number": 2,
            "title": "Pay Your Bills on Time",
            "content": "Late payments on loans, utility bills, or mobile money loans can significantly damage your score. Since farmers often earn seasonally, plan your payments around your harvest or other income peaks."
        },
        {
            "number": 3,
            "title": "Limit the Number of Loans",
            "content": "Avoid taking multiple loans at the same time. It can put pressure on your finances and signal desperation to lenders. Only borrow when necessary, and space out your loan applications."
        },
        {
            "number": 4,
            "title": "Keep Old Accounts Open",
            "content": "If you have a loan account with a good repayment history, don't close it. Older credit accounts with a good record strengthen your score."
        },
        {
            "number": 5,
            "title": "Reduce Your Debt-to-Income Ratio",
            "content": "The less you owe compared to what you earn, the better. Avoid borrowing more than you can comfortably repay based on your expected farm income. Keep farming records of your sales and expenses to help assess this."
        },
        {
            "number": 6,
            "title": "Check and Correct Errors",
            "content": "Sometimes, credit reports have mistakes (e.g., incorrect loan balances or personal information). Dispute errors by contacting the credit bureau."
        },
        {
            "number": 7,
            "title": "Join a Cooperative Society",
            "content": "Cooperatives can help members access loans without strict credit checks. They also help build a culture of regular saving and repayment, which indirectly improves your credit standing."
        },
        {
            "number": 8,
            "title": "Use Mobile Lending Responsibly",
            "content": "Apps like FairMoney, Carbon, or Palmcredit now report your repayment behavior to credit bureaus. Borrow small, repay on time. Doing this consistently improves your score."
        },
        {
            "number": 9,
            "title": "Negotiate During Emergencies",
            "content": "Events like droughts, flooding, or market crashes can impact your ability to repay loans. Instead of defaulting, speak to your lender early to renegotiate repayment terms."
        },
        {
            "number": 10,
            "title": "Diversify Your Income Streams",
            "content": "Lenders prefer borrowers with more than one income stream because it reduces the risk of default. A cassava farmer who also raises chickens is more likely to keep up with loan payments during a bad harvest season."
        }
    ]
    
    # Displaying tips as cards
    for tip in tips:
        st.markdown(tip_card(tip["number"], tip["title"], tip["content"]), unsafe_allow_html=True)

with col2:
    st.markdown("<h2>Useful Resources</h2>", unsafe_allow_html=True)
    
    # Credit Bureaus
    st.markdown("<h3>Credit Bureaus</h3>", unsafe_allow_html=True)
    st.markdown(url_card(
        "CRC Credit Bureau", 
        "https://crccreditbureau.com", 
        "Get your credit report and check your credit score"
    ), unsafe_allow_html=True)
    
    st.markdown(url_card(
        "FirstCentral Credit Bureau", 
        "https://firstcentralcreditbureau.com", 
        "Access your credit information and report"
    ), unsafe_allow_html=True)
    
    # Mobile Lending Apps
    st.markdown("<h3>Mobile Lending Apps</h3>", unsafe_allow_html=True)
    st.markdown(url_card(
        "FairMoney", 
        "https://fairmoney.io", 
        "Loans up to ₦1,000,000 with terms of 1-12 months"
    ), unsafe_allow_html=True)
    
    st.markdown(url_card(
        "Carbon", 
        "https://getcarbon.co", 
        "Instant loans with no paperwork or guarantors"
    ), unsafe_allow_html=True)
    
    st.markdown(url_card(
        "Palmcredit", 
        "https://palmcredit.com", 
        "Quick loans with flexible repayment options"
    ), unsafe_allow_html=True)
    
    # Agricultural Financing Programs
    st.markdown("<h3>Agricultural Financing Programs</h3>", unsafe_allow_html=True)
    st.markdown(url_card(
        "NIRSAL MFB", 
        "https://nirsal.com", 
        "Access to agricultural loans with competitive rates"
    ), unsafe_allow_html=True)
    
    st.markdown(url_card(
        "CBN Anchor Borrowers Programme", 
        "https://www.cbn.gov.ng/dev.asp", 
        "Government-backed loans for smallholder farmers"
    ), unsafe_allow_html=True)
    
    st.markdown(url_card(
        "Licensed Lenders via CBN Portal", 
        "https://cbn.gov.ng", 
        "Find legitimate financial institutions"
    ), unsafe_allow_html=True)
    
    # Quick Tips Section
    st.markdown("<h3>Quick Actions</h3>", unsafe_allow_html=True)
    
    st.info("📱 **Set up reminders** for loan repayments to avoid missing due dates")
    st.warning("⚠️ **Avoid informal loan sharks** that charge extremely high interest rates")
    st.success("💰 **Save consistently** with a bank or licensed cooperative to build trust")

# Calculator Section - FIXED the unclosed paragraph tag
st.markdown("<h2>Debt-to-Income Ratio Calculator</h2>", unsafe_allow_html=True)
st.markdown("<p>This calculator helps you determine if you're borrowing more than you can afford based on your farm income.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    monthly_income = st.number_input("Monthly Farm Income (₦)", min_value=0, value=100000)
    other_income = st.number_input("Other Monthly Income (₦)", min_value=0, value=20000)
    total_income = monthly_income + other_income
    
with col2:
    loan_payments = st.number_input("Monthly Loan Payments (₦)", min_value=0, value=30000)
    other_debts = st.number_input("Other Monthly Debts (₦)", min_value=0, value=10000)
    total_debts = loan_payments + other_debts

if total_income > 0:
    ratio = (total_debts / total_income) * 100
    
    st.markdown(f"""
    <div class="card">
        <h3>Your Debt-to-Income Ratio: {ratio:.1f}%</h3>
        <div style="background: linear-gradient(to right, green, yellow, red); height: 30px; border-radius: 15px; position: relative;">
            <div style="position: absolute; height: 30px; width: 5px; background-color: black; left: {min(ratio, 100)}%; transform: translateX(-50%);"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
            <span style="color: green;">Good (0-36%)</span>
            <span style="color: #b58105;">Concerning (37-42%)</span>
            <span style="color: red;">Risky (43%+)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if ratio <= 36:
        st.success("✅ Your debt ratio is healthy! Lenders typically prefer a ratio below 36%.")
    elif ratio <= 42:
        st.warning("⚠️ Your debt level is getting high. Consider reducing some debt before taking on more loans.")
    else:
        st.error("❌ Your debt ratio is too high. Most lenders would consider this risky. Focus on reducing your debt.")

# FAQ Section
with st.expander("Frequently Asked Questions"):
    st.markdown("""
    ### How long does it take to improve my credit score?
    It depends on your situation, but you should start seeing improvements in 3-6 months with consistent good practices.
    
    ### Will checking my credit score lower it?
    No, checking your own credit score is considered a "soft inquiry" and doesn't affect your score.
    
    ### Can I get a loan with a low credit score?
    Yes, but you'll likely face higher interest rates or may need to provide more collateral.
    
    ### How often should I check my credit report?
    It's good practice to check your credit report at least once a year, or before applying for any significant loan.
    
    ### Can I build credit without taking loans?
    Yes, through mobile money services, consistent savings with formal institutions, and joining cooperatives with good standing.
    """)


st.markdown("""
<div class="footer">
    <p>© 2025 NaijaYield | This tool is a submission for the AgriConnect Hackathon</p>
</div>
""", unsafe_allow_html=True)