# Mobix Field Pay Portal: SMS-Driven Timecard Tracking & Analytics Pipeline

## Project Overview
In many operational field environments across Zambia, managing teams and tracking performance is incredibly difficult due to one major hurdle: a lack of internet access and smartphones. Most enterprise workforce tracking systems rely heavily on mobile apps or web forms. When field agents are forced to use basic feature phones due to mobile data costs or device limitations, management loses visibility. This leads to delayed payroll cycles, administrative paperwork bottlenecks, and zero daily transparency for the workers regarding what they have earned.

The **Mobix Field Pay Portal** directly addresses this infrastructure gap. Built using **Python (Streamlit)** for the manager dashboard and **SQL (Supabase/PostgreSQL)** for the backend data warehouse, this application captures real-time clock-in and clock-out timestamps, handles complex data aggregations on the server side, and **democratizes operational data**. It compresses individual worked hours and calculated pay into clean text messages, sending automated payslips right to field workers' basic feature phones via SMS—requiring no smartphone or mobile data on the receiving end.

### Core Impact
* **Information Transparency:** Gives field workers immediate visibility into their calculated shifts, hours worked, and deductions. This eliminates pay disputes and builds deep organizational trust.
* **Overcoming the Digital Divide:** Operates entirely over standard cellular networks to reach offline teams, saving thousands of Kwacha in smartphone deployment and mobile internet data costs.
* **Real-Time Tracking:** Replaces messy paper logs with a centralized web dashboard, giving managers an accurate view of operational metrics the moment they happen.

---

## Solving Real Operational Bottlenecks

### 1. Boosting Field Productivity
* **The Problem:** Traditional paper-based time tracking meant management only saw attendance trends weeks late, making it impossible to address scheduling gaps or absenteeism dynamically.
* **The Solution:** A centralized, live-updating Streamlit portal. Managers log field shifts as they happen, shifting data usage from historical tracking into an active operational tool.

### 2. Eliminating the Smart Device Dependency
* **The Problem:** Offline field agents are typically left out of digital business systems because they lack reliable web connections or high-tier hardware.
* **The Solution:** A lightweight python data engine that connects straight to the Twilio SMS Gateway. This architecture drops vital payroll details directly onto the screens of standard mobile phones.

### 3. Creating Clean Data for Better Decisions
* **The Problem:** Fragmented tables and mismatched spreadsheets make it difficult to calculate true operational totals or download accurate histories for deeper analysis.
* **The Solution:** A robust relational warehouse that processes time series and joins data cleanly, allowing managers to export complete, accurate summaries to `.csv` formats for ad-hoc business analysis.

---

## Repository Architecture & Design Layout

This project is built following clean, modular software engineering patterns. The user interface, custom visual styles, and core database queries are separated into independent files to keep the codebase highly maintainable and easy to scale:

```text
├── database/
│   └── schema.sql       -- Relational table structures, performance indexes, and SQL views
├── src/
│   ├── __init__.py       -- Standard marker file to define Python project modules
│   ├── db_utils.py       -- Main integration engine (Supabase connections & Twilio SMS payloads)
│   └── styles.css        -- Custom CSS overrides to optimize the dashboard viewport layout
├── app.py                -- Administrative user interface, authorization, and analytics panel
├── requirements.txt      -- Complete python package environment dependencies
└── .gitignore            -- Security filter keeping local API tokens out of public view
