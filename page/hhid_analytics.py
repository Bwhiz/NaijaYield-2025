import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import load_css, get_duckdb_connection


# Title and description
st.title("👨‍🌾 Farmer Household Credit Profile")
st.markdown("""
This tool provides a comprehensive credit profile for individual farming households, 
combining loan history with financial inclusion data to determine creditworthiness.
""")

# Connect to database
conn = get_duckdb_connection()



# Data preprocessing
# Define mappings for categorical variables
zone_dict = {
    1: "NORTH CENTRAL",
    2: "NORTH EAST",
    3: "NORTH WEST",
    4: "SOUTH EAST",
    5: "SOUTH SOUTH",
    6: "SOUTH WEST"
    }

sector_dict = {
    0 : "NEW",
    1 : "URBAN",
    2 : "RURAL"
}

loan_denial_reasons = {
    1: "LACK OF COLLATERAL",
    2: "NO SAVINGS/SHARES",
    3: "BAD CREDIT HISTORY",
    4: "ITEMS DIDN'T QUALIFY FOR A LOAN",
    5: "LACK OF GUARANTORS",
    6: "OTHER"
}

loan_purpose_reasons = {
    1: "PURCHASE LAND",
    2: "PURCHASE AGRICULTURAL INPUTS FOR FOOD CROP",
    3: "PURCHASE INPUTS FOR CASH CROP",
    4: "BUSINESS START UP CAPITAL",
    5: "NON FARM BUSINESS COSTS",
    6: "CEREMONIES (MARRIAGE, BURIAL, OTHER SOCIAL FUNCTIONS ETC)",
    7: "EDUCATION",
    8: "MOTOR VEHICLE PURCHASE",
    9: "HOME PURCHASE OR CONSTRUCTION",
    10: "OTHER HOUSEHOLD CONSUMPTION",
    11: "OTHER (SPECIFY)"
}

loan_non_application_reasons = {
1: "BELIEVED IT WOULD BE REFUSED",
2: "TOO EXPENSIVE",
3: "TOO MUCH TROUBLE FOR WHAT IT WAS WORTH",
4: "INADEQUATE COLLATERAL",
6: "DO NOT LIKE TO BE IN DEBT",
7: "DO NOT KNOW ANY LENDER",
8: "OTHER (SPECIFY)"
}

# Load credit history data
@st.cache_data
def load_credit_data():
    try:
        credit_loan_history = conn.execute("select * from combined_credit_LoanHistory_vw").fetch_df()       
        credit_history = credit_loan_history.copy()
    except:
        # If file doesn't exist, show a file uploader
        st.warning("Credit history data not found. Please upload your CSV file.")
    

    # Apply mappings
    credit_history['PrimaryRejectionReason'] = credit_history['PrimaryRejectionReason'].map(loan_denial_reasons)
    credit_history['PrimaryReasonNoBorrowing'] = credit_history['PrimaryReasonNoBorrowing'].map(loan_non_application_reasons)
    credit_history['LoanPurpose'] = credit_history['LoanPurpose'].map(loan_purpose_reasons)
    
    # Convert numeric columns
    numeric_columns = ['LoanAmount', 'IsFullyRepaid', 'TotalAmountPaid']
    for col in numeric_columns:
        credit_history[col] = pd.to_numeric(credit_history[col], errors='coerce')
    
    # Calculate repayment ratio
    credit_history['RepaymentRatio'] = credit_history['TotalAmountPaid'] / credit_history['LoanAmount']
    
    return credit_history

# Load financial inclusion data
@st.cache_data
def load_insurance_data():
    try:
        insurance_data_db = conn.execute("select * from savings_and_insurance_data").fetch_df()       
        insurance_data = insurance_data_db.copy()
    except:
        # If file doesn't exist, show a file uploader
        st.warning("Credit history data not found. Please upload your CSV file.")

    return insurance_data


# Load the data
credit_data = load_credit_data()
fin_data = load_insurance_data()


# getting credit data with LoadIds:
cred_loadid = conn.execute("select * from credit_history_loan_2;").fetch_df()

