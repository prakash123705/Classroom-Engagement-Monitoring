# =========================================
# dashboard.py
# =========================================

import os
import subprocess
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from streamlit_autorefresh import st_autorefresh

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Classroom Monitoring",
    layout="wide",
    page_icon="🎓"
)

# =========================================
# AUTO REFRESH
# =========================================
st_autorefresh(
    interval=2000,
    key="refresh"
)

# =========================================
# SESSION STATE
# =========================================
if "process" not in st.session_state:
    st.session_state.process = None

# =========================================
# CHECK PROCESS STATUS
# =========================================
if st.session_state.process is not None:

    # PROCESS CLOSED AUTOMATICALLY
    if st.session_state.process.poll() is not None:

        st.session_state.process = None

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

.stApp {

    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );

    color: white;
}

/* TITLE */
.title {

    text-align: center;

    font-size: 50px;

    font-weight: bold;

    color: #38bdf8;

    margin-bottom: 35px;

    text-shadow: 0px 0px 20px #38bdf8;
}

/* METRIC CARD */
.metric-card {

    background: linear-gradient(
        145deg,
        #111827,
        #1e293b
    );

    border-radius: 20px;

    padding: 25px;

    border: 1px solid #38bdf8;

    box-shadow:
        0px 0px 15px rgba(56,189,248,0.3);

    text-align: center;
}

/* CARD TITLE */
.metric-card h3 {

    color: #cbd5e1;

    font-size: 22px;

    margin-bottom: 10px;
}

/* CARD VALUE */
.metric-card h1 {

    color: #38bdf8;

    font-size: 42px;

    font-weight: bold;
}

/* SECTION TITLE */
.section-title {

    color: #38bdf8;

    font-size: 28px;

    margin-top: 25px;

    margin-bottom: 15px;

    font-weight: bold;
}

/* BUTTON */
div.stButton > button:first-child {

    background: linear-gradient(
        to right,
        #06b6d4,
        #2563eb
    );

    color: white;

    border-radius: 14px;

    height: 55px;

    width: 100%;

    font-size: 20px;

    font-weight: bold;

    border: none;

    transition: 0.3s;

    box-shadow:
        0px 0px 15px rgba(56,189,248,0.5);
}

div.stButton > button:first-child:hover {

    transform: scale(1.02);

    background: linear-gradient(
        to right,
        #0891b2,
        #1d4ed8
    );
}

/* DOWNLOAD BUTTON */
div.stDownloadButton > button {

    background: linear-gradient(
        to right,
        #16a34a,
        #22c55e
    );

    color: white;

    border-radius: 14px;

    height: 55px;

    width: 100%;

    font-size: 20px;

    font-weight: bold;

    border: none;

    transition: 0.3s;

    box-shadow:
        0px 0px 15px rgba(34,197,94,0.5);
}

