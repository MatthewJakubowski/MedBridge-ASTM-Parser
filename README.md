<div align="center">
  <img src="https://raw.githubusercontent.com/MatthewJakubowski/Universal-Lab-Converter/main/going_dark_cover.jpg" width="100%" alt="System Status: Going Dark. Deep Work Protocol.">

# 🔬 MedBridge-ASTM-Parser

### Deterministic ASTM E1381/E1394 Protocol Parser & Hardware Telemetry Engine

[![CI - Pytest Suite](https://github.com/MatthewJakubowski/MedBridge-ASTM-Parser/actions/workflows/ci.yml/badge.svg)](https://github.com/MatthewJakubowski/MedBridge-ASTM-Parser/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3b82f6?logo=python&logoColor=white)](https://github.com/MatthewJakubowski/MedBridge-ASTM-Parser)
[![Standard](https://img.shields.io/badge/Standard-ASTM%20E1381%20%2F%20E1394-00e5ff)](https://github.com/MatthewJakubowski/MedBridge-ASTM-Parser)
[![Research & PoC](https://img.shields.io/badge/Status-Educational%20%2F%20PoC-f59e0b)](https://github.com/MatthewJakubowski/MedBridge-ASTM-Parser)
[![License: MIT](https://img.shields.io/badge/License-MIT-06b6d4.svg)](https://opensource.org/licenses/MIT)

> **Automated Laboratory Interoperability Package**  
> A deterministic, zero-black-box parser implementing ASTM E1381 Modulo 256 framing checksums, ASTM E1394 clinical record extraction, and telemetry serialization directly to Pandas DataFrames.

---

### 🌐 Ecosystem & Professional Profiles

[🌐 Portfolio Hub](https://mateusz-jakubowski.ai.studio/) • [🚀 Project Showroom](https://from-pipette-to-python.ai.studio/) • [💼 LinkedIn](https://www.linkedin.com/in/mateuszjakubowski) • [🐙 GitHub](https://github.com/MatthewJakubowski)  
[🏆 Kaggle](https://www.kaggle.com/matthewjakubowski) • [🤗 Hugging Face](https://huggingface.co/matthewjakubowski) • [𝕏 Twitter / X](https://x.com/M_S_Jakubowski) • [🍷 Vivino](http://www.vivino.com/users/mateusz.jakubowski/)

</div>

---

## 🤖 AI & Learning Transparency

This project documents my technical transition from Medical Diagnostic Analysis to Software Engineering and Explainable AI (**#FromPipetteToPython**).

While the core domain knowledge (Laboratory Information Systems, analyzer serial communication, preanalytical flags, ISO 15189 compliance) stems from my 15 years of experience in clinical diagnostic laboratories, the modular parser architecture, framing validators, and pytest test matrices were engineered with the technical co-pilot assistance of **Google Gemini**.

The entire codebase is developed and tested in a mobile-only engineering environment (**Samsung DeX + Pydroid 3 / Termux**).

---

## 📊 Overview

In clinical diagnostic laboratories, analytical reliability starts at the physical analyzer port. Diagnostic instruments transmit patient orders and analytical runs using the low-level **ASTM E1381** framing specification and the **ASTM E1394** clinical hierarchy.

**MedBridge-ASTM-Parser** provides:
1. **Low-Level Framing Integrity (ASTM E1381):** Verifies serial/TCP packets using deterministic **Modulo 256 Checksum** calculation.
2. **Stream Defragmentation:** Handles message frames, intermediate blocks (`<ETB>`), and session terminations (`<ETX>`, `<EOT>`).
3. **Hierarchical Semantic Extraction (ASTM E1394):** Ingests Header (`H`), Patient (`P`), Order (`O`), Result (`R`), and Terminator (`L`) lines into strictly typed dataclasses.
4. **Data Science Integration:** Serializes clinical records directly into structured **Pandas DataFrames** ready for downstream statistical quality control and validation pipelines.

---

## 🏛️ Architecture & Data Flow

┌─────────────────────────────────────────────────────────────┐
│                    Diagnostic Analyzer                      │
│        (Biochemistry, Hematology, Immunochemistry)          │
└──────────────────────────────┬──────────────────────────────┘
│ Serial RS-232 / TCP-IP Stream
▼
┌─────────────────────────────────────────────────────────────┐
│             ASTM E1381 Framing & Transport Layer            │
│  - Control Characters: <STX>, <ETB>, <ETX>, <CR>, <LF>      │
│  - Modulo 256 Checksum Validation                           │
└──────────────────────────────┬──────────────────────────────┘
│ Verified Frame Payloads
▼
┌─────────────────────────────────────────────────────────────┐
│             ASTM E1394 Clinical Semantic Parser             │
│  - Record Hierarchy: H (Header) ➔ P (Patient) ➔             │
│                      O (Order)  ➔ R (Result)  ➔ L (End)     │
└──────────────────────────────┬──────────────────────────────┘
│ Structured Dataclasses
▼
┌─────────────────────────────────────────────────────────────┐
│             Pandas DataFrame / JSON Export                  │
│  - Clean Analytical Data ready for XAI & Decision Suites    │
└─────────────────────────────────────────────────────────────┘


---

## ⚡ Quick Start

```python
from medbridge.framing import ASTMFrameValidator
from medbridge.parser import ASTM1394Parser

# 1. Verify low-level ASTM E1381 frame
raw_frame = "\x021H|\\^&|||Cobas_Pro|||||||P|1\r\x0303\r\n"
frame_result = ASTMFrameValidator.validate_and_extract(raw_frame)
print(f"Checksum Valid: {frame_result.is_valid}")

# 2. Parse complete multi-record session to Pandas DataFrame
raw_session = (
    "H|\\^&|||Cobas_Pro|||||||P|1\r"
    "P|1||PAT_1092^^^||Kowalski^Jan||19800101|M\r"
    "O|1|SMP_9921|||Routine||||||A\r"
    "R|1|^^^GLU^Glucose|105.2|mg/dL|70-99|H||F||||20260816080000\r"
    "L|1|N\r"
)

parser = ASTM1394Parser()
patients = parser.parse_text(raw_session)
df = parser.to_dataframe(patients)

print(df[["patient_id", "sample_id", "test_name", "value_numeric", "units", "abnormal_flag"]])
```
## 🧪 Unit Testing
​Run the automated test suite verifying checksum arithmetic, frame edge-cases, and DataFrame serializations:
```bash
pytest tests/ -v
```
## ⚖️ Legal & Medical Device Disclaimer
​IMPORTANT NOTICE / NON-MEDICAL SOFTWARE DISCLAIMER:
​Educational & Research Proof of Concept (PoC): This repository is developed solely for educational, technical demonstrative, and scientific research purposes under the #FromPipetteToPython initiative.
​Not a Certified Medical Device: This software is NOT a certified Medical Device (neither CE-IVD, IVDR 2017/746, nor FDA 510(k)/SaMD certified). It is not intended, designed, or approved for clinical decision-making, direct patient diagnosis, treatment monitoring, or live medical diagnostic execution without human verification.
​No Clinical Liability: All data processed in examples or unit tests are synthetic or anonymized mock datasets. The author disclaims any express or implied liability for errors, analytical discrepancies, or data integrity issues resulting from the direct or indirect use of this code in clinical or commercial production environments.
​Provided "AS IS": The software is provided under the terms of the MIT License, without warranty of any kind.
## ​🛡️ License
​Distributed under the MIT License.

## 👨‍💻 About the Author

**Matthew (Mateusz) Jakubowski**  
*Senior Laboratory Technologist & Healthcare Data Engineer*  
Creator of the **#FromPipetteToPython** initiative.

With over 15 years of hands-on experience in high-throughput clinical diagnostic laboratories, I bridge the gap between laboratory medicine and modern data science. My engineering focus centers on **Explainable AI (XAI)**, **Statistical Quality Control (ISO 15189)**, and **deterministic hardware interoperability**—building robust, transparent tools that eliminate "black-box" risks in healthcare analytics.

* **Domain Expertise:** Clinical Laboratory Diagnostics, Hematology & Biochemistry Automation, LIS/HIS Interoperability, Statistical Metrology ($6\sigma$, Westgard Multirule).
* **Engineering Stack:** Python, Pandas, Scikit-Learn, Pytest, FastAPI, Docker, Google Colab.
* **Development Environment:** 100% Mobile-First Engineering on **Samsung DeX** (Galaxy S24 Ultra & Tab S11 Ultra) via Termux, Pydroid 3, and Google AI Studio.

---

### 📬 Connect & Collaborate

* 🌐 **Portfolio Hub:** [mateusz-jakubowski.ai.studio](https://mateusz-jakubowski.ai.studio/)
* 🚀 **Showroom:** [from-pipette-to-python.ai.studio](https://from-pipette-to-python.ai.studio/)
* 💼 **LinkedIn:** [/in/mateuszjakubowski](https://www.linkedin.com/in/mateuszjakubowski)
* 🐙 **GitHub:** [@MatthewJakubowski](https://github.com/MatthewJakubowski)
* 🏆 **Kaggle:** [@matthewjakubowski](https://www.kaggle.com/matthewjakubowski)
* 🤗 **Hugging Face:** [@matthewjakubowski](https://huggingface.co/matthewjakubowski)
* 𝕏 **Twitter / X:** [@M_S_Jakubowski](https://x.com/M_S_Jakubowski)
* 🍷 **Vivino:** [mateusz.jakubowski](http://www.vivino.com/users/mateusz.jakubowski/)
