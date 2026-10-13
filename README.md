# MammoConnect

MammoConnect is a breast cancer screening outreach initiative supported by a Python dashboard for recording outreach encounters, documenting mammography bookings, and understanding whether patient education leads to action.

I started the project after seeing how uncertainty about screening options and appointment booking can become barriers to preventive care. The goal is to help more eligible people access mammography and support earlier breast cancer detection.

## Live demo

This repository contains a public demonstration built with **Python, Streamlit, and Pandas**. It includes fictional sample records, a preliminary OBSP screening checker, editable outreach outcomes, appointment tracking, daily and monthly summaries, and CSV export.

**This is a synthetic-data demonstration, not an approved patient-record system.** Do not enter real patient or clinic information. Records are held in the visitor's Streamlit session and may disappear when the session ends.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Clinical boundaries

Eligibility prompts are based on selected Ontario Breast Screening Program criteria and do not determine eligibility or replace clinical review. Real-world use would require organizational approval, verified clinical logic, access controls, audit logs, and approved data storage under applicable privacy requirements.

See [Ontario Health screening guidance](https://www.cancercareontario.ca/en/guidelines-advice/cancer-continuum/screening/breast-screening-recommendations-summary).

Developed by Safa Hamidi.

