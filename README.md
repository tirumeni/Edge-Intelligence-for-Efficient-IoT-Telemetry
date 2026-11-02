# Industrial IoT Telemetry Compression & Network Optimization Platform
### Interactive Gateway Dashboard & Algorithmic Analysis System

[![Test Suite](https://img.shields.io/badge/Pytest-16%2F16%20Passed-emerald.svg)](docs/TESTING_REPORT.md)
[![Python Version](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](backend/)
[![React Version](https://img.shields.io/badge/React-18.3-cyan.svg)](frontend/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-teal.svg)](backend/)
[![License](https://img.shields.io/badge/License-MIT-slate.svg)](LICENSE)

An academic and enterprise-grade full-stack web platform designed to analyze, mathematically validate, simulate, and deploy optimal telemetry compression for bandwidth-constrained Industrial IoT networks.

---

## 1. Executive Problem Summary

An industrial edge gateway aggregates periodic telemetry from **5,000 field sensor nodes** transmitting over a **9.6 kbps (9,600 bps)** narrowband physical carrier (Sub-GHz / RS-485 / Satellite). 

- **Legacy Baseline:** Telemetry is transmitted using a uniform fixed-length 3-bit binary code ($\lceil \log_2(8) \rceil = 3$ bits/message) at an aggregate rate of **40 messages per second**.
- **The Optimization Goal:** Construct an optimal prefix-free codebook from calibrated empirical frequencies to maximize network bandwidth headroom.
- **The Embedded Hardware Bottleneck:** Receiver field units (e.g. ARM Cortex-M0+, PIC24) possess **4-bit hardware bit-manipulation registers**. Unconstrained Huffman coding produces codewords of 5 and 6 bits, causing register overflow and firmware crashes.
- **The Engineering Solution:** Deploy the **Package-Merge algorithm (Larmore & Hirschberg, 1990)** to construct an optimal length-limited prefix codebook ($L_{\max} = 4$ bits), surrendering only **0.10 bits/message (4.5% efficiency trade-off)** to guarantee **100% firmware register compatibility** while achieving a continuous **23.33% bandwidth reduction** (28 bps freed).

---

## 2. Ground Truth Telemetry Input Data

| Symbol Identifier | Semantic Meaning | Observed Frequency (per 100 msgs) | Empirical Probability $p_i$ | Legacy 3-Bit Code | Standard Huffman | Package-Merge ($L \le 4$) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| `OK` | Nominal status | 52 | 0.5200 | `000` (3b) | `1` (1b) | `0` (1b) |
| `TEMP_HI` | High temp alert | 14 | 0.1400 | `001` (3b) | `010` (3b) | `100` (3b) |
| `TEMP_LO` | Low temp alert | 11 | 0.1100 | `010` (3b) | `001` (3b) | `1110` (4b) |
| `HUM` | Humidity alert | 9 | 0.0900 | `011` (3b) | `000` (3b) | `1100` (4b) |
| `VIB` | Vibration alert | 7 | 0.0700 | `100` (3b) | `0110` (4b) | `1111` (4b) |
| `DOOR` | Hatch open | 4 | 0.0400 | `101` (3b) | `01111` (5b) ⚠️ | `1010` (4b) ✅ |
| `FAULT` | Inverter trip | 2 | 0.0200 | `110` (3b) | `011101` (6b) ⚠️ | `1011` (4b) ✅ |
| `RESET` | Watchdog pulse | 1 | 0.0100 | `111` (3b) | `011100` (6b) ⚠️ | `1101` (4b) ✅ |
| **TOTAL** | | **100** | **1.0000** | **3.00 bits** | **2.20 bits** | **2.30 bits** |

*Notice: In standard Huffman, `DOOR` (5b), `FAULT` (6b), and `RESET` (6b) exceed 4 bits, violating the receiver register limit. Package-Merge achieves exact 4-bit compliance.*

---

## 3. Mathematical Results Summary

- **Shannon Information Entropy ($H(X)$):** **2.1843 bits/message** (Theoretical lower bound).
- **Unconstrained Huffman ($L_{\text{Huff}}$):** **2.2000 bits/message** (Coding efficiency: 99.28%, Savings: 26.67%).
- **Length-Limited Package-Merge ($L_{\text{PM}}$):** **2.3000 bits/message** (Savings: 23.33%, 100% Hardware Compliant).
- **Brute-Force Optimal Cost ($4^8 = 65,536$ search space):** **2.3000 bits/message** (Package-Merge optimality proven).
- **Two-Queue Linear Time Equivalence:** Exactly **2.2000 bits/message** (100% equivalence with min-heap).
- **Shannon-Fano Counterexample:** On $\Sigma = [37, 16, 16, 9, 7, 7, 5, 3]$, Shannon-Fano produces $2.6900$ bits vs Huffman $2.6500$ bits (**+0.0400 bits/msg deficit**).
- **Continuous Bandwidth Freed:**
  - Original: $40 \times 3 = 120.0 \text{ bps}$ (1.250% link utilization).
  - Compressed: $40 \times 2.3 = 92.0 \text{ bps}$ (0.958% link utilization).
  - Bandwidth Saved: **28.0 bps** ($23.33\%$).
  - Data Saved per Hour: **100,800 bits/hour (12.60 kBytes/hour)**.
  - Additional Link Capacity: Accommodates **+1,818 sensors** without expanding physical link bandwidth.

---

## 4. Key Platform Modules

1. **Huffman Tree & Codebook Engine:** Interactive probability normalization, React Flow binary prefix tree with $0/1$ branches, codebook table, mathematical metric strip, and sample message encoder/decoder.
2. **Algorithm Laboratory:** Side-by-side Huffman vs Shannon-Fano comparison, verified suboptimal counterexample loader, step-by-step Two-Queue linear-time animation ($O(N)$ vs $O(N \log N)$), and real empirical benchmark harness.
3. **Live Telemetry & Network Dashboard:** Real-time WebSocket packet streaming, throughput area chart, channel utilization gauge, cumulative bits saved, and 1-hour fast-forward projection modal (144,000 messages).
4. **Embedded Hardware Constraint Inspector:** Detection of register overflow in ordinary Huffman, configurable $L_{\max}$ Package-Merge execution, Kraft inequality validator, brute-force global optimality confirmation, and export of firmware-ready C headers (`telemetry_codebook.h`).
5. **Gateway Codebook Management:** Version tracking (`v1.0.0`), over-the-air broadcast simulation across 5,000 receivers with ACK receipts, retry modeling under lossy channels, and prevention of decoding with outdated codebook versions.
6. **Documentation & Reference Viewer:** In-app rendering of academic proofs, mathematical specifications, and direct download of the generated PDF document.

---

## 5. Technology Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS v4, React Flow (`@xyflow/react`), Recharts, Lucide React.
- **Backend:** Python 3.14+, FastAPI, Pydantic v2, Uvicorn, WebSockets, NumPy, ReportLab.
- **Testing:** Pytest (16 automated tests covering all algorithms, Kraft inequality, and bandwidth math).

---

## 6. Local Setup & Execution Instructions (macOS)

### Prerequisites
- Python 3.10+ (Tested on Python 3.14.5)
- Node.js 18+ (Tested on Node.js v24.14.1, npm 11.11.0)

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone <repo-url>
cd "DAA THEORY"

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
npm install --prefix frontend
```

### Step 3: Run Automated Test Suite
```bash
# Run all 16 algorithmic, mathematical, and integration tests
.venv/bin/pytest backend/app/tests -v
```

### Step 4: Generate Mathematical Specification PDF
```bash
# Generates docs/MATHEMATICAL_SPECIFICATION.pdf using ReportLab
.venv/bin/python backend/app/utils/generate_pdf.py
```

### Step 5: Start Backend Server
```bash
# In terminal 1:
source .venv/bin/activate
uvicorn backend.app.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000` (OpenAPI Swagger docs at `http://localhost:8000/docs`).

### Step 6: Start Frontend Development Server
```bash
# In terminal 2:
npm run dev --prefix frontend
```
Frontend will be live at `http://localhost:5173`.

---

## 7. Project Structure

```
.
├── README.md                           # Master setup and project guide
├── requirements.txt                    # Python dependencies
├── package.json                        # Root npm script orchestrator
├── pytest.ini                          # Test configuration
├── .env.example                        # Environment variable template
├── docs/                               # Formal academic documentation
│   ├── MATHEMATICAL_SPECIFICATION.md   # Mathematical specification
│   ├── MATHEMATICAL_SPECIFICATION.pdf  # Formatted PDF specification
│   ├── SYSTEM_ARCHITECTURE.md          # Systems & component architecture
│   ├── API_DOCUMENTATION.md            # REST and WebSocket endpoints
│   ├── ALGORITHM_COMPLEXITY.md         # O(N) vs O(N log N) asymptotic proofs
│   ├── TESTING_REPORT.md               # 16/16 test execution report
│   └── PROJECT_REPORT_OUTLINE.md       # University project report outline
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI app, CORS, routes & WebSockets
│   │   ├── algorithms/                 # Huffman, Shannon-Fano, Two-Queue, Package-Merge
│   │   ├── services/                   # Compression, benchmark, telemetry, codebook
│   │   ├── api/                        # REST controllers
│   │   ├── schemas/                    # Pydantic v2 schemas
│   │   ├── utils/                      # Validation, metrics, PDF generator
│   │   └── tests/                      # Pytest unit & integration test suite
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/                 # TreeVisualizer, FrequencyEditor, TwoQueueStepper, MessageCodec
    │   ├── views/                      # Overview, Huffman, Lab, Live, Hardware, Codebook, Docs
    │   ├── services/api.ts             # Centralized typed HTTP API
    │   ├── types/index.ts              # TypeScript interface definitions
    │   ├── App.tsx                     # Top-level state coordinator
    │   └── main.tsx                    # Entry point
    ├── vite.config.ts                  # Vite + Tailwind + Proxy configuration
    └── package.json
```

---

## 8. Verification & Acceptance Criteria

- [x] Full Mathematical Specification document and PDF generated.
- [x] Standard Min-heap Huffman algorithm implemented with exchange argument proof.
- [x] Shannon-Fano implemented with mathematically validated counterexamples.
- [x] Linear-time Two-Queue algorithm implemented with invariant proof and visual animation.
- [x] Package-Merge algorithm implemented for $L_{\max} = 4$ and verified against brute-force optimal search.
- [x] Exact network bandwidth calculations and physical overhead models provided.
- [x] Live WebSocket telemetry stream simulation maintaining aggregate 40 msgs/s.
- [x] Over-the-air codebook broadcast simulation and version mismatch rejection.
- [x] 16/16 automated tests passed.
- [x] Full-stack application built and tested.

