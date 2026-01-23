import streamlit as st
import time
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 0. CONFIGURATION ---
st.set_page_config(
    page_title="Nexus Supply-OS",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

# --- 1. CSS STYLING ---
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
    /* FORCE DARK MODE GLOBALLY */
    .stApp { 
        background-color: #0f172a !important; 
        font-family: 'Inter', system-ui, sans-serif;
        color: #f8fafc !important;
    }
    
    /* Hide Streamlit Chrome */
    header[data-testid="stHeader"], footer, section[data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 0; padding-bottom: 80px; max-width: 1000px;} 

    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6, .report-title { color: #ffffff !important; }
    p, div, li, span { color: #cbd5e1; }
    strong { color: #f8fafc; }

    /* Header */
    .custom-header {
        background: rgba(15, 23, 42, 0.95); 
        border-bottom: 1px solid #334155;
        padding: 1rem 2rem; position: sticky; top: 0; z-index: 50;
        display: flex; justify-content: space-between; align-items: center;
        margin-left: -5rem; margin-right: -5rem; margin-bottom: 2rem;
    }
    .hud-stats { display: flex; gap: 30px; }
    .stat-label { font-size: 0.7rem; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; }
    .stat-value { font-family: monospace; font-weight: 700; font-size: 1.2rem; color: #f8fafc; }
    .val-pos { color: #10b981 !important; } .val-neg { color: #ef4444 !important; }

    /* START SCREEN STYLING */
    .mission-header {
        text-align: center;
        margin-top: 40px;
        margin-bottom: 40px;
    }
    .mission-title {
        font-size: 3.5rem; 
        font-weight: 800; 
        color: white; 
        text-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
        text-transform: uppercase;
    }
    .context-box {
        border-left: 4px solid #0ea5e9;
        padding-left: 20px;
        margin-bottom: 30px;
    }
    .financial-box {
        background: rgba(0,0,0,0.3);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
    }
    .trigger-box {
        border: 1px solid #f59e0b;
        background: rgba(245, 158, 11, 0.1);
        padding: 20px;
        border-radius: 8px;
        color: #fcd34d;
    }

    /* AI Console */
    .ai-console {
        background: #000000 !important; 
        border: 1px solid #334155; 
        border-radius: 8px; 
        padding: 1.5rem;
        margin-bottom: 2rem; 
        border-left: 4px solid #0ea5e9; 
        font-family: monospace; 
        color: #e2e8f0;
    }
    .console-header {
        display: flex; align-items: center; gap: 10px; color: #0ea5e9; font-family: monospace;
        font-size: 0.85rem; margin-bottom: 1rem; border-bottom: 1px solid #333; padding-bottom: 0.5rem;
    }
    .console-text ul { padding-left: 20px; margin: 0; }
    .console-text li { margin-bottom: 12px; list-style-type: none; color: #e2e8f0; line-height: 1.5;}

    /* Option Cards */
    .scenario-card { background: #1e293b !important; border: 1px solid #334155; border-radius: 12px; padding: 2rem; }
    .option-box {
        background: rgba(255,255,255,0.03); border: 1px solid #334155; border-radius: 8px;
        padding: 1.5rem; height: 100%; transition: all 0.2s ease;
        display: flex; flex-direction: column; justify-content: space-between; 
        padding-bottom: 3rem; 
    }
    .option-box.selected { border-color: #0ea5e9; background: rgba(14, 165, 233, 0.1); }
    
    /* Report Card */
    .report-card { background: #1e293b !important; border-radius: 12px; padding: 20px; border: 1px solid #334155; margin-bottom: 20px; }
    .report-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; }

    /* Buttons */
    div.stButton > button { width: 100%; background: transparent; border: 1px dashed #334155; color: #0ea5e9; margin-top: 15px; }
    div.stButton > button:hover { background: rgba(14, 165, 233, 0.1); }
    .primary-btn div.stButton > button { background: #0ea5e9; color: #0f172a; border: none; font-weight: bold; margin-top: 0; }
    .primary-btn div.stButton > button:hover { background: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# --- 2. SCENARIO DATA (UPDATED NARRATIVES) ---
SCENARIO_DATA = {
    "icon": "fa-microchip", 
    "stageName": "CRITICAL INCIDENT RESPONSE", 
    "title": "The Silent Chip Crisis",
    "desc": "Your primary supplier, 'TechCore', reports a '2-week delay' due to a server outage. They have been a trusted partner for 5 years. However, Nexus AI has detected conflicting signals in the market.",
    "aiMsg": "<span style='color:#ef4444; font-weight:bold;'>ALERT: Discrepancy detected. TechCore reports a 'glitch', but Global Risk Intelligence feeds indicate a ransomware lockout of their water filtration systems. Insolvency risk model: 94%.</span>",
    "options": [
        {
            "title": "Trust TechCore (Wait)", 
            "desc": "Accept the 2-week delay based on relationship history.", 
            "icon": "fa-handshake", 
            "type": "bad", 
            "impact": -96.0, 
            "resultText": "Catastrophic Insolvency", 
            "outcome": "The 'Server Glitch' was a lie. A massive <strong>Ransomware Attack</strong> permanently locked TechCore's industrial <strong>Water Filtration Systems</strong> (critical for chip cooling). They declared bankruptcy 10 days later. Your factory went dark for 8 weeks, creating a solvency crisis.",
            "analysis": "You ignored the insolvency signal. The resulting production halt cost the company $96M in burn rate and lost revenue.",
            "value": "Loss: -$96.0M",
            "calc": "8 Weeks Downtime * ($2M Burn Rate + $10M Lost Margin) = -$96M"
        },
        {
            "title": "Spot Market (Panic)", 
            "desc": "Buy immediate stock from unverified brokers.", 
            "icon": "fa-cart-shopping", 
            "type": "avg", 
            "impact": -15.0, 
            "resultText": "Quality Disaster", 
            "outcome": "You secured chips, but they were unverified grey-market stock. <strong>20% were counterfeit or heat-damaged.</strong> Ventilators failed in active hospital use, triggering a Class I FDA Recall and massive liability lawsuits.",
            "analysis": "You solved the schedule problem but destroyed the brand. Resilience is about verifying the *quality* of the supply, not just the existence of it.",
            "value": "Loss: -$15.0M",
            "calc": "Recall Logistics ($10M) + Legal Settlements ($5M) = -$15M"
        },
        {
            "title": "OmniChip Pivot (AI)", 
            "desc": "Pay $2M retainer to switch vendors immediately.", 
            "icon": "fa-shuffle", 
            "type": "good", 
            "impact": 18.0, 
            "resultText": "Market Dominance", 
            "outcome": "While competitors were paralyzed by the <strong>TechCore Ransomware Lockdown</strong>, you had already secured a new supply line. You became the sole reliable supplier in the market, capturing critical hospital contracts from failed competitors.",
            "analysis": "Strategic execution. You treated the $2M pivot fee as an investment in continuity, which paid off 9x in market capture.",
            "value": "Gain: +$18.0M",
            "calc": "Market Share Gain (+$20M Profit) - Switch Cost ($2M) = +$18M Net"
        }
    ]
}

# --- 3. SESSION STATE ---
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'total_pnl' not in st.session_state: st.session_state.total_pnl = 0.0
if 'history' not in st.session_state: st.session_state.history = []
if 'nexus_analysis' not in st.session_state: st.session_state.nexus_analysis = "Initializing System... Scanning Global Supplier Nodes..."
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
        
        # --- DYNAMIC PROMPT LOGIC ---
        logic_instruction = ""
        
        if "Wait" in option_label or "TechCore" in option_label:
            logic_instruction = """
            CRITICAL: Assume WORST CASE (Insolvency).
            The supplier WILL go bankrupt. Delay is 8 weeks (not 2).
            Math: 8 weeks * ($2M Burn Rate + $10M Lost Profit) = $96M.
            Outcome: -$96M (Use Red Color).
            """
        elif "Spot" in option_label:
            logic_instruction = """
            CRITICAL: Assume QUALITY FAILURE.
            Spot chips have 20% failure.
            Math: Recall Costs ($10M) + Liability ($5M) = $15M.
            Outcome: -$15M (Use Red Color).
            """
        elif "Pivot" in option_label or "OmniChip" in option_label:
            logic_instruction = """
            CRITICAL: Assume MARKET CAPTURE.
            Competitors fail. You sell 2,000 extra units.
            Math: (2000 units * $10k Margin) - $2M Fee = +$18M Net Gain.
            Outcome: +$18M (Use Green Color).
            """

        # PROMPT
        prompt = f"""
        Role: You are 'Nexus', a Supply Chain Risk AI. 
        Context: {context}.
        User Option: {option_label}.
        
        {logic_instruction}
        
        Task: Provide a Risk & Impact analysis based on the CRITICAL INSTRUCTION above.
        Constraint: Use HTML List format only. No paragraphs.
        
        COLOR RULES:
        - If the impact is NEGATIVE/LOSS: Use <span style="color:#ef4444; font-weight:bold;">
        - If the impact is POSITIVE/GAIN: Use <span style="color:#10b981; font-weight:bold;">
        
        Output Format:
        <ul>
        <li><b>Calculated Risk:</b> [One sentence summary].</li>
        <li><b>The Math:</b> [The equation from instructions] = [Total]. <br> [One sentence explaining the cost].</li>
        <li><b>Total Projected Impact:</b> [Insert Color Span Here][Final Number w/ Sign]</span></li>
        </ul>
        """
        response = active_model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error: {str(e)}"

# --- 5. RENDER LOGIC ---

# A. HEADER
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
        <div><span class="stat-label">System Status</span><br><span class="stat-value val-pos">MONITORING</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# B. MISSION BRIEFING (START SCREEN)
if not st.session_state.game_started:
    st.markdown("""
    <div class="mission-header">
        <div style="color:#0ea5e9; font-weight:bold; letter-spacing:3px; margin-bottom:10px;">CRITICAL INCIDENT DETECTED</div>
        <div class="mission-title">THE SILENT CHIP CRISIS</div>
    </div>
    
    <div class="context-box">
        <h3 style="margin-bottom:10px;">MISSION CONTEXT</h3>
        <p style="font-size:1.1rem; line-height:1.6;">
            You are the <strong>Supply Chain Director</strong> for a Medical Device company.<br>
            You manufacture life-saving <strong>ventilators</strong>. Production is running lean.
        </p>
    </div>
    
    <div class="financial-box">
        <h3 style="color:#0ea5e9; margin-bottom:15px; font-size:1.1rem;"><i class="fa-solid fa-calculator"></i> FINANCIAL LOGIC (THE MATH)</h3>
        <ul style="list-style:none; padding:0; margin:0; font-size:1rem;">
            <li style="margin-bottom:10px;"><strong>• Product:</strong> LifeBreath-3000 Ventilator</li>
            <li style="margin-bottom:10px;"><strong>• Weekly Production:</strong> 1,000 Units</li>
            <li style="margin-bottom:10px;"><strong>• Revenue per Unit:</strong> $25,000</li>
            <li style="margin-bottom:10px;"><strong>• Gross Margin (Profit):</strong> <span style="color:#10b981;">$10,000 per unit</span></li>
            <li style="margin-bottom:10px;"><strong>• Fixed Factory Burn Rate:</strong> <span style="color:#ef4444;">$2.0M per week</span> (Cost to keep factory open even if idle)</li>
        </ul>
    </div>

    <div class="trigger-box">
        <h3 style="color:#f59e0b; margin-bottom:10px;"><i class="fa-solid fa-bell"></i> INCOMING TRIGGER</h3>
        <p style="color:#fcd34d; font-size:1.1rem;">
            Your primary microcontroller supplier, <strong>TechCore</strong>, just reported a 2-week delay due to a "minor server outage."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("OPEN COMMAND CENTER", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# C. MAIN SCENARIO INTERFACE
elif not st.session_state.stage_complete:
    data = SCENARIO_DATA
    
    # Progress (Just 1 Node)
    st.markdown("""
    <div class="progress-track" style="justify-content:center;">
        <div class="track-node active" style="width:60px; height:60px; font-size:1.5rem;"><i class="fa-solid fa-triangle-exclamation"></i></div>
    </div>
    """, unsafe_allow_html=True)

    # AI Console
    ai_box = st.empty()
    current_text = st.session_state.nexus_analysis if st.session_state.nexus_analysis != "Initializing System... Scanning Global Supplier Nodes..." else data['aiMsg']
    
    # Check if text is HTML (list) or plain text
    if "<ul>" in current_text or "<span" in current_text:
        ai_content = current_text # Render as HTML
    else:
        ai_content = f"<div>{current_text}</div>"

    ai_box.markdown(f"""
    <div class="ai-console">
        <div class="console-header">
            <i class="fa-solid fa-robot" style="color:#0ea5e9;"></i> <span>NEXUS INTELLIGENCE FEED</span>
        </div>
        <div class="console-text">{ai_content}</div>
    </div>
    """, unsafe_allow_html=True)

    # Scenario Card
    st.markdown(f"""
    <div class="scenario-card">
        <div style="color:#0ea5e9; font-weight:bold; font-size:0.8rem;">{data['stageName']}</div>
        <h2 style="color:white; margin:0;">{data['title']}</h2>
        <p style="color:#94a3b8; font-size:1.1rem; margin-top:10px;">{data['desc']}</p>
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
            
            c1, c2 = st.columns(2)
            with c1: 
                if st.button("Consult Nexus", key=f"c{i}"):
                    # Spinner Animation
                    ai_box.markdown(f"""
                    <div class="ai-console">
                        <div class="console-header">
                            <i class="fa-solid fa-robot fa-spin" style="color:#0ea5e9;"></i> <span>ANALYZING INTELLIGENCE FEEDS...</span>
                        </div>
                        <div class="console-text" style="color:#0ea5e9;">Running Monte Carlo simulations on Profit Margins and Burn Rates...</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.nexus_analysis = get_gemini_response(data['desc'] + " " + data['aiMsg'], opt['title'])
                    st.rerun()

            with c2:
                if st.button("Select Option", key=f"s{i}"):
                    st.session_state.selected_option = i
                    st.rerun()

    # Finalize Button
    if st.session_state.selected_option is not None:
        st.markdown('<br><div class="primary-btn">', unsafe_allow_html=True)
        if st.button("EXECUTE DECISION", use_container_width=True):
            st.session_state.stage_complete = True
            choice = data['options'][st.session_state.selected_option]
            st.session_state.total_pnl = choice['impact']
            st.session_state.history.append({
                "stage": data['stageName'],
                "decision": choice['title'],
                "full_choice_data": choice
            })
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# D. END SCREEN (IMPACT REPORT)
else:
    # Logic for grading
    choice = SCENARIO_DATA['options'][st.session_state.selected_option]
    if choice['impact'] > 0:
        grade = "A+ (Resilient Strategist)"
        color = "#10b981" # Green
        icon = "fa-trophy"
        summary = "Excellent work. You correctly identified the insolvency signal and prioritized long-term continuity over short-term stability."
    elif choice['impact'] > -20:
        grade = "C- (Operational Failure)"
        color = "#f59e0b" # Orange
        icon = "fa-triangle-exclamation"
        summary = "The supply gap was closed, but significant quality risks were introduced. Resilience requires verifying the source of the supply."
    else:
        grade = "F (Catastrophic Collapse)"
        color = "#ef4444" # Red
        icon = "fa-skull-crossbones"
        summary = "Reliance on a single point of failure without verifying external data signals led to a complete production halt."

    st.markdown(f"""
    <div style="text-align:center; margin-bottom:3rem;">
        <i class="fa-solid fa-clipboard-check" style="font-size:3rem; color:#0ea5e9; margin-bottom:1rem;"></i>
        <h1 style="color:white;">Simulation Complete</h1>
        <p style="color:#94a3b8;">Financial Impact Assessment</p>
    </div>
    """, unsafe_allow_html=True)

    # Big Score Card
    st.markdown(f"""
    <div style="background:var(--panel-glass); border-radius:12px; padding:3rem; text-align:center; border:1px solid var(--border); margin-bottom:30px;">
        <h2 style="margin-bottom:15px; color:{color} !important;"><i class="fa-solid {icon}"></i> Overall Rating: {grade}</h2>
        <div style="font-size:1.2rem; color:white; margin-bottom:20px;">{summary}</div>
        <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:8px; display:inline-block;">
            <div style="font-size:0.9rem; color:#94a3b8; text-transform:uppercase; letter-spacing:1px;">Net P&L Impact</div>
            <div style="font-family:monospace; font-size:2.5rem; font-weight:bold; color:{color};">{pnl_display}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Math Card
    st.markdown("### <span style='color: white;'>Analysis Logic</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="report-card">
        <div class="report-title" style="color:{color};">
            <i class="fa-solid fa-calculator"></i> The Math Behind Your Result
        </div>
        <div style="color:#e2e8f0; margin-bottom:15px; font-size:1.1rem;">
            You chose: <strong>{choice['title']}</strong>
        </div>
        <div style="background:rgba(0,0,0,0.3); padding:15px; border-radius:6px; border-left:3px solid {color}; margin-bottom:15px;">
            <div style="font-family:monospace; color:#cbd5e1; font-size:1rem;">{choice['calc']}</div>
        </div>
        <div style="color:#94a3b8; font-size:0.95rem; line-height:1.6;">
            <strong>AI Post-Mortem:</strong> {choice['outcome']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("RESTART MISSION", use_container_width=True):
            st.session_state.clear()
            st.rerun()