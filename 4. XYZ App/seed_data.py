"""Seed data for the DMAIC tracker — all 71 tools mapped to assignment questions."""

# (phase, substep_code, substep_title, tool_name, tool_desc, questions, initial_status, initial_note)
TOOLS = [
    # ===== DEFINE =====
    ("DEFINE", "1.1", "Define Business Case", "Problem Statement", "What's wrong? Quantified, time-bound.", "Q1", "done", "Documented in project charter"),
    ("DEFINE", "1.1", "Define Business Case", "Goal Statement", "What do you want to achieve?", "Q1", "done", "Documented in project charter"),
    ("DEFINE", "1.1", "Define Business Case", "Cost of Quality", "Financial impact of current state", "Q1", "partial", "Qualitatively addressed via lost bids; no hard $ figure"),
    ("DEFINE", "1.2", "Understand Customer", "Voice of Customer (VOC)", "How does the problem link to the customer?", "Q1", "partial", "Have seller/BSS text feedback (75K samples); no formal VOC session"),
    ("DEFINE", "1.2", "Understand Customer", "Kano Model", "Classify needs: must-have, want, delighter", "Q1", "todo", ""),
    ("DEFINE", "1.2", "Understand Customer", "CTQ Tree", "Critical-to-Quality tree from customer needs", "Q1", "todo", ""),
    ("DEFINE", "1.3", "Define the Process", "SIPOC Map", "Suppliers, Inputs, Process, Outputs, Customers", "Q2", "todo", ""),
    ("DEFINE", "1.3", "Define the Process", "Initial Process Map", "High-level flow of the process", "Q2", "done", "Swim lanes built for all 5 regions"),
    ("DEFINE", "1.4", "Manage the Project", "Project Structure & Plans", "Timeline, milestones, resources", "Q1", "done", "DMAIC 12-week roadmap"),
    ("DEFINE", "1.4", "Manage the Project", "Stakeholder Analysis", "Who has power/interest in the project", "Q1", "partial", "Listed in charter; no power/interest matrix"),
    ("DEFINE", "1.4", "Manage the Project", "Effective Teams & Meetings", "Who's on the team, how they work together", "Q1", "done", "Team listed in charter: Sponsor, BB, PSM, BSS, Sellers"),
    ("DEFINE", "1.5", "Gain Approval", "Project Charter", "Formal sign-off document from sponsor", "Q1", "done", "Single-page charter per slide 41 template"),

    # ===== MEASURE =====
    ("MEASURE", "2.1", "Develop Process Measures", "Y = f(X)", "Output = function of input variables", "Q2,Q3", "todo", ""),
    ("MEASURE", "2.1", "Develop Process Measures", "KPIs", "Key performance indicators", "Q3,Q4", "todo", ""),
    ("MEASURE", "2.1", "Develop Process Measures", "Operational Definitions", "Formal definition of how each KPI is measured", "Q3", "todo", ""),
    ("MEASURE", "2.2", "Collect Process Data", "Data Collection Methods", "In-process (automatic) vs manual", "Q3", "todo", ""),
    ("MEASURE", "2.2", "Collect Process Data", "Data Collection Plan", "Source, sample size, frequency, who, how", "Q3", "todo", ""),
    ("MEASURE", "2.2", "Collect Process Data", "Sampling", "Random, stratified, systematic, cluster", "Q3", "todo", ""),
    ("MEASURE", "2.3", "Understand Process Behavior", "Distributions", "Shape of the data - normal, skewed, etc.", "Q3", "todo", ""),
    ("MEASURE", "2.3", "Understand Process Behavior", "1st Pass Analysis", "Time series plot + histogram", "Q3", "todo", ""),
    ("MEASURE", "2.3", "Understand Process Behavior", "Process Stability", "Common-cause vs special-cause variation", "Q3", "todo", ""),
    ("MEASURE", "2.3", "Understand Process Behavior", "Process Capability Analysis", "Cp, Cpk relative to spec limits", "Q3,Q4", "partial", "Sigma calculated in validation workbook; Cp/Cpk not formally reported"),
    ("MEASURE", "2.4", "Check Data Quality", "Measurement System Evaluation", "Sources of error in measurement", "Q3", "todo", ""),
    ("MEASURE", "2.4", "Check Data Quality", "Data Quality Checks", "Completeness, accuracy, consistency", "Q3", "todo", ""),
    ("MEASURE", "2.5", "Baseline Process Capability", "DPMO", "Defects per million opportunities", "Q4", "done", "281,053 DPMO overall (formula-driven in workbook)"),
    ("MEASURE", "2.5", "Baseline Process Capability", "Sigma Level", "Z-score + 1.5 shift", "Q4", "done", "Overall 2.08 sigma (formula-driven in workbook)"),
    ("MEASURE", "2.5", "Baseline Process Capability", "Segmented Baselines", "By region and brand", "Q3,Q5", "done", "Per-region and per-brand breakdowns in workbook"),

    # ===== ANALYZE =====
    ("ANALYZE", "3.1", "Analyze the Process", "Process Mapping", "Detailed mapping of how it really works", "Q2,Q6", "done", "Swim lanes reveal ZQT6 + ZQT8 bottlenecks"),
    ("ANALYZE", "3.1", "Analyze the Process", "VA / NVA Analysis", "Value-add vs non-value-add step classification", "Q9", "todo", ""),
    ("ANALYZE", "3.1", "Analyze the Process", "7/8 Wastes (DOWNTIME)", "Defect, Over-prod, Waiting, Non-utilized talent, Transport, Inventory, Motion, Excess", "Q9", "todo", ""),
    ("ANALYZE", "3.1", "Analyze the Process", "Spaghetti Diagrams", "Visualize physical/info flow", "Q9", "todo", ""),
    ("ANALYZE", "3.1", "Analyze the Process", "Process Cycle Efficiency", "VA time / total cycle time", "Q9", "todo", ""),
    ("ANALYZE", "3.2", "Analyze the Data", "Data Visualization", "Bar, pie, scatter, histogram, trend", "Q5,Q6,Q7", "partial", "Regional feedback visualizations done; seller/BSS-level not yet"),
    ("ANALYZE", "3.2", "Analyze the Data", "Pareto Chart", "80/20 rule - vital few vs trivial many", "Q9", "done", "5 Pareto charts done for feedback"),
    ("ANALYZE", "3.2", "Analyze the Data", "Correlation & Regression", "Relationship between variables", "Q8", "todo", ""),
    ("ANALYZE", "3.2", "Analyze the Data", "Hypothesis Testing", "Is difference between groups significant?", "Q7,Q8", "todo", ""),
    ("ANALYZE", "3.2", "Analyze the Data", "Individual Performance Analysis", "Compare sellers and BSS individually", "Q7", "todo", ""),
    ("ANALYZE", "3.3", "Develop Potential Root Causes", "Brainstorming", "Generate candidate causes", "Q9", "todo", ""),
    ("ANALYZE", "3.3", "Develop Potential Root Causes", "Affinity Diagram", "Group similar ideas into themes", "Q9", "todo", ""),
    ("ANALYZE", "3.3", "Develop Potential Root Causes", "Fishbone (Ishikawa)", "Cause & effect: People/Process/Methods/Materials/Measurement/Environment", "Q9", "todo", ""),
    ("ANALYZE", "3.3", "Develop Potential Root Causes", "5 Whys", "Drill from symptom to root cause", "Q9", "todo", ""),
    ("ANALYZE", "3.3", "Develop Potential Root Causes", "Measles Chart", "Defect location check sheet", "Q9", "todo", ""),
    ("ANALYZE", "3.4", "Verify Root Causes", "Hypothesis Testing", "Confirm cause-effect statistically", "Q8", "todo", ""),
    ("ANALYZE", "3.4", "Verify Root Causes", "Confidence Intervals", "Range of likely true values", "Q8", "todo", ""),
    ("ANALYZE", "3.4", "Verify Root Causes", "Correlation & Regression", "Quantify the X -> Y relationship", "Q8", "todo", ""),
    ("ANALYZE", "3.4", "Verify Root Causes", "FMEA", "Failure Mode & Effects Analysis (RPN score)", "Q9", "todo", ""),

    # ===== IMPROVE =====
    ("IMPROVE", "4.1", "Generate Potential Solutions", "Brainstorming", "Idea generation from team", "Q10", "todo", ""),
    ("IMPROVE", "4.1", "Generate Potential Solutions", "Benchmarking", "Learn from best-in-class peers", "Q10", "todo", ""),
    ("IMPROVE", "4.1", "Generate Potential Solutions", "Robotic Process Automation (RPA)", "Automate repetitive transactional steps", "Q10", "todo", ""),
    ("IMPROVE", "4.1", "Generate Potential Solutions", "Best Practices", "Industry/sector best practices", "Q10", "todo", ""),
    ("IMPROVE", "4.1", "Generate Potential Solutions", "Six Thinking Hats / Mind Maps", "Structured creativity", "Q10", "todo", ""),
    ("IMPROVE", "4.2", "Select the Best Solution", "Prioritization Matrix", "Impact vs effort matrix", "Q10", "todo", ""),
    ("IMPROVE", "4.2", "Select the Best Solution", "Solution Screening", "Filter against criteria", "Q10", "todo", ""),
    ("IMPROVE", "4.2", "Select the Best Solution", "Paired Comparisons", "Head-to-head evaluation", "Q10", "todo", ""),
    ("IMPROVE", "4.3", "Assess the Risk", "Solution FMEA", "Failure mode analysis on new process", "Q10", "todo", ""),
    ("IMPROVE", "4.3", "Assess the Risk", "Assumption Busting", "Challenge implicit assumptions", "Q10", "todo", ""),
    ("IMPROVE", "4.4", "Pilot and Implement", "Pilot Studies", "Test in limited scope first", "Q10", "todo", ""),
    ("IMPROVE", "4.4", "Pilot and Implement", "Error Proofing (Poka-Yoke)", "Design out possibility of error", "Q10", "todo", ""),
    ("IMPROVE", "4.4", "Pilot and Implement", "Change Management", "People-side of the transition", "Q10", "todo", ""),
    ("IMPROVE", "4.4", "Pilot and Implement", "Visual Management / 5S", "Workplace organization", "Q10", "todo", ""),

    # ===== CONTROL =====
    ("CONTROL", "5.1", "Implement Ongoing Measurement", "Statistical Process Control (SPC)", "Control charts for CTQs", "Q11", "todo", ""),
    ("CONTROL", "5.1", "Implement Ongoing Measurement", "Control Plan", "What to check, how often, reaction plan", "Q11", "todo", ""),
    ("CONTROL", "5.1", "Implement Ongoing Measurement", "KPI Dashboards", "Real-time visibility for managers", "Q11", "todo", ""),
    ("CONTROL", "5.2", "Quantify the Improvement", "Before/After Comparison", "Baseline vs post-improvement metrics", "Q11", "todo", ""),
    ("CONTROL", "5.2", "Quantify the Improvement", "Hypothesis Testing", "Is improvement statistically significant?", "Q11", "todo", ""),
    ("CONTROL", "5.3", "Standardize the Solutions", "Standardized Processes (SOPs)", "Written procedures", "Q11", "todo", ""),
    ("CONTROL", "5.3", "Standardize the Solutions", "Training Plans", "Cross-region training rollout", "Q11", "todo", ""),
    ("CONTROL", "5.3", "Standardize the Solutions", "5S Visual Management", "Workplace standards", "Q11", "todo", ""),
    ("CONTROL", "5.4", "Close the Project", "Project Report", "Final summary of findings/outcomes", "Q11", "todo", ""),
    ("CONTROL", "5.4", "Close the Project", "Closure Action Log", "Open items and owners", "Q11", "todo", ""),
    ("CONTROL", "5.4", "Close the Project", "Lessons Learned", "What worked / what didn't", "Q11", "todo", ""),
]

