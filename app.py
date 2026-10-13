import csv
import io
import sqlite3
from datetime import date, datetime
import streamlit as st

DB = 'mammoconnect_demo.db'
STATUSES = ['Booked', 'Declined', 'Already screened', 'Considering', 'Needs review']

def connection():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute('''CREATE TABLE IF NOT EXISTS encounters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        encounter_date TEXT NOT NULL,
        age INTEGER NOT NULL,
        population TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        cancer_history TEXT NOT NULL,
        mastectomy TEXT NOT NULL,
        recent_mammogram TEXT NOT NULL,
        hormone_criteria TEXT NOT NULL,
        eligibility TEXT NOT NULL,
        status TEXT NOT NULL,
        appointment_date TEXT,
        data_source TEXT NOT NULL DEFAULT 'Demo',
        created_at TEXT NOT NULL
    )''')
    return con

def eligibility(age, population, symptoms, history, mastectomy, recent, hormones):
    if not 40 <= age <= 74:
        return 'Outside standard age range — clinical review'
    if population == 'Not established':
        return 'Needs review — population criteria unknown'
    if any(x == 'Yes' for x in (symptoms, history, mastectomy, recent)):
        return 'Not eligible for routine OBSP screening — refer for review'
    if population == 'Transfeminine' and hormones == 'No':
        return 'Does not meet standard hormone criterion — review'
    if any(x == 'Unknown' for x in (symptoms, history, mastectomy, recent)):
        return 'Needs review — incomplete screening information'
    if population == 'Transfeminine' and hormones != 'Yes':
        return 'Needs review — hormone criterion unknown'
    if age <= 49:
        return 'Preliminary criteria met — informed decision encouraged'
    return 'Preliminary criteria met — confirm with OBSP staff'

st.set_page_config(page_title='MammoConnect | Demo', page_icon='🎗️', layout='wide')
st.title('🎗️ MammoConnect')
st.caption('Privacy-conscious prototype • No names, health card numbers, contact information or identifiable medical records')
st.warning('DEMO ONLY: Do not enter real patient information. Use only synthetic data. For clinic deployment, obtain organizational approval, security review, and integration with an authorized clinical system.')
con = connection()
tab1, tab2, tab3 = st.tabs(['New encounter', 'Daily dashboard', 'Records & export'])
with tab1:
    with st.form('new_encounter'):
        c1, c2 = st.columns(2)
        with c1:
            encounter = st.date_input('Date approached', value=date.today())
            age = st.number_input('Age', 0, 110, 50)
            population = st.selectbox('OBSP population criterion', ['Woman', 'Two-Spirit / trans / nonbinary', 'Transfeminine', 'Not established'])
            symptoms = st.selectbox('Current breast symptoms?', ['Unknown', 'No', 'Yes'])
            history = st.selectbox('Personal history of breast cancer?', ['Unknown', 'No', 'Yes'])
        with c2:
            mastectomy = st.selectbox('Previous mastectomy?', ['Unknown', 'No', 'Yes'])
            recent = st.selectbox('Screening mammogram in the past 11 months?', ['Unknown', 'No', 'Yes'])
            hormones = st.selectbox('If transfeminine: 5 consecutive years of feminizing hormones?', ['Not applicable', 'Unknown', 'Yes', 'No'])
            status = st.selectbox('Encounter outcome', STATUSES)
            appointment = st.date_input('Appointment date (only for Booked)', value=None)
        submitted = st.form_submit_button('Save demo encounter', type='primary')
    if submitted:
        result = eligibility(age, population, symptoms, history, mastectomy, recent, hormones)
        if status == 'Booked' and appointment is None:
            st.error('Please enter an appointment date for booked encounters.')
        elif status != 'Booked' and appointment is not None:
            st.error('Only booked encounters should have an appointment date.')
        elif appointment is not None and appointment < encounter:
            st.error('Appointment date cannot precede the encounter.')
        else:
            con.execute('''INSERT INTO encounters (encounter_date,age,population,symptoms,cancer_history,mastectomy,recent_mammogram,hormone_criteria,eligibility,status,appointment_date,data_source,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (str(encounter),age,population,symptoms,history,mastectomy,recent,hormones,result,status,str(appointment) if appointment else None,'Synthetic demo',datetime.now().isoformat(timespec='seconds')))
            con.commit()
            st.success('Synthetic encounter saved.')
            st.info('Eligibility assessment: ' + result)
with tab2:
    rows = con.execute('''SELECT encounter_date, COUNT(*) approached,
        SUM(CASE WHEN status='Booked' THEN 1 ELSE 0 END) booked,
        SUM(CASE WHEN status='Declined' THEN 1 ELSE 0 END) declined,
        SUM(CASE WHEN status='Already screened' THEN 1 ELSE 0 END) already_screened,
        SUM(CASE WHEN status='Considering' THEN 1 ELSE 0 END) considering,
        SUM(CASE WHEN status='Needs review' THEN 1 ELSE 0 END) needs_review
        FROM encounters GROUP BY encounter_date ORDER BY encounter_date''').fetchall()
    if not rows:
        st.info('No demo records yet. Add an encounter to see your daily summary.')
    else:
        data = [dict(r) for r in rows]
        for r in data:
            denominator = r['approached'] - r['already_screened']
            r['booking_rate_%'] = round(100*r['booked']/denominator, 1) if denominator else 0
        a,b,c = st.columns(3)
        a.metric('Total approaches',sum(r['approached'] for r in data))
        b.metric('Bookings',sum(r['booked'] for r in data))
        c.metric('Days tracked',len(data))
        st.dataframe(data, use_container_width=True, hide_index=True)
        st.bar_chart({r['encounter_date']:r['booked'] for r in data}, x_label='Date', y_label='Bookings')
        st.caption('Booking rate = booked / (approached − already screened). Pending and review outcomes remain in the denominator.')
with tab3:
    records = [dict(r) for r in con.execute('SELECT * FROM encounters ORDER BY encounter_date DESC, id DESC')]
    date_filter = st.text_input('Filter by encounter date (YYYY-MM-DD)', '')
    status_filter = st.selectbox('Filter by status', ['All'] + STATUSES)
    shown = [r for r in records if (not date_filter or r['encounter_date']==date_filter) and (status_filter=='All' or r['status']==status_filter)]
    st.dataframe(shown, use_container_width=True, hide_index=True)
    if shown:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(shown[0]))
        writer.writeheader(); writer.writerows(shown)
        st.download_button('Export filtered synthetic records (CSV)',output.getvalue(),'mammoconnect_demo.csv','text/csv')
    st.caption('All records are locally stored in the SQLite demo database. The demo does not implement authentication, encryption, audit logs or clinical-system integration.')
con.close()
