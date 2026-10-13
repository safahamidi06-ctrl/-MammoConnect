# MammoConnect
### Turning breast screening outreach into earlier detection opportunities

**MammoConnect** is a clinic-focused mammography outreach initiative supported by a Python application for documenting patient conversations, coordinating screening appointments, and measuring results. Its goal is to help more people who are eligible for breast screening understand their options and take the next step toward getting a mammogram.

The idea grew out of conversations at the clinic: a patient may qualify for publicly funded screening but not know when to start, where to book, or how to arrange an appointment. A short, informed conversation and practical booking assistance can help close that gap. MammoConnect brings that outreach into a consistent, measurable workflow.

**Our mission:** Increase informed participation in breast cancer screening through proactive outreach and easier appointment access, supporting earlier detection and potentially better outcomes.

> Mammograms are screening tests, not a way to prevent breast cancer from developing. The project's intended impact is increased screening participation and earlier detection—not a demonstrated reduction in breast cancer incidence.

## The problem we are addressing

Screening programs are only effective when people can access and use them. In a busy clinic, opportunities to discuss mammography can be missed, and outreach efforts are difficult to evaluate without a reliable way to record what happened after each conversation.

MammoConnect focuses on three practical questions:

1. **Who might benefit from a screening conversation?** Identify patients who may meet Ontario Breast Screening Program (OBSP) criteria and refer uncertain cases for staff review.
2. **What is preventing the next step?** Provide clear information, answer general questions within staff roles, and help interested patients navigate booking.
3. **Did outreach lead to action?** Record whether an appointment was booked, declined, already completed, or still under consideration, and summarize trends over time.

## How the initiative works

**1. Identify.** During an appropriate clinic interaction, staff recognize a possible screening opportunity and check basic criteria. The app's rules are preliminary prompts, not clinical clearance.

**2. Educate.** Staff explain the purpose of routine mammography, the availability of publicly funded screening, and the practical booking process. Participation remains the patient's informed choice.

**3. Assist.** When appropriate and requested, staff help arrange a mammography appointment through the clinic's authorized booking workflow.

**4. Document.** The encounter is recorded with a status and, for a booking, the scheduled appointment date.

**5. Evaluate.** Daily summaries show how many people were approached and how many conversations led to bookings. These results can guide improvements to outreach.

## Application features implemented

| Feature | What it provides |
| --- | --- |
| Encounter entry | Records the approach date, age, selected screening responses, and outreach outcome |
| Preliminary OBSP screening prompts | Flags common age and screening factors and cases requiring further review |
| Booking documentation | Captures an appointment date when the outcome is **Booked** |
| Outcome categories | **Booked**, **Declined**, **Already screened**, **Considering**, **Needs review** |
| Daily dashboard | Counts approaches, bookings, declines, prior screening, pending decisions, and review cases |
| Booking conversion metric | Calculates bookings as a share of approached patients not marked already screened |
| Records view | Filters entries by encounter date or outcome |
| CSV export | Exports filtered records for analysis and reporting |
| Local database | Stores demonstration encounters in SQLite between sessions |

The application is built with **Python, Streamlit, and SQLite**. It uses form validation, conditional eligibility logic, SQL aggregation, and visual reporting. It is a working application with an initial set of features, not just a design proposal.

## What success looks like

MammoConnect is designed to track the path from **outreach → interest → booking → screening completion**. The current application records outreach and bookings; verified completion tracking is a planned enhancement.

Useful measures include:

- **Patients approached:** Number of documented outreach encounters.
- **Potential screening opportunities:** Encounters flagged for screening discussion or verification.
- **Appointments booked:** Number of encounters resulting in a scheduled mammogram.
- **Booking conversion rate:** `Booked / (Approached − Already screened) × 100` in the current dashboard.
- **Patients declining or considering:** Indicators that may help staff improve communication and follow-up.
- **Completed mammograms:** A future metric that must be verified separately from appointments booked.

Booking counts demonstrate outreach activity and scheduling uptake; they do **not** on their own establish that screening occurred or that cancer outcomes improved. Measuring completed screenings over time would provide a stronger indicator of participation.

## Intended clinic value

For patients, MammoConnect supports easier access to understandable screening information and help with scheduling. For clinic staff, it creates a repeatable outreach process and reduces reliance on informal tallying. For clinic leadership, it provides a clearer picture of activity, conversion, and opportunities for workflow improvement.

The longer-term aim is to make proactive screening outreach a sustainable part of routine clinic operations, while keeping eligibility decisions and patient care under the clinic's existing clinical processes.

## Technology and setup

**Stack:** Python 3.10+, Streamlit, SQLite.

From the project folder, run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The browser will open the application. The program creates a local `mammoconnect_demo.db` database automatically.

**Current navigation:**

1. **New encounter:** Enter screening responses, select an outcome, and add an appointment date if booked.
2. **Daily dashboard:** Review daily totals, booking conversion rates, and booking trends.
3. **Records & export:** Filter demonstration records and export them as CSV.

## Screening eligibility and clinical boundaries

The current eligibility checker considers age 40–74 and selected screening-related responses. It can flag uncertainty or possible exclusions, but it **does not implement every OBSP eligibility pathway or replace staff verification**. In particular, screening history, symptoms, risk factors, gender-related eligibility criteria, and individual clinical circumstances may require further assessment.

The OBSP includes eligible women as well as eligible Two-Spirit, trans, and nonbinary people. Screening recommendations and pathways should always be checked against current Ontario Health guidance and clinic policy.

Reference: [Ontario Health / Cancer Care Ontario — Breast Screening Recommendations](https://www.cancercareontario.ca/en/guidelines-advice/cancer-continuum/screening/breast-screening-recommendations-summary).

## Proposed clinic rollout

MammoConnect is intended for real-world clinic workflow evaluation. **The current software must not be used to store real patient information yet.** It is configured for synthetic demonstration data and does not include staff authentication, role-based permissions, encryption, audit trails, or integration with an approved clinical record system.

A practical deployment pathway is:

1. **Workflow review:** Demonstrate the application to clinic management and reception/clinical staff; confirm where outreach fits into existing operations.
2. **Clinical review:** Validate the eligibility questions, status definitions, booking workflow, and escalation rules against current OBSP guidance.
3. **Privacy and security review:** Obtain organizational approval and implement the controls required for handling personal health information under applicable Ontario privacy requirements, including PHIPA.
4. **Controlled pilot:** Test the approved workflow, monitor data quality and staff usability, and make adjustments.
5. **Outcome evaluation:** Compare outreach volume, booking rates, and eventually verified screening completion across reporting periods.

Until the necessary approvals and protections are in place, use **fictional records only**—not names, health card numbers, contact information, or real patient screening details.

## Development roadmap

The current release establishes encounter entry, preliminary eligibility prompts, appointment documentation, and daily reporting. The next priorities are:

- Secure staff access, permissions, audit logging, and approved data storage.
- Authorized patient matching and duplicate-encounter prevention.
- Editing and updating encounters while preserving a change history.
- Separate tracking for **appointment booked**, **appointment attended**, and **screening completed**.
- Follow-up workflow for interested patients, with appropriate consent and clinic procedures.
- Monthly reporting that compares outreach activity with verified outcomes.
- Clinical validation and maintenance of eligibility rules as OBSP guidance changes.

## Vision

**MammoConnect is about making screening opportunities easier to recognize, discuss, and act on.** The software makes that work organized and measurable; the real goal is helping more eligible patients access mammography and improving the chances that breast cancer is detected early.
