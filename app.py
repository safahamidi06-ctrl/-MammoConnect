import io
from datetime import date, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(page_title="MammoConnect | Outreach Dashboard", page_icon="🎗️", layout="wide")

STATUSES = ["Booked", "Declined", "Already screened", "Considering", "Needs review"]
POPULATIONS = ["Woman", "Two-Spirit", "Trans / nonbinary", "Transfeminine", "Prefer not to answer / unsure"]


def assess(age, population, symptoms, history, mastectomy, recent, hormones):
    """Informational OBSP prompts only. Not a clinical eligibility determination."""
    if any(x == "Unsure" for x in (symptoms, history, mastectomy, recent)):
        return "Needs clinical review", "Some screening answers are uncertain."
    if symptoms == "Yes":
        return "Needs clinical review", "Symptoms require clinical assessment, not routine screening clearance."
    if history == "Yes" or mastectomy == "Yes":
        return "Needs clinical review", "History or surgery may require a different clinical pathway."
    if population == "Prefer not to answer / unsure":
        return "Needs clinical review", "The screening pathway needs confirmation."
    if population == "Transfeminine" and hormones != "Yes":
        return "Needs clinical review", "The applicable hormone criterion needs confirmation."
    if age < 40:
        return "Outside routine age range", "A high-risk or diagnostic pathway may apply; ask clinical staff."
    if age > 74:
        return "Needs clinical review", "Screening after age 74 may be available with a provider referral."
    if recent == "Yes":
        return "Not due under basic interval check", "A screening mammogram was reported within the last 11 months."
    if age < 50:
        return "Preliminary criteria met — informed choice", "Ages 40–49: discuss screening benefits, harms, and preferences."
    return "Preliminary criteria met", "Confirm with the OBSP location and authorized clinical workflow."


def make_demo():
    # Entirely fictional records; not clinic observations.
    specs = [
        ("2026-10-03", 52, "Booked", 4), ("2026-10-03", 61, "Declined", None),
        ("2026-10-03", 44, "Considering", None), ("2026-10-04", 47, "Booked", 6),
        ("2026-10-04", 58, "Booked", 9), ("2026-10-04", 69, "Already screened", None),
        ("2026-10-10", 54, "Booked", 5), ("2026-10-10", 63, "Declined", None),
        ("2026-10-10", 41, "Needs review", None), ("2026-10-11", 62, "Booked", 5),
        ("2026-10-11", 49, "Considering", None), ("2026-10-11", 71, "Already screened", None),
        ("2026-10-12", 56, "Declined", None), ("2026-10-12", 50, "Booked", 8),
    ]
    rows = []
    for i, (day, age, status, offset) in enumerate(specs, 1):
        eligibility, _ = assess(age, "Woman", "No", "No", "No", "No", "Not applicable")
        rows.append({"ID": f"DEMO-{i:03d}", "Date approached": day, "Age": age,
                     "Population": "Woman", "Symptoms": "No", "Cancer history": "No",
                     "Mastectomy": "No", "Mammogram in past 11 months": "No",
                     "Hormone criterion": "Not applicable", "Eligibility prompt": eligibility,
                     "Outreach status": status,
                     "Appointment date": (date.fromisoformat(day) + timedelta(days=offset)).isoformat() if offset else "",
                     "Screening follow-up": "Not verified"})
    return rows


def table():
    return pd.DataFrame(st.session_state.encounters)


if "encounters" not in st.session_state:
    st.session_state.encounters = make_demo()
if "next_id" not in st.session_state:
    st.session_state.next_id = 100

st.markdown("""<style>
.block-container {padding-top: 2rem; max-width: 1250px}
[data-testid="stMetric"] {background: #17202a; border: 1px solid #344454; border-radius: 14px; padding: 14px}
[data-testid="stMetricLabel"] {font-size: 0.95rem}
</style>""", unsafe_allow_html=True)

st.title("🎗️ MammoConnect")
st.caption("Breast screening outreach • Appointment tracking • Impact reporting")
st.write("Helping more people understand and access mammography screening through proactive outreach and practical booking assistance.")
st.warning("**PUBLIC DEMO — FICTIONAL DATA ONLY.** Do not enter names, contact details, health card numbers, or any real patient or clinic information. Data entered here is temporary and is not a clinical record.")

