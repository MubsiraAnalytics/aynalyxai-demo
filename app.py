"""
AynalyxAI - Interactive Demo
Streamlit-based demo for the AynalyxAI anomaly detection tool.
"""

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Page config
st.set_page_config(
    page_title="AynalyxAI Demo",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0d9488;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .highlight-box {
        background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 100%);
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 4px solid #0d9488;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔍 AynalyxAI Demo</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload any spreadsheet with headers. Get instant anomaly detection.</p>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="highlight-box">
    <strong>💡 How it works:</strong> Upload an Excel or CSV file with headers. 
    Select numeric columns to analyze. Get a color-coded report showing unusual values.
</div>
""", unsafe_allow_html=True)


def detect_anomalies(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    """
    Detect anomalies using Z-score based multi-column analysis.
    Same logic as the main AynalyxAI application.
    """
    result_df = df.copy()
    n_rows = len(result_df)
    
    if n_rows == 0 or len(numeric_cols) == 0:
        result_df['Anomaly_Level'] = 'Normal'
        result_df['Anomaly_Deviation'] = 0.0
        result_df['Anomaly_AI_Score'] = 0.0
        result_df['Anomaly_Explanation'] = 'No numeric data to analyze'
        return result_df
    
    # Initialize score tracking
    composite_scores = np.zeros(n_rows)
    max_deviations = np.zeros(n_rows)
    anomaly_reasons = [[] for _ in range(n_rows)]
    
    # Analyze each numeric column using Z-scores
    for col in numeric_cols:
        if col not in result_df.columns:
            continue
            
        values = pd.to_numeric(result_df[col], errors='coerce')
        
        if values.isna().all() or values.std() == 0:
            continue
        
        mean_val = values.mean()
        std_val = values.std()
        
        if std_val == 0 or pd.isna(std_val):
            continue
        
        # Calculate Z-scores
        z_scores = np.abs((values - mean_val) / std_val)
        z_scores = z_scores.fillna(0)
        
        # Calculate percentage deviation from mean
        with np.errstate(divide='ignore', invalid='ignore'):
            pct_deviation = np.abs((values - mean_val) / mean_val) * 100
            pct_deviation = pct_deviation.fillna(0)
            pct_deviation = np.where(np.isinf(pct_deviation), 0, pct_deviation)
        
        max_deviations = np.maximum(max_deviations, pct_deviation)
        composite_scores += z_scores * 10
        
        for idx in range(n_rows):
            z = z_scores.iloc[idx] if hasattr(z_scores, 'iloc') else z_scores[idx]
            if z > 2:
                val = values.iloc[idx] if hasattr(values, 'iloc') else values[idx]
                direction = "above" if val > mean_val else "below"
                anomaly_reasons[idx].append(f"{col}: {z:.1f}σ {direction} mean")
    
    # Normalize composite score to 0-100
    if composite_scores.max() > 0:
        ai_scores = (composite_scores / composite_scores.max()) * 100
    else:
        ai_scores = np.zeros(n_rows)
    
    # Determine anomaly levels
    levels = []
    for score in ai_scores:
        if score >= 80:
            levels.append('Critical')
        elif score >= 60:
            levels.append('High')
        elif score >= 40:
            levels.append('Medium')
        elif score >= 20:
            levels.append('Low')
        else:
            levels.append('Normal')
    
    # Generate explanations
    explanations = []
    for idx, reasons in enumerate(anomaly_reasons):
        if not reasons:
            explanations.append("Values within normal range")
        elif len(reasons) == 1:
            explanations.append(f"Unusual: {reasons[0]}")
        else:
            explanations.append(f"Multiple anomalies: {'; '.join(reasons[:3])}")
    
    # Add analytics columns
    result_df['Anomaly_Level'] = levels
    result_df['Anomaly_Deviation'] = np.round(max_deviations, 2)
    result_df['Anomaly_AI_Score'] = np.round(ai_scores, 1)
    result_df['Anomaly_Explanation'] = explanations
    
    # Sort by AI Score descending
    result_df = result_df.sort_values('Anomaly_AI_Score', ascending=False).reset_index(drop=True)
    
    return result_df


def style_anomaly_level(val):
    """Color-code the anomaly level."""
    colors = {
        'Critical': 'background-color: #fecaca; color: #991b1b; font-weight: bold',
        'High': 'background-color: #fed7aa; color: #9a3412; font-weight: bold',
        'Medium': 'background-color: #fef08a; color: #854d0e',
        'Low': 'background-color: #d9f99d; color: #3f6212',
        'Normal': 'background-color: #bbf7d0; color: #166534'
    }
    return colors.get(val, '')


def to_excel(df):
    """Convert DataFrame to Excel bytes."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Anomaly Report')
    return output.getvalue()


# File upload
st.markdown("### 📁 Upload Your File")
uploaded_file = st.file_uploader(
    "Drop your Excel or CSV file here",
    type=['xlsx', 'xls', 'csv'],
    help="File must have headers in the first row"
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Loaded **{uploaded_file.name}** — {len(df):,} rows × {len(df.columns)} columns")
        
        with st.expander("📋 Preview Raw Data", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.warning("⚠️ No numeric columns detected.")
        else:
            st.markdown("### ⚙️ Select Columns to Analyze")
            
            selected_cols = st.multiselect(
                "Choose numeric columns for anomaly detection:",
                options=numeric_cols,
                default=numeric_cols[:5] if len(numeric_cols) > 5 else numeric_cols
            )
            
            if selected_cols:
                if st.button("🔍 Detect Anomalies", type="primary", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        results_df = detect_anomalies(df, selected_cols)
                        st.session_state['results'] = results_df
                        st.session_state['analyzed'] = True
        
        if st.session_state.get('analyzed') and 'results' in st.session_state:
            results_df = st.session_state['results']
            
            st.markdown("---")
            st.markdown("### 📊 Analysis Results")
            
            # Summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            level_counts = results_df['Anomaly_Level'].value_counts()
            
            with col1:
                st.metric("🔴 Critical", level_counts.get('Critical', 0))
            with col2:
                st.metric("🟠 High", level_counts.get('High', 0))
            with col3:
                st.metric("🟡 Medium", level_counts.get('Medium', 0))
            with col4:
                st.metric("🟢 Low", level_counts.get('Low', 0))
            with col5:
                st.metric("✅ Normal", level_counts.get('Normal', 0))
            
            st.markdown("---")
            
            # Reorder: original columns first, analytics columns last
            analytics_cols = ['Anomaly_Level', 'Anomaly_Deviation', 'Anomaly_AI_Score', 'Anomaly_Explanation']
            original_cols = [c for c in results_df.columns if c not in analytics_cols]
            ordered_cols = original_cols + analytics_cols
            results_display = results_df[ordered_cols]
            
            styled_df = results_display.style.applymap(
                style_anomaly_level, subset=['Anomaly_Level']
            )
            
            st.dataframe(styled_df, use_container_width=True, height=400)
            
            # Download
            st.markdown("---")
            excel_data = to_excel(results_display)
            st.download_button(
                label="📥 Download Report (Excel)",
                data=excel_data,
                file_name=f"AynalyxAI_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")

else:
    st.info("👆 Upload a file to get started. Supports Excel (.xlsx, .xls) and CSV files.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.85rem;">
    <p>🔒 This is a limited online demo. The full desktop version offers 100% offline privacy.</p>
    <p>© 2025 Mubsira Analytics</p>
</div>
""", unsafe_allow_html=True)
