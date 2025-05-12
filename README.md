# Nigerian Agricultural Credit Assessment Tool (NaijaYield)

## 🧭 Overview

**NaijaYield** is a data-driven decision support application designed to evaluate creditworthiness, financial inclusion, and agricultural productivity of Nigerian farming households. The tool is tailored to empower young agripreneurs by improving their access to agricultural finance through data analytics and scoring models.

---

## 🎯 Features

- **Credit History Dashboard**  
  Visualize loan applications, approvals, rejections, and repayment behaviors across regions and demographic groups.

- **Household Credit Profiling**  
  Generate detailed credit profiles for individual farming households with personalized recommendations.

- **Financial Inclusion Analysis**  
  Measure access to formal and informal financial services and understand their impact on creditworthiness.

- **Agricultural Productivity Integration**  
  Analyze farm production, commercialization, and risk management practices to understand financial needs.

- **Credit Scoring Algorithm**  
  A custom model combining repayment behavior, financial inclusion metrics, and loan utilization patterns.

- **Interactive Visualizations**  
  Engaging dashboards built using Plotly and Streamlit for exploratory and comparative analysis.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+
- **Web Framework**: Streamlit
- **Database**: DuckDB (via MotherDuck)
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib

---

## 📁 Project Structure

```
├── data/
├── main.py
├── notebooks/
│   ├── data_preprocessing_ETL.ipynb
│   └── prototype.ipynb
├── page/
│   ├── Dashboard.py
│   └── hhid_analytics.py
├── pyproject.toml
├── README.md
├── static/
│   ├── css//
│   │   └── style.css
│   └── images//
├── transformed_data/
│   
├── utils/
│   ├── __init__.py
│   ├── functions.py
│   
└── uv.lock
```

---

## 🚀 Getting Started (with `uv`)

1. **Create a virtual environment**
   ```bash
   uv venv
   ```

2. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

   or if you're using a plain `pyproject.toml`:
   ```bash
   uv pip install -r pyproject.toml
   ```

3. **Launch the app**  
   ```bash
   streamlit run main.py
   ```

4. **Explore Notebooks**  
   Use the `notebooks/` folder to examine preprocessing and prototyping workflows.

---

## 📌 Notes

- Ensure DuckDB is accessible locally or via MotherDuck.
- The app is designed with background customization and interactive plots.

---

## 🧑‍🌾 Purpose

This tool supports data-driven decisions to extend financial inclusion and fair credit access to rural Nigerian farmers — helping bridge the gap between agriculture and fintech.

---

### 🔗 [Link to Project](https://naijayield.streamlit.app/)

