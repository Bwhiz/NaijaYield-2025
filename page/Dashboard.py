import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import load_css, get_duckdb_connection

# Title and description
st.title("🌱 Agricultural Credit Access Dashboard")
st.markdown("""
This dashboard provides insights into agricultural financing patterns and barriers to credit access
for Nigerian farmers, analyzing loan applications, approvals, rejections, and repayment behaviors.
""")

conn = get_duckdb_connection()

# Function to load data (replace with your actual data loading)
@st.cache_data
def load_credit_data():
    try:
        credit_loan_history = conn.execute("select * from combined_credit_LoanHistory_vw").fetch_df()       
        credit_history = credit_loan_history.copy()
    except:
        # If file doesn't exist, show a file uploader
        st.warning("Credit history data not found. Please upload your CSV file.")
    
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
credit_history = load_credit_data()
insurance_data = load_insurance_data()


# Check if data is loaded
if credit_history.empty:
    st.error("No data available. Please upload the credit history data to continue.")
    st.stop()

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Loan Access Overview", "Rejection Analysis", "Loan Characteristics", "Repayment Analysis"])

with tab1:
    st.header("Loan Access Overview")
    
    # Create two columns for the first row
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Loan Application Status Distribution
        loan_status_counts = credit_history.groupby(['Borrowed_Or_appliedLoan']).size().reset_index(name='count')
        
        # Add labels
        loan_status_counts['Status'] = loan_status_counts['Borrowed_Or_appliedLoan'].map(
            {2: 'No Application', 1: 'Applied for Loan'})
        
        fig = px.pie(loan_status_counts, values='count', names='Status',
                    title='Proportion of Farmers Who Applied for Loans',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(legend_title=None, paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 2. Loan Application Outcomes
        # Calculate values for each category
        approved = credit_history[credit_history['Borrowed_Or_appliedLoan'] == 1]
        approved = approved[approved['LoanApplicationRejected'] != 1].shape[0]
        
        rejected = credit_history[credit_history['LoanApplicationRejected'] == 1].shape[0]
        
        needed_no_apply = credit_history[(credit_history['Borrowed_Or_appliedLoan'] != 1) & 
                                        (credit_history['NeededLoan'] == 1)].shape[0]
        
        outcomes_data = pd.DataFrame({
            'Outcome': ['Approved', 'Rejected', 'Needed but Did Not Apply'],
            'Count': [approved, rejected, needed_no_apply]
        })
        
        # Calculate percentages
        total = outcomes_data['Count'].sum()
        outcomes_data['Percentage'] = outcomes_data['Count'] / total * 100
        
        # Create bar chart
        fig = px.bar(outcomes_data, x='Outcome', y='Count', 
                    title='Loan Application Outcomes',
                    color='Outcome', 
                    color_discrete_map={
                        'Approved': '#2ecc71', 
                        'Rejected': '#e74c3c', 
                        'Needed but Did Not Apply': '#f39c12'
                    },
                    text=outcomes_data['Percentage'].apply(lambda x: f'{x:.1f}%'))
        
        fig.update_traces(textposition='outside')
        fig.update_layout(yaxis_title='Number of Farmers', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333')
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row - Loan purpose distribution
    st.subheader("Loan Purpose Distribution")
    
    loan_purposes = credit_history['LoanPurpose'].dropna().value_counts().reset_index()
    loan_purposes.columns = ['Purpose', 'Count']
    loan_purposes = loan_purposes.sort_values('Count', ascending=True).tail(10)  # Get top 10
    
    fig = px.bar(loan_purposes, y='Purpose', x='Count', 
                orientation='h',
                title='Top Loan Purposes',
                color_discrete_sequence=['#9b59b6'])
    
    fig.update_traces(texttemplate='%{x}', textposition='outside')
    fig.update_layout(xaxis_title='Number of Loans', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Loan Rejection Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 3. Primary Reasons for Loan Rejection
        rejection_reasons = credit_history[credit_history['LoanApplicationRejected'] == 1]['PrimaryRejectionReason']
        rejection_counts = rejection_reasons.value_counts().reset_index()
        rejection_counts.columns = ['Reason', 'Count']
        rejection_counts = rejection_counts.sort_values('Count', ascending=True)
        
        fig = px.bar(rejection_counts, y='Reason', x='Count', 
                    orientation='h',
                    title='Primary Reasons for Loan Rejection',
                    color_discrete_sequence=['#e74c3c'])
        
        fig.update_traces(texttemplate='%{x}', textposition='outside')
        fig.update_layout(xaxis_title='Number of Farmers', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 4. Reasons for Not Applying Despite Need
        no_apply_reasons = credit_history[(credit_history['Borrowed_Or_appliedLoan'] != 1) & 
                                        (credit_history['NeededLoan'] == 1)]['PrimaryReasonNoBorrowing']
        no_apply_counts = no_apply_reasons.value_counts().reset_index()
        no_apply_counts.columns = ['Reason', 'Count']
        no_apply_counts = no_apply_counts.sort_values('Count', ascending=True)
        
        fig = px.bar(no_apply_counts, y='Reason', x='Count', 
                    orientation='h',
                    title='Primary Reasons for Not Applying Despite Needing a Loan',
                    color_discrete_sequence=['#f39c12'])
        
        fig.update_traces(texttemplate='%{x}', textposition='outside')
        fig.update_layout(xaxis_title='Number of Farmers', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Loan Characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 5. Loan Amount Distribution
        # Remove outliers for better visualization
        loan_amounts = credit_history['LoanAmount'].dropna()
        q1, q3 = loan_amounts.quantile([0.25, 0.75])
        iqr = q3 - q1
        upper_bound = q3 + 1.5 * iqr
        filtered_amounts = loan_amounts[loan_amounts <= upper_bound]
        
        fig = px.histogram(filtered_amounts, 
                          title='Distribution of Loan Amounts',
                          labels={'value': 'Loan Amount (Naira)'},
                          color_discrete_sequence=['#3498db'])
        
        # Add mean and median lines
        fig.add_vline(x=filtered_amounts.mean(), line_dash="dash", line_color="red", 
                     annotation_text=f"Mean: {filtered_amounts.mean():.2f}", 
                     annotation_position="top")
        
        fig.add_vline(x=filtered_amounts.median(), line_dash="dash", line_color="green", 
                     annotation_text=f"Median: {filtered_amounts.median():.2f}", 
                     annotation_position="bottom")
        
        fig.update_layout(yaxis_title='Frequency', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Loan amount by purpose
        # Group by loan purpose and calculate average amount
        purpose_amounts = credit_history.groupby('LoanPurpose')['LoanAmount'].agg(['mean', 'count']).reset_index()
        purpose_amounts.columns = ['Purpose', 'Mean', 'Count']
        
        # Filter to purposes with at least 5 loans for relevance
        purpose_amounts = purpose_amounts[purpose_amounts['Count'] >= 5]
        purpose_amounts = purpose_amounts.sort_values('Mean', ascending=True)
        
        fig = px.bar(purpose_amounts, y='Purpose', x='Mean', 
                    orientation='h',
                    title='Average Loan Amount by Purpose',
                    color_discrete_sequence=['#9b59b6'])
        
        fig.update_traces(texttemplate='%{x:.0f}', textposition='outside')
        fig.update_layout(xaxis_title='Average Loan Amount (Naira)', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
        st.plotly_chart(fig, use_container_width=True)
    
    # Loan characteristics - additional metrics
    st.subheader("Loan Sufficiency Analysis")
    
    # Convert to numeric
    credit_history['LoanSufficient'] = pd.to_numeric(credit_history['LoanSufficient'], errors='coerce')
    
    loan_sufficiency = credit_history['LoanSufficient'].value_counts().reset_index()
    loan_sufficiency.columns = ['Status', 'Count']
    loan_sufficiency['Label'] = loan_sufficiency['Status'].map({2: 'Insufficient', 1: 'Sufficient'})
    
    fig = px.pie(loan_sufficiency, values='Count', names='Label',
                title='Were Approved Loans Sufficient for Intended Purpose?',
                color_discrete_map={'Insufficient': '#e74c3c', 'Sufficient': '#2ecc71'})
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Loan Repayment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 6. Loan Repayment Status
        repayment_status = credit_history['IsFullyRepaid'].value_counts().reset_index()
        repayment_status.columns = ['Status', 'Count']
        repayment_status['Label'] = repayment_status['Status'].map({2: 'Not Fully Repaid', 1: 'Fully Repaid'})
        
        fig = px.pie(repayment_status, values='Count', names='Label',
                    title='Loan Repayment Status',
                    color_discrete_map={'Not Fully Repaid': '#e74c3c', 'Fully Repaid': '#2ecc71'})
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Repayment ratio distribution
        valid_ratios = credit_history['RepaymentRatio'].dropna()
        # Filter out extreme values
        valid_ratios = valid_ratios[(valid_ratios >= 0) & (valid_ratios <= 2)]
        
        fig = px.histogram(valid_ratios, 
                          title='Distribution of Loan Repayment Ratios',
                          labels={'value': 'Repayment Ratio (Amount Paid / Amount Borrowed)'},
                          color_discrete_sequence=['#3498db'])
        
        # Add full repayment and mean ratio lines
        fig.add_vline(x=1.0, line_dash="dash", line_color="red", 
                     annotation_text="Full Repayment", 
                     annotation_position="top")
        
        fig.add_vline(x=valid_ratios.mean(), line_dash="dash", line_color="green", 
                     annotation_text=f"Mean: {valid_ratios.mean():.2f}", 
                     annotation_position="bottom")
        
        fig.update_layout(yaxis_title='Frequency', paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)', font_color='#333333' )
        st.plotly_chart(fig, use_container_width=True)
    
    # # Loan repayment performance by loan amount
    # st.subheader("Repayment Performance by Loan Size")
    
    # # Create loan amount categories
    # credit_history['LoanAmountCategory'] = pd.cut(
    #     credit_history['LoanAmount'], 
    #     bins=[0, 50000, 100000, 250000, 500000, float('inf')],
    #     labels=['< 50K', '50K-100K', '100K-250K', '250K-500K', '> 500K']
    # )
    
    # # Group by amount category and calculate repayment rate
    # repayment_by_amount = credit_history.groupby('LoanAmountCategory')['IsFullyRepaid'].mean().reset_index()
    # repayment_by_amount.columns = ['Loan Size', 'Repayment Rate']
    # repayment_by_amount['Repayment Rate'] = repayment_by_amount['Repayment Rate'] * 100
    
    # fig = px.bar(repayment_by_amount, x='Loan Size', y='Repayment Rate',
    #             title='Loan Repayment Rate by Loan Amount',
    #             color_discrete_sequence=['#3498db'],
    #             text=repayment_by_amount['Repayment Rate'].apply(lambda x: f'{x:.1f}%'))
    
    # fig.update_traces(textposition='outside')
    # fig.update_layout(yaxis_title='Repayment Rate (%)', yaxis_range=[0, 100])
    # st.plotly_chart(fig, use_container_width=True)


# # Add a section for creditworthiness factors
# st.header("Creditworthiness Factors")
# st.markdown("""
# Based on this data analysis, the following factors appear to be most predictive of loan repayment:

# 1. **Previous repayment history**: Farmers who have repaid loans fully in the past are more likely to repay future loans
# 2. **Loan size appropriateness**: Loans that match the intended purpose (neither too small nor too large)
# 3. **Loan purpose**: Certain purposes show higher repayment rates
# 4. **Financial inclusion**: Farmers with formal banking relationships show better repayment patterns

# These factors can be used to develop a credit scoring model for agricultural loans, 
# especially focusing on young agripreneurs who may lack traditional collateral.
# """)

# # Add a sidebar with filters
# st.sidebar.header("Filters")
# st.sidebar.markdown("Filter the data to explore specific segments")

# # Add loan purpose filter if available
# if 'LoanPurpose' in credit_history.columns:
#     purposes = credit_history['LoanPurpose'].dropna().unique()
#     selected_purposes = st.sidebar.multiselect("Loan Purpose", options=purposes)
    
#     if selected_purposes:
#         st.sidebar.info(f"You've selected {len(selected_purposes)} loan purposes. The dashboard would filter to show only loans for these purposes.")

# # Add loan amount range filter
# min_amount = int(credit_history['LoanAmount'].min())
# max_amount = int(credit_history['LoanAmount'].max())
# amount_range = st.sidebar.slider("Loan Amount Range", min_amount, max_amount, (min_amount, max_amount))

# if amount_range != (min_amount, max_amount):
#     st.sidebar.info(f"You've selected loans between {amount_range[0]} and {amount_range[1]} Naira. The dashboard would filter to show only these loans.")

# # Add about section
# st.sidebar.markdown("---")
# st.sidebar.header("About")
# st.sidebar.info(
#     """
#     This dashboard visualizes data from the Nigerian Agricultural Survey 
#     to develop a credit scoring solution for young agripreneurs.
    
#     **Project Goal**: Develop a data-driven approach to help young farmers 
#     obtain access to affordable finance.
#     """
# )

# # Add download buttons for reports and data
# st.sidebar.markdown("---")
# st.sidebar.header("Download")
# st.sidebar.download_button(
#     label="Download Analysis Report (PDF)",
#     data=b"Sample PDF content",  # Replace with actual PDF content
#     file_name="agripreneur_credit_analysis.pdf",
#     mime="application/pdf",
#     key="report-pdf"
# )

# st.sidebar.download_button(
#     label="Download Dashboard Data (CSV)",
#     data=credit_history.to_csv().encode('utf-8'),
#     file_name="credit_history_data.csv",
#     mime="text/csv",
#     key="data-csv"
# )

# # Footer
# st.markdown("---")
# st.markdown("Created for the Agricultural Finance Hackathon | Data source: Nigerian Agricultural Survey")