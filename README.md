# Device Log Summarizer CLI

A Python-based CLI tool and data processing pipeline built for the Software Engineering Intern Technical Assessment.

---

## 📌 Project Overview

This project consists of three distinct modules addressing data sanitization, aggregation, and visualization:

1. **Section 1: Data Sanitization (`sanitize.py`)**  
   Cleans and normalizes noisy sensor data (type casting, handling `None` / invalid strings, dropping negative values, clipping values $> 500.0$, and edge-case testing).

2. **Section 2: Telemetry Summarizer (`summarizer.py`)**  
   Reads `device_telemetry.csv`, aggregates telemetry metrics by `device_id` (record count, mean temperature, error count), filters out overheating devices (average temperature $> 80.0^\circ\text{C}$), displays a terminal table, and exports the results to `output.json`.

3. **Section 3: Visualization & AI Log (`chart.py` & `PROMPT_LOG.md`)**  
   Loads `output.json` and renders a clean, color-coded bar chart comparing average temperatures and error counts per device saved as `chart.png`. Accompanied by documentation detailing AI collaboration.

---

## 📁 Repository Structure

```text
├── sanitize.py              # Section 1: Sensor data cleaning function and tests
├── summarizer.py            # Section 2: CSV ingestion, aggregation, filtering & export
├── chart.py                 # Section 3: Matplotlib visualization script
├── device_telemetry.csv     # Sample telemetry input dataset
├── output.json              # Sample exported JSON summary
├── chart.png                # Generated temperature comparison bar chart
├── PROMPT_LOG.md            # AI prompt documentation & bug resolution log
├── requirements.txt         # Project dependencies (matplotlib)
└── README.md                # Documentation & instructions
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
- Python 3.8+ installed

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Section 1 (Sanitization Tests)
```bash
python sanitize.py
```
*Executes all test cases verifying data cleaning and edge-case handling.*

### 4. Run Section 2 (Telemetry Summarizer)
```bash
python summarizer.py
```
*Processes `device_telemetry.csv`, displays the terminal summary table, and generates `output.json`.*

### 5. Run Section 3 (Generate Chart)
```bash
python chart.py
```
*Parses `output.json` and outputs `chart.png`.*

---

## 📊 Sample Outputs

### Terminal Summary Table
```text
--------------------------------------------------
Device       |  Records |  Avg Temp (°C) |  Errors
--------------------------------------------------
DEV_A        |        5 |          69.74 |       1
DEV_C        |        5 |          56.20 |       1
DEV_D        |        5 |          46.78 |       1
--------------------------------------------------
  Total devices: 3
```

### Exported Files
- **JSON File:** [output.json](output.json)
- **Bar Chart:** [chart.png](chart.png)
