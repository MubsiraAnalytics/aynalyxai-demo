# AynalyxAI Demo - Streamlit Cloud Version
# This is a simplified demo version for online preview

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Page config
st.set_page_config(
    page_title="AynalyxAI Demo",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .anomaly-high { background-color: #fee2e2; }
    .anomaly-medium { background-color: #fef3c7; }
    .anomaly-low { background-color: #d1fae5; }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
    }
    .demo-badge {
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Language selection
lang = st.sidebar.selectbox("🌐 Language / Langue", ["English", "Français"])
is_fr = lang == "Français"

# Translations
t = {
    "title": "AynalyxAI Demo" if not is_fr else "Démo AynalyxAI",
    "subtitle": "AI-Powered Anomaly Detection" if not is_fr else "Détection d'Anomalies par IA",
    "demo_notice": "⚡ This is a FREE online demo. Get the full desktop version for unlimited analysis!" if not is_fr else "⚡ Ceci est une démo GRATUITE. Obtenez la version desktop complète pour une analyse illimitée!",
    "upload": "Upload your CSV or Excel file" if not is_fr else "Téléchargez votre fichier CSV ou Excel",
    "or_try": "Or try with sample data:" if not is_fr else "Ou essayez avec des données d'exemple:",
    "sample_invoices": "📄 Invoices" if not is_fr else "📄 Factures",
    "sample_expenses": "💰 Expenses" if not is_fr else "💰 Dépenses",
    "sample_payroll": "👥 Payroll" if not is_fr else "👥 Paie",
    "sample_inventory": "📦 Inventory" if not is_fr else "📦 Inventaire",
    "select_columns": "Select numeric columns to analyze" if not is_fr else "Sélectionnez les colonnes numériques à analyser",
    "sensitivity": "Detection Sensitivity" if not is_fr else "Sensibilité de Détection",
    "run_analysis": "🔍 Run Anomaly Detection" if not is_fr else "🔍 Lancer la Détection",
    "results": "Analysis Results" if not is_fr else "Résultats de l'Analyse",
    "anomalies_found": "anomalies detected" if not is_fr else "anomalies détectées",
    "download_excel": "📥 Download Results (Excel)" if not is_fr else "📥 Télécharger les Résultats (Excel)",
    "get_full": "🚀 Get Full Version - $79" if not is_fr else "🚀 Obtenir la Version Complète - 79$",
    "data_preview": "Data Preview" if not is_fr else "Aperçu des Données",
    "high": "High" if not is_fr else "Élevée",
    "medium": "Medium" if not is_fr else "Moyenne", 
    "low": "Low" if not is_fr else "Faible",
}

# Header
st.markdown(f"""
<div class="main-header">
    <h1>🔬 {t['title']}</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">{t['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Demo notice
st.markdown(f'<div class="demo-badge">{t["demo_notice"]}</div>', unsafe_allow_html=True)

# Sample data generators
def generate_sample_invoices():
    np.random.seed(42)
    n = 100
    data = {
        'Invoice_ID': [f'INV-{1000+i}' for i in range(n)],
        'Client': np.random.choice(['Acme Corp', 'TechStart Inc', 'Global Services', 'Local Shop', 'Big Enterprise'], n),
        'Amount': np.concatenate([np.random.normal(1500, 500, n-5), [15000, 25, 18000, 12, 22000]]),  # Some anomalies
        'Quantity': np.concatenate([np.random.randint(1, 20, n-3), [150, 200, 1]]),  # Some anomalies
        'Date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    }
    return pd.DataFrame(data)

def generate_sample_expenses():
    np.random.seed(43)
    n = 80
    data = {
        'Expense_ID': [f'EXP-{2000+i}' for i in range(n)],
        'Category': np.random.choice(['Travel', 'Office Supplies', 'Software', 'Marketing', 'Utilities'], n),
        'Vendor': np.random.choice(['Amazon', 'Office Depot', 'Google Ads', 'Airlines Inc', 'Power Co'], n),
        'Amount': np.concatenate([np.random.normal(250, 100, n-4), [5000, 8, 7500, 3]]),  # Anomalies
        'Date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    }
    return pd.DataFrame(data)

def generate_sample_payroll():
    np.random.seed(44)
    n = 50
    data = {
        'Employee_ID': [f'EMP-{100+i}' for i in range(n)],
        'Department': np.random.choice(['Sales', 'Engineering', 'HR', 'Marketing', 'Finance'], n),
        'Salary': np.concatenate([np.random.normal(5000, 1000, n-3), [25000, 500, 30000]]),  # Anomalies
        'Hours': np.concatenate([np.random.normal(160, 10, n-2), [250, 40]]),  # Anomalies
        'Bonus': np.concatenate([np.random.normal(500, 200, n-2), [5000, 0]])
    }
    return pd.DataFrame(data)

def generate_sample_inventory():
    np.random.seed(45)
    n = 60
    data = {
        'SKU': [f'SKU-{3000+i}' for i in range(n)],
        'Product': np.random.choice(['Widget A', 'Gadget B', 'Tool C', 'Part D', 'Supply E'], n),
        'Quantity': np.concatenate([np.random.randint(50, 500, n-4), [5000, 2, 8000, 1]]),  # Anomalies
        'Unit_Cost': np.concatenate([np.random.normal(25, 10, n-3), [500, 1, 800]]),  # Anomalies
        'Total_Value': np.zeros(n)  # Will calculate
    }
    df = pd.DataFrame(data)
    df['Total_Value'] = df['Quantity'] * df['Unit_Cost']
    return df

# Sidebar - Data Selection
st.sidebar.header("📊 " + ("Data Source" if not is_fr else "Source de Données"))

# File upload
uploaded_file = st.sidebar.file_uploader(t['upload'], type=['csv', 'xlsx', 'xls'])

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{t['or_try']}**")

# Sample data buttons
col1, col2 = st.sidebar.columns(2)
sample_type = None
with col1:
    if st.button(t['sample_invoices'], use_container_width=True):
        sample_type = 'invoices'
    if st.button(t['sample_payroll'], use_container_width=True):
        sample_type = 'payroll'
with col2:
    if st.button(t['sample_expenses'], use_container_width=True):
        sample_type = 'expenses'
    if st.button(t['sample_inventory'], use_container_width=True):
        sample_type = 'inventory'

# Store sample type in session state
if sample_type:
    st.session_state['sample_type'] = sample_type

# Load data
df = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state['df'] = df
    except Exception as e:
        st.error(f"Error loading file: {e}")
elif 'sample_type' in st.session_state:
    sample = st.session_state['sample_type']
    if sample == 'invoices':
        df = generate_sample_invoices()
    elif sample == 'expenses':
        df = generate_sample_expenses()
    elif sample == 'payroll':
        df = generate_sample_payroll()
    elif sample == 'inventory':
        df = generate_sample_inventory()
    st.session_state['df'] = df
elif 'df' in st.session_state:
    df = st.session_state['df']

# Main content
if df is not None:
    st.subheader(f"📋 {t['data_preview']}")
    st.dataframe(df.head(10), use_container_width=True)
    st.caption(f"Showing 10 of {len(df)} rows")
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        st.markdown("---")
        
        # Column selection
        selected_cols = st.multiselect(
            t['select_columns'],
            numeric_cols,
            default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols
        )
        
        # Sensitivity slider
        sensitivity = st.slider(t['sensitivity'], 1.0, 3.0, 2.0, 0.1)
        
        if selected_cols and st.button(t['run_analysis'], type="primary"):
            with st.spinner("Analyzing..." if not is_fr else "Analyse en cours..."):
                # Simple anomaly detection using Z-score
                results = df.copy()
                results['Anomaly_Score'] = 0.0
                results['Anomaly_Level'] = 'Normal'
                
                for col in selected_cols:
                    mean = df[col].mean()
                    std = df[col].std()
                    if std > 0:
                        z_scores = np.abs((df[col] - mean) / std)
                        results['Anomaly_Score'] = np.maximum(results['Anomaly_Score'], z_scores)
                
                # Classify anomalies
                results.loc[results['Anomaly_Score'] > sensitivity, 'Anomaly_Level'] = t['low']
                results.loc[results['Anomaly_Score'] > sensitivity + 0.5, 'Anomaly_Level'] = t['medium']
                results.loc[results['Anomaly_Score'] > sensitivity + 1.0, 'Anomaly_Level'] = t['high']
                
                # Filter to show only anomalies
                anomalies = results[results['Anomaly_Level'] != 'Normal'].sort_values('Anomaly_Score', ascending=False)
                
                st.markdown("---")
                st.subheader(f"🎯 {t['results']}")
                
                # Stats
                n_anomalies = len(anomalies)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🔴 " + t['high'], len(anomalies[anomalies['Anomaly_Level'] == t['high']]))
                with col2:
                    st.metric("🟡 " + t['medium'], len(anomalies[anomalies['Anomaly_Level'] == t['medium']]))
                with col3:
                    st.metric("🟢 " + t['low'], len(anomalies[anomalies['Anomaly_Level'] == t['low']]))
                
                st.success(f"✅ {n_anomalies} {t['anomalies_found']}")
                
                if n_anomalies > 0:
                    # Show anomalies table
                    st.dataframe(anomalies, use_container_width=True)
                    
                    # Download button
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        anomalies.to_excel(writer, index=False, sheet_name='Anomalies')
                    output.seek(0)
                    
                    st.download_button(
                        label=t['download_excel'],
                        data=output,
                        file_name="aynalyxai_anomalies.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                # CTA for full version
                st.markdown("---")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 2rem; border-radius: 15px; text-align: center; border: 2px solid #667eea;">
                    <h3>🚀 Want More Features?</h3>
                    <p>The full desktop version includes:</p>
                    <ul style="text-align: left; max-width: 400px; margin: 1rem auto;">
                        <li>✅ Advanced AI (Isolation Forest) detection</li>
                        <li>✅ Data aggregation & grouping</li>
                        <li>✅ Custom ratio analysis</li>
                        <li>✅ 100% offline - your data stays private</li>
                        <li>✅ Unlimited file size</li>
                    </ul>
                    <a href="https://mubsira.gumroad.com/l/aynalyxai" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; margin-top: 1rem;">
                        🚀 Get Full Version - $79 (One-time)
                    </a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No numeric columns found in this file." if not is_fr else "Aucune colonne numérique trouvée dans ce fichier.")
else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: #f8f9fc; border-radius: 15px;">
        <h2>👆 Get Started</h2>
        <p style="font-size: 1.1rem; color: #666;">
            Upload a file or click a sample data button in the sidebar to begin.
        </p>
    </div>
    """ if not is_fr else """
    <div style="text-align: center; padding: 3rem; background: #f8f9fc; border-radius: 15px;">
        <h2>👆 Commencer</h2>
        <p style="font-size: 1.1rem; color: #666;">
            Téléchargez un fichier ou cliquez sur un bouton de données d'exemple dans la barre latérale.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>© 2025 Mubsira Analytics | <a href="https://mubsira.gumroad.com/l/aynalyxai" target="_blank">Get Full Version</a></p>
</div>
""", unsafe_allow_html=True)
