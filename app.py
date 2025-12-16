# AynalyxAI Demo - Streamlit Cloud Version
# Sample data only - no file upload

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from openpyxl.styles import PatternFill, Font, Border, Side

st.set_page_config(page_title="AynalyxAI Demo", page_icon="", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    [data-testid="stSidebar"] { min-width: 320px; max-width: 400px; }
    .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 1.5rem; }
    .main-header h1 { margin: 0; font-size: 2.5rem; }
    .main-header p { margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.1rem; }
    .demo-badge { background: #fef3c7; color: #92400e; padding: 0.75rem 1.25rem; border-radius: 10px; font-weight: 600; display: block; text-align: center; margin-bottom: 1.5rem; border: 2px solid #f59e0b; }
    .feature-box { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #0ea5e9; }
    .feature-box h3 { color: #0369a1; margin: 0 0 0.5rem 0; }
    .feature-box p { color: #475569; margin: 0; line-height: 1.6; }
    .stat-card { background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid; }
    .stat-critical { border-color: #dc2626; }
    .stat-high { border-color: #f59e0b; }
    .stat-low { border-color: #22c55e; }
    .sidebar-title { font-size: 1.3rem; font-weight: bold; color: #1e293b; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #667eea; }
    .how-it-works { background: #f8fafc; padding: 1.25rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #e2e8f0; }
    .cta-box { background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1.5rem; border-radius: 12px; text-align: center; border: 2px solid #667eea; margin-top: 2rem; }
    .cta-box h3 { color: #667eea; margin-bottom: 0.5rem; }
    .cta-button { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white !important; padding: 0.75rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: bold; margin-top: 1rem; }
    .advantage-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0; }
    .advantage-item { background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
    .advantage-item .icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .advantage-item h4 { color: #334155; margin: 0 0 0.25rem 0; font-size: 0.95rem; }
    .advantage-item p { color: #64748b; margin: 0; font-size: 0.85rem; }
    div[data-testid="stDataFrame"] > div { width: 100% !important; }
    div[data-testid="stDataFrame"] table { width: 100% !important; table-layout: fixed !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p class="sidebar-title"> Language / Langue</p>', unsafe_allow_html=True)
    lang = st.selectbox("", ["English", "Francais"], label_visibility="collapsed")
    is_fr = lang == "Francais"

t = {
    "title": "AynalyxAI Demo" if not is_fr else "Demo AynalyxAI",
    "subtitle": "AI-Powered Financial Anomaly Detection" if not is_fr else "Detection d Anomalies Financieres par IA",
    "demo_notice": " FREE DEMO - Test our AI with sample financial data!" if not is_fr else " DEMO GRATUITE - Testez notre IA!",
    "sample_title": " Select Sample Data" if not is_fr else " Choisir des Donnees",
    "sample_invoices": " Invoices" if not is_fr else " Factures",
    "sample_expenses": " Expenses" if not is_fr else " Depenses",
    "sample_payroll": " Payroll" if not is_fr else " Paie",
    "sample_inventory": " Inventory" if not is_fr else " Inventaire",
    "results": " AI Detection Results" if not is_fr else " Resultats IA",
    "download_excel": " Download Full Report" if not is_fr else " Telecharger Rapport",
    "data_preview": " Sample Data Preview" if not is_fr else " Apercu des Donnees",
    "high_anomaly": "High Anomaly" if not is_fr else "Anomalie Haute",
    "medium_anomaly": "Medium Anomaly" if not is_fr else "Anomalie Moyenne",
    "normal": "Normal",
    "explanation": "Explanation" if not is_fr else "Explication",
    "level": "Level" if not is_fr else "Niveau",
    "ai_score": "AI Score" if not is_fr else "Score IA",
    "welcome_title": " Select Sample Data to Start" if not is_fr else " Selectionnez des Donnees",
    "welcome_text": "Choose a sample dataset in the sidebar to see AI in action!" if not is_fr else "Choisissez un jeu de donnees!",
    "get_full": "Get Full Desktop Version" if not is_fr else "Version Complete",
    "full_features": "Isolation Forest AI - Data Aggregation - Custom Ratios - 100% Offline - Unlimited Files" if not is_fr else "IA Isolation Forest - Agregation - Ratios - Hors-ligne",
    "what_is": "What is AynalyxAI?" if not is_fr else "Quest-ce que AynalyxAI?",
    "what_is_desc": "AynalyxAI is an intelligent financial analysis tool that automatically detects anomalies, errors, and irregularities in your accounting data using advanced AI algorithms." if not is_fr else "AynalyxAI detecte automatiquement les anomalies et irregularites dans vos donnees comptables.",
    "how_works": "How It Works" if not is_fr else "Comment ca Marche",
    "step1": "Upload your Excel/CSV data" if not is_fr else "Telechargez vos donnees",
    "step2": "AI analyzes patterns" if not is_fr else "L IA analyse les patterns",
    "step3": "Anomalies flagged with severity" if not is_fr else "Anomalies signalees",
    "step4": "Export color-coded reports" if not is_fr else "Exportez des rapports",
    "adv1_title": "Save Time" if not is_fr else "Gain de Temps",
    "adv1_desc": "Analyze thousands of transactions in seconds" if not is_fr else "Analysez des milliers de transactions",
    "adv2_title": "Reduce Errors" if not is_fr else "Reduire les Erreurs",
    "adv2_desc": "Catch mistakes humans might miss" if not is_fr else "Detectez les erreurs cachees",
    "adv3_title": "Detect Anomalies" if not is_fr else "Detecter les Anomalies",
    "adv3_desc": "Identify suspicious patterns early" if not is_fr else "Identifiez les patterns suspects",
    "example_desc": "Sample data with embedded anomalies. AI will identify unusual patterns." if not is_fr else "Donnees avec anomalies. L IA identifiera les patterns inhabituels.",
    "all_rows_note": "Showing ALL rows sorted by AI score. Anomalies highlighted, normal shown for context." if not is_fr else "TOUTES les lignes triees par score IA.",
}

THRESHOLD_HIGH = 2.0
THRESHOLD_MEDIUM = 1.2

def gen_invoices():
    np.random.seed(42)
    n = 50
    return pd.DataFrame({
        'Invoice_ID': [f'INV-{1000+i}' for i in range(n)],
        'Client': np.random.choice(['Acme Corp', 'TechStart', 'Global Services', 'Local Shop', 'Enterprise'], n),
        'Amount': np.concatenate([np.random.normal(1500, 400, n-6), [18500, 22000, 15, 8, 19800, 12]]),
        'Quantity': np.concatenate([np.random.randint(1, 25, n-6), [180, 250, 1, 1, 200, 1]]),
        'Date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    })

def gen_expenses():
    np.random.seed(43)
    n = 40
    return pd.DataFrame({
        'Expense_ID': [f'EXP-{2000+i}' for i in range(n)],
        'Category': np.random.choice(['Travel', 'Office', 'Software', 'Marketing', 'Utilities'], n),
        'Vendor': np.random.choice(['Amazon', 'Office Depot', 'Google', 'Airlines', 'Power Co'], n),
        'Amount': np.concatenate([np.random.normal(280, 120, n-5), [5800, 7200, 5, 3, 6500]]),
        'Date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist()
    })

def gen_payroll():
    np.random.seed(44)
    n = 30
    return pd.DataFrame({
        'Employee_ID': [f'EMP-{100+i}' for i in range(n)],
        'Department': np.random.choice(['Sales', 'Engineering', 'HR', 'Marketing', 'Finance'], n),
        'Salary': np.concatenate([np.random.normal(5200, 800, n-4), [28000, 32000, 450, 380]]),
        'Hours': np.concatenate([np.random.normal(160, 12, n-4), [280, 310, 35, 42]]),
        'Bonus': np.concatenate([np.random.normal(400, 150, n-4), [8500, 12000, 0, 0]])
    })

def gen_inventory():
    np.random.seed(45)
    n = 35
    df = pd.DataFrame({
        'SKU': [f'SKU-{3000+i}' for i in range(n)],
        'Product': np.random.choice(['Widget A', 'Gadget B', 'Tool C', 'Part D', 'Supply E'], n),
        'Quantity': np.concatenate([np.random.randint(80, 400, n-5), [5500, 8200, 2, 1, 6800]]),
        'Unit_Cost': np.concatenate([np.random.normal(28, 8, n-5), [380, 520, 2, 1, 450]])
    })
    df['Total_Value'] = df['Quantity'] * df['Unit_Cost']
    return df

st.markdown(f'<div class="main-header"><h1> {t["title"]}</h1><p>{t["subtitle"]}</p></div>', unsafe_allow_html=True)
st.markdown(f'<div class="demo-badge">{t["demo_notice"]}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.markdown(f'<p class="sidebar-title">{t["sample_title"]}</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        b1 = st.button(t['sample_invoices'], use_container_width=True, type="primary")
        b3 = st.button(t['sample_payroll'], use_container_width=True, type="primary")
    with c2:
        b2 = st.button(t['sample_expenses'], use_container_width=True, type="primary")
        b4 = st.button(t['sample_inventory'], use_container_width=True, type="primary")
    if b1: st.session_state['sample_type'], st.session_state['auto_run'] = 'invoices', True
    elif b2: st.session_state['sample_type'], st.session_state['auto_run'] = 'expenses', True
    elif b3: st.session_state['sample_type'], st.session_state['auto_run'] = 'payroll', True
    elif b4: st.session_state['sample_type'], st.session_state['auto_run'] = 'inventory', True
    st.markdown("---")
    st.markdown(f"**{t['how_works']}**")
    st.markdown(f"1 {t['step1']}")
    st.markdown(f"2 {t['step2']}")
    st.markdown(f"3 {t['step3']}")
    st.markdown(f"4 {t['step4']}")

df, data_name = None, ""
if 'sample_type' in st.session_state:
    s = st.session_state['sample_type']
    if s == 'invoices': df, data_name = gen_invoices(), "Invoices"
    elif s == 'expenses': df, data_name = gen_expenses(), "Expenses"
    elif s == 'payroll': df, data_name = gen_payroll(), "Payroll"
    elif s == 'inventory': df, data_name = gen_inventory(), "Inventory"

if df is not None:
    st.markdown(f'<div class="feature-box"><h3> {t["what_is"]}</h3><p>{t["what_is_desc"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="advantage-grid">
        <div class="advantage-item"><div class="icon"></div><h4>{t['adv1_title']}</h4><p>{t['adv1_desc']}</p></div>
        <div class="advantage-item"><div class="icon"></div><h4>{t['adv2_title']}</h4><p>{t['adv2_desc']}</p></div>
        <div class="advantage-item"><div class="icon"></div><h4>{t['adv3_title']}</h4><p>{t['adv3_desc']}</p></div>
    </div>''', unsafe_allow_html=True)
    
    st.subheader(f"{t['data_preview']} - {data_name}")
    st.caption(t['example_desc'])
    st.dataframe(df.head(8), use_container_width=True, height=220)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols and st.session_state.get('auto_run', False):
        st.session_state['auto_run'] = False
        st.markdown("---")
        st.subheader(t['results'])
        
        with st.spinner(" AI Analyzing..."):
            results = df.copy()
            
            # Round all numeric columns to 2 decimals
            for col in numeric_cols:
                results[col] = results[col].round(2)
            
            # Calculate z-scores
            z_scores = {}
            for col in numeric_cols:
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    z_scores[col] = (df[col] - mean) / std
                else:
                    z_scores[col] = pd.Series([0.0] * len(df))
            
            # Average deviation (mean of absolute z-scores)
            z_matrix = np.column_stack([np.abs(z_scores[col].values) for col in numeric_cols])
            avg_deviation = np.mean(z_matrix, axis=1)
            
            # AI Score: scale 0-10 (capped), 2 decimals
            # Based on average deviation: 0 = normal, 10 = extreme
            results['AI_Score'] = np.clip(avg_deviation * 2.5, 0, 10).round(2)
            
            # Generate short explanations
            def generate_explanation(idx, is_fr):
                explanations = []
                for col in numeric_cols:
                    z = z_scores[col].iloc[idx]
                    if abs(z) >= 1.5:
                        direction = "above" if z > 0 else "below"
                        if is_fr:
                            direction = "+" if z > 0 else "-"
                        col_short = col.replace('_', ' ')[:12]
                        explanations.append(f"{col_short} {abs(z):.1f}x {direction}")
                if len(explanations) == 0:
                    return "Normal" if not is_fr else "Normal"
                return " | ".join(explanations[:2])
            
            results['Explanation'] = [generate_explanation(i, is_fr) for i in range(len(df))]
            
            # Classify levels
            def classify_level(avg_dev):
                if avg_dev >= THRESHOLD_HIGH:
                    return t['high_anomaly']
                elif avg_dev >= THRESHOLD_MEDIUM:
                    return t['medium_anomaly']
                else:
                    return t['normal']
            
            results['Level'] = [classify_level(avg_deviation[i]) for i in range(len(df))]
            
            # Sort by AI Score descending
            results_sorted = results.sort_values('AI_Score', ascending=False).reset_index(drop=True)
            
            # Count anomalies
            n_high = len(results_sorted[results_sorted['Level'] == t['high_anomaly']])
            n_med = len(results_sorted[results_sorted['Level'] == t['medium_anomaly']])
            n_normal = len(results_sorted[results_sorted['Level'] == t['normal']])
            n_total = n_high + n_med
            
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f'<div class="stat-card stat-critical"><div style="font-size:2rem;font-weight:bold;color:#dc2626;">{n_high}</div><div>High</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card stat-high"><div style="font-size:2rem;font-weight:bold;color:#f59e0b;">{n_med}</div><div>Medium</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="stat-card stat-low"><div style="font-size:2rem;font-weight:bold;color:#22c55e;">{n_normal}</div><div>Normal</div></div>', unsafe_allow_html=True)
            c4.markdown(f'<div class="stat-card" style="border-color:#667eea;"><div style="font-size:2rem;font-weight:bold;color:#667eea;">{n_total}</div><div>Flagged</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.success(f" **{len(results_sorted)}** rows analyzed - **{n_total}** anomalies - **{n_normal}** normal")
            
            # Get first ID column for display
            id_col = [c for c in results_sorted.columns if 'ID' in c.upper() or 'SKU' in c.upper()]
            id_col = id_col[0] if id_col else results_sorted.columns[0]
            
            # Create compact display table (ID + key numeric + AI Score + Level + Explanation)
            # Select only essential columns to fit on screen
            key_numeric = numeric_cols[:2]  # First 2 numeric columns only
            display_cols = [id_col] + key_numeric + ['AI_Score', 'Level', 'Explanation']
            display_df = results_sorted[display_cols].copy()
            
            # Rename for display
            display_df = display_df.rename(columns={
                'AI_Score': t['ai_score'],
                'Level': t['level'],
                'Explanation': t['explanation']
            })
            
            def color_level(val):
                if val == t['high_anomaly']: return 'background-color:#dc2626;color:white;font-weight:bold;'
                if val == t['medium_anomaly']: return 'background-color:#f59e0b;color:white;font-weight:bold;'
                return 'background-color:#22c55e;color:white;'
            
            def color_row(row):
                lv = row[t['level']]
                if lv == t['high_anomaly']: return ['background-color:#fee2e2;'] * len(row)
                if lv == t['medium_anomaly']: return ['background-color:#fffbeb;'] * len(row)
                return [''] * len(row)
            
            styled = display_df.style.apply(color_row, axis=1).map(color_level, subset=[t['level']]).format(precision=2)
            st.dataframe(styled, use_container_width=True, height=500, hide_index=True)
            
            # Full report for download (all columns)
            full_df = results_sorted.rename(columns={
                'AI_Score': t['ai_score'],
                'Level': t['level'],
                'Explanation': t['explanation']
            })
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                full_df.to_excel(writer, index=False, sheet_name='Results')
                ws = writer.sheets['Results']
                fill_h = PatternFill(start_color='667EEA', end_color='667EEA', fill_type='solid')
                fill_c = PatternFill(start_color='DC2626', end_color='DC2626', fill_type='solid')
                fill_cr = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid')
                fill_m = PatternFill(start_color='F59E0B', end_color='F59E0B', fill_type='solid')
                fill_mr = PatternFill(start_color='FFFBEB', end_color='FFFBEB', fill_type='solid')
                fill_l = PatternFill(start_color='22C55E', end_color='22C55E', fill_type='solid')
                font_w = Font(color='FFFFFF', bold=True)
                bdr = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                for cell in ws[1]: cell.fill, cell.font, cell.border = fill_h, font_w, bdr
                lv_idx = list(full_df.columns).index(t['level']) + 1
                for r in range(2, len(full_df) + 2):
                    lv = ws.cell(row=r, column=lv_idx).value
                    rf, lf = None, None
                    if lv == t['high_anomaly']: rf, lf = fill_cr, fill_c
                    elif lv == t['medium_anomaly']: rf, lf = fill_mr, fill_m
                    elif lv == t['normal']: lf = fill_l
                    for c in range(1, len(full_df.columns) + 1):
                        cell = ws.cell(row=r, column=c)
                        cell.border = bdr
                        if rf: cell.fill = rf
                        if c == lv_idx and lf: cell.fill, cell.font = lf, font_w
                for i, col in enumerate(full_df.columns, 1):
                    ws.column_dimensions[ws.cell(1, i).column_letter].width = min(30, max(len(str(col)), 10) + 2)
                ws.auto_filter.ref = f"A1:{ws.cell(1, len(full_df.columns)).column_letter}{len(full_df) + 1}"
                ws.freeze_panes = 'A2'
            output.seek(0)
            st.download_button(t['download_excel'], output, f"aynalyxai_{data_name.lower()}_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary")
        
        st.markdown(f'<div class="cta-box"><h3> {t["get_full"]}</h3><p style="color:#555;">{t["full_features"]}</p><a href="https://mubsira.gumroad.com/l/aynalyxai" target="_blank" class="cta-button"> Get AynalyxAI Pro</a></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="feature-box"><h3> {t["what_is"]}</h3><p>{t["what_is_desc"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f'''<div class="advantage-grid">
        <div class="advantage-item"><div class="icon"></div><h4>{t['adv1_title']}</h4><p>{t['adv1_desc']}</p></div>
        <div class="advantage-item"><div class="icon"></div><h4>{t['adv2_title']}</h4><p>{t['adv2_desc']}</p></div>
        <div class="advantage-item"><div class="icon"></div><h4>{t['adv3_title']}</h4><p>{t['adv3_desc']}</p></div>
    </div>''', unsafe_allow_html=True)
    st.markdown(f'<div class="how-it-works"><h4> {t["how_works"]}</h4><ul><li>1 {t["step1"]}</li><li>2 {t["step2"]}</li><li>3 {t["step3"]}</li><li>4 {t["step4"]}</li></ul></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;padding:3rem 2rem;background:linear-gradient(135deg,#f8fafc 0%,#e2e8f0 100%);border-radius:16px;margin-top:1rem;"><div style="font-size:4rem;margin-bottom:1rem;"></div><h2 style="color:#1e293b;">{t["welcome_title"]}</h2><p style="color:#64748b;font-size:1.1rem;">{t["welcome_text"]}</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align:center;color:#94a3b8;padding:1rem;">© 2025 Mubsira Analytics | <a href="https://mubsira.gumroad.com/l/aynalyxai" style="color:#667eea;">Get Full Version</a></div>', unsafe_allow_html=True)
