
# MammoConnect
### Breast Cancer Screening Outreach & Patient Tracking System

MammoConnect is a Python-based application I developed to support mammography outreach in a clinical setting. It helps document patient interactions, check preliminary screening eligibility, track appointment bookings, and measure the results of outreach efforts.

The idea came from my experience working in healthcare. I noticed that some patients who could benefit from routine mammography weren't aware of their screening options, while others were unsure about eligibility or how to arrange an appointment.

I began speaking with patients about breast cancer screening and helping interested patients book mammograms. As I started keeping track of these conversations, I wanted a better way to organize the information and understand whether my outreach was making a difference.

That's where MammoConnect started.

**The goal is to increase mammography participation through patient education and easier access to appointments, supporting earlier breast cancer detection.**

---

## Why I Built It

Working in a clinic has shown me that access to healthcare involves more than having services available. Patients also need to know those services exist, understand when they should use them, and know how to access them.

I wanted to make mammography outreach a more consistent part of the clinic workflow rather than relying on occasional conversations.

Initially, I tracked how many patients I approached, how many were already screened, and how many agreed to book appointments. Over time, I realized that a simple tally wasn't enough to understand patterns in screening participation.

I decided to build a program that could organize these encounters, help identify potential screening opportunities, and automatically summarize the results.

## What the Application Does

MammoConnect combines patient encounter tracking, preliminary eligibility checks, appointment documentation, and daily analytics.

### Patient Encounter Tracking

Each encounter can include:

- Date of interaction
- Patient age
- Preliminary screening responses
- Screening or booking status
- Scheduled appointment date, if applicable

Records are stored in a local SQLite database.

### Preliminary OBSP Eligibility Checker

The application includes a rule-based screening checker informed by Ontario Breast Screening Program (OBSP) guidelines.

It considers:

- The routine screening age range of 40–74
- Selected screening history
- Breast symptoms
- Previous breast cancer history
- Other factors requiring additional review

The checker helps identify possible screening opportunities. It does not replace clinical eligibility verification or account for every OBSP pathway.

### Screening and Booking Statuses

| Status | Description |
|--------|-------------|
| Booked | A mammography appointment was scheduled |
| Declined | The patient chose not to book |
| Already screened | The patient reported previous screening |
| Considering | The patient has not made a decision |
| Needs review | Additional eligibility verification is needed |

### Daily Dashboard

The dashboard automatically calculates:

- Total patients approached
- Number of appointments booked
- Patients already screened
- Patients who declined
- Patients considering screening
- Cases requiring review
- Daily booking conversion rates

The current booking rate is calculated as:

`Booking Rate (%) = Booked / (Approached - Already Screened) × 100`

This allows me to compare outreach results across different clinic days without manually calculating each total.

### Records and CSV Export

Encounter records can be filtered by date and screening outcome.

The application also supports CSV exports for further analysis and reporting.

---

## How MammoConnect Fits Into Clinic Outreach

The outreach process follows five steps:

**Identify → Educate → Assist → Record → Evaluate**

1. **Identify:** Recognize a potential screening opportunity and check basic eligibility criteria.
2. **Educate:** Explain mammography screening and the publicly funded services available through Ontario's screening program.
3. **Assist:** Help interested patients arrange appointments through the clinic's authorized booking process.
4. **Record:** Document the interaction, patient response, and appointment date when applicable.
5. **Evaluate:** Review the daily results and identify ways to improve outreach.

The software supports the process, but the conversations with patients remain the most important part of the initiative.

---

## Technology

MammoConnect was built using Python and a small set of supporting technologies.

| Technology | Purpose |
|------------|---------|
| Python | Application logic and data processing |
| Streamlit | User interface and dashboard |
| SQLite | Local database |
| SQL | Record retrieval and daily summaries |
| CSV | Exporting records for analysis |

The application uses input validation, conditional logic, database operations, and automated calculations to manage outreach information.

## Running the Application

### Requirements

- Python 3.10 or newer
- pip

### 1. Clone the repository

```bash
git clone https://github.com/safahamidi06-ctrl/-MammoConnect.git
cd -- -MammoConnect
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the application

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal, usually:

`http://localhost:8501`

The program automatically creates a SQLite database for local demonstration records.

---

## Measuring Outreach Impact

One of the main reasons I built MammoConnect was to understand whether patient outreach was translating into actual screening appointments.

The application currently measures:

- Number of patients approached
- Number of new mammography bookings
- Number of patients already screened
- Number of patients declining or considering screening
- Daily booking conversion rates

These measures help identify patterns in patient responses and compare outreach activity over time.

An appointment booking does not necessarily mean a mammogram was completed. Tracking verified screening completion separately is an important future improvement.

My longer-term goal is to understand how many patients ultimately access screening after an outreach conversation, not just how many agree to book.

## Clinic Implementation

MammoConnect is being developed with real clinical workflows in mind.

The current application provides encounter documentation, preliminary screening prompts, appointment tracking, and reporting.

Before using the application with identifiable patient information, it will need clinic approval, clinical validation, and appropriate privacy and security protections.

Future implementation requirements include secure staff authentication, access controls, audit logs, approved data storage, and compliance with Ontario's Personal Health Information Protection Act (PHIPA).

The current application should only be tested with synthetic patient information.

## Future Development

I plan to continue improving MammoConnect based on feedback from clinic staff and the needs of the outreach initiative.

Planned improvements include:

- **Screening completion tracking:** Distinguish appointments booked from mammograms completed.
- **Patient follow-ups:** Track interested patients who have not scheduled appointments.
- **Monthly reporting:** Compare screening outreach and booking trends across reporting periods.
- **Record management:** Support authorized edits and prevent duplicate encounters.
- **Secure staff accounts:** Introduce authentication, permissions, and audit logging.
- **Eligibility updates:** Expand and validate the screening checker against current OBSP guidelines.

---

## Long-Term Goal

I want MammoConnect to become a useful part of routine clinic operations, helping staff identify screening opportunities and making it easier for patients to access mammography.

The software helps organize and measure the work, but the larger purpose is to improve participation in breast cancer screening.

I started MammoConnect because I noticed a problem in the environment where I work and wanted to build something that could help address it. I hope to continue developing the application into a practical tool that benefits both patients and clinic staff.

---

**Developed by Safa Hamidi**

*Python · Healthcare Technology · Breast Cancer Screening · Clinical Workflow Improvement*
