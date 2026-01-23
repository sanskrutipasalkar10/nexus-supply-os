# 🕸️ Nexus Supply-OS: The Silent Chip Crisis

## 📌 Project Overview
**Nexus Supply-OS** is an AI-driven supply chain simulation game designed to train professionals in strategic decision-making under pressure. This specific scenario, **"The Silent Chip Crisis,"** places the user in the role of a Supply Chain Director at a medical device company facing a critical supplier failure.

The application demonstrates how AI intelligence (Nexus) can uncover hidden risks (insolvency, ransomware) that traditional human intuition might miss, quantifying the financial impact of every decision.

---

## 🚀 Scenario: "The Silent Chip Crisis"

### **Context**
* **Role:** Supply Chain Director, MedTech Corp.
* **Product:** LifeBreath-3000 Ventilator (Critical Medical Device).
* **Status:** Production is JIT (Just-in-Time) and running lean.
* **Trigger:** Your trusted supplier, **TechCore**, reports a "2-week delay" due to a "server glitch."

### **The Intelligence Gap**
* **Human View:** Trust the 5-year partner. Wait it out.
* **AI View (Nexus):** Detected dark web chatter about a **Ransomware Attack** on industrial water filtration systems and a spike in executive stock dumping. **Prediction:** 94% Insolvency Risk.

### **The Decisions**
1. **Trust TechCore (Wait):** Stick with the partner.
   * *Risk:* Bankruptcy & Production Halt.
2. **Spot Market (Panic):** Buy unverified stock immediately.
   * *Risk:* Counterfeit parts & FDA Recalls.
3. **OmniChip Pivot (AI Strategic):** Pay a premium to switch vendors *now*.
   * *Result:* Market Dominance & Continuity.

---

## 💰 Financial Logic (The Math)

The application calculates impact based on these hardcoded variables:

| Variable | Value | Description |
| :--- | :--- | :--- |
| **Weekly Burn Rate** | **$2M** | Fixed factory costs (wages, energy) paid even if idle. |
| **Profit Margin** | **$10k/unit** | Net profit per ventilator. |
| **Recall Cost** | **$15M** | Logistics + Legal liability for bad quality chips. |
| **Pivot Fee** | **$2M** | Upfront cost to switch suppliers immediately. |

### **Impact Calculations**
* **Insolvency (Option A):** 8 Weeks Downtime × ($2M Burn + $10M Lost Profit) = **-$96M**
* **Recall (Option B):** Fixed Cost = **-$15M**
* **Pivot (Option C):** (2,000 Extra Units × $10k Margin) - $2M Fee = **+$18M**

---

## 🎮 Key Features

- **Interactive Decision-Making**: Real-time scenario with three strategic options
- **AI Risk Analysis**: Real-time risk assessments powered by Google Gemini API
- **Financial Impact Tracking**: P&L calculations based on your decisions
- **Professional UI**: Dark-themed, glassmorphic interface with responsive design
- **Performance Grading**: Executive-level business impact assessment
- **Detailed Post-Mortem**: Analysis of each decision and financial implications

## 🛠️ Installation & Setup

### **Prerequisites**
* Python 3.10 or higher
* A Google Gemini API Key (Get one [here](https://aistudio.google.com/app/apikey))
* pip (Python package manager)

### **1. Clone the Repository**
```bash
git clone https://github.com/sanskrutipasalkar10/nexus-supply-os.git
cd nexus-supply-os
```

### **2. Create a Virtual Environment (Recommended)**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure API Key**
Create a `.env` file in the project root and add your Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

Or set it as an environment variable directly in your terminal.

---

## 🚀 Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   - Opens automatically at `http://localhost:8501`
   - If not, copy the URL from terminal output

3. **Play the simulation**
   - Click "OPEN COMMAND CENTER" to begin
   - Review the scenario and financial logic
   - Use "Consult Nexus" to get AI risk analysis for each option
   - Select your decision with "Select Option"
   - Click "EXECUTE DECISION" to finalize
   - Review your performance grade and financial impact

## 📂 Project Structure

```
nexus-supply-os/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (API keys)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── static/               # Static assets
│   └── style.css         # Custom styling
└── templates/            # HTML templates (if applicable)
    └── index.html
```

## 🔧 Technologies Used

- **Streamlit** - Web application framework for data apps
- **Google Generative AI (Gemini)** - LLM-powered risk analysis
- **Python 3.10+** - Core language
- **python-dotenv** - Environment variable management
- **Font Awesome 6.4** - Icon library

---

## 📊 Performance Ratings

Your final grade is determined by the financial P&L impact:

| Grade | P&L Impact | Description |
| :--- | :--- | :--- |
| **A+ (Resilient Strategist)** | +$18M | Excellent strategic execution with market dominance |
| **C- (Operational Failure)** | -$15M | Supply gap closed but significant quality risks |
| **F (Catastrophic Collapse)** | -$96M | Total production halt and company crisis |

---

## 🎯 Strategic Tips

1. **Always consult the AI analysis** before making decisions
2. **Pay attention to data signals** (insolvency risk %, dark web chatter)
3. **Think beyond immediate costs** - Consider total financial impact over time
4. **Quality vs. Speed trade-off** - A cheaper solution isn't always better
5. **Use predictive intelligence** to make proactive decisions

---

## ⚠️ Troubleshooting

**"API KEY MISSING IN CODE"**
- Ensure your `.env` file has `GEMINI_API_KEY=your_key`
- Or set the environment variable before running

**"No compatible Gemini model found"**
- Check your internet connection
- Verify your API key is valid and has quota remaining
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to check status

**Port 8501 already in use**
- Run on a different port: `streamlit run app.py --server.port 8502`

**Application won't load**
- Try clearing Streamlit cache: `streamlit cache clear`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

## 📝 License

This project is provided as-is for educational and business simulation purposes.

---

## 👤 Author & Contact

**Nexus Supply-OS** - AI-Driven Resilience Engine

Built with Streamlit and Google Gemini AI

**GitHub:** [sanskrutipasalkar10/nexus-supply-os](https://github.com/sanskrutipasalkar10/nexus-supply-os)

---

**Last Updated:** January 23, 2026  
**Version:** 1.0  
**Status:** Active Development
