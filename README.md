# Mobix Pay Portal: Democratized Timecard Tracking & Low-Resource SMS Data Pipeline

## Mission Statement
In emerging economies like Zambia, data transparency shouldn't require high-tier smartphones or costly mobile data bundles. Traditional operational tools alienate field agents without internet access, leading to administrative blind spots, delayed metrics, and suppressed team performance.

**Mobix Pay Portal** resolves these friction points by functioning as a high-impact, low-resource digital pipeline. It digitizes timecard metrics, tracks real-time shifts, and **democratizes data transparency** by broadcasting automated payroll summaries and worked hours directly to field agents via standard SMS to their non-smart feature phones.

---

## Core Functionality
* **Real-Time Digital Punch Clock:** Enables managers to sign workers on/off shifts instantaneously, centralizing attendance data the moment it happens.
* **Transparent Payroll Computations:** Dynamically aggregates total accumulated hours, hourly operational rates, and contextual shortage adjustments.
* **Feature Phone Telecomm Gateway:** Translates administrative grid arrays into ultra-lean text blocks optimized for cellular networks, dispatching automated payslips without requiring internet access on the receiving end.

---

## Strategic Business Pain Points Resolved

### 1. Reversing Sluggish Field Productivity
* **The Pain Point:** Delayed visibility into attendance structures left management reactive, making it difficult to spot operational bottlenecks until weeks later.
* **The Solution:** A centralized, live-updating Streamlit control portal. Managers observe shift distributions instantly as they populate, turning data into immediate operational oversight.

### 2. Bridging the Digital Divide (The Smartphone / Data Gap)
* **The Pain Point:** Field workers in localized zones frequently lack smartphones or steady internet configurations, excluding them from conventional workforce tracking applications.
* **The Solution:** A backend pipeline linked directly to the Twilio SMS Gateway. This architecture drops vital financial accountability right into basic feature phone viewports over standard cellular frequencies.

### 3. Structural Analytics for Gap Analysis
* **The Pain Point:** Disconnected data silos make it nearly impossible to identify patterns of operational leakages, payroll errors, or human resource shortages.
* **The Solution:** A clean backend data warehouse tied to automated database aggregation layers. Managers can export cleanly formatted time series files into CSV format for deep-dive exploratory data analysis (EDA) and capacity optimization.

---

## Technical Architecture & Component Mapping



The repository is built following clean modular paradigms to maintain rigid separation between visual formatting and internal data calculations:

```text
├── src/
│   ├── __init__.py       # Signals Python module parsing boundaries
│   ├── db_utils.py       # Interacts with Supabase transactions & Twilio payloads
│   └── styles.css        # Implements viewport layouts for dashboard uniformity
├── app.py                # Serves as the interactive administrative interface
├── requirements.txt      # Lists application infrastructure packages
└── .gitignore            # Conceals local token configurations from public view
