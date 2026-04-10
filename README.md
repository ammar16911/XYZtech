# XYZtech DMAIC Project

Lean Six Sigma case study analyzing XYZtech's proposal creation process. The goal is to reduce end-to-end cycle time by 15% using the DMAIC framework.

**Team:** Anthony, Basilio, Chirag, Sau

---

## Folder Structure

```
xyztech-dmaic/
├── 1. XYZ Tech Case Study/      # The original case study PDF
├── 2. Case Study Data Set/      # Raw ERP dataset (75K transactions)
├── 3. Case Study Instructions/  # Assignment docx + deliverables list
├── 4. XYZ App/                  # Flask progress tracker web app
│   ├── app.py                   # Backend (SQLite + REST API)
│   ├── seed_data.py             # 71 DMAIC tools + initial attachments
│   ├── requirements.txt
│   ├── templates/index.html     # Single-page UI
│   └── seed_files/              # Shared deliverables bundled with the repo
└── 5. XYZ Data/                 # Uploads (populated on first run from seed_files)
    ├── 1. Define/
    ├── 2. Measure/
    ├── 3. Analyze/
    ├── 4. Improve/
    └── 5. Control/
```

Uploads made through the web app go into `5. XYZ Data/<phase>/<substep>/<tool>/` so you can also browse them in File Explorer.

---

## Running the Web App

One person on the team runs it, everyone else connects over LAN.

### First-time setup (one-time)

```bash
cd "4. XYZ App"
pip install -r requirements.txt
```

### Start the server

```bash
cd "4. XYZ App"
python app.py
```

Then open **http://localhost:5000** in your browser. The first run seeds the 71 DMAIC tools and copies the initial files from `seed_files/` into `5. XYZ Data/`.

### Share with teammates

Find your local IP (`ipconfig` on Windows) and share **http://YOUR-IP:5000**. The app binds to `0.0.0.0` so any teammate on the same WiFi can connect.

For off-network access, use `ngrok http 5000`.

---

## What's Already Done

| # | Assignment Question | Status |
|---|---|---|
| Q1 | Project Charter (sponsor, scope, goals, team) | Done |
| Q2 | Process Map (swim lanes for all 5 regions) | Done |
| Q3 | Baseline cycle time per step (geo/brand) | Partial — numbers in validation workbook |
| Q4 | DPMO & Sigma level (35-day SLA defect) | Done — in validation workbook |
| Q5 | Brand/geography comparison + feedback analysis | Partial — feedback & Pareto visuals done |
| Q6 | Timestamp root-cause analysis | Not started |
| Q7 | Individual seller & BSS performance | Not started |
| Q8 | Bid complexity ↔ cycle time correlation | Not started |
| Q9 | LSS tools (Fishbone, VA/NVA, FMEA, 5 Whys) | Partial — only Pareto done |
| Q10 | Improvement recommendations | Not started |
| Q11 | Control plan | Not started |

See the web app for live progress tracking across all **71 DMAIC sub-step tools** mapped to the assignment questions.

---

## Key Findings

- **Geography is the primary driver of variation** — brand differences are negligible (~31.3–31.9 days across all brands)
- **Two universal bottlenecks:** ZQT6 (Config Review, 7.4 days) and ZQT8 (Pricing/Brand Approval, 6.5 days) account for 44% of total cycle time
- **NA has unique problems** at ZQT3 (routing: 4.5d) and ZQT4 (manager review: 5.3d) — nearly 2x other regions
- **Seller ↔ BSS friction:** sellers complain about BSS inexperience; BSS complains about incomplete seller documentation. Top theme in both feedback datasets.
- **JPN is best-in-class** at 27.2 days (7.0% defect rate) — same process, 30% faster execution. Internal benchmark candidate.

## Numbers at a Glance

| Metric | Value |
|---|---|
| Total transactions analyzed | 75,000 |
| Overall avg cycle time | 31.6 days |
| Defect rate (>35 day SLA) | 28.1% |
| DPMO | 281,053 |
| Sigma level | 2.08σ |
| NA defect rate | 44.5% (worst) |
| JPN defect rate | 7.0% (best) |
