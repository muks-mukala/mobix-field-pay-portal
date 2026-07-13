# Low-Resource Field Insights Tracker (SMS-to-Data Pipeline)

## Project Overview
In many developing markets like Zambia, field teams operate in environments without reliable internet access or smartphones. Traditional data collection tools (like ODK or custom mobile apps) fail here because of mobile data costs and hardware limitations.

This project is a functional, end-to-end data pipeline designed to bridge that gap. It manages operational data, processes workflows, and generates an administrative control center. Best of all, it features a custom communication gateway built to dispatch text-based insights directly back to field agents operating standard **non-smart feature phones** over standard cellular networks.

### Core Impact
* **Zero-Barrier Adherence:** Field agents require no internet data packages or smartphones to interact with the operational loop.
* **Cost-Effective Scalability:** Leverages standard SMS architecture to digitize real-time ground tracking.
* **Secure Data-Driven Decisions:** Centralizes disparate field milestones into a secure cloud system with a custom-styled modern dashboard.

---

## Architecture & System Design
The logic is fully modular and separated into dedicated functional layers to maintain clean, enterprise-grade codebase standards:

1. **Presentation Layer (`app.py`):** A custom Web Application UI displaying secure portal authentication, live operational timecard metrics, deduction entry logs, and interactive date-filtered dataframes.
2. **Database & Integration Engine (`src/db_utils.py`):** Acts as the transactional controller handling secure queries to cloud views, parsing operational metrics, and generating network-optimized payload blocks for SMS transmission.
3. **Design