with st.sidebar:
    st.header("MammoConnect")
    st.caption("Demonstration workspace")
    st.info("The sample data is fictional. Your entries are held only in your current Streamlit session and can disappear when the session ends.")
    if st.button("Reset fictional demo data", use_container_width=True):
        st.session_state.encounters = make_demo()
        st.session_state.next_id = 100
        st.rerun()
    st.markdown("[Ontario Health screening guidance](https://www.cancercareontario.ca/en/guidelines-advice/cancer-continuum/screening/breast-screening-recommendations-summary)")

tab_dashboard, tab_new, tab_records, tab_about = st.tabs(["📊 Dashboard", "➕ New encounter", "📋 Records & follow-up", "ℹ️ About"])

with tab_dashboard:
    df = table()
    if not df.empty:
        df["Date approached"] = pd.to_datetime(df["Date approached"])
        df["Month"] = df["Date approached"].dt.strftime("%Y-%m")
        months = sorted(df["Month"].unique().tolist())
        period = st.selectbox("Reporting period", ["All dates"] + months)
        view = df if period == "All dates" else df[df["Month"] == period]
        approached = len(view)
        booked = int((view["Outreach status"] == "Booked").sum())
        screened = int((view["Outreach status"] == "Already screened").sum())
        declined = int((view["Outreach status"] == "Declined").sum())
        pending = int(view["Outreach status"].isin(["Considering", "Needs review"]).sum())
        denom = approached - screened
        rate = booked / denom * 100 if denom else 0
        a, b, c, d, e = st.columns(5)
        a.metric("Approached", approached)
        b.metric("Booked", booked)
        c.metric("Booking conversion", f"{rate:.1f}%")
        d.metric("Already screened", screened)
        e.metric("Pending / review", pending)
        st.caption("Booking conversion = Booked ÷ (Approached − Already screened). This is an outreach metric, not verified screening completion.")
        st.subheader("Daily outreach activity")
        summary = (view.groupby(view["Date approached"].dt.strftime("%Y-%m-%d"))["Outreach status"]
                   .value_counts().unstack(fill_value=0))
        for status in STATUSES:
            if status not in summary.columns:
                summary[status] = 0
        summary["Approached"] = summary[STATUSES].sum(axis=1)
        summary["Booking rate (%)"] = (100 * summary["Booked"] /
                                      (summary["Approached"] - summary["Already screened"]).replace(0, float("nan"))).fillna(0).round(1)
        st.bar_chart(summary[["Approached", "Booked"]], color=["#8ac5e8", "#d987aa"])
        st.dataframe(summary[["Approached", "Booked", "Declined", "Already screened", "Considering", "Needs review", "Booking rate (%)"]].reset_index().rename(columns={"Date approached": "Date"}), hide_index=True, use_container_width=True)
        st.subheader("Outreach outcomes")
        outcome = view["Outreach status"].value_counts().reindex(STATUSES, fill_value=0)
        st.bar_chart(outcome, horizontal=True, color="#8ac5e8")
        st.caption(f"Declined in selected period: {declined}. All sample records are fictional.")
    else:
        st.info("No encounters yet. Add a fictional record to get started.")

with tab_new:
    st.subheader("Document a fictional outreach encounter")
    st.caption("Do not enter real patient details. The questions below are preliminary prompts, not clinical screening clearance.")
    with st.form("new_encounter", clear_on_submit=False):
        left, right = st.columns(2)
        with left:
            encounter_day = st.date_input("Date approached", value=date.today())
            age = st.number_input("Age", min_value=18, max_value=110, value=52, step=1)
            population = st.selectbox("OBSP population / pathway", POPULATIONS)
            symptoms = st.selectbox("Current breast symptoms?", ["No", "Yes", "Unsure"])
            history = st.selectbox("Personal history of breast cancer?", ["No", "Yes", "Unsure"])
        with right:
            mastectomy = st.selectbox("Previous mastectomy?", ["No", "Yes", "Unsure"])
            recent = st.selectbox("Screening mammogram within the last 11 months?", ["No", "Yes", "Unsure"])
            hormones = st.selectbox("If transfeminine: 5 consecutive years of feminizing hormones?", ["Not applicable", "Yes", "No", "Unsure"])
            status = st.selectbox("Outreach outcome", STATUSES)
            appointment = st.date_input("Appointment date (if booked)", value=date.today() + timedelta(days=7)) if status == "Booked" else None
        submitted = st.form_submit_button("Save fictional encounter", type="primary")
    eligibility, explanation = assess(age, population, symptoms, history, mastectomy, recent, hormones)
    st.info(f"**Preliminary OBSP prompt:** {eligibility}. {explanation}")
    if submitted:
        if status == "Booked" and appointment < encounter_day:
            st.error("Appointment date cannot be before the encounter date.")
        else:
            st.session_state.next_id += 1
            st.session_state.encounters.append({"ID": f"DEMO-{st.session_state.next_id:03d}",
                "Date approached": encounter_day.isoformat(), "Age": age, "Population": population,
                "Symptoms": symptoms, "Cancer history": history, "Mastectomy": mastectomy,
                "Mammogram in past 11 months": recent, "Hormone criterion": hormones,
                "Eligibility prompt": eligibility, "Outreach status": status,
                "Appointment date": appointment.isoformat() if appointment else "",
                "Screening follow-up": "Not verified"})
            st.success("Fictional encounter saved for this session. View it under Records & follow-up.")
            if status == "Booked" and eligibility not in ("Preliminary criteria met", "Preliminary criteria met — informed choice"):
                st.warning("This record is marked Booked but requires eligibility review. A booking status does not confirm OBSP eligibility.")

