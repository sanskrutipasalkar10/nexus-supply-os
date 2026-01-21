# Nexus Supply-OS 🕸️

**AI-Driven Supply Chain Risk Simulation Engine**

An interactive, gamified supply chain management simulator powered by Google Gemini AI. Navigate critical supply chain decisions across Raw Material Sourcing, Manufacturing Partnerships, Global Logistics, and Quality Assurance to bring a flagship EV (Model-X) to market profitably.

## Features

- **Interactive Decision-Making**: Navigate 4 critical supply chain stages with realistic scenarios
- **AI Risk Analysis**: Real-time risk assessments powered by Google Gemini API
- **Financial Impact Tracking**: Real-time P&L calculations based on your decisions
- **Professional UI**: Dark-themed, glassmorphic interface with responsive design
- **Performance Grading**: Executive-level business impact assessment at the end
- **Stage-by-Stage Review**: Detailed analysis of each decision made during the simulation

## Scenarios Included

1. **Raw Material Sourcing** - Navigate lithium supply volatility and mining strikes
2. **Manufacturing Partner** - Select vendors balancing cost, quality, and reliability
3. **Global Logistics** - Respond to geopolitical disruptions (Red Sea blockade)
4. **Quality Assurance** - Balance speed-to-market with product safety

## Prerequisites

- Python 3.8 or higher
- Google Gemini API Key
- pip (Python package manager)

## Installation

1. **Clone/Download the project**
   ```bash
   cd "path/to/project"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### API Key Setup

1. Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Open `app.py` and replace the placeholder:
   ```python
   GEMINI_API_KEY = "YOUR_API_KEY_HERE"
   ```

> ⚠️ **Security Warning**: Never commit API keys to version control. For production, use environment variables:
> ```python
> import os
> GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
> ```

## Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   - Opens automatically at `http://localhost:8501`
   - If not, copy the URL from terminal output

3. **Play the simulation**
   - Click "INITIALIZE OPERATIONS" to begin
   - Review AI analysis for each scenario using "Consult"
   - Select your decision and click "FINALIZE DECISION"
   - Progress through all 4 stages
   - Review your executive summary and performance grade

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Technologies Used

- **Streamlit** - Web application framework
- **Google Generative AI** - Gemini API for risk analysis
- **Font Awesome** - Icon library
- **Python 3** - Core language

## Performance Ratings

- **A+ (Resilient Strategist)**: Final P&L > $0M - Excellent predictive work
- **B (Operational Manager)**: Final P&L between -$10M and $0M - Operations stable
- **C (Critical Failure)**: Final P&L < -$10M - Supply chain collapsed

## Tips for Success

1. Always consult the AI analysis before making decisions
2. Pay attention to probability warnings (e.g., "85% probability of strikes")
3. Consider Total Cost of Ownership, not just upfront costs
4. Balance speed with safety in quality decisions
5. Use AI insights to predict market movements

## Troubleshooting

**"API KEY MISSING IN CODE"**
- Ensure you've set `GEMINI_API_KEY` in the code

**"No compatible Gemini model found"**
- Check your internet connection
- Verify API key is valid and has sufficient quota

**Port 8501 already in use**
- Run on a different port: `streamlit run app.py --server.port 8502`

## License

This project is provided as-is for educational and business simulation purposes.

## Author

Nexus Supply-OS - AI-Driven Resilience Engine
Built with Streamlit and Google Gemini AI

---

**Last Updated**: January 2026
**Version**: 1.0
