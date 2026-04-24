import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataCenter360 Intelligence Platform",
    page_icon="🖥️",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    health    = pd.read_csv("data/server_health_scores.csv")
    incidents = pd.read_csv("data/incident_summary.csv")
    pue       = pd.read_csv("data/pue_metrics.csv")
    weather   = pd.read_csv("data/weather_performance_correlation.csv")
    anomaly   = pd.read_csv("data/server_anomaly_scores.csv")
    return health, incidents, pue, weather, anomaly

health, incidents, pue, weather, anomaly = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/server.png", width=60)
st.sidebar.title("DataCenter360")
st.sidebar.markdown("**Intelligence Platform**")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Executive Summary",
     "🖥️ Server Health",
     "🚨 Incident Analysis",
     "⚡ PUE & Power",
     "🌤️ Weather & Performance",
     "🤖 Predictive Alerts"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("📍 Ashburn, VA")
st.sidebar.markdown("🔄 Data refreshed daily at 6AM ET")

# ── Helper: KPI card row ──────────────────────────────────────────────────────
def kpi(col, label, value, color="#4CAF50"):
    col.markdown(
        f"""
        <div style='background:#1e1e2e;padding:16px;border-radius:10px;
                    border-left:4px solid {color};text-align:center;'>
            <div style='color:#aaa;font-size:13px'>{label}</div>
            <div style='color:white;font-size:28px;font-weight:bold'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Executive Summary
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Executive Summary":
    st.title("🖥️ DataCenter360 Intelligence Platform")
    st.markdown("### Executive Summary — Ashburn, VA Operations")
    st.markdown("---")

    # ── KPI Row 1: Operations ─────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    total_servers  = len(health)
    critical       = len(health[health["health_status"] == "Critical"])
    open_incidents = int(incidents["open_incidents"].sum())
    avg_pue        = round(pue["pue_proxy"].mean(), 3)

    kpi(c1, "Total Servers",    total_servers,  "#2196F3")
    kpi(c2, "Critical Servers", critical,       "#f44336")
    kpi(c3, "Open Incidents",   open_incidents, "#FF9800")
    kpi(c4, "Avg PUE Proxy",    avg_pue,        "#4CAF50")

    st.markdown("###")

    # ── KPI Row 2: ML Anomaly Alerts ─────────────────────────────────────────
    c5, c6, c7, c8 = st.columns(4)
    high_risk    = len(anomaly[anomaly["risk_level"] == "High Risk"])
    medium_risk  = len(anomaly[anomaly["risk_level"] == "Medium Risk"])
    anomaly_rate = round(len(anomaly[anomaly["is_anomaly"] == "Anomaly"]) / len(anomaly) * 100, 1)
    total_anomalies = len(anomaly[anomaly["is_anomaly"] == "Anomaly"])

    kpi(c5, "ML: High Risk Servers",    high_risk,       "#f44336")
    kpi(c6, "ML: Medium Risk Servers",  medium_risk,     "#FF9800")
    kpi(c7, "ML: Total Anomalies",      total_anomalies, "#9C27B0")
    kpi(c8, "ML: Anomaly Rate %",       anomaly_rate,    "#2196F3")

    st.markdown("---")
    col1, col2 = st.columns(2)

    # Health status donut
    with col1:
        st.subheader("Server Health Distribution")
        fig = px.pie(
            health, names="health_status",
            color="health_status",
            color_discrete_map={
                "Healthy":"#4CAF50","Warning":"#FF9800",
                "Critical":"#f44336","Decommissioned":"#9E9E9E"
            },
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

    # PUE status donut
    with col2:
        st.subheader("PUE Status Distribution")
        fig = px.pie(
            pue, names="pue_status",
            color="pue_status",
            color_discrete_map={
                "Efficient":"#4CAF50",
                "Acceptable":"#FF9800",
                "Inefficient":"#f44336"
            },
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    # Anomaly risk breakdown bar
    with col3:
        st.subheader("ML Anomaly Risk by Location")
        df_risk_loc = anomaly[anomaly["is_anomaly"] == "Anomaly"] \
            .groupby(["data_center_location", "risk_level"])["is_anomaly"] \
            .count().reset_index()
        df_risk_loc.columns = ["data_center_location", "risk_level", "count"]
        fig = px.bar(
            df_risk_loc,
            x="data_center_location",
            y="count",
            color="risk_level",
            color_discrete_map={
                "High Risk":   "#f44336",
                "Medium Risk": "#FF9800",
                "Low Risk":    "#4CAF50"
            },
            barmode="stack"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Incident summary bar
    with col4:
        st.subheader("Incidents by Location & Severity")
        fig = px.bar(
            incidents, x="data_center_location",
            y="total_incidents", color="severity",
            color_discrete_map={
                "Critical":"#f44336","High":"#FF9800",
                "Medium":"#2196F3","Low":"#4CAF50"
            },
            barmode="stack"
        )
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Server Health
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🖥️ Server Health":
    st.title("🖥️ Server Health Overview")
    st.markdown("---")

    # Filters
    col1, col2 = st.columns(2)
    locations = ["All"] + list(health["data_center_location"].dropna().unique())
    statuses  = ["All"] + list(health["health_status"].dropna().unique())
    loc_filter = col1.selectbox("Filter by Location", locations)
    sts_filter = col2.selectbox("Filter by Health Status", statuses)

    df = health.copy()
    if loc_filter != "All":
        df = df[df["data_center_location"] == loc_filter]
    if sts_filter != "All":
        df = df[df["health_status"] == sts_filter]

    # KPIs
    c1, c2, c3 = st.columns(3)
    kpi(c1, "Filtered Servers",  len(df),                              "#2196F3")
    kpi(c2, "Avg Health Score",  round(df["health_score"].mean(), 1),  "#4CAF50")
    kpi(c3, "Avg CPU %",         round(df["avg_cpu_pct"].mean(), 1),   "#FF9800")

    st.markdown("---")

    # Health score bar chart
    st.subheader("Health Score by Server")
    fig = px.bar(
        df.sort_values("health_score"),
        x="server_id", y="health_score",
        color="health_status",
        color_discrete_map={
            "Healthy":"#4CAF50","Warning":"#FF9800",
            "Critical":"#f44336","Decommissioned":"#9E9E9E"
        }
    )
    fig.add_hline(y=70, line_dash="dash", line_color="#4CAF50",
                  annotation_text="Healthy threshold")
    fig.add_hline(y=50, line_dash="dash", line_color="#FF9800",
                  annotation_text="Warning threshold")
    st.plotly_chart(fig, use_container_width=True)

    # Scatter CPU vs RAM
    st.subheader("CPU vs RAM Utilization")
    fig = px.scatter(
        df.dropna(subset=["avg_power_watts"]), x="avg_cpu_pct", y="avg_ram_pct",
        color="health_status", size="avg_power_watts",
        hover_data=["server_id", "data_center_location"],
        color_discrete_map={
            "Healthy":"#4CAF50","Warning":"#FF9800",
            "Critical":"#f44336","Decommissioned":"#9E9E9E"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    # Raw data table
    st.subheader("Server Detail Table")
    st.dataframe(df[[
        "server_id","data_center_location","server_type",
        "health_status","health_score","avg_cpu_pct",
        "avg_ram_pct","avg_power_watts","status"
    ]].reset_index(drop=True), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Incident Analysis
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🚨 Incident Analysis":
    st.title("🚨 Incident Analysis")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    kpi(c1, "Total Incidents",    int(incidents["total_incidents"].sum()),  "#2196F3")
    kpi(c2, "Open Incidents",     int(incidents["open_incidents"].sum()),   "#f44336")
    kpi(c3, "Avg Resolution Hrs", round(incidents["avg_resolution_hrs"].mean(), 2), "#FF9800")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incidents by Type")
        fig = px.pie(
            incidents, names="incident_type",
            values="total_incidents", hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Incidents by Severity")
        fig = px.pie(
            incidents, names="severity",
            values="total_incidents",
            color="severity",
            color_discrete_map={
                "Critical":"#f44336","High":"#FF9800",
                "Medium":"#2196F3","Low":"#4CAF50"
            },
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Avg Resolution Time by Incident Type")
    fig = px.bar(
        incidents.groupby("incident_type")["avg_resolution_hrs"]
        .mean().reset_index().sort_values("avg_resolution_hrs", ascending=False),
        x="incident_type", y="avg_resolution_hrs",
        color="avg_resolution_hrs",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Incident Detail Table")
    st.dataframe(incidents.reset_index(drop=True), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PUE & Power
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚡ PUE & Power":
    st.title("⚡ PUE & Power Efficiency")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    kpi(c1, "Avg PUE Proxy",        round(pue["pue_proxy"].mean(), 3),         "#2196F3")
    kpi(c2, "Total Power (W)",       int(pue["total_power_watts"].sum()),       "#FF9800")
    kpi(c3, "Inefficient Readings",  len(pue[pue["pue_status"]=="Inefficient"]), "#f44336")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("PUE Status Distribution")
        fig = px.pie(
            pue, names="pue_status",
            color="pue_status",
            color_discrete_map={
                "Efficient":"#4CAF50",
                "Acceptable":"#FF9800",
                "Inefficient":"#f44336"
            },
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("PUE by Location")
        fig = px.bar(
            pue.groupby("data_center_location")["pue_proxy"]
            .mean().reset_index(),
            x="data_center_location", y="pue_proxy",
            color="data_center_location"
        )
        fig.add_hline(y=1.5, line_dash="dash",
                      line_color="red", annotation_text="Industry threshold (1.5)")
        fig.add_hline(y=1.3, line_dash="dash",
                      line_color="green", annotation_text="Efficient threshold (1.3)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("CPU Utilization vs Power Consumption")
    fig = px.scatter(
        pue, x="avg_cpu_pct", y="total_power_watts",
        color="pue_status", size="pue_proxy",
        color_discrete_map={
            "Efficient":"#4CAF50",
            "Acceptable":"#FF9800",
            "Inefficient":"#f44336"
        },
        hover_data=["data_center_location"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — Weather & Performance
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌤️ Weather & Performance":
    st.title("🌤️ Weather & Performance Correlation")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    kpi(c1, "Avg Max Temp (°F)",     round(weather["temp_max_f"].mean(), 1),      "#FF9800")
    kpi(c2, "Avg CPU %",             round(weather["avg_cpu_pct"].mean(), 1),     "#2196F3")
    kpi(c3, "Avg Power (W)",         round(weather["avg_power_watts"].mean(), 1), "#f44336")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Heat Stress Distribution")
        fig = px.pie(
            weather, names="heat_stress",
            color="heat_stress",
            color_discrete_map={
                "High":"#f44336",
                "Moderate":"#FF9800",
                "Low":"#4CAF50"
            },
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Temperature vs Power Consumption")
        fig = px.scatter(
            weather, x="temp_max_f", y="avg_power_watts",
            color="heat_stress",
            color_discrete_map={
                "High":"#f44336",
                "Moderate":"#FF9800",
                "Low":"#4CAF50"
            },
            hover_data=["date"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Temperature vs CPU Performance Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weather["date"], y=weather["temp_max_f"],
        name="Max Temp (°F)", line=dict(color="#FF9800")
    ))
    fig.add_trace(go.Scatter(
        x=weather["date"], y=weather["avg_cpu_pct"],
        name="Avg CPU %", line=dict(color="#2196F3"),
        yaxis="y2"
    ))
    fig.update_layout(
        yaxis=dict(title="Max Temp (°F)"),
        yaxis2=dict(title="Avg CPU %", overlaying="y", side="right"),
        legend=dict(x=0, y=1.1, orientation="h")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Weather & Performance Detail Table")
    st.dataframe(weather.reset_index(drop=True), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — Predictive Alerts (ML Anomaly Detection)
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 Predictive Alerts":
    st.title("🤖 Predictive Alerts — ML Anomaly Detection")
    st.markdown("**Model: Isolation Forest | Features: CPU, RAM, Storage, Network, Power**")
    st.markdown("---")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    high_risk   = len(anomaly[anomaly["risk_level"] == "High Risk"])
    medium_risk = len(anomaly[anomaly["risk_level"] == "Medium Risk"])
    low_risk    = len(anomaly[anomaly["risk_level"] == "Low Risk"])
    anomaly_pct = round(len(anomaly[anomaly["is_anomaly"] == "Anomaly"]) / len(anomaly) * 100, 1)

    kpi(c1, "High Risk Readings",   high_risk,   "#f44336")
    kpi(c2, "Medium Risk Readings", medium_risk, "#FF9800")
    kpi(c3, "Low Risk Readings",    low_risk,    "#4CAF50")
    kpi(c4, "Anomaly Rate %",       anomaly_pct, "#2196F3")

    st.markdown("---")
    col1, col2 = st.columns(2)

    # Risk level distribution
    with col1:
        st.subheader("Risk Level Distribution")
        fig = px.pie(
            anomaly, names="risk_level",
            color="risk_level",
            color_discrete_map={
                "High Risk":   "#f44336",
                "Medium Risk": "#FF9800",
                "Low Risk":    "#4CAF50"
            },
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    # Anomaly flag by location
    with col2:
        st.subheader("Anomalies by Data Center Location")
        df_loc = anomaly[anomaly["is_anomaly"] == "Anomaly"] \
            .groupby("data_center_location")["is_anomaly"] \
            .count().reset_index()
        df_loc.columns = ["data_center_location", "anomaly_count"]
        fig = px.bar(
            df_loc, x="data_center_location",
            y="anomaly_count",
            color="data_center_location"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Anomaly score scatter
    st.subheader("Anomaly Score vs CPU Utilization")
    fig = px.scatter(
        anomaly,
        x="cpu_pct", y="anomaly_score",
        color="risk_level",
        color_discrete_map={
            "High Risk":   "#f44336",
            "Medium Risk": "#FF9800",
            "Low Risk":    "#4CAF50"
        },
        hover_data=["server_id", "data_center_location", "server_type"],
        size="power_watts"
    )
    fig.add_hline(y=0, line_dash="dash",
                  line_color="white", annotation_text="Risk threshold")
    st.plotly_chart(fig, use_container_width=True)

    # High and medium risk servers table
    st.subheader("⚠️ High & Medium Risk Servers — Action Required")
    df_alerts = anomaly[anomaly["risk_level"].isin(["High Risk", "Medium Risk"])] \
        [[
            "server_id", "data_center_location", "server_type",
            "cpu_pct", "ram_pct", "storage_pct",
            "power_watts", "anomaly_score", "risk_level"
        ]].sort_values("anomaly_score")
    st.dataframe(
        df_alerts.reset_index(drop=True),
        use_container_width=True
    )

    st.markdown("---")
    st.info(
        "**Model Info:** Isolation Forest trained on 151 server readings across 5 features. "
        "Contamination rate set at 10% based on historical incident frequency. "
        "Scores below 0 indicate anomalous behavior requiring investigation."
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#666;font-size:12px'>"
    "DataCenter360 Intelligence Platform | "
    "Built with Microsoft Fabric + Streamlit | "
    "Ashburn, VA"
    "</div>",
    unsafe_allow_html=True
)