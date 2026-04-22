# ⚡ EnviroSync — Smart Room Automation System

An intelligent room automation system that monitors temperature, 
lighting, and occupancy in real-time and automatically controls 
AC, fan, heater, and lighting.

## Features
- Real-time temperature and light monitoring
- Auto AC, heater, and fan control
- Occupancy detection with auto shutdown
- Live graphical insights
- Multiple themes including temperature-based dynamic theme
- Automation history log with download option

## How to Run
1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   streamlit run app.py

## Project Structure
project/
├── app.py          # Streamlit UI
├── backend.py      # Automation logic
├── requirements.txt
├── icons/
│   └── fan.png
└── data/           # Auto-created on first run