TEAM_MEMBERS = [
    "Unassigned",
    "Anthony",
    "Basilio",
    "Chirag",
    "Sau",
]

# ===========================================================================
# INITIAL_ATTACHMENTS
# Files auto-attached to tool cards on first DB initialization.
# Only files we actually built collaboratively are included here.
# ===========================================================================

# Paths are relative to the "4. XYZ App" folder.
# All seed files live in 4. XYZ App/seed_files/ and are checked into git,
# so the app works on any machine after a fresh clone.
_S = "seed_files"
_SW = f"{_S}/Swim Lanes"
_FB = f"{_S}/Feedback Analysis"
_PA = f"{_S}/Pareto Analysis"

INITIAL_ATTACHMENTS = [
    # --- Project Charter ---
    (f"{_S}/Project_Charter.pdf", "DEFINE", "1.1", "Problem Statement"),
    (f"{_S}/Project_Charter.pdf", "DEFINE", "1.1", "Goal Statement"),
    (f"{_S}/Project_Charter.pdf", "DEFINE", "1.4", "Effective Teams & Meetings"),
    (f"{_S}/Project_Charter.pdf", "DEFINE", "1.5", "Project Charter"),

    # --- DMAIC Roadmap (tracking doc) ---
    (f"{_S}/DMAIC_Roadmap.pdf", "DEFINE", "1.4", "Project Structure & Plans"),

    # --- Swim Lane Process Maps (Q2) ---
    (f"{_SW}/SwimLane_NA.jpg",   "DEFINE", "1.3", "Initial Process Map"),
    (f"{_SW}/SwimLane_EMEA.jpg", "DEFINE", "1.3", "Initial Process Map"),
    (f"{_SW}/SwimLane_AP.jpg",   "DEFINE", "1.3", "Initial Process Map"),
    (f"{_SW}/SwimLane_SA.jpg",   "DEFINE", "1.3", "Initial Process Map"),
    (f"{_SW}/SwimLane_JPN.jpg",  "DEFINE", "1.3", "Initial Process Map"),

    (f"{_SW}/SwimLane_NA.jpg",   "ANALYZE", "3.1", "Process Mapping"),
    (f"{_SW}/SwimLane_EMEA.jpg", "ANALYZE", "3.1", "Process Mapping"),
    (f"{_SW}/SwimLane_AP.jpg",   "ANALYZE", "3.1", "Process Mapping"),
    (f"{_SW}/SwimLane_SA.jpg",   "ANALYZE", "3.1", "Process Mapping"),
    (f"{_SW}/SwimLane_JPN.jpg",  "ANALYZE", "3.1", "Process Mapping"),

    # --- Validation Workbook (formula-driven evidence for DPMO/Sigma) ---
    (f"{_S}/XYZTech_Validation_Workbook.xlsx", "MEASURE", "2.3", "Process Capability Analysis"),
    (f"{_S}/XYZTech_Validation_Workbook.xlsx", "MEASURE", "2.5", "DPMO"),
    (f"{_S}/XYZTech_Validation_Workbook.xlsx", "MEASURE", "2.5", "Sigma Level"),
    (f"{_S}/XYZTech_Validation_Workbook.xlsx", "MEASURE", "2.5", "Segmented Baselines"),

    # --- Feedback analysis visuals -> Analyze 3.2 Data Visualization ---
    (f"{_FB}/Feedback_Seller_ByRegion.png",        "ANALYZE", "3.2", "Data Visualization"),
    (f"{_FB}/Feedback_BSS_ByRegion.png",           "ANALYZE", "3.2", "Data Visualization"),
    (f"{_FB}/Feedback_WordClouds_ByRegion.png",    "ANALYZE", "3.2", "Data Visualization"),
    (f"{_FB}/Feedback_Sentiment_vs_Performance.png","ANALYZE", "3.2", "Data Visualization"),
    (f"{_FB}/Feedback_Themes_ByRegion.png",        "ANALYZE", "3.2", "Data Visualization"),
    (f"{_FB}/Feedback_Defect_Association.png",     "ANALYZE", "3.2", "Data Visualization"),

    # --- Pareto charts -> Analyze 3.2 Pareto Chart ---
    (f"{_PA}/Pareto_Seller_Feedback.png", "ANALYZE", "3.2", "Pareto Chart"),
    (f"{_PA}/Pareto_BSS_Feedback.png",    "ANALYZE", "3.2", "Pareto Chart"),
    (f"{_PA}/Pareto_Seller_Defects.png",  "ANALYZE", "3.2", "Pareto Chart"),
    (f"{_PA}/Pareto_BSS_Defects.png",     "ANALYZE", "3.2", "Pareto Chart"),
    (f"{_PA}/Pareto_Combined_Themes.png", "ANALYZE", "3.2", "Pareto Chart"),
]
