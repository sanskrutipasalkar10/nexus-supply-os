import streamlit as st
import time
import google.generativeai as genai

# --- 0. CONFIGURATION ---
st.set_page_config(
    page_title="Nexus Supply-OS",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# *** HARDCODE YOUR API KEY HERE ***
GEMINI_API_KEY = "AIzaSyCinHnlOj1ILtR7CuvPqs4NaqT-XJJT3Vs" 

# --- 1. CSS STYLING (Fixed Visibility & Spacing) ---
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
    /* VARIABLES */
    :root {
        --bg-dark: #0f172a;
        --panel-bg: #1e293b;
        --panel-glass: rgba(30, 41, 59, 0.7);
        --primary: #0ea5e9;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --text-main: #f8fafc;
        --text-muted: #cbd5e1;
        --border: #334155;
        --font-stack: 'Inter', system-ui, sans-serif;
    }

    .stApp { background-color: var(--bg-dark); font-family: var(--font-stack); color: var(--text-main); }
    
    /* Hide Streamlit Chrome */
    header[data-testid="stHeader"], footer, section[data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 0; padding-bottom: 80px; max-width: 1000px;} 

    /* --- TEXT VISIBILITY FIXES --- */
    h1, h2, h3, .report-title { color: #ffffff !important; }
    p, div { color: var(--text-main); }

    /* Header */
    .custom-header {
        background: rgba(15, 23, 42, 0.95); border-bottom: 1px solid var(--border);
        padding: 1rem 2rem; position: sticky; top: 0; z-index: 50;
        display: flex; justify-content: space-between; align-items: center;
        margin-left: -5rem; margin-right: -5rem; margin-bottom: 2rem;
    }
    .hud-stats { display: flex; gap: 30px; }
    .stat-label { font-size: 0.7rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 1px; }
    .stat-value { font-family: monospace; font-weight: 700; font-size: 1.2rem; color: var(--text-main); }
    .val-pos { color: var(--success); } .val-neg { color: var(--danger); }

    /* Intro Card */
    .intro-card {
        background: var(--panel-glass); border: 1px solid var(--border); border-radius: 12px; padding: 3rem;
        text-align: center; max-width: 700px; margin: 60px auto; border-top: 4px solid var(--primary);
    }
    .intro-title { font-size: 2.5rem; font-weight: 800; color: white; margin-bottom: 10px; }
    .intro-subtitle { font-size: 1.1rem; color: var(--text-muted); margin-bottom: 30px; }
    .intro-warning {
        text-align: left; background: rgba(0,0,0,0.4); padding: 20px; border-radius: 8px;
        margin-bottom: 30px; border: 1px solid #334155; color: #e2e8f0; 
    }
    
    /* Progress */
    .progress-track { display: flex; justify-content: space-between; margin-bottom: 2rem; position: relative; padding: 0 20px; }
    .track-line { position: absolute; top: 50%; left: 20px; right: 20px; height: 2px; background: var(--border); z-index: 0; transform: translateY(-50%); }
    .track-node {
        background: var(--bg-dark); border: 2px solid var(--border); color: var(--text-muted);
        width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        position: relative; z-index: 1; transition: all 0.4s ease;
    }
    .track-node.active { border-color: var(--primary); background: var(--primary); color: #0f172a; transform: scale(1.1); }
    .track-node.done { border-color: var(--success); color: var(--success); }

    /* AI Console */
    .ai-console {
        background: #000; border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem;
        margin-bottom: 2rem; border-left: 4px solid var(--primary); font-family: monospace; color: #e2e8f0;
    }
    .console-header {
        display: flex; align-items: center; gap: 10px; color: var(--primary); font-family: monospace;
        font-size: 0.85rem; margin-bottom: 1rem; border-bottom: 1px solid #333; padding-bottom: 0.5rem;
    }

    /* Cards */
    .scenario-card { background: var(--panel-glass); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; }
    
    /* --- SPACING FIX --- */
    .option-box {
        background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px;
        padding: 1.5rem; height: 100%; transition: all 0.2s ease;
        display: flex; flex-direction: column; justify-content: space-between; 
        padding-bottom: 3rem; /* Increased bottom padding */
    }
    .option-box.selected { border-color: var(--primary); background: rgba(14, 165, 233, 0.1); }
    
    /* Report Card */
    .report-card { background: var(--panel-glass); border-radius: 12px; padding: 20px; border: 1px solid var(--border); margin-bottom: 20px; }
    .report-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }

    /* Buttons */
    div.stButton > button { width: 100%; background: transparent; border: 1px dashed var(--border); color: var(--primary); margin-top: 15px; }
    div.stButton > button:hover { background: rgba(14, 165, 233, 0.1); }
    .primary-btn div.stButton > button { background: var(--primary); color: #0f172a; border: none; font-weight: bold; margin-top: 0; }
    .primary-btn div.stButton > button:hover { background: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# --- 2. SCENARIO DATA ---
SCENARIOS = [
    {
        "icon": "fa-battery-full", "stageName": "Raw Material Sourcing", "title": "Lithium Supply Volatility",
        "desc": "Production starts in 6 months. Lithium prices are stable ($20/kg), but news reports hint at labor unrest in Chilean mines.",
        "aiMsg": "System Alert: Detecting 85% probability of mining strikes in Q3. Current market prices do not yet reflect this risk.",
        "options": [
            {
                "title": "Spot Market", "desc": "Buy at market price when needed.", "icon": "fa-chart-line", 
                "riskMsg": "Strike occurs. Price spikes to $35/kg. Cost overrun: $12M.", 
                "type": "bad", "impact": -12.5, "resultText": "Huge Cost Overrun", 
                "outcome": "Cash saved initially, but you bought at peak panic prices.",
                "analysis": "You gambled on stability. The strike hit, causing massive overruns.",
                "value": "Loss: -$12.5M"
            },
            {
                "title": "Hedge Contract", "desc": "Lock price at $22/kg (10% premium).", "icon": "fa-file-signature", 
                "riskMsg": "Price spikes to $35/kg. You pay $22. Savings: $8M.", 
                "type": "good", "impact": 8.2, "resultText": "Cost Avoidance Success", 
                "outcome": "Smart move. The market spiked, but contract protected margin.",
                "analysis": "You correctly interpreted the AI warning. Competitors bled cash while you were protected.",
                "value": "Value Created: +$8.2M (Cost Avoidance)"
            },
            {
                "title": "Delay & Monitor", "desc": "Wait 3 months for signals.", "icon": "fa-clock", 
                "riskMsg": "50% chance of delay penalties. Buffer depleted.", 
                "type": "avg", "impact": -1.5, "resultText": "Operational Delay", 
                "outcome": "Avoided worst costs, but incurred expedite fees.",
                "analysis": "You hesitated. The delay forced you to pay expedite fees to catch up.",
                "value": "Loss: -$1.5M (Expedite Fees)"
            }
        ]
    },
    {
        "icon": "fa-industry", "stageName": "Manufacturing Partner", "title": "Vendor Selection",
        "desc": "Select primary assembler for motor units. Two bids on the table.",
        "aiMsg": "Analyzing Bidder Financial Health and Historical Quality Metrics...",
        "options": [
            {
                "title": "Vendor Alpha", "desc": "15% lower cost. History of disputes.", "icon": "fa-money-bill-wave", 
                "riskMsg": "Vendor runs lean. Disruption risk HIGH. Downtime cost: $4M.", 
                "type": "bad", "impact": -4.0, "resultText": "Production Stoppage", 
                "outcome": "Vendor Alpha faced a walkout. Line stopped for 3 days.",
                "analysis": "You chose the cheapest option, ignoring the risk. The strike cost more than the savings.",
                "value": "Loss: -$4.0M (Downtime)"
            },
            {
                "title": "Vendor Beta", "desc": "Standard price. Automated facility.", "icon": "fa-robot", 
                "riskMsg": "99.9% uptime projection. Zero disruption risk.", 
                "type": "good", "impact": 0.0, "resultText": "Smooth Launch", 
                "outcome": "Perfect execution. Automation handled volume surge.",
                "analysis": "You prioritized 'Total Cost of Ownership'. Automation ensured zero downtime.",
                "value": "Value Created: Operational Continuity"
            }
        ]
    },
    {
        "icon": "fa-ship", "stageName": "Global Logistics", "title": "Red Sea Blockade",
        "desc": "Geopolitical conflict closes Red Sea route. Container ship stuck. Inventory: 5 Days.",
        "aiMsg": "CRITICAL ALERT: Shipping route blocked. ETA delayed 14 days. Stockout imminent.",
        "options": [
            {
                "title": "Re-route Ship", "desc": "Go around Africa. 14-day delay.", "icon": "fa-route", 
                "riskMsg": "Plant shuts down for 9 days. Revenue loss: $15M.", 
                "type": "bad", "impact": -15.0, "resultText": "Revenue Collapse", 
                "outcome": "The plant went dark. Market share lost due to stockouts.",
                "analysis": "You chose the slow route during a crisis. The factory ran out of parts.",
                "value": "Loss: -$15.0M (Revenue)"
            },
            {
                "title": "Full Air Freight", "desc": "Fly all inventory. 8x Cost.", "icon": "fa-plane-departure", 
                "riskMsg": "Logistics spend will exceed budget by 400%.", 
                "type": "avg", "impact": -8.0, "resultText": "Budget Bleed", 
                "outcome": "Production saved, but profitability wiped out by shipping.",
                "analysis": "You panicked and flew everything. You saved the line, but destroyed profit.",
                "value": "Loss: -$8.0M (Logistics Cost)"
            },
            {
                "title": "Hybrid Bridge", "desc": "Fly 5 days stock; Ship rest.", "icon": "fa-boxes-stacked", 
                "riskMsg": "Covers gap with minimal spend. Recommended.", 
                "type": "good", "impact": -1.2, "resultText": "Optimized Spend", 
                "outcome": "Precision Logistics. You bridged the gap perfectly.",
                "analysis": "You used AI to calculate the exact 'Bridge' needed, balancing speed and cost.",
                "value": "Value Created: Minimized Loss (-$1.2M vs -$15M)"
            }
        ]
    },
    {
        "icon": "fa-triangle-exclamation", "stageName": "Quality Assurance", "title": "The Micro-Crack Defect",
        "desc": "2% of casings have micro-cracks. Technically out of spec, but looks safe.",
        "aiMsg": "Defect Analysis: Thermal stress modeling shows cracks may widen over 2 years.",
        "options": [
            {
                "title": "Stop & Purge", "desc": "Recall batch. 100% Inspect. 24hr Delay.", "icon": "fa-ban", 
                "riskMsg": "Long term: Costly now ($2M), but prevents massive liability.", 
                "type": "good", "impact": -2.0, "resultText": "Brand Secured", 
                "outcome": "Expensive pause, but you caught a safety hazard. Customers trust you.",
                "analysis": "You sacrificed short-term speed for brand safety. You avoided a future recall.",
                "value": "Value Created: Brand Integrity"
            },
            {
                "title": "Ship with Waiver", "desc": "Sign deviation. Keep shipping.", "icon": "fa-file-contract", 
                "riskMsg": "Liability Alert: 15% Failure rate predicted in field. Recall cost: $45M.", 
                "type": "bad", "impact": -45.0, "resultText": "Massive Recall", 
                "outcome": "Disaster. Batteries failed in the field. Massive PR and financial blow.",
                "analysis": "You ignored the quality signal. The result was a massive recall and lawsuit.",
                "value": "Loss: -$45.0M (Recall)"
            }
        ]
    }
]

# --- 3. SESSION STATE ---
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'current_stage' not in st.session_state: st.session_state.current_stage = 0
if 'total_pnl' not in st.session_state: st.session_state.total_pnl = 0.0
if 'history' not in st.session_state: st.session_state.history = []
if 'nexus_analysis' not in st.session_state: st.session_state.nexus_analysis = "Initializing System... Accessing Global Logistics Database..."
if 'selected_option' not in st.session_state: st.session_state.selected_option = None
if 'stage_complete' not in st.session_state: st.session_state.stage_complete = False

# --- 4. API FUNCTION ---
def get_gemini_response(context, option_label):
    if not GEMINI_API_KEY: return "⚠️ API KEY MISSING IN CODE."
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash-exp', 'gemini-pro']
        active_model = None
        for m in models:
            try:
                active_model = genai.GenerativeModel(m)
                break
            except: continue
        
        if not active_model: return "Error: No compatible Gemini model found."
        
        prompt = f"Role: Supply Chain AI. Context: {context}. User Option: {option_label}. Task: Provide 1 sentence financial risk analysis. Start with '>> RISK CALCULATION:'"
        response = active_model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error: {str(e)}"

# --- 5. RENDER LOGIC ---

# A. HEADER (Always Visible)
pnl_val = st.session_state.total_pnl
pnl_class = "val-pos" if pnl_val >= 0 else "val-neg"
pnl_sign = "+" if pnl_val >= 0 else ""
pnl_display = f"{pnl_sign}${abs(pnl_val):.2f}M"

st.markdown(f"""
<div class="custom-header">
    <div style="display:flex; align-items:center; gap:12px;">
        <i class="fa-solid fa-layer-group" style="font-size:1.5rem; color:#0ea5e9;"></i>
        <div><div style="font-weight:700; color:white;">NEXUS SUPPLY-OS</div><div style="font-size:0.75rem; color:#94a3b8;">AI-Driven Resilience Engine</div></div>
    </div>
    <div class="hud-stats">
        <div><span class="stat-label">Net P&L Impact</span><br><span class="stat-value {pnl_class}">{pnl_display}</span></div>
        <div><span class="stat-label">BCP Protocol</span><br><span class="stat-value val-pos">ACTIVE</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# B. MISSION BRIEFING (START SCREEN)
if not st.session_state.game_started:
    st.markdown("""
    <div class="intro-card">
        <div style="color:#0ea5e9; font-weight:bold; letter-spacing:2px; margin-bottom:10px;">OPERATIONS COMMAND CENTER</div>
        <div class="intro-title">PROJECT MODEL-X LAUNCH</div>
        <div class="intro-subtitle">
            <p><strong>Time to Launch:</strong> 6 Months</p>
            <p><strong>Objective:</strong> Navigate global supply chain risks to get the flagship EV to market profitably.</p>
        </div>
        <div class="intro-warning">
            <i class="fa-solid fa-triangle-exclamation" style="color:#f59e0b;"></i> <strong>THREAT LEVEL: CRITICAL</strong><br>
            Intelligence reports indicate high volatility in Raw Materials (Chile), Manufacturing Labor (Asia), and Logistics Routes (Red Sea).
            <br><br>
            Your AI Partner, <strong>Nexus</strong>, is online to simulate risks. Use it wisely.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("INITIALIZE OPERATIONS", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# C. GAME LOOP
elif st.session_state.current_stage < len(SCENARIOS):
    data = SCENARIOS[st.session_state.current_stage]
    
    # Progress Tracker
    nodes = ""
    for i, s in enumerate(SCENARIOS):
        status = "active" if i == st.session_state.current_stage else ("done" if i < st.session_state.current_stage else "")
        nodes += f'<div class="track-node {status}"><i class="fa-solid {s["icon"]}"></i></div>'
    st.markdown(f'<div class="progress-track"><div class="track-line"></div>{nodes}</div>', unsafe_allow_html=True)

    # AI Console Placeholder (For Spinner Animation)
    ai_box = st.empty()

    # Default View (Static Icon)
    current_text = st.session_state.nexus_analysis if st.session_state.nexus_analysis != "Initializing System... Accessing Global Logistics Database..." else data['aiMsg']
    ai_box.markdown(f"""
    <div class="ai-console">
        <div class="console-header">
            <i class="fa-solid fa-robot" style="color:#0ea5e9;"></i> <span>NEXUS INTELLIGENCE FEED</span>
        </div>
        <div class="console-text">{current_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # Scenario Card
    st.markdown(f"""
    <div class="scenario-card">
        <div style="color:#0ea5e9; font-weight:bold; font-size:0.8rem;">STAGE 0{st.session_state.current_stage + 1} // {data['stageName']}</div>
        <h2 style="color:white; margin:0;">{data['title']}</h2>
        <p style="color:#94a3b8;">{data['desc']}</p>
    </div><br>
    """, unsafe_allow_html=True)

    # Options Grid
    cols = st.columns(len(data['options']))
    for i, opt in enumerate(data['options']):
        sel = "selected" if st.session_state.selected_option == i else ""
        with cols[i]:
            st.markdown(f"""
            <div class="option-box {sel}">
                <div>
                    <div style="font-weight:bold; color:white; margin-bottom:5px;"><i class="fa-solid {opt['icon']}" style="color:#0ea5e9;"></i> {opt['title']}</div>
                    <div style="font-size:0.9rem; color:#94a3b8;">{opt['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if not st.session_state.stage_complete:
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("Consult", key=f"c{i}"):
                        # 1. Show Spinning Bot via Placeholder
                        ai_box.markdown(f"""
                        <div class="ai-console">
                            <div class="console-header">
                                <i class="fa-solid fa-robot fa-spin" style="color:#0ea5e9;"></i> <span>ANALYZING RISK VECTORS...</span>
                            </div>
                            <div class="console-text" style="color:#0ea5e9;">Running Risk Analysis on {opt['title']}...</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 2. Run API Call
                        st.session_state.nexus_analysis = get_gemini_response(data['desc'], opt['title'])
                        
                        # 3. Rerun to show result (Static Bot returns)
                        st.rerun()

                with c2:
                    if st.button("Select", key=f"s{i}"):
                        st.session_state.selected_option = i
                        st.rerun()

    # Finalize
    if st.session_state.selected_option is not None and not st.session_state.stage_complete:
        st.markdown('<br><div class="primary-btn">', unsafe_allow_html=True)
        if st.button("FINALIZE DECISION", use_container_width=True):
            st.session_state.stage_complete = True
            choice = data['options'][st.session_state.selected_option]
            st.session_state.total_pnl += choice['impact']
            st.session_state.history.append({
                "stage": data['stageName'],
                "decision": choice['title'],
                "full_choice_data": choice
            })
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Outcome Modal
    if st.session_state.stage_complete:
        choice = data['options'][st.session_state.selected_option]
        sign = "+" if choice['impact'] >= 0 else "-"
        st.markdown(f"""
        <div class="outcome-modal" style="background:rgba(30, 41, 59, 0.9); border:1px solid #334155; padding:2rem; border-radius:12px; border-left:4px solid #0ea5e9;">
            <h3 style="color:white; margin:0;">{choice['resultText']}</h3>
            <p style="color:#94a3b8;">{choice['outcome']}</p>
            <div style="font-family:monospace; font-weight:bold; color:white;">IMPACT: {sign}${abs(choice['impact']):.2f}M</div>
        </div><br>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("NEXT STAGE ➔", use_container_width=True):
            st.session_state.current_stage += 1
            st.session_state.selected_option = None
            st.session_state.stage_complete = False
            st.session_state.nexus_analysis = "Loading next stage..."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# D. END SCREEN (REPORT)
else:
    st.markdown("""
    <div style="text-align:center; margin-bottom:3rem;">
        <i class="fa-solid fa-clipboard-check" style="font-size:3rem; color:#0ea5e9; margin-bottom:1rem;"></i>
        <h1 style="color:white;">Simulation Complete</h1>
        <p style="color:#94a3b8;">Executive Business Impact Assessment</p>
    </div>
    """, unsafe_allow_html=True)

    # Grading Logic
    final = st.session_state.total_pnl
    if final > 0:
        grade = "A+ (Resilient Strategist)"
        icon = '<i class="fa-solid fa-trophy" style="color:#10b981;"></i>'
        msg = "You monetized the chaos. Excellent predictive work."
    elif final > -10:
        grade = "B (Operational Manager)"
        icon = '<i class="fa-solid fa-scale-balanced" style="color:#f59e0b;"></i>'
        msg = "Operations ran, but reactivity cost margin."
    else:
        grade = "C (Critical Failure)"
        icon = '<i class="fa-solid fa-skull-crossbones" style="color:#ef4444;"></i>'
        msg = "Supply chain collapsed. Critical failures detected."

    st.markdown(f"""
    <div style="background:var(--panel-glass); border-radius:12px; padding:2rem; text-align:center; border:1px solid var(--border); margin-bottom:30px;">
        <h2 style="margin-bottom:10px; color:white;">{icon} Overall Rating: {grade}</h2>
        <div style="color:var(--text-muted);">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Cards (Replaced Notepad emoji with fa-list-check)
    st.markdown("### <span style='color: white;'>Stage-by-Stage Review</span>", unsafe_allow_html=True)
    for idx, step in enumerate(st.session_state.history):
        if 'full_choice_data' not in step: continue
        c_data = step['full_choice_data']
        
        # Professional Icons instead of emojis
        icon = "fa-circle-check" if c_data['type'] == 'good' else ("fa-circle-xmark" if c_data['type'] == 'bad' else "fa-triangle-exclamation")
        color = "#10b981" if c_data['type'] == 'good' else ("#ef4444" if c_data['type'] == 'bad' else "#f59e0b")
        
        st.markdown(f"""
        <div class="report-card">
            <div class="report-title" style="color:{color};">
                <i class="fa-solid {icon}"></i> Stage {idx+1}: {step['stage']}
            </div>
            <div style="color:#e2e8f0; margin-bottom:5px;"><strong>Decision:</strong> {step['decision']}</div>
            <div style="color:#94a3b8; font-size:0.9rem;">{c_data['analysis']}</div>
            <div style="color:{color}; font-weight:bold; margin-top:10px;">{c_data['value']}</div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("RESTART MISSION", use_container_width=True):
            st.session_state.clear()
            st.rerun()