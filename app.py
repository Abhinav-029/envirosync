import streamlit as st
from backend import smart_controller, update_occupancy, init_system
import time
import os
import base64
import pandas as pd


init_system()

DATA_DIR = "data"
def p(filename):
    return os.path.join(DATA_DIR, filename)



def get_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def read_log(filename):
    if not os.path.exists(filename):
        return pd.DataFrame()
    
    return pd.read_csv(filename)


def temp_based_theme(room_temp):
    if room_temp <= 20:
        color = "#38bdf8"
        bg_color = "#050d1a"
        side_color = "#030912"
        border =   "#0a2040"
    elif room_temp <= 28:
        color = "#818cf8"
        bg_color = "#0d0f1f"
        side_color = "#0a0c1a"
        border=  "#1e2050"
    elif room_temp <= 35:
        color = "#f59e0b"
        bg_color = "#1a1200"
        side_color = "#150e00"
        border=  "#3d2a00"
    elif room_temp > 35:
        color = "#ef4444"
        bg_color = "#1f0a0a"
        side_color = "#180808"
        border =  "#3d1010"
    return [color, bg_color, side_color, border]

st.set_page_config(layout="wide", page_title="EnviroSync - Smart Room Automation System", page_icon="⚡", initial_sidebar_state="collapsed")
st.title("EnviroSync")

st.markdown(
    '''

    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&family=Orbitron:wght@400..900&display=swap');
    h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
}

    </style>
''', unsafe_allow_html=True
)





des1, des2 = st.columns(2)

with des1:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&family=Orbitron:wght@400..900&family=Red+Rose:wght@300..700&display=swap');
</style>
                
<div style= "color: white; font-family: 'Red Rose';">
                EnviroSync is an intelligent room automation system that continuously
    monitors temperature, lighting, and occupancy in real-time. It
    automatically adjusts AC, fan speed, and lighting to maintain a
    comfortable and energy-efficient environment.