div.stDownloadButton > button:hover {

    transform: scale(1.02);

    background: linear-gradient(
        to right,
        #15803d,
        #16a34a
    );
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================
st.markdown(
    """
    <div class="title">
        🎓 Classroom Engagement Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# BUTTONS
# =========================================
col1, col2 = st.columns(2)

# =========================================
# START BUTTON
# =========================================
with col1:

    if st.button("▶ START MONITORING"):

        if st.session_state.process is None:

            # REMOVE OLD CURRENT SESSION
            if os.path.exists(
                "current_session.txt"
            ):

                os.remove(
                    "current_session.txt"
                )

            # START APP PROCESS
            st.session_state.process = (
                subprocess.Popen(
                    [
                        r"D:\Project\venv\Scripts\python.exe",
                        r"D:\Project\app.py"
                    ]
                )
            )

            st.success(
                "Real-Time Monitoring Started"
            )

# =========================================
# STOP BUTTON
# =========================================
with col2:

    if st.button("⏹ STOP MONITORING"):

        if st.session_state.process is not None:

            try:

                # FORCE STOP PROCESS
                st.session_state.process.kill()

            except:

                pass

            st.session_state.process = None

            # FORCE REMOVE PYTHON PROCESSES
            os.system(
                "taskkill /F /IM python.exe >nul 2>&1"
            )

            st.success(
                "Monitoring Stopped"
            )

# =========================================
# LOAD CSV
# =========================================
try:

    csv_file_path = None

    # =========================================
    # CURRENT SESSION
    # =========================================
    if os.path.exists(
        "current_session.txt"
    ):

        with open(
            "current_session.txt",
            "r"
        ) as f:

            csv_file_path = (
                f.read().strip()
            )

    # =========================================
    # LOAD LAST SESSION
    # =========================================
    if (
        csv_file_path is None
        or
        not os.path.exists(
            csv_file_path
        )
    ):

        session_folder = "sessions"

        if os.path.exists(
            session_folder
        ):

            csv_files = [

                os.path.join(
                    session_folder,
                    file
                )

                for file in os.listdir(
                    session_folder
                )

                if file.endswith(".csv")
            ]

            if len(csv_files) > 0:

                csv_file_path = max(
                    csv_files,
                    key=os.path.getctime
                )

    # =========================================
    # READ CSV
    # =========================================
    if csv_file_path is not None:

        df = pd.read_csv(
            csv_file_path
        )

    else:

        raise FileNotFoundError

    # =========================================
    # METRICS
    # =========================================
    total_students = df[
        "Student_ID"
    ].nunique()

    engaged = len(
        df[
            df["Status"] == "Engaged"
        ]
    )

    disengaged = len(
        df[
            df["Status"] == "Disengaged"
        ]
    )

    total_records = len(df)

    # =========================================
    # ENGAGEMENT %
    # =========================================
    if total_records > 0:

        engagement_percentage = (
            engaged /
            total_records
        ) * 100
        # =========================================
        # CLASSROOM STATUS
        # =========================================
        if engagement_percentage >= 50:

            classroom_status = "🟢 Engaged"

        else:

            classroom_status = "🔴 Disengaged"
    else:

        engagement_percentage = 0
        classroom_status = "⚪ No Data"
    # =========================================
    # METRIC CARDS
    # =========================================
    c1, c2, c3, c4 = st.columns(4)

    card1 = f"""
    <div class="metric-card">
    <h3>👨‍🎓 Students</h3>
    <h1>{total_students}</h1>
    </div>
    """

    card2 = f"""
    <div class="metric-card">
    <h3>✅ Engaged</h3>
    <h1>{engaged}</h1>
    </div>
    """

    card3 = f"""
    <div class="metric-card">
    <h3>❌ Disengaged</h3>
    <h1>{disengaged}</h1>
    </div>
    """

    card4 = f"""
    <div class="metric-card">
    <h3>📈 Engagement</h3>
    <h1>{engagement_percentage:.1f}%</h1>
    </div>
    """

    with c1:
        st.markdown(
            card1,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            card2,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            card3,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            card4,
            unsafe_allow_html=True
        )

    st.write("")
    
    st.markdown(
        f"""
        <h2 style='text-align:center;color:white;'>
            {classroom_status}
        </h2>
        """,
        unsafe_allow_html=True
    )
    # =========================================
    # CHARTS
    # =========================================
    left_col, right_col = st.columns(2)

    # =========================================
    # GAUGE CHART
    # =========================================
    with left_col:

        st.markdown(
            """
            <div class="section-title">
                📊 Engagement Ratio
            </div>
            """,            unsafe_allow_html=True
        )

        gauge = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=engagement_percentage,

                number={
                    'font': {
                        'size': 48,
                        'color': "#38bdf8"
                    },

                    'suffix': "%"
                },

                gauge={

                    'axis': {

                        'range': [0,100],

                        'tickcolor': "white",

                        'tickwidth': 2,

                        'tickfont': {
                            'color': "white",
                            'size': 14
                        }
                    },

                    'bar': {
                        'color': "#06b6d4",
                        'thickness': 0.35
                    },

                    'bgcolor': "#0f172a",

                    'borderwidth': 3,

                    'bordercolor': "#38bdf8",

                    'steps': [

                        {
                            'range': [0,40],
                            'color': "#ef4444"
                        },

                        {
                            'range': [40,70],
                            'color': "#facc15"
                        },

                        {
                            'range': [70,100],
                            'color': "#22c55e"
                        }
                    ]
                }
            )
        )

        gauge.update_layout(

            paper_bgcolor="#111827",

            font={
                'color': "white"
            },

            height=420
        )

        st.plotly_chart(
            gauge,
            width='stretch'
        )

    # =========================================
    # PIE CHART
    # =========================================
    with right_col:

        st.markdown(
            """
            <div class="section-title">
                📌 Status Distribution
            </div>
            """,
            unsafe_allow_html=True
        )

        status_counts = df[
            "Status"
        ].value_counts()

        pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            hole=0.5
        )

        pie.update_layout(

            paper_bgcolor="#111827",

            plot_bgcolor="#111827",

            font={
                'color': 'white',
                'size': 16
            },

            legend=dict(

                font=dict(
                    color="white",
                    size=14
                )
            ),

            height=420
        )

        st.plotly_chart(
            pie,
            width='stretch'
        )

    # =========================================
    # TABLE
    # =========================================
    st.markdown(
        """
        <div class="section-title">
            🧑‍💻 Student Records
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        df.tail(100),
        width='stretch',
        height=320
    )

    # =========================================
    # DOWNLOAD CSV
    # =========================================
    csv_file = df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download CSV Report",
        data=csv_file,
        file_name="engagement_report.csv",
        mime="text/csv"
    )

except:

    st.warning(
        "No engagement data found yet"
    )