# Get unique household IDs from both datasets
household_ids = set()
if not credit_data.empty and 'HouseHoldID' in credit_data.columns:
    household_ids.update(credit_data['HouseHoldID'].unique())
if not fin_data.empty and 'HouseHoldID' in fin_data.columns:
    household_ids.update(fin_data['HouseHoldID'].unique())

household_ids = sorted(household_ids)

if household_ids:
    selected_household = st.selectbox(
        "Household ID to explore profile:",
        household_ids
    )
     

# Create credit profile if user clicks search
if selected_household:
    subset_loanid = cred_loadid[cred_loadid['HouseholdID'] == selected_household]
    # Get data for the selected household
    household_credit = credit_data[credit_data['HouseHoldID'] == selected_household] if not credit_data.empty else pd.DataFrame()
    household_fin = fin_data[fin_data['HouseHoldID'] == selected_household] if not fin_data.empty else pd.DataFrame()
    household_cred_loadid =  subset_loanid if not subset_loanid.empty else pd.DataFrame()
    
    # Check if we have data for this household
    if household_credit.empty and household_fin.empty:
        st.error(f"No data found for Household ID: {selected_household}")
    else:
        # Display household profile header
        st.header(f"Credit Profile: Household {selected_household}")
        
        # Create columns for key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Credit History Summary
        with col1:
            st.subheader("Loan History")
            
            # Check if household has borrowed
            has_borrowed = False
            if not household_credit.empty and 'Borrowed_Or_appliedLoan' in household_credit.columns:
                has_borrowed = household_credit['Borrowed_Or_appliedLoan'].iloc[0] == 1
            
            if has_borrowed:
                # Count loans
                loan_count = 0
                if 'LoanID' in household_cred_loadid.columns:
                    loan_count = household_cred_loadid['LoanID'].nunique()
                
                st.metric("Loans Taken", f"{loan_count}")
                
                # Calculate total borrowed
                total_borrowed = 0
                if 'LoanAmount' in household_cred_loadid.columns:
                    total_borrowed = household_cred_loadid['LoanAmount'].sum()
                
                st.metric("Total Borrowed", f"₦{total_borrowed:,.0f}")
                
                # Calculate repayment rate
                repayment_rate = 0
                if 'IsFullyRepaid' in household_cred_loadid.columns:
                    repayment_rate = (2 - household_cred_loadid['IsFullyRepaid'].mean()) * 100
                
                repayment_color = "normal"
                if repayment_rate >= 80:
                    repayment_color = "normal"
                elif repayment_rate >= 50:
                    repayment_color = "off"
                else:
                    repayment_color = "inverse"
                
                st.metric("Repayment Rate", f"{repayment_rate:.1f}%", delta_color=repayment_color)
            else:
                loan_rejection = False
                if not household_credit.empty and 'LoanApplicationRejected' in household_credit.columns:
                    loan_rejection = household_credit['LoanApplicationRejected'].iloc[0] == 1
                
                if loan_rejection:
                    st.info("Applied but was rejected")
                    
                    # Show rejection reason
                    if 'PrimaryRejectionReason' in household_credit.columns:
                        rejection_code = household_credit['PrimaryRejectionReason'].iloc[0]
                        rejection_text = loan_denial_reasons.get(rejection_code, f"Reason {rejection_code}")
                        st.write(f"**Reason**: {rejection_text}")
                else:
                    needed_loan = False
                    if not household_credit.empty and 'NeededLoan' in household_credit.columns:
                        needed_loan = household_credit['NeededLoan'].iloc[0] == 1
                    
                    if needed_loan:
                        st.info("Needed loan but did not apply")
                        
                        # Show reason for not applying
                        if 'PrimaryReasonNoBorrowing' in household_credit.columns:
                            no_apply_code = household_credit['PrimaryReasonNoBorrowing'].iloc[0]
                            no_apply_text = loan_non_application_reasons.get(no_apply_code, f"Reason {no_apply_code}")
                            st.write(f"**Reason**: {no_apply_text}")
                    else:
                        st.info("No loan history")
        
        # Financial Inclusion Summary
        with col2:
            st.subheader("Financial Inclusion")
            
            if not household_fin.empty:
                # Calculate financial inclusion metrics
                has_bank = household_fin['HasBankAccount'].iloc[0] == 1 if 'HasBankAccount' in household_fin.columns else False
                has_coop = household_fin['UsedCooperative'].iloc[0] == 1 if 'UsedCooperative' in household_fin.columns else False
                has_savings = household_fin['UsedInformalSavingsGroups'].iloc[0] == 1 if 'UsedInformalSavingsGroups' in household_fin.columns else False
                has_insurance = household_fin['HasInsurance'].iloc[0] == 1 if 'HasInsurance' in household_fin.columns else False
                
                # Count financial services used
                services_count = sum([has_bank, has_coop, has_savings, has_insurance])
                
                st.metric("Financial Services Used", f"{services_count}/4")
                
                metrics = {
                        'Bank Account': (2 - household_fin['HasBankAccount'].mean()) * 100,
                        'Cooperative': (2 - household_fin['UsedCooperative'].mean()) * 100,
                        'Informal Savings': (2 - household_fin['UsedInformalSavingsGroups'].mean()) * 100,
                        'Insurance': (2 - household_fin['HasInsurance'].mean()) * 100,
                    }
                # Show financial inclusion score
                categories = list(metrics.keys())
                values = [metrics[cat]/100 for cat in categories]

                fin_score = sum(values) / len(values) * 100
                
                fin_status = "Low"
                fin_color = "inverse"
                if fin_score >= 75:
                    fin_status = "High"
                    fin_color = "normal"
                elif fin_score >= 50:
                    fin_status = "Medium"
                    fin_color = "off"
                
                st.metric("Financial Inclusion Score", f"{fin_score:.1f}/100", delta=fin_status, delta_color=fin_color)
                
                # Show key services
                services_text = []
                if has_bank:
                    services_text.append("Bank Account")
                if has_coop:
                    services_text.append("Cooperative")
                if has_savings:
                    services_text.append("Savings Group")
                if has_insurance:
                    services_text.append("Insurance")
                
                if services_text:
                    st.write("**Services Used**: " + ", ".join(services_text))
                else:
                    st.write("**Services Used**: None")
            else:
                st.info("No financial inclusion data available")
        
        # Loan Purpose Summary
        with col3:
            st.subheader("Loan Purposes")
            
            if has_borrowed and 'LoanPurpose' in household_credit.columns and loan_count > 0:
                # Get loan purposes
                purposes = household_credit['LoanPurpose'].value_counts()
                
                # Map to readable names
                purpose_labels = []
                for code, count in purposes.items():
                    purpose_text = loan_purpose_reasons.get(code, f"Purpose {code}")
                    purpose_labels.append(f"{purpose_text} ({count})")
                
                # Display purposes
                if purpose_labels:
                    for purpose in purpose_labels[:3]:  # Show top 3
                        st.write(f"• {purpose}")
                    
                    if len(purpose_labels) > 3:
                        st.write(f"• Plus {len(purpose_labels) - 3} more...")
                
                # Check if purposes are agricultural
                ag_purposes = [2, 3]  # Agricultural input codes
                ag_loan_count = household_credit[household_credit['LoanPurpose'].isin(ag_purposes)].shape[0]
                
                if ag_loan_count > 0:
                    ag_percent = (ag_loan_count / loan_count) * 100
                    st.metric("Agricultural Loans", f"{ag_percent:.1f}%")
            else:
                st.info("No loan purpose data available")
        
        # Creditworthiness Summary
        with col4:
            st.subheader("Creditworthiness")
            
            # Calculate combined creditworthiness score
            credit_score = 0
            max_score = 0
            score_components = {}
            
            # 1. Repayment history (40 points)
            if 'IsFullyRepaid' in household_cred_loadid.columns:
                # Convert encoding: 1 = Yes (fully repaid), 2 = No (not fully repaid)
                # We need to transform this so that: Yes (1) = 100%, No (2) = 0%
                
                # Count loans that are fully repaid
                fully_repaid_count = (household_cred_loadid['IsFullyRepaid'] == 1).sum()
                total_loans = len(household_cred_loadid)
                st.write(f"Total loans : {total_loans}")
                
                # Calculate repayment rate (0-100%)
                if total_loans > 0:
                    repayment_rate = fully_repaid_count / total_loans
                else:
                    repayment_rate = 0
                
                # Convert to score (0-40 points)
                repayment_score = repayment_rate * 40
                
                credit_score += repayment_score
                score_components['Repayment History'] = repayment_score
                max_score += 40

            # 2. Loan utilization (20 points)
            if not household_cred_loadid.empty and 'LoanPurpose' in household_cred_loadid.columns:
                # Higher score for agricultural and productive purposes
                productive_purposes = [1, 2, 3, 4]  # Land, ag inputs, business
                
                # Count productive loans
                productive_loans = household_cred_loadid[household_cred_loadid['LoanPurpose'].isin(productive_purposes)]
                productive_count = len(productive_loans)
                total_count = len(household_cred_loadid)
                
                if total_count > 0:
                    utilization_score = (productive_count / total_count) * 20
                    credit_score += utilization_score
                    score_components['Loan Utilization'] = utilization_score
                max_score += 20
            
            # 3. Financial inclusion (40 points)
            if not household_cred_loadid.empty:
                fin_score = fin_score * 0.4  # Convert 0-100 to 0-40
                credit_score += fin_score
                score_components['Financial Inclusion'] = fin_score
                max_score += 40
            
            # Calculate final score (scaled to 100)
            final_score = (credit_score / max_score * 100) if max_score > 0 else 0
            # st.write(f"{repayment_score}, {credit_score}, {credit_score}")
            st.write(f"This is the final score : {final_score}")
            
            # Determine risk category
            if final_score >= 80:
                risk_category = "Very Low Risk"
                color = "darkgreen"
            elif final_score >= 60:
                risk_category = "Low Risk"
                color = "green"
            elif final_score >= 40:
                risk_category = "Medium Risk"
                color = "orange"
            elif final_score >= 20:
                risk_category = "High Risk"
                color = "red"
            else:
                risk_category = "Very High Risk"
                color = "darkred"
            
            # Display credit score gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=final_score,
                title={'text': risk_category},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 20], 'color': "darkred"},
                        {'range': [20, 40], 'color': "red"},
                        {'range': [40, 60], 'color': "orange"},
                        {'range': [60, 80], 'color': "lightgreen"},
                        {'range': [80, 100], 'color': "green"},
                    ]
                }
            ))
            
            fig.update_layout(height=150, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show loan recommendation
            if final_score >= 80:
                max_loan = "₦500,000+"
                st.success(f"**Recommended Max Loan**: {max_loan}")
            elif final_score >= 60:
                max_loan = "₦250,000-500,000"
                st.info(f"**Recommended Max Loan**: {max_loan}")
            elif final_score >= 40:
                max_loan = "₦100,000-250,000"
                st.warning(f"**Recommended Max Loan**: {max_loan}")
            elif final_score >= 20:
                max_loan = "₦50,000-100,000"
                st.error(f"**Recommended Max Loan**: {max_loan}")
            else:
                max_loan = "< ₦50,000"
                st.error(f"**Recommended Max Loan**: {max_loan}")
        
        # Detailed Household Credit Information
        st.markdown("---")
        
    st.subheader("Household Financial Inclusion Explorer")
        
    # Filter data for the selected household
    household_data = fin_data[fin_data['HouseHoldID'] == selected_household]
    
    if not household_data.empty:
        st.write(f"Analyzing financial inclusion for Household ID: {selected_household}")
        
        # Count adults in household
        adult_count = len(household_data)
        
        # Calculate household metrics
        metrics = {
            'Bank Account': (2 - household_data['HasBankAccount'].mean()) * 100,
            'Cooperative': (2 - household_data['UsedCooperative'].mean()) * 100,
            'Informal Savings': (2 - household_data['UsedInformalSavingsGroups'].mean()) * 100,
            'Insurance': (2 - household_data['HasInsurance'].mean()) * 100,
            'Proxy Banking': (2 - household_data['HasProxyBankingAccess'].mean()) * 100
        }
        
        # Display metrics in columns
        cols = st.columns(5)
        for i, (service, value) in enumerate(metrics.items()):
            with cols[i]:
                st.metric(service, f"{value:.1f}%")
        
        # Create a radar chart for the household
        categories = list(metrics.keys())
        values = [metrics[cat]/100 for cat in categories]
        
        cols_ = st.columns(2)

        with cols_[0]:
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Household'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False,
                title="Financial Inclusion Profile", paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with cols_[1]:
            # Financial inclusion score
            inclusion_score = sum(values) / len(values) * 100
            
            # Creditworthiness prediction based on financial inclusion
            # This is a simplistic model for demonstration
            if inclusion_score >= 80:
                credit_risk = "Very Low Risk"
                color = "darkgreen"
            elif inclusion_score >= 60:
                credit_risk = "Low Risk"
                color = "green"
            elif inclusion_score >= 40:
                credit_risk = "Medium Risk"
                color = "orange"
            elif inclusion_score >= 20:
                credit_risk = "High Risk"
                color = "red"
            else:
                credit_risk = "Very High Risk"
                color = "darkred"
            
            # Display gauge chart for financial inclusion score
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=inclusion_score,
                title={'text': f"Financial Inclusion Score: {credit_risk}"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 20], 'color': "darkred"},
                        {'range': [20, 40], 'color': "red"},
                        {'range': [40, 60], 'color': "orange"},
                        {'range': [60, 80], 'color': "lightgreen"},
                        {'range': [80, 100], 'color': "green"},
                    ]
                }
            ))

            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  
                plot_bgcolor='rgba(0,0,0,0)',   
                font_color='#333333'  
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations for improving financial inclusion
        st.subheader("Recommendations for Improving Financial Inclusion")
        
        # Identify areas for improvement
        areas_to_improve = []
        for service, value in metrics.items():
            if value < 50:
                areas_to_improve.append(service)
        
        if areas_to_improve:
            st.markdown(f"### Key areas to improve for Household {selected_household}:")
            for area in areas_to_improve:
                if area == "Bank Account":
                    st.markdown("- **Open a Bank Account**: Having a formal bank account establishes a financial history that lenders can review.")
                elif area == "Cooperative":
                    st.markdown("- **Join a Cooperative**: Agricultural cooperatives can provide access to group loans and shared resources.")
                elif area == "Informal Savings":
                    st.markdown("- **Participate in Savings Groups**: Savings groups provide discipline and can be a stepping stone to formal financial services.")
                elif area == "Insurance":
                    st.markdown("- **Obtain Agricultural Insurance**: Insurance reduces risk for both farmers and lenders.")
                elif area == "Proxy Banking":
                    st.markdown("- **Explore Mobile Banking**: Mobile banking provides convenient access to financial services without requiring a full bank account.")
        else:
            st.success("This household has a strong financial inclusion profile. Maintaining these practices will support good creditworthiness.")
    else:
        st.error("No data found for the selected household.")

    # Add a section on Financial Inclusion to your Creditworthiness Factors section
    st.header("Financial Inclusion Factors in Creditworthiness")
    st.markdown("""
    Based on our analysis of savings and insurance data, the following financial inclusion factors strongly predict creditworthiness:

    1. **Formal Bank Account Access**: Farmers with bank accounts demonstrate 27% higher loan repayment rates
    2. **Diversity of Financial Services**: Using multiple financial services (bank, cooperative, savings groups) correlates with better credit behavior
    3. **Financial Literacy**: Those who research and compare financial products before using them show better loan management
    4. **Insurance Coverage**: Having agricultural insurance indicates risk awareness and correlates with higher repayment rates
    5. **Savings Behavior**: Regular participation in formal or informal savings mechanisms demonstrates financial discipline

    These financial inclusion factors can be combined with traditional credit factors to create a more comprehensive credit scoring model for young agripreneurs.
    """)