</div>
""", unsafe_allow_html=True)

    st.divider()


data = smart_controller()
# st.write(data)
room_temp = data["room_temp"]
occ_status = data["status"]
lux = data["light_intensity"]
fan = data["fan"]
ac_temp = data["ac_temp"]
light_status = data["light"]
empty_duration = data["empty_duration"]

ac_on_off_color = "#ef4444" if data["ac"] == "OFF" else "#00b7ffff"
ac_color = "#10b981" if data['ac'] == "ON" else "#ef4444"
fan_color = {"OFF":"#ef4444","LOW":"#f59e0b","MEDIUM":"#00b7ffff","HIGH":"#10b981"}.get(data['fan'], "#00d4ff")
occ_color = "#10b981" if occ_status == "Occupied" else "#ef4444"
light_color = {"OFF":"#ef4444","DIM":"#f59e0b","NORMAL":"#00b7ffff","BRIGHT":"#10b981"}.get(data['light'], "#00d4ff")
duration_color = "#00b7ffff" if empty_duration == "NA" else "#00b7ffff" if empty_duration <= 10 else "#ef4444"




fan_duration = {
    "OFF":    "0s",      
    "LOW":    "3s",    
    "MEDIUM": "1.5s",  
    "HIGH":   "0.5s"     
}.get(data['fan'], "0s")


st.subheader("📊 Live Sensor Readings")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Room Temperature: ", f"{room_temp}°C")
    st.divider()
    
with col2:
    st.metric("🧍 Occupancy", occ_status)
    st.divider()

with col3:
    st.metric("💡 Light Intensity", f"{lux} lux")
    st.divider()



left, right = st.columns(2)

with left:
    st.subheader("⚡ Device Status")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # AC Card
        st.markdown(f"""
        <div style="background:#1a2234;
                    border:1px solid {ac_on_off_color};
                    border-radius:12px;
                    padding:16px;
                    margin-bottom:12px;">
            <div style="color:#64748b; font-size:0.75rem;">❄️ AC STATE</div>
            <div style="color:{ac_on_off_color}; font-size:1.4rem; font-weight:bold;">
                {data['ac']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Fan Card
        st.markdown(f"""
<style>
@keyframes spin {{
    from {{ transform: rotate(0deg); }}
    to   {{ transform: rotate(360deg); }}
}}
.fan-icon {{
    width: 50px;
    height: 50px;
    animation: spin {fan_duration} linear infinite;
    opacity: {"0.3" if data['fan'] == "OFF" else "1"};
}}
</style>

<div style="background:#1a2234;
            border:1px solid {fan_color};
            border-top:3px solid {fan_color};
            border-radius:12px;
            padding:16px;
            margin-bottom:12px;
            display:flex;
            justify-content:space-between;
            align-items:center;">
    <div>
        <div style="color:#64748b; font-size:0.75rem;">🌀 FAN SPEED</div>
        <div style="color:{fan_color}; font-size:1.4rem; font-weight:bold;">
            {data['fan']}
        </div>
    </div>
    <img class="fan-icon" src="data:image/png;base64,{get_image_base64("icons/fan.png")}"/>
</div>
""", unsafe_allow_html=True)
        
        # Light Status Card
        st.markdown(f"""
        <div style="background:#1a2234; border:1px solid {light_color};
                    border-radius:12px; padding:16px; margin-bottom:12px;">
            <div style="color:#64748b; font-size:0.75rem;">💡 LIGHT STATUS</div>
            <div style="color:{light_color}; font-size:1.4rem; font-weight:bold;">
                {data['light']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # Occupancy Card
        st.markdown(f"""
        <div style="background:#1a2234; border:1px solid {occ_color};
                    border-radius:12px; padding:16px; margin-bottom:12px;">
            <div style="color:#64748b; font-size:0.75rem;">🧍 OCCUPANCY</div>
            <div style="color:{occ_color}; font-size:1.4rem; font-weight:bold;">
                {data['status']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AC Temp Card
        st.markdown(f"""
        <div style="background:#1a2234; border:1px solid {ac_color};
                    border-radius:12px; padding:16px; margin-bottom:12px;">
            <div style="color:#64748b; font-size:0.75rem;">🌡️ AC TEMP</div>
            <div style="color:{ac_color}; font-size:1.4rem; font-weight:bold;">
                {f"{data['ac_temp']}°C" if data['ac_temp'] else "OFF"}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Empty Duration Card
        st.markdown(f"""
        <div style="background:#1a2234; border:1px solid {duration_color};
                    border-radius:12px; padding:16px; margin-bottom:12px;">
            <div style="color:#64748b; font-size:0.75rem;">⏱ EMPTY DURATION</div>
            <div style="color:{duration_color}; font-size:1.4rem; font-weight:bold;">
                {"NA" if occ_status == "Occupied" else f"{empty_duration}s"}
            </div>
        </div>
        """, unsafe_allow_html=True)


with right:
    st.subheader("📋 History")
    if os.path.exists(p("history.txt")):
        with open(p("history.txt"), "r", encoding='utf-8') as f:
            history = f.read()
        history_li = history.split("\n\n")
        history_li_10 = history_li[-11:]
        rev_history = history_li_10[-2::-1]
        history_html = "<br><br>".join(
    [entry.replace("\n", "<br>") for entry in rev_history]
)
        if len(history) < 10:
            history_html = "No history yet..."
        st.markdown("""
        <style>
        .scroll-box {
            height: 275px;
            overflow-y: scroll;
            padding: 10px;
            border: 1px solid #3C3C3C;
            border-radius: 10px;
            background-color: #0e1117;
            color: #FAFAFA;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="scroll-box">
                {history_html}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.write("No history yet...")

    st.markdown("""
<div style="
    color: #cbd5f5;
    font-size: 1.1rem;
    margin-top: 10px;
    margin-bottom: 10px;">
    📥 Download History
</div>
""", unsafe_allow_html=True)
    download_content = "\n\n".join(rev_history)
    st.download_button(label="Download", data=download_content.encode("utf-8"), file_name="history_log.txt")
    
st.divider()


with st.sidebar:
    st.subheader("⚙️ Controls")
    
    auto_run = st.toggle("🔄 Auto Refresh", value=False)
    
    if auto_run:
        refresh_rate = st.slider("Refresh every (seconds)",
                                  min_value=1,
                                  max_value=30,
                                  value=5)
    
    occ = st.toggle("Occupancy", value=True)
    if occ:
        update_occupancy(1)
    else:
        update_occupancy(0)
    
    st.markdown(f"""
    <div style="color:#64748b; font-size:0.8rem;">
        Last updated: {time.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("🎨 Customizations")
    theme = st.selectbox(f"Change Theme", ["Default", "Temperature Based",  "Purple Galaxy", "Teal Storm"])
    if theme == "Default":
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0a0e1a;
            color: #00d4ff;
        }



        [data-testid="stSidebar"] {
            background-color: #111827 !important;  
            border-right: 2px solid #00d4ff !important;  
        }
        </style>
        """, unsafe_allow_html=True)
    
    elif theme == "Purple Galaxy":
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0d0a1a;
            color: #a855f7;
        }



        [data-testid="stSidebar"] {
            background-color: #130d24 !important;  
            border-right: 2px solid #a855f7 !important;  
        }
        </style>
        """, unsafe_allow_html=True)
    
    elif theme == "Teal Storm":
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #00100f;
            color: #2dd4bf;
        }



        [data-testid="stSidebar"] {
            background-color: #051a18 !important;  
            border-right: 2px solid #2dd4bf !important;  
        }
        </style>
        """, unsafe_allow_html=True)
    
    else:
        colors = temp_based_theme(room_temp)

        st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-color: {colors[1]};
            color: {colors[0]};
        }}



        [data-testid="stSidebar"] {{
            background-color: {colors[2]} !important;  
            border-right: 2px solid {colors[3]} !important;  
        }}
        </style>
        """, unsafe_allow_html=True)

    st.divider()

    

    


st.subheader("📈 Graphical Insights")

temp_graph, light_graph = st.columns(2)

with temp_graph:

    st.markdown("""
<div style="
    color: white;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 10px;">
    🌡️ Temperature Graph(°C)
</div>
""", unsafe_allow_html=True)
    

    df1 = read_log(p("temp_log.csv")).tail(50)

    if not df1.empty:
        st.line_chart(df1.set_index("Time")["Temperature"])
    else:
        st.write("No data yet...")

with light_graph:
    st.markdown("""
<div style="
    width:20px,
    color: white;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 10px;">
    💡 Light Graph(lux)
</div>
""", unsafe_allow_html=True)
    


    df2 = read_log(p("light_log.csv")).tail(50)
    if not df2.empty:
        st.line_chart(df2.set_index("Time")["Light"])
    else:
        st.write("No data yet...")
    

st.divider()

if auto_run:
    time.sleep(refresh_rate)
    st.rerun()

# st.markdown("")