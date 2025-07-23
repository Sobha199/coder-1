
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="S2M Portal", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #e6f2ff;
    }
    .stTextInput>div>div>input {
        border: 1px solid black;
    }
    </style>
""", unsafe_allow_html=True)

# Load user data from CSV
csv_path = "Tracking Sample.csv"
user_data = pd.read_csv(csv_path)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.image("s2m-logo.png", width=200)
    st.title("S2M Health Private Ltd - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with st.spinner("Authenticating..."):
            st.write("Columns in CSV:", user_data.columns.tolist())
            user_match = user_data[(user_data["Login name"] == username) & (user_data["Password"] == Password)]
            if not user_match.empty:
                st.session_state.logged_in = True
                st.session_state.emp_id = user_match.iloc[0]["Emp Id"]
                st.session_state.emp_name = user_match.iloc[0]["Emp Name"]
                st.session_state.team_lead = user_match.iloc[0]["Team lead name"]
                st.session_state.login_id = user_match.iloc[0]["Login Id"]
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")

def form_page():
    st.title("Form Submission")
    today = datetime.date.today()
    emp_id = st.session_state.emp_id
    emp_name = st.session_state.emp_name
    team_lead = st.session_state.team_lead
    login_id = st.session_state.login_id

    with st.form("entry_form"):
        date = st.date_input("Date", value=today)
        st.text_input("Emp ID", value=emp_id, disabled=True)
        st.text_input("Emp Name", value=emp_name, disabled=True)
        project = st.selectbox("Project", ["Elevance MA", "Elevance ACA", "Health OS"])
        category = st.selectbox("Project Category", ["Entry", "Recheck", "QA"])
        login_name = st.multiselect("Login Name", user_data["Login name"].unique())
        st.text_input("Login ID", value=login_id, disabled=True)
        st.text_input("Team Lead", value=team_lead, disabled=True)
        chart_id = st.text_input("Chart ID")
        page_no = st.text_input("Page No")
        no_dos = st.number_input("No of DOS", min_value=0)
        no_codes = st.number_input("No of Codes", min_value=0)
        error_type = st.text_input("Error Type")
        error_comments = st.text_input("Error Comments")
        no_errors = st.number_input("No of Errors", min_value=0)
        chart_status = st.text_input("Chart Status")
        auditor_emp_id = st.text_input("Auditor Emp ID")
        auditor_emp_name = st.text_input("Auditor Emp Name")
        submitted = st.form_submit_button("Submit")

        if submitted:
            form_data = {
                "Date": date,
                "Emp Id": emp_id,
                "Emp Name": emp_name,
                "Project": project,
                "Project Category": category,
                "Login Id": login_id,
                "Login Name": login_name,
                "Team lead name": team_lead,
                "Chart id": chart_id,
                "Page no": page_no,
                "No of Dos": no_dos,
                "No of codes": no_codes,
                "Error type": error_type,
                "Error comments": error_comments,
                "No of errors": no_errors,
                "Chart status": chart_status,
                "Auditor emp id": auditor_emp_id,
                "Auditor Emp name": auditor_emp_name
            }
            df = pd.DataFrame([form_data])
            if os.path.exists("form_data.csv"):
                df.to_csv("form_data.csv", mode='a', index=False, header=False)
            else:
                df.to_csv("form_data.csv", index=False)
            st.success("Form submitted successfully!")

    if os.path.exists("form_data.csv"):
        st.subheader("Submitted Data")
        st.dataframe(pd.read_csv("form_data.csv"))

def dashboard_page():
    st.title("Dashboard")
    if os.path.exists("form_data.csv"):
        df = pd.read_csv("form_data.csv")
        st.metric("Working Days", df["Date"].nunique())
        st.metric("No of Charts", df["Chart id"].nunique())
        st.metric("No of DOS", df["No of Dos"].sum())
        st.metric("No of ICD", df["No of codes"].sum())
        if len(df) > 0:
            cph = df["No of codes"].sum() / len(df)
            st.metric("CPH", round(cph, 2))
    else:
        st.info("No data submitted yet.")

if not st.session_state.logged_in:
    login_page()
else:
    page = st.sidebar.radio("Navigation", ["Form Entry", "Dashboard"])
    if page == "Form Entry":
        form_page()
    elif page == "Dashboard":
        dashboard_page()