with tab_records:
    st.subheader("Encounter records")
    df = table()
    if not df.empty:
        x, y = st.columns(2)
        with x:
            chosen_status = st.selectbox("Filter by outreach status", ["All"] + STATUSES)
        with y:
            date_options = sorted(df["Date approached"].unique().tolist())
            chosen_date = st.selectbox("Filter by date", ["All"] + date_options)
        filtered = df.copy()
        if chosen_status != "All":
            filtered = filtered[filtered["Outreach status"] == chosen_status]
        if chosen_date != "All":
            filtered = filtered[filtered["Date approached"] == chosen_date]
        st.dataframe(filtered, hide_index=True, use_container_width=True)
        st.download_button("Download filtered fictional records (CSV)", filtered.to_csv(index=False).encode("utf-8"),
                           "mammoconnect_synthetic_demo.csv", "text/csv")
        st.divider()
        st.subheader("Update a fictional encounter")
        st.caption("Updates are temporary and apply only to this session. This is not an audit-trailed clinical record system.")
        chosen_id = st.selectbox("Encounter ID", df["ID"].tolist())
        record = next(r for r in st.session_state.encounters if r["ID"] == chosen_id)
        with st.form("update_record"):
            updated_status = st.selectbox("Outreach status", STATUSES, index=STATUSES.index(record["Outreach status"]))
            default_appt = date.fromisoformat(record["Appointment date"]) if record["Appointment date"] else date.today() + timedelta(days=7)
            updated_appt = st.date_input("Appointment date", value=default_appt) if updated_status == "Booked" else None
            followup = st.selectbox("Screening follow-up (fictional)", ["Not verified", "Appointment attended (unverified demo)", "Completed (fictional verified example)", "Cancelled / not attended"],
                                    index=["Not verified", "Appointment attended (unverified demo)", "Completed (fictional verified example)", "Cancelled / not attended"].index(record["Screening follow-up"]))
            save_update = st.form_submit_button("Update fictional record")
        if save_update:
            if updated_status == "Booked" and updated_appt < date.fromisoformat(record["Date approached"]):
                st.error("Appointment date cannot be before the encounter date.")
            else:
                record["Outreach status"] = updated_status
                record["Appointment date"] = updated_appt.isoformat() if updated_appt else ""
                record["Screening follow-up"] = followup
                st.success("Fictional record updated.")
                st.rerun()
    else:
        st.info("No records available.")

with tab_about:
    st.subheader("Why MammoConnect?")
    st.write("MammoConnect supports breast cancer screening outreach by organizing educational encounters, appointment assistance, and measurable results. The goal is to help more eligible people access screening and support earlier detection.")
    st.markdown("**Current demonstration features:** encounter entry, preliminary screening prompts, booking documentation, editable demo records, daily analytics, and CSV export.")
    st.markdown("**Before real clinic use:** management authorization, privacy and security review, approved patient-data infrastructure, user authentication, audit logs, verified screening pathways, and clinical oversight are required.")
    st.caption("Mammography supports early detection; it does not prevent breast cancer from developing. Bookings are not equivalent to completed screening.")
    st.markdown("Source: [Ontario Health / Cancer Care Ontario — Breast Screening Recommendations](https://www.cancercareontario.ca/en/guidelines-advice/cancer-continuum/screening/breast-screening-recommendations-summary)")
    st.markdown("**Developed by Safa Hamidi**")
