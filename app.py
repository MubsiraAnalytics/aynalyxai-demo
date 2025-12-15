# AynalyxAI Demo - Streamlit Cloud Version
# Sample data only - no file upload

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Page config - WIDE layout for better visibility
st.set_page_config(
    page_title="AynalyxAI Demo",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for wider sidebar and colored results
st.markdown("""
<style>
    /* Wider sidebar */
    [data-testid="stSidebar"] {
        min-width: 320px;
        max-width: 400px;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Demo notice */
    .demo-badge {
        background: #fef3c7;
        color: #92400e;
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        font-weight: 600;
        display: block;
        text-align: center;
        margin-bottom: 1.5rem;
        border: 2px solid #f59e0b;
    }
    
    /* Sample buttons styling */
    .sample-btn-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 1rem 0;
    }
    
    /* Anomaly level colors - matching real app */
    .anomaly-critical {
        background-color: #dc2626 !important;
        color: white !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    .anomaly-high {
        background-color: #ef4444 !important;
        color: white !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    .anomaly-medium {
        background-color: #f59e0b !important;
        color: white !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    .anomaly-low {
        background-color: #22c55e !important;
        color: white !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    /* Results table styling */
    .results-container {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid;
    }
    
    .stat-critical { border-color: #dc2626; }
    .stat-high { border-color: #ef4444; }
    .stat-medium { border-color: #f59e0b; }
    .stat-low { border-color: #22c55e; }
    
    /* Sidebar title */
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* CTA Box */
    .cta-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #667eea;
        margin-top: 2rem;
    }
    
    .cta-box h3 {
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .cta-button {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 1rem;
    }
    
    /* Hide file uploader completely */
    .stFileUploader {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Language selection in sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-title">🌐 Language / Langue</p>', unsafe_allow_html=True)
    lang = st.selectbox("", ["English", "Français"], label_visibility="collapsed")
    is_fr = lang == "Français"

# Translations
t = {
    "title": "AynalyxAI Demo" if not is_fr else "Démo AynalyxAI",
    "subtitle": "AI-Powered Anomaly Detection" if not is_fr else "Détection d'Anomalies par IA",
    "demo_notice": "🎯 FREE DEMO — Try with our sample data below!" if not is_fr else "🎯 DÉMO GRATUITE — Essayez avec nos données d'exemple ci-dessous!",
    "sample_title": "📊 Select Sample Data" if not is_fr else "📊 Sélectionner des Données",
    "sample_invoices": "📄 Invoices" if not is_fr else "📄 Factures",
    "sample_expenses": "💰 Expenses" if not is_fr else "💰 Dépenses",
    "sample_payroll": "👥 Payroll" if not is_fr else "👥 Paie",
    "sample_inventory": "📦 Inventory" if not is_fr else "📦 Inventaire",
    "run_analysis": "🔍 Run Anomaly Detection" if not is_fr else "🔍 Lancer la Détection",
    "results": "🎯 Detection Results" if not is_fr else "🎯 Résultats de Détection",
    "anomalies_found": "anomalies detected" if not is_fr else "anomalies détectées",
    "download_excel": "📥 Download Results (Excel)" if not is_fr else "📥 Télécharger (Excel)",
    "data_preview": "📋 Data Preview" if not is_fr else "📋 Aperçu des Données",
    "critical": "CRITICAL" if not is_fr else "CRITIQUE",
    "high": "HIGH" if not is_fr else "ÉLEVÉ",
    "medium": "MEDIUM" if not is_fr else "MOYEN", 
    "low": "LOW" if not is_fr else "FAIBLE",
    "normal": "Normal" if not is_fr else "Normal",
    "explanation": "Explanation" if not is_fr else "Explication",
    "level": "Level" if not is_fr else "Niveau",
    "score": "Score" if not is_fr else "Score",
    "welcome_title": "👈 Select Sample Data to Begin" if not is_fr else "👈 Sélectionnez des Données pour Commencer",
    "welcome_text": "Click one of the 4 sample data buttons in the sidebar to see the AI anomaly detection in action." if not is_fr else "Cliquez sur l'un des 4 boutons de données dans la barre latérale pour voir la détection d'anomalies en action.",
    "get_full": "Get Full Desktop Version" if not is_fr else "Obtenir la Version Complète",
    "full_features": "The full version includes: Advanced AI (Isolation Forest), Data Aggregation, Custom Ratios, 100% Offline Privacy, Unlimited Files" if not is_fr else "La version complète inclut: IA Avancée (Isolation Forest), Agrégation, Ratios Personnalisés, 100% Hors-ligne, Fichiers Illimités",
}

# Explanation templates
def get_explanation(value, mean, std, col_name, is_fr):
    z_score = abs((value - mean) / std) if std > 0 else 0
    pct_diff = ((value - mean) / mean * 100) if mean != 0 else 0
    
    if z_score > 3:
        if value > mean:
            return f"{'Valeur EXTRÊME:' if is_fr else 'EXTREME value:'} {value:,.2f} {'est' if is_fr else 'is'} {abs(pct_diff):.0f}% {'au-dessus de la moyenne' if is_fr else 'above average'} ({mean:,.2f}). {'Score Z:' if is_fr else 'Z-score:'} {z_score:.1f}"
        else:
            return f"{'Valeur EXTRÊME:' if is_fr else 'EXTREME value:'} {value:,.2f} {'est' if is_fr else 'is'} {abs(pct_diff):.0f}% {'en-dessous de la moyenne' if is_fr else 'below average'} ({mean:,.2f}). {'Score Z:' if is_fr else 'Z-score:'} {z_score:.1f}"
    elif z_score > 2.5:
        if value > mean:
            return f"{'Très élevé:' if is_fr else 'Very high:'} {value:,.2f} {'dépasse la moyenne de' if is_fr else 'exceeds average by'} {abs(pct_diff):.0f}% ({mean:,.2f})"
        else:
            return f"{'Très bas:' if is_fr else 'Very low:'} {value:,.2f} {'est inférieur à la moyenne de' if is_fr else 'is below average by'} {abs(pct_diff):.0f}% ({mean:,.2f})"
    elif z_score > 2:
        return f"{'Valeur inhabituelle:' if is_fr else 'Unusual value:'} {value:,.2f} {'vs moyenne' if is_fr else 'vs average'} {mean:,.2f} ({'+' if pct_diff > 0 else ''}{pct_diff:.0f}%)"
    else:
        return f"{'Légèrement atypique:' if is_fr else 'Slightly unusual:'} {value:,.2f} {'vs moyenne' if is_fr else 'vs average'} {mean:,.2f}"

# Sample data generators with realistic anomalies
def generate_sample_invoices():
    np.random.seed(42)
    n = 100
    
    # Normal data
    amounts = np.random.normal(1500, 400, n-8)
    quantities = np.random.randint(1, 25, n-8)
    
    # Add clear anomalies
    anomaly_amounts = [18500, 22000, 15, 8, 19800, 25, 16500, 12]  # High and low anomalies
    anomaly_quantities = [180, 250, 1, 1, 200, 1, 150, 1]
    
    all_amounts = np.concatenate([amounts, anomaly_amounts])
    all_quantities = np.concatenate([quantities, anomaly_quantities])
    
    data = {
        'Invoice_ID': [f'INV-{1000+i}' for i in range(n)],
        'Client': np.random.choice(['Acme Corp', 'TechStart Inc', 'Global Services', 'Local Shop', 'Big Enterprise', 'Quick Mart', 'Pro Solutions'], n),
        'Amount': all_amounts,
        'Quantity': all_quantities,
        'Date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    }
    return pd.DataFrame(data)

def generate_sample_expenses():
    np.random.seed(43)
    n = 80
    
    amounts = np.random.normal(280, 120, n-6)
    anomaly_amounts = [5800, 7200, 5, 3, 6500, 8]  # Anomalies
    all_amounts = np.concatenate([amounts, anomaly_amounts])
    
    data = {
        'Expense_ID': [f'EXP-{2000+i}' for i in range(n)],
        'Category': np.random.choice(['Travel', 'Office Supplies', 'Software', 'Marketing', 'Utilities', 'Meals'], n),
        'Vendor': np.random.choice(['Amazon', 'Office Depot', 'Google Ads', 'Airlines Inc', 'Power Co', 'Staples'], n),
        'Amount': all_amounts,
        'Date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    }
    return pd.DataFrame(data)

def generate_sample_payroll():
    np.random.seed(44)
    n = 50
    
    salaries = np.random.normal(5200, 800, n-5)
    hours = np.random.normal(160, 12, n-5)
    bonuses = np.random.normal(400, 150, n-5)
    
    # Anomalies
    anomaly_salaries = [28000, 32000, 450, 380, 26000]
    anomaly_hours = [280, 310, 35, 42, 260]
    anomaly_bonuses = [8500, 12000, 0, 0, 9000]
    
    data = {
        'Employee_ID': [f'EMP-{100+i}' for i in range(n)],
        'Department': np.random.choice(['Sales', 'Engineering', 'HR', 'Marketing', 'Finance', 'Operations'], n),
        'Salary': np.concatenate([salaries, anomaly_salaries]),
        'Hours_Worked': np.concatenate([hours, anomaly_hours]),
        'Bonus': np.concatenate([bonuses, anomaly_bonuses])
    }
    return pd.DataFrame(data)

def generate_sample_inventory():
    np.random.seed(45)
    n = 60
    
    quantities = np.random.randint(80, 400, n-6)
    unit_costs = np.random.normal(28, 8, n-6)
    
    # Anomalies
    anomaly_qty = [5500, 8200, 2, 1, 6800, 3]
    anomaly_cost = [380, 520, 2, 1, 450, 3]
    
    data = {
        'SKU': [f'SKU-{3000+i}' for i in range(n)],
        'Product': np.random.choice(['Widget A', 'Gadget B', 'Tool C', 'Part D', 'Supply E', 'Component F'], n),
        'Quantity': np.concatenate([quantities, anomaly_qty]),
        'Unit_Cost': np.concatenate([unit_costs, anomaly_cost]),
    }
    df = pd.DataFrame(data)
    df['Total_Value'] = df['Quantity'] * df['Unit_Cost']
    return df

# Header
st.markdown(f"""
<div class="main-header">
    <h1>🔬 {t['title']}</h1>
    <p>{t['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Demo notice
st.markdown(f'<div class="demo-badge">{t["demo_notice"]}</div>', unsafe_allow_html=True)

# Sidebar - Sample Data Selection (NO FILE UPLOAD)
with st.sidebar:
    st.markdown("---")
    st.markdown(f'<p class="sidebar-title">{t["sample_title"]}</p>', unsafe_allow_html=True)
    
    # 2x2 grid of sample buttons
    col1, col2 = st.columns(2)
    
    with col1:
        btn_invoices = st.button(t['sample_invoices'], use_container_width=True, type="primary")
        btn_payroll = st.button(t['sample_payroll'], use_container_width=True, type="primary")
    
    with col2:
        btn_expenses = st.button(t['sample_expenses'], use_container_width=True, type="primary")
        btn_inventory = st.button(t['sample_inventory'], use_container_width=True, type="primary")
    
    # Track which sample is selected
    if btn_invoices:
        st.session_state['sample_type'] = 'invoices'
        st.session_state['auto_run'] = True
    elif btn_expenses:
        st.session_state['sample_type'] = 'expenses'
        st.session_state['auto_run'] = True
    elif btn_payroll:
        st.session_state['sample_type'] = 'payroll'
        st.session_state['auto_run'] = True
    elif btn_inventory:
        st.session_state['sample_type'] = 'inventory'
        st.session_state['auto_run'] = True

# Load data based on selection
df = None
data_name = ""
if 'sample_type' in st.session_state:
    sample = st.session_state['sample_type']
    if sample == 'invoices':
        df = generate_sample_invoices()
        data_name = "Invoices" if not is_fr else "Factures"
    elif sample == 'expenses':
        df = generate_sample_expenses()
        data_name = "Expenses" if not is_fr else "Dépenses"
    elif sample == 'payroll':
        df = generate_sample_payroll()
        data_name = "Payroll" if not is_fr else "Paie"
    elif sample == 'inventory':
        df = generate_sample_inventory()
        data_name = "Inventory" if not is_fr else "Inventaire"

# Main content
if df is not None:
    # Data preview
    st.subheader(f"{t['data_preview']} — {data_name}")
    st.dataframe(df.head(10), use_container_width=True, height=300)
    st.caption(f"{'Affichage de 10 sur' if is_fr else 'Showing 10 of'} {len(df)} {'lignes' if is_fr else 'rows'}")
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Auto-run analysis when sample is selected
    if numeric_cols and st.session_state.get('auto_run', False):
        st.session_state['auto_run'] = False
        
        st.markdown("---")
        st.subheader(t['results'])
        
        with st.spinner("🔍 " + ("Analyse en cours..." if is_fr else "Analyzing...")):
            # Perform anomaly detection
            results = df.copy()
            results['Anomaly_Score'] = 0.0
            results['Anomaly_Level'] = t['normal']
            results['Anomaly_Explanation'] = ""
            
            # Calculate anomaly scores for each numeric column
            explanations = []
            for idx in range(len(df)):
                row_explanations = []
                max_score = 0
                for col in numeric_cols:
                    mean = df[col].mean()
                    std = df[col].std()
                    if std > 0:
                        z_score = abs((df[col].iloc[idx] - mean) / std)
                        if z_score > max_score:
                            max_score = z_score
                        if z_score > 1.8:  # Only explain significant deviations
                            row_explanations.append(f"[{col}] " + get_explanation(df[col].iloc[idx], mean, std, col, is_fr))
                
                results.loc[idx, 'Anomaly_Score'] = max_score
                results.loc[idx, 'Anomaly_Explanation'] = " | ".join(row_explanations) if row_explanations else ""
            
            # Classify anomaly levels with colors
            results.loc[results['Anomaly_Score'] > 3.0, 'Anomaly_Level'] = t['critical']
            results.loc[(results['Anomaly_Score'] > 2.5) & (results['Anomaly_Score'] <= 3.0), 'Anomaly_Level'] = t['high']
            results.loc[(results['Anomaly_Score'] > 2.0) & (results['Anomaly_Score'] <= 2.5), 'Anomaly_Level'] = t['medium']
            results.loc[(results['Anomaly_Score'] > 1.8) & (results['Anomaly_Score'] <= 2.0), 'Anomaly_Level'] = t['low']
            
            # Filter to anomalies only and sort by score
            anomalies = results[results['Anomaly_Level'] != t['normal']].sort_values('Anomaly_Score', ascending=False)
            
            # Count by level
            n_critical = len(anomalies[anomalies['Anomaly_Level'] == t['critical']])
            n_high = len(anomalies[anomalies['Anomaly_Level'] == t['high']])
            n_medium = len(anomalies[anomalies['Anomaly_Level'] == t['medium']])
            n_low = len(anomalies[anomalies['Anomaly_Level'] == t['low']])
            n_total = len(anomalies)
            
            # Statistics cards
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.markdown(f"""
                <div class="stat-card stat-critical">
                    <div style="font-size: 2rem; font-weight: bold; color: #dc2626;">{n_critical}</div>
                    <div style="color: #666;">🔴 {t['critical']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stat-card stat-high">
                    <div style="font-size: 2rem; font-weight: bold; color: #ef4444;">{n_high}</div>
                    <div style="color: #666;">🟠 {t['high']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="stat-card stat-medium">
                    <div style="font-size: 2rem; font-weight: bold; color: #f59e0b;">{n_medium}</div>
                    <div style="color: #666;">🟡 {t['medium']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="stat-card stat-low">
                    <div style="font-size: 2rem; font-weight: bold; color: #22c55e;">{n_low}</div>
                    <div style="color: #666;">🟢 {t['low']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col5:
                st.markdown(f"""
                <div class="stat-card" style="border-color: #667eea;">
                    <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{n_total}</div>
                    <div style="color: #666;">📊 Total</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if n_total > 0:
                # Create colored display dataframe
                display_df = anomalies.copy()
                display_df['Anomaly_Score'] = display_df['Anomaly_Score'].round(2)
                
                # Rename columns for display
                col_rename = {
                    'Anomaly_Level': t['level'],
                    'Anomaly_Score': t['score'],
                    'Anomaly_Explanation': t['explanation']
                }
                display_df = display_df.rename(columns=col_rename)
                
                # Apply color styling function
                def color_level(val):
                    if val == t['critical']:
                        return 'background-color: #dc2626; color: white; font-weight: bold;'
                    elif val == t['high']:
                        return 'background-color: #ef4444; color: white; font-weight: bold;'
                    elif val == t['medium']:
                        return 'background-color: #f59e0b; color: white; font-weight: bold;'
                    elif val == t['low']:
                        return 'background-color: #22c55e; color: white; font-weight: bold;'
                    return ''
                
                def color_row(row):
                    level = row[t['level']]
                    if level == t['critical']:
                        return ['background-color: #fee2e2;'] * len(row)
                    elif level == t['high']:
                        return ['background-color: #fef2f2;'] * len(row)
                    elif level == t['medium']:
                        return ['background-color: #fffbeb;'] * len(row)
                    elif level == t['low']:
                        return ['background-color: #f0fdf4;'] * len(row)
                    return [''] * len(row)
                
                # Style and display ALL results
                styled_df = display_df.style.apply(color_row, axis=1).applymap(
                    color_level, subset=[t['level']]
                )
                
                st.dataframe(styled_df, use_container_width=True, height=500)
                
                # Download button
                st.markdown("<br>", unsafe_allow_html=True)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    display_df.to_excel(writer, index=False, sheet_name='Anomalies')
                output.seek(0)
                
                st.download_button(
                    label=t['download_excel'],
                    data=output,
                    file_name=f"aynalyxai_{data_name.lower()}_anomalies.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )
            else:
                st.success("✅ " + ("Aucune anomalie détectée!" if is_fr else "No anomalies detected!"))
        
        # CTA Box
        st.markdown(f"""
        <div class="cta-box">
            <h3>🚀 {t['get_full']}</h3>
            <p style="color: #555; font-size: 0.95rem;">{t['full_features']}</p>
            <a href="https://mubsira.gumroad.com/l/aynalyxai" target="_blank" class="cta-button">
                💎 {'Obtenir AynalyxAI Pro — 79 $' if is_fr else 'Get AynalyxAI Pro — $79'}
            </a>
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome screen when no data selected
    st.markdown(f"""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 16px; margin-top: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">👈</div>
        <h2 style="color: #1e293b; margin-bottom: 1rem;">{t['welcome_title']}</h2>
        <p style="font-size: 1.1rem; color: #64748b; max-width: 500px; margin: 0 auto;">
            {t['welcome_text']}
        </p>
        <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span style="background: #667eea20; color: #667eea; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500;">📄 {'Factures' if is_fr else 'Invoices'}</span>
            <span style="background: #667eea20; color: #667eea; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500;">💰 {'Dépenses' if is_fr else 'Expenses'}</span>
            <span style="background: #667eea20; color: #667eea; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500;">👥 {'Paie' if is_fr else 'Payroll'}</span>
            <span style="background: #667eea20; color: #667eea; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500;">📦 {'Inventaire' if is_fr else 'Inventory'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; padding: 1rem;">
    <p>© 2025 Mubsira Analytics | <a href="https://mubsira.gumroad.com/l/aynalyxai" target="_blank" style="color: #667eea;">Get Full Version — $79</a></p>
</div>
""", unsafe_allow_html=True)
