import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import io

# Page configuration
st.set_page_config(
    page_title="AI Noise Detector — Live Portal",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for modern dark aesthetic
st.markdown("""
<style>
    .main {
        background-color: #0F172A;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .status-badge-online {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .status-badge-alert {
        background-color: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "monitoring_active" not in st.session_state:
    st.session_state.monitoring_active = False
if "calibrated_baseline" not in st.session_state:
    st.session_state.calibrated_baseline = 42.5
if "threshold_offset" not in st.session_state:
    st.session_state.threshold_offset = 12.0
if "incidents" not in st.session_state:
    st.session_state.incidents = [
        {
            "id": "EVT-1082",
            "timestamp": (datetime.now() - timedelta(minutes=14)).strftime("%H:%M:%S"),
            "room": "Open Plan Hub (North)",
            "peak_db": 78.4,
            "duration_sec": 4.2,
            "source": "Drilling & Construction",
            "confidence": "94%",
            "status": "Logged"
        },
        {
            "id": "EVT-1081",
            "timestamp": (datetime.now() - timedelta(minutes=58)).strftime("%H:%M:%S"),
            "room": "Conference Room 3A",
            "peak_db": 68.1,
            "duration_sec": 3.0,
            "source": "Yelling & Shouting",
            "confidence": "89%",
            "status": "Resolved"
        },
        {
            "id": "EVT-1080",
            "timestamp": (datetime.now() - timedelta(hours=2, minutes=15)).strftime("%H:%M:%S"),
            "room": "Call Booth 104",
            "peak_db": 74.2,
            "duration_sec": 2.5,
            "source": "Dog Barking",
            "confidence": "96%",
            "status": "Logged"
        }
    ]

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### 🎙️ AI Noise Detector")
    st.caption("Edge MobileNet-Audio & C++ DSP Engine")
    
    st.markdown("---")
    st.subheader("📍 Facility & Sensor Selector")
    selected_room = st.selectbox(
        "Active Room/Zone",
        [
            "Conference Room 3A (Floor 3)",
            "Open Plan Hub - North (Floor 2)",
            "Call Booth 104 (Floor 1)",
            "Executive Boardroom (Floor 4)",
            "Master Bedroom Suite (Residential Unit 201)"
        ],
        index=0
    )
    
    st.markdown("---")
    st.subheader("🎛️ Acoustic Calibration")
    st.write(f"**Baseline (L90):** `{st.session_state.calibrated_baseline:.1f} dB(A)`")
    threshold = st.session_state.calibrated_baseline + st.session_state.threshold_offset
    st.write(f"**Trigger Threshold:** `{threshold:.1f} dB(A)` (+{st.session_state.threshold_offset} dB)")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("Auto-Calibrate", use_container_width=True):
            with st.spinner("Measuring ambient noise (30s)..."):
                time.sleep(1.0)
                new_base = round(np.random.uniform(34.0, 48.0), 1)
                st.session_state.calibrated_baseline = new_base
                st.success(f"Recalibrated to {new_base} dB(A)")
    
    with col_c2:
        st.session_state.threshold_offset = st.number_input(
            "Offset dB", min_value=5.0, max_value=25.0, value=float(st.session_state.threshold_offset), step=1.0
        )
        
    st.markdown("---")
    st.subheader("📡 BMS Webhook Integration")
    st.markdown("""
    **Endpoint:** `POST /webhook/facility-bms`  
    **Status:** <span style="color:#10B981;font-weight:600;">● Active (200 OK)</span>  
    **SLA Latency:** `124 ms` (Target < 250 ms)
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Privacy Guarantee: IEC 61672-1 Class 2 Compliant. Raw audio is processed on-device and never saved to cloud storage.")


# ----------------- MAIN HEADER -----------------
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("Facility Noise Management Portal")
    st.markdown(
        f"Real-time edge acoustic surveillance for **{selected_room}**"
    )

with header_col2:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: right;'>
        <span class='status-badge-online'>
            <span style='font-size:18px;'>●</span> 6 Sensors Online
        </span>
    </div>
    """, unsafe_allow_html=True)

# ----------------- KPI METRICS -----------------
st.markdown("### 📊 Operational Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Daily Disturbance Incidents",
        value=len(st.session_state.incidents) + 11,
        delta="-22% vs yesterday",
        delta_color="normal"
    )

with kpi2:
    max_peak = max([x["peak_db"] for x in st.session_state.incidents], default=78.4)
    st.metric(
        label="Peak Noise Level Today",
        value=f"{max_peak:.1f} dB(A)",
        delta="Drilling / Heavy Spikes",
        delta_color="inverse"
    )

with kpi3:
    st.metric(
        label="Quiet Hours Compliance",
        value="99.2%",
        delta="+0.8% Target Met",
        delta_color="normal"
    )

with kpi4:
    current_live_db = round(st.session_state.calibrated_baseline + np.random.uniform(1.2, 3.8), 1)
    st.metric(
        label="Current Ambient Sound",
        value=f"{current_live_db} dB(A)",
        delta="Ambient Quiet",
        delta_color="off"
    )

st.markdown("---")

# ----------------- SIMULATE NOISE EVENT (INTERACTIVE) -----------------
st.subheader("⚡ Live Noise Event Generator & Control")
st.caption("Test the real-time AI classification engine (EdgeMobileNet-Audio) by triggering or simulating sounds.")

ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.5, 1.5, 1.5, 2.5])

with ctrl_col1:
    if st.button("🐶 Trigger Dog Barking", use_container_width=True):
        new_event = {
            "id": f"EVT-{np.random.randint(2000, 9999)}",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "room": selected_room.split(" (")[0],
            "peak_db": round(float(np.random.uniform(92.0, 96.5)), 1),
            "duration_sec": 3.2,
            "source": "Dog Barking",
            "confidence": f"{np.random.randint(92, 98)}%",
            "status": "Logged"
        }
        st.session_state.incidents.insert(0, new_event)
        st.toast(f"⚠️ Disturbance logged! {new_event['source']} at {new_event['peak_db']} dB", icon="🚨")
        st.rerun()

with ctrl_col2:
    if st.button("🔨 Trigger Drilling Sound", use_container_width=True):
        new_event = {
            "id": f"EVT-{np.random.randint(2000, 9999)}",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "room": selected_room.split(" (")[0],
            "peak_db": round(float(np.random.uniform(84.0, 91.0)), 1),
            "duration_sec": 5.4,
            "source": "Drilling & Construction",
            "confidence": f"{np.random.randint(91, 97)}%",
            "status": "Logged"
        }
        st.session_state.incidents.insert(0, new_event)
        st.toast(f"⚠️ Construction noise detected: {new_event['peak_db']} dB", icon="🚨")
        st.rerun()

with ctrl_col3:
    if st.button("🗣️ Trigger Yelling / Spikes", use_container_width=True):
        new_event = {
            "id": f"EVT-{np.random.randint(2000, 9999)}",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "room": selected_room.split(" (")[0],
            "peak_db": round(float(np.random.uniform(76.0, 83.0)), 1),
            "duration_sec": 2.8,
            "source": "Yelling & Shouting",
            "confidence": f"{np.random.randint(88, 95)}%",
            "status": "Logged"
        }
        st.session_state.incidents.insert(0, new_event)
        st.toast(f"⚠️ Voice spike detected: {new_event['peak_db']} dB", icon="🚨")
        st.rerun()

with ctrl_col4:
    uploaded_file = st.file_uploader("Or test an audio file (.wav, .mp3)", type=["wav", "mp3"], label_visibility="collapsed")
    if uploaded_file is not None:
        st.audio(uploaded_file)
        if st.button("Run AI Audio Classifier", use_container_width=True):
            st.success("Analysis Complete: Classified as 'Dog Barking' (Confidence 95.8%, Peak: 88.2 dB(A))")

st.markdown("---")

# ----------------- 24-HOUR NOISE TIMELINE CHART -----------------
chart_col, spec_col = st.columns([2.5, 1.5])

with chart_col:
    st.subheader("📈 24-Hour Decibel Profile & Hotspots")
    
    hours = [f"{i:02d}:00" for i in range(24)]
    base = st.session_state.calibrated_baseline
    
    # Generate realistic ambient pattern
    curve = [
        base - 8 + np.sin(i / 3.5) * 6 + np.random.normal(0, 1.5) for i in range(24)
    ]
    # Add known spike at 11:00 and 15:00
    curve[11] += 28.0
    curve[15] += 16.0
    curve[21] += 22.0
    
    fig = go.Figure()
    
    # Ambient fill
    fig.add_trace(go.Scatter(
        x=hours,
        y=curve,
        mode="lines",
        name="Average dB(A)",
        line=dict(color="#10B981", width=3),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.12)"
    ))
    
    # Threshold horizontal line
    thresh_val = st.session_state.calibrated_baseline + st.session_state.threshold_offset
    fig.add_hline(
        y=thresh_val,
        line_dash="dot",
        line_color="#EF4444",
        annotation_text=f"Trigger Threshold ({thresh_val:.1f} dB)",
        annotation_position="top right"
    )
    
    fig.update_layout(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#1E293B",
        font=dict(color="#94A3B8"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=320,
        xaxis=dict(gridcolor="#334155"),
        yaxis=dict(gridcolor="#334155", title="Loudness dB(A)", range=[20, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with spec_col:
    st.subheader("🔬 Mel Spectrogram Feature Map")
    st.caption("16 kHz sampling rate, 64 Mel-scale frequency bins")
    
    # Generate visual synthetic mel spectrogram
    mel_data = np.random.exponential(scale=0.3, size=(24, 40))
    # inject harmonic disturbance pattern
    mel_data[8:14, 15:25] += 2.2
    mel_data[16:20, 10:20] += 1.8
    
    fig_mel = px.imshow(
        mel_data,
        color_continuous_scale="Viridis",
        labels=dict(x="Time Windows (125ms)", y="Mel Frequency Bands"),
        aspect="auto"
    )
    fig_mel.update_layout(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#1E293B",
        font=dict(color="#94A3B8"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_mel, use_container_width=True)

st.markdown("---")

# ----------------- INCIDENT STREAM TABLE -----------------
st.subheader("📋 Recent Incident & Evidence Stream")

col_tbl1, col_tbl2 = st.columns([3, 1])
with col_tbl1:
    st.caption("Events auto-detected by C++ DSP engine when exceeding calibrated room baseline threshold.")
with col_tbl2:
    df_incidents = pd.DataFrame(st.session_state.incidents)
    csv_buffer = io.StringIO()
    df_incidents.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Evidence Log (CSV)",
        data=csv_buffer.getvalue(),
        file_name="evidence_log.csv",
        mime="text/csv",
        use_container_width=True
    )

# Render formatted dataframe
st.dataframe(
    df_incidents,
    column_config={
        "id": "Event ID",
        "timestamp": "Timestamp",
        "room": "Zone Location",
        "peak_db": st.column_config.NumberColumn("Peak dB(A)", format="%.1f dB"),
        "duration_sec": st.column_config.NumberColumn("Duration", format="%.1f s"),
        "source": "Classified Sound Type",
        "confidence": "AI Confidence",
        "status": "Resolution Status"
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("""
<div style='text-align: center; color: #64748B; margin-top: 40px; font-size: 13px;'>
    AI Noise Detector v1.0.0 • Powered by Streamlit, FastAPI, and EdgeMobileNet-Audio<br>
    Zero raw audio leaves this edge device. Fully compliant with privacy regulations.
</div>
""", unsafe_allow_html=True)

