import streamlit as st
import pandas as pd
from datetime import date, timedelta


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Study Planner Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ============================================================
# CUSTOM CSS - SOFT PASTEL THEME
# ============================================================

st.markdown("""
<style>

/* =========================
   MAIN APP BACKGROUND
   ========================= */

.stApp {
    background: linear-gradient(
        135deg,
        #FDF6F0 0%,
        #F4F1FF 35%,
        #EAF7F5 70%,
        #FFF4E6 100%
    );
    background-attachment: fixed;
}


/* =========================
   MAIN CONTENT AREA
   ========================= */

.main {
    background: transparent !important;
}


/* =========================
   SIDEBAR - SOFT PASTEL
   ========================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #E8F1FF 0%,
        #EDE7F6 50%,
        #E8F8F5 100%
    ) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #26354A !important;
}


/* =========================
   MAIN TITLE
   ========================= */

.main-title {
    background: linear-gradient(
        135deg,
        #DDEBFF,
        #EDE4FF,
        #DDF5EF
    );
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid #D8E2F0;
    box-shadow: 0 5px 20px rgba(100, 120, 150, 0.08);
}

.main-title h1 {
    color: #26354A;
    margin: 0;
    font-size: 2.3rem;
}

.main-title p {
    color: #64748B;
    margin-top: 8px;
    font-size: 1rem;
}


/* =========================
   FEATURE TITLE
   ========================= */

.feature-title {
    background-color: #FFF9F2;
    color: #334155;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 10px;
    border-radius: 10px;
}


/* =========================
   FEATURE DESCRIPTION
   ========================= */

.feature-description {
    background-color: #F5F2FF;
    color: #64748B;
    font-size: 0.85rem;
    padding: 10px;
    border-radius: 10px;
}


/* =========================
   QUOTE
   ========================= */

.quote-text {
    background: linear-gradient(
        135deg,
        #FFF1F5,
        #F1EDFF
    );
    color: #475569;
    font-size: 1.3rem;
    font-weight: 700;
    font-style: italic;
    text-align: center;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #E8DFF0;
}


/* =========================
   SECTION TITLE
   ========================= */

.section-title {
    color: #334155;
    font-size: 1.5rem;
    font-weight: 700;
}


/* =========================
   FOOTER
   ========================= */

.footer-text {
    text-align: center;
    padding: 15px;
    background: linear-gradient(
        135deg,
        #E8F7EF,
        #E7F3FF
    );
    border-radius: 12px;
    color: #3F6B58;
    font-weight: 600;
    border: 1px solid #D6EADF;
}


/* =========================
   STREAMLIT INPUT BOXES
   ========================= */

.stTextInput > div > div,
.stTextArea > div > div,
.stNumberInput > div > div,
.stDateInput > div > div,
.stSelectbox > div > div {
    background-color: #FFFCF8 !important;
    border-radius: 10px !important;
}


/* =========================
   BUTTON
   ========================= */

.stButton > button {
    background: linear-gradient(
        135deg,
        #BFD7FF,
        #DCCBFF
    );
    color: #26354A;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #AEC9F5,
        #CDB9F5
    );
    transform: translateY(-2px);
}


/* =========================
   METRIC CARDS
   ========================= */

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #FFF8F1,
        #F1F5FF
    );
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #E4E8F0;
    box-shadow: 0 4px 15px rgba(100, 120, 150, 0.06);
}


/* =========================
   DATAFRAME
   ========================= */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* =========================
   GENERAL TEXT
   ========================= */

body {
    color: #334155;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "study_plan" not in st.session_state:
    st.session_state.study_plan = pd.DataFrame()

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False


# ============================================================
# PLAN GENERATION FUNCTION
# ============================================================

def generate_plan(
    start_date,
    end_date,
    subjects,
    hours_per_day,
    study_days,
    priority_topics,
    weak_subject,
    priority_strategy,
    add_revision,
    add_mock_tests
):
    plan = []

    current_date = start_date
    subject_index = 0

    while current_date <= end_date:

        day_name = current_date.strftime("%a")

        if day_name in study_days:

            remaining_hours = float(hours_per_day)

            # ------------------------------------------------
            # PRIORITY SUBJECT
            # ------------------------------------------------

            selected_subject = subjects[
                subject_index % len(subjects)
            ]

            selected_lower = selected_subject.lower()

            is_priority = False

            for topic in priority_topics:
                topic_lower = topic.lower()

                if (
                    topic_lower in selected_lower
                    or selected_lower in topic_lower
                ):
                    is_priority = True
                    break

            is_weak = (
                selected_lower == weak_subject.lower()
            )

            # ------------------------------------------------
            # FIRST STUDY SESSION
            # ------------------------------------------------

            if priority_strategy == "Priority First":

                if is_priority:

                    session_hours = min(
                        2.0,
                        remaining_hours
                    )

                    task = "🔥 Priority Topic Study"

                elif is_weak:

                    session_hours = min(
                        1.5,
                        remaining_hours
                    )

                    task = "🧠 Weak Subject Practice"

                else:

                    session_hours = min(
                        1.0,
                        remaining_hours
                    )

                    task = "📚 Concept Learning"

            else:

                session_hours = min(
                    1.0,
                    remaining_hours
                )

                if is_weak:
                    task = "🧠 Weak Subject Practice"
                elif is_priority:
                    task = "⭐ Important Topic Study"
                else:
                    task = "📚 Concept Learning"

            if session_hours > 0:

                plan.append({
                    "Date": current_date,
                    "Day": day_name,
                    "Subject": selected_subject,
                    "Task": task,
                    "Hours": round(session_hours, 1)
                })

                remaining_hours -= session_hours

            # ------------------------------------------------
            # SECOND SUBJECT
            # ------------------------------------------------

            if remaining_hours >= 1 and len(subjects) > 1:

                second_index = (
                    subject_index + 1
                ) % len(subjects)

                second_subject = subjects[second_index]

                plan.append({
                    "Date": current_date,
                    "Day": day_name,
                    "Subject": second_subject,
                    "Task": "📖 Practice & Examples",
                    "Hours": 1.0
                })

                remaining_hours -= 1.0

            # ------------------------------------------------
            # REVISION
            # ------------------------------------------------

            if add_revision and remaining_hours >= 0.5:

                plan.append({
                    "Date": current_date,
                    "Day": day_name,
                    "Subject": "Revision",
                    "Task": "🔄 Review Previous Topics",
                    "Hours": 0.5
                })

                remaining_hours -= 0.5

            # ------------------------------------------------
            # MOCK TEST
            # ------------------------------------------------

            if (
                add_mock_tests
                and day_name in ["Sat", "Sun"]
                and remaining_hours >= 1
            ):

                plan.append({
                    "Date": current_date,
                    "Day": day_name,
                    "Subject": "Mock Test",
                    "Task": "📝 Practice Test & Evaluation",
                    "Hours": 1.0
                })

            subject_index += 1

        current_date += timedelta(days=1)

    return pd.DataFrame(plan)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎓 AI Study Planner Pro")
    st.caption("Plan • Learn • Achieve")

    st.divider()

    # --------------------------------------------------------
    # STUDY CONSTRAINTS
    # --------------------------------------------------------

    st.markdown("### ⚡ Study Constraints")

    start_date = st.date_input(
        "Start Date",
        value=date.today()
    )

    end_date = st.date_input(
        "End Date",
        value=date.today() + timedelta(days=7)
    )

    hours_per_day = st.number_input(
        "Available Study Hours Per Day",
        min_value=1.0,
        max_value=24.0,
        value=4.0,
        step=0.5
    )

    # --------------------------------------------------------
    # SUBJECTS
    # --------------------------------------------------------

    st.markdown("### 📚 Subjects")

    subjects_text = st.text_area(
        "Enter Subjects",
        value="Python, Database, AI, Physics",
        height=100,
        help="Enter subjects separated by commas."
    )

    subjects = [
        subject.strip()
        for subject in subjects_text.split(",")
        if subject.strip()
    ]

    # --------------------------------------------------------
    # PRIORITY TOPICS
    # --------------------------------------------------------

    st.markdown("### 🔥 Priority Subjects / Topics")

    priority_text = st.text_input(
        "Enter Priority Topics",
        value="AI, Python"
    )

    priority_topics = [
        item.strip()
        for item in priority_text.split(",")
        if item.strip()
    ]

    # --------------------------------------------------------
    # WEAK SUBJECT
    # --------------------------------------------------------

    st.markdown("### 🧠 Difficult / Weak Subject")

    if subjects:

        weak_subject = st.selectbox(
            "Select Weak Subject",
            subjects
        )

    else:

        weak_subject = ""

    # --------------------------------------------------------
    # PRIORITY STRATEGY
    # --------------------------------------------------------

    st.markdown("### ⚙️ Priority Strategy")

    priority_strategy = st.radio(
        "Choose Strategy",
        ["Priority First", "Balanced"]
    )

    # --------------------------------------------------------
    # STUDY DAYS
    # --------------------------------------------------------

    st.markdown("### 📅 Study Days")

    study_days = st.multiselect(
        "Select Study Days",
        [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ],
        default=[
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri"
        ]
    )

    # --------------------------------------------------------
    # ADVANCED OPTIONS
    # --------------------------------------------------------

    st.markdown("### 🚀 Advanced Features")

    add_revision = st.checkbox(
        "🔄 Add Revision Sessions",
        value=True
    )

    add_mock_tests = st.checkbox(
        "📝 Add Mock Tests",
        value=True
    )

    st.write("")

    # --------------------------------------------------------
    # GENERATE BUTTON
    # --------------------------------------------------------

    generate_button = st.button(
        "🚀 Generate Study Plan",
        type="primary",
        use_container_width=True
    )


# ============================================================
# GENERATE PLAN
# ============================================================

if generate_button:

    if not subjects:

        st.error(
            "❌ Please enter at least one subject."
        )

    elif start_date > end_date:

        st.error(
            "❌ End Date must be after Start Date."
        )

    elif not study_days:

        st.error(
            "❌ Please select at least one study day."
        )

    else:

        generated_plan = generate_plan(
            start_date=start_date,
            end_date=end_date,
            subjects=subjects,
            hours_per_day=hours_per_day,
            study_days=study_days,
            priority_topics=priority_topics,
            weak_subject=weak_subject,
            priority_strategy=priority_strategy,
            add_revision=add_revision,
            add_mock_tests=add_mock_tests
        )

        st.session_state.study_plan = generated_plan
        st.session_state.plan_generated = True

        st.success(
            "🎉 Your personalized study plan has been generated!"
        )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
<div class="main-title">
    <h1>🎓 AI Study Planner Pro</h1>
    <p>
        Smart Study Planning • Priority Management •
        Task Decomposition • Analytics • Progress Tracking
    </p>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# FEATURE CARDS
# ============================================================

st.markdown("### ✨ Smart Planning Features")

feature_columns = st.columns(5)

features = [
    (
        "🧩",
        "Task Decomposition",
        "Break subjects into smaller study tasks."
    ),
    (
        "⭐",
        "Priority Handling",
        "Give more attention to important topics."
    ),
    (
        "🧠",
        "Difficulty Analysis",
        "Focus on weak and difficult subjects."
    ),
    (
        "📅",
        "Schedule Generation",
        "Create a personalized study schedule."
    ),
    (
        "🔄",
        "Iterative Refinement",
        "Generate a new plan whenever required."
    )
]

for column, feature in zip(
    feature_columns,
    features
):

    icon, title, description = feature

    with column:

        with st.container(border=True):

            st.markdown(
                f"### {icon}"
            )

            st.markdown(
                f"**{title}**"
            )

            st.caption(
                description
            )


# ============================================================
# WELCOME SECTION
# ============================================================

st.write("")

welcome_col, quote_col = st.columns([2, 1])

with welcome_col:

    with st.container(border=True):

        st.markdown(
            "## 🎯 Welcome to AI Study Planner Pro!"
        )

        st.write(
            "Your personalized study plan is just a few "
            "steps away."
        )

        st.write(
            "Enter your subjects, available study hours, "
            "priority topics, difficult subject and study "
            "days using the sidebar."
        )

        st.info(
            "🔍 Smart Planning  •  📚 Better Learning  •  "
            "🎯 Better Results"
        )


with quote_col:

    with st.container(border=True):

        st.markdown(
            '<p class="quote-text">'
            '"Small steps every day lead to big results."'
            '</p>',
            unsafe_allow_html=True
        )

        st.success(
            "Keep going! 💪📚"
        )


# ============================================================
# STUDY DASHBOARD
# ============================================================

if st.session_state.plan_generated:

    plan = st.session_state.study_plan.copy()

    st.write("")

    st.markdown("## 📊 Study Dashboard")

    # --------------------------------------------------------
    # CALCULATE METRICS
    # --------------------------------------------------------

    total_subjects = len(subjects)

    total_tasks = len(plan)

    total_hours = float(
        plan["Hours"].sum()
    )

    total_study_days = (
        plan["Date"].nunique()
    )

    available_hours = (
        total_study_days * hours_per_day
    )

    if available_hours > 0:

        completion_ratio = min(
            total_hours / available_hours,
            1.0
        )

    else:

        completion_ratio = 0.0

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "📚 Subjects",
            total_subjects
        )

    with m2:

        st.metric(
            "📝 Tasks",
            total_tasks
        )

    with m3:

        st.metric(
            "⏱️ Planned Hours",
            f"{total_hours:.1f}"
        )

    with m4:

        st.metric(
            "📅 Study Days",
            total_study_days
        )

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.write("")

    st.markdown("### 📈 Study Plan Utilization")

    st.progress(
        completion_ratio
    )

    st.caption(
        f"{total_hours:.1f} planned hours out of "
        f"{available_hours:.1f} available hours"
    )

    # --------------------------------------------------------
    # PLAN TABLE
    # --------------------------------------------------------

    st.markdown(
        "### 📋 Your Personalized Study Plan"
    )

    display_plan = plan.copy()

    display_plan["Date"] = display_plan[
        "Date"
    ].apply(
        lambda x: x.strftime("%d-%m-%Y")
    )

    st.dataframe(
        display_plan,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # SUBJECT ANALYTICS
    # --------------------------------------------------------

    st.markdown("### 📊 Subject-wise Study Analysis")

    subject_hours = (
        plan[
            ~plan["Subject"].isin(
                ["Revision", "Mock Test"]
            )
        ]
        .groupby("Subject")["Hours"]
        .sum()
        .reset_index()
    )

    subject_hours = subject_hours.sort_values(
        by="Hours",
        ascending=False
    )

    chart_col, info_col = st.columns([2, 1])

    with chart_col:

        st.bar_chart(
            subject_hours.set_index("Subject")
        )

    with info_col:

        st.markdown("#### 📌 Study Distribution")

        for _, row in subject_hours.iterrows():

            st.write(
                f"**{row['Subject']}** — "
                f"{row['Hours']:.1f} hours"
            )

    # --------------------------------------------------------
    # PLAN SUMMARY
    # --------------------------------------------------------

    st.markdown("### 📝 Plan Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    revision_hours = plan[
        plan["Subject"] == "Revision"
    ]["Hours"].sum()

    mock_hours = plan[
        plan["Subject"] == "Mock Test"
    ]["Hours"].sum()

    with summary_col1:

        st.info(
            f"🔄 Revision Time\n\n"
            f"**{revision_hours:.1f} hours**"
        )

    with summary_col2:

        st.warning(
            f"📝 Mock Test Time\n\n"
            f"**{mock_hours:.1f} hours**"
        )

    with summary_col3:

        st.success(
            f"🎯 Daily Target\n\n"
            f"**{hours_per_day:.1f} hours/day**"
        )

    # --------------------------------------------------------
    # DOWNLOAD PLAN
    # --------------------------------------------------------

    st.markdown("### 💾 Download Your Plan")

    download_plan = plan.copy()

    download_plan["Date"] = download_plan[
        "Date"
    ].apply(
        lambda x: x.strftime("%d-%m-%Y")
    )

    csv_data = download_plan.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download Study Plan as CSV",
        data=csv_data,
        file_name="AI_Study_Planner.csv",
        mime="text/csv",
        use_container_width=True
    )

    # --------------------------------------------------------
    # REGENERATE
    # --------------------------------------------------------

    generate_button = st.button(
    "🚀 Generate Study Plan",
    type="primary",
    use_container_width=True
)

if generate_button:
    st.success("✅ Study Plan Generated Successfully!")
# ============================================================
# HOW IT WORKS
# ============================================================

st.write("")

st.markdown("## 🗺️ How It Works")

workflow_columns = st.columns(6)

workflow = [
    ("📥", "Input", "Enter your study requirements."),
    ("🧩", "Break Down", "Divide subjects into tasks."),
    ("⭐", "Prioritize", "Focus on important topics."),
    ("📅", "Schedule", "Create your study timetable."),
    ("📋", "Evaluate", "Check the generated plan."),
    ("🔄", "Regenerate", "Create another plan if needed.")
]

for column, item in zip(
    workflow_columns,
    workflow
):

    icon, title, description = item

    with column:

        with st.container(border=True):

            st.markdown(
                f"### {icon}"
            )

            st.markdown(
                f"**{title}**"
            )

            st.caption(
                description
            )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.markdown(
    """
<div class="footer-text">
    🎯 Stay Focused • Be Consistent • Achieve Your Goals ✨
</div>
""",
    unsafe_allow_html=True
)