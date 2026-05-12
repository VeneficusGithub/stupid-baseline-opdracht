# Challenge Creator Guide: "Masterpiece of Misery"
## Building ML Lessons that Teach Through Intentional Chaos

**Version:** 1.0  
**Purpose:** A comprehensive guide for instructors/creators building the first two days of the Data Science traineeship  
**Audience:** Challenge creators, not students

---

## 🎯 Executive Summary

You are building a **didactic catastrophe on purpose**. Your goal is to force smart students (CS/Econometrics/Data Science graduates) to learn that:

1. **Baseline > Blindness** — A dumb business heuristic beats complex ML when the problem is simple
2. **Data > Model** — Dirty data will destroy even perfect algorithms
3. **Engineering > Theory** — Robust code that handles edge cases beats brilliant math that crashes on missing values

This guide tells you **what to build, why it works pedagogically, and where to hide the landmines**.

---

## Part 1: Program Context & Your Role

### 1.1 The Timeline: Where You Fit

This material forms the **foundation of the traineeship's first two days**. Here's how it flows:

#### Day 1: Stupid Baseline
- **Student expectation:** "Finally! Let's build ML models!"
- **Your intervention:** "No. First, let's calculate what happens if we do nothing."
- **Your material:** `docs/scenario_stupid_baseline.md` + `notebooks/student_challenge.ipynb`
- **Learning outcome:** ROI beats complexity. Always.

#### Day 2: Dirty Data Reality
- **Student expectation:** "Data is clean. Let's model it."
- **Your intervention:** Your `data/raw_returns.csv` makes their scripts crash spectacularly.
- **Your material:** Same notebook continued, but now the dataset teaches the lesson.
- **Learning outcome:** Data cleaning > algorithm selection. Period.

### 1.2 Your Learners (And Why This Matters)

**Who they are:**
- University-educated in CS, Econometrics, or Data Science
- They know Python syntax
- They've seen ML in textbooks
- They have **zero business sense** and **no engineering discipline**

**What this means for you:**
- Don't make it mathematically easy. They're smart enough to spot trivial problems.
- Make it **emotionally painful**. Watching their brilliant model fail on messy data hits harder than any lecture.
- Build trust first, then break it intentionally.

---

## Part 2: Pedagogical Framework

### 2.1 The "Bad Teacher" Philosophy

You are deliberately bad at giving them what they want. This is intentional.

**Rule 1: No Slides**
- Zero PowerPoints
- All theory, context, and didactic scaffolding lives in:
  - `docs/` — Markdown files with business context and math
  - `notebooks/` — Jupyter notebooks with instructions, examples, and traps
- The students **read and learn from your materials**, not from a presentation.

**Rule 2: The 80/20 Chaos Principle**
- 80% of your code and data is perfect, polished, professional.
- 20% is deliberately broken: hidden NaNs, bad data types, shifted probabilities.
- When a student asks: "Is this too mean?" — The answer is **no, this is the point**.

### 2.2 Your Double Audience

You are writing for **two people simultaneously**:

1. **The Student** — They see:
   - Clear instructions and empty cells to fill
   - Automatic tests that validate their work
   - A dataset that mysteriously breaks their code
   - A gradual realization that the problem isn't the algorithm

2. **The Instructor** — They see:
   - `solution.ipynb` with working code
   - **Explicit warnings** about where the traps are
   - Mathematical proof that the baseline wins
   - Clear notes: "Trap: Students will use `dropna()` and destroy the target variable. Watch for this."

---

## Part 3: User Story 1 — The Dirty Data Generator

### 3.1 Overview

**File:** `scripts/generate_dirty_data.py`  
**Output:** `data/raw_returns.csv` (exactly 100,000 rows)  
**Topic:** Retail bicycle sales with a deliberately hidden defect pattern

### 3.2 The Hidden Baseline (The Trap)

This is the **pattern students must discover**:

```
IF shift_type == 'Night' AND location == 'Amsterdam':
    Defect probability = 30%  (multiplicative effect)
ELIF shift_type == 'Night':
    Defect probability = 15%
ELIF location == 'Amsterdam':
    Defect probability = 15%
ELSE:
    Defect probability = 5%
```

This is **not random**. It's causal and findable, but only if students:
1. Don't blindly apply `dropna()`
2. Explore the data deeply (including the location variable)
3. Test hypotheses instead of throwing algorithms at it
4. Discover the interaction effect between shift and location

### 3.3 Required Data Corruption

Inject these imperfections at the specified rates. Each serves a pedagogical purpose:

#### 3.3.1 Price Column Corruption (~30%)
- **Inject:** String values with comma as decimal separator (e.g., "€ 1200,50")
- **Why:** Students assume numeric columns are numeric. This breaks `.astype(float)` silently if they're not careful.
- **Expected error:** `ValueError` when converting non-parseable strings to float

#### 3.3.2 Date Format Inconsistency (~20%)
- **Inject:** Mix of formats in `order_date`:
  - Standard: `YYYY-MM-DD`
  - Corrupt: `DD/MM/YYYY`
  - Some: European notation like `31.12.2023`
- **Why:** Demonstrates that "dates" aren't guaranteed to parse automatically. Pandas will read them as strings.
- **Expected error:** Silent type casting to `object` instead of `datetime64[ns]`

#### 3.3.3 Categorical NaN Masquerading (~10%)
- **Inject:** In categorical columns, replace some NaNs with strings:
  - `"null"`
  - `"N/A"`
  - `" "` (single space)
- **Why:** `df.isna()` doesn't catch these. Students learn to validate and clean, not just drop.
- **Expected behavior:** Their `isna().sum()` looks fine, but `.value_counts()` shows garbage values.

#### 3.3.4 Target Variable Corruption (CRITICAL - ~40%)
- **Inject:** Replace ~40% of the `1` values in `is_defect` with `NaN`
- **Why:** This is the pedagogical landmine.
  - Students who naively use `dropna()` remove actual defects from the dataset
  - Their model becomes biased: it never sees defects because they deleted them
  - The "perfect" baseline (always predict "no defect") suddenly wins
  - They realize: **data cleaning ≠ dropping rows**
- **Expected realization:** "Wait, why does dropping NaNs make my model worse?"

### 3.4 Generation Requirements

**Dependencies:** `faker`, `pandas`, `numpy`

**Pseudo-code logic:**

```python
def get_defect_probability(shift, location):
    """
    Determine defect probability based on shift and location.
    
    Rules:
    - Night shift + Amsterdam: 30% (multiplicative effect)
    - Night shift only: 15%
    - Amsterdam only: 15%
    - Other combinations: 5%
    """
    if shift == 'Night' and location == 'Amsterdam':
        return 0.30
    elif shift == 'Night':
        return 0.15
    elif location == 'Amsterdam':
        return 0.15
    else:
        return 0.05

def generate_dirty_data(n_rows=100000):
    # 1. Create base dataset with realistic values
    shifts = ['Night', 'Day', 'Evening']
    locations = ['Amsterdam', 'Rotterdam', 'Utrecht', 'The Hague', 'Amsterdam', 'Groningen']  # Note: Amsterdam appears more
    
    shift_types = [shifts[i % 3] for i in range(n_rows)]
    location_types = [random.choice(locations) for _ in range(n_rows)]
    
    data = {
        'bike_id': [uuid.uuid4() for _ in range(n_rows)],
        'order_date': [random_dates() for _ in range(n_rows)],
        'customer_name': [faker.name() for _ in range(n_rows)],
        'category': ['Road', 'Mountain', 'Hybrid', ...],
        'price': [random.uniform(500, 5000) for _ in range(n_rows)],
        'shift_type': shift_types,
        'location': location_types,
        'is_defect': [
            1 if random.random() < get_defect_probability(shift, location) else 0
            for shift, location in zip(shift_types, location_types)
        ],
    }
    
    # 2. Corrupt price (~30%)
    corrupt_indices = np.random.choice(n_rows, int(n_rows * 0.30), replace=False)
    for idx in corrupt_indices:
        data['price'][idx] = f"€ {data['price'][idx]:.2f}".replace('.', ',')
    
    # 3. Corrupt dates (~20%)
    corrupt_indices = np.random.choice(n_rows, int(n_rows * 0.20), replace=False)
    for idx in corrupt_indices:
        data['order_date'][idx] = data['order_date'][idx].strftime('%d/%m/%Y')
    
    # 4. Corrupt categories with fake NaNs (~10%)
    corrupt_indices = np.random.choice(n_rows, int(n_rows * 0.10), replace=False)
    for idx in corrupt_indices:
        data['category'][idx] = np.random.choice(['null', 'N/A', ' '])
    
    # 5. Corrupt target variable (~40%)
    #    Find all indices where is_defect == 1
    defect_indices = [i for i, val in enumerate(data['is_defect']) if val == 1]
    corrupt_target = np.random.choice(defect_indices, int(len(defect_indices) * 0.40), replace=False)
    for idx in corrupt_target:
        data['is_defect'][idx] = np.nan
    
    # 6. Convert to DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv('data/raw_returns.csv', index=False)
```

### 3.5 Definition of Done

- [ ] Script runs without errors
- [ ] Output CSV has exactly 100,000 rows
- [ ] All corruption requirements are met (prices, dates, categories, target)
- [ ] `data/raw_returns.csv` exists and is version-controlled (or generated on-the-fly during setup)
- [ ] Documentation in script explains what was injected and why

---

## Part 4: User Story 2 — Scenario Document

### 4.1 Overview

**File:** `docs/scenario_stupid_baseline.md`  
**Audience:** Students (but created with instructor understanding)  
**Content:** Business case, cost matrix, and the math of doing nothing

### 4.2 Required Sections

#### 4.2.1 Business Context

Write this **narratively**, not mathematically. Example structure:

```markdown
## The Bicycle Shop Problem

A major bicycle retailer suspects that bikes assembled during night shifts
are more likely to have defects. They ship directly to customers—if a defect
reaches a customer, it costs €100 in returns, logistics, and reputation damage.

They can add a quality control checkpoint before shipping, but each inspection
costs €10.

The question: **Which bikes should we inspect?**
```

**Key pedagogical goal:** Students should feel the *realness* of the problem before seeing any numbers.

#### 4.2.2 Cost Matrix

Explicit and simple:

```markdown
## Cost Matrix

| Prediction | Actual | Cost | Reasoning |
|------------|--------|------|-----------|
| Inspect    | Defect | €0   | Caught early |
| Inspect    | OK     | €10  | Wasted inspection |
| Don't inspect | Defect | €100 | Customer damage |
| Don't inspect | OK | €0 | Normal operation |
```

**Why this structure:**
- It's explicit and unambiguous
- Students can later compute expected cost = $\sum$ (cost × probability)
- It forces them to think in business terms, not classification metrics

#### 4.2.3 Three Scenarios

Present three decision rules, in increasing complexity:

**Scenario 1: Do Nothing**
```
Rule: Never inspect anything.
Cost per defect: €100
Expected cost: (Defect probability) × €100
Expected total cost: (Defects in dataset) × €100
```

**Scenario 2: Inspect All**
```
Rule: Inspect everything.
Cost per bike: €10
Expected cost: 100,000 × €10 = €1,000,000
```

**Scenario 3: Stupid Baseline** ← **This is the trap**
```
Rule: Inspect only bikes assembled during night shift.

Cost breakdown:
- Night shift bikes inspected: Success rate = 65% caught
- Day shift bikes not inspected: 5% defect rate still gets through

Expected cost: [Calculation the students must do]
```

**Pedagogical purpose:** By the time they implement this, they've accepted it's reasonable. Then their complex ML model gets the exact same cost, and they realize: *the business problem was already solved*.

#### 4.2.4 The Hard Pass/Fail Criterion

This is **non-negotiable**:

```markdown
## Hard Constraint

**It is strictly forbidden to import `sklearn`, `torch`, `tensorflow`, or any
other ML library until the Stupid Baseline cost has been calculated and
validated.**

Why? Because the point of this exercise is to prove that a heuristic can beat
a model when the problem is simple and the data tells a clear story.

If you import ML libraries before calculating the baseline, you fail this part
of the challenge and must restart.
```

**Why this matters:** It prevents the "algorithm first, analysis never" trap that kills junior data scientists.

### 4.3 Definition of Done

- [ ] Markdown file exists in `docs/scenario_stupid_baseline.md`
- [ ] Business context is narrative and relatable (not just math)
- [ ] Cost matrix is explicit and covers all four combinations
- [ ] Three scenarios (Do Nothing, Inspect All, Stupid Baseline) are clearly described
- [ ] The hard constraint on ML imports is stated clearly
- [ ] No spelling or grammar errors
- [ ] A student can reconstruct the cost calculation in Python after reading this

---

## Part 5: User Story 3 — The Notebooks

### 5.1 Overview

You create **two notebooks**:

1. **`notebooks/student_challenge.ipynb`** — What students see (instructions + empty cells + tests)
2. **`notebooks/solution.ipynb`** — What instructors see (working code + trap documentation)

### 5.2 The Portilla Standard

Every exercise follows this format:

```
[CELL 1: Problem Statement in Markdown]

ASSIGNMENT: [Clear, one-sentence instruction]
Your task:
- Bullet point 1
- Bullet point 2

[CELL 2: Code Stub (optional)]

[CELL 3: YOUR CODE HERE (empty cell for student)]

[CELL 4: TEST CELL (do not modify)]
# Automated validation
assert condition_1, "Error message"
assert condition_2, "Error message"
print("✅ Success: [Description]")
```

**Why this works:**
- Students get immediate feedback
- They can't cheat (test cell is final truth)
- Each step builds on the previous one
- Failures are explicit and actionable

### 5.3 Student Notebook Structure

#### Cell 1: Introduction
```markdown
# Masterpiece of Misery: Can You Beat the Baseline?

## What's In This Notebook
You're tasked with answering ONE question:
**Can a machine learning model predict defective bicycles cheaper than 
simply inspecting all bikes from the night shift?**

But your data is dirty, incomplete, and designed to trick you.

## Your Job
1. Load and explore the data
2. Clean it robustly (don't just drop rows!)
3. Calculate the cost of the Stupid Baseline
4. (If you get here) Try to beat it with ML

## Rules
- **No ML libraries** until you've calculated the baseline cost
- Every step is automatically tested
- The tests aren't trying to trick you; your data is
```

#### Cells 2-10: Data Loading & Exploration

**Example Exercise:**

```markdown
## ASSIGNMENT: Load the Dataset

Load `data/raw_returns.csv` into a pandas DataFrame called `df`.

Your task:
- Use `pd.read_csv()` with appropriate parameters
- Inspect the shape, dtypes, and first few rows
- Note anything suspicious

[YOUR CODE HERE]

--- TEST CELL (Do not modify) ---

assert isinstance(df, pd.DataFrame), "df must be a DataFrame"
assert df.shape[0] == 100000, f"Expected 100,000 rows, got {df.shape[0]}"
assert 'shift_type' in df.columns, "Missing shift_type column"
assert 'is_defect' in df.columns, "Missing is_defect column"
print("✅ Success: Dataset loaded correctly!")
```

**Why this test is crucial:** It checks both the happy path (data exists) and implicitly prepares them to fail later (when data is corrupted).

#### Cells 11-20: The Corruption Discovery

**Example Exercise (Price Cleaning):**

```markdown
## ASSIGNMENT: Clean the Price Column

You may notice that some prices are strings with commas (e.g., "€ 1200,50").

Your task:
- Create a new column `price_clean`
- Convert all prices to float (replace commas, remove currency symbols)
- Handle any rows that can't convert (they're genuinely broken)
- Do NOT use dropna() on the entire dataset

Hint: Use `pd.to_numeric(df['price'], errors='coerce')` or equivalent.

[YOUR CODE HERE]

--- TEST CELL (Do not modify) ---

assert 'price_clean' in df.columns, "Create a 'price_clean' column"
assert df['price_clean'].dtype == 'float64', \
    f"price_clean must be float64, got {df['price_clean'].dtype}"
assert df['price_clean'].isna().sum() < 100, \
    "Too many NaNs after cleaning. Did you drop the entire dataset?"
assert (df['price_clean'] > 0).all(), \
    "All prices should be positive after cleaning"
print("✅ Success: Prices cleaned to float64!")
```

**Trap hidden here:** Students who use `.replace()` carelessly or `.dropna()` fail this test. They learn precision.

#### Cells 21-30: The Baseline Calculation

**Example Exercise:**

```markdown
## ASSIGNMENT: Calculate the Stupid Baseline Cost

Based on the scenario (see `docs/scenario_stupid_baseline.md`):
- Cost of inspection: €10
- Cost of missed defect: €100
- Rule: Inspect only bikes from night shift

Your task:
1. Count bikes from the night shift
2. Assume 65% are actually defective (based on historical data)
3. Count bikes from day/evening shifts
4. Assume 5% are defective
5. Calculate total cost: (inspected bikes × €10) + (missed defects × €100)

[YOUR CODE HERE]

stupid_baseline_cost = ...

--- TEST CELL (Do not modify) ---

assert isinstance(stupid_baseline_cost, (int, float)), \
    "Cost must be numeric"
assert 2000000 < stupid_baseline_cost < 3000000, \
    f"Cost seems wrong: {stupid_baseline_cost}. Check your math."
print(f"✅ Baseline cost: €{stupid_baseline_cost:,.2f}")
```

**Pedagogical moment:** This is where they realize the baseline isn't stupid at all.

#### Cells 31+: ML (If They Get Here)

```markdown
## OPTIONAL: Beat the Baseline with ML

Now you can use `sklearn`.

Your task:
1. Train a classification model on cleaned, properly-handled data
2. Calculate the cost using the cost matrix
3. Compare to the baseline

If your model costs more than the baseline, you haven't beaten it. 
This is **not a failure**—it's the lesson.

[YOUR CODE HERE]
```

### 5.4 Solution Notebook Structure

Same structure as student notebook, but with:

1. **Working code** for every exercise
2. **Explicit trap warnings** for the instructor

**Example annotation in solution:**

```python
# TRAP FOR INSTRUCTOR: 
# Students will see 40% of is_defect as NaN and think "I should drop these rows."
# If they do, they remove actual defects from the dataset, biasing the model.
# Watch for this in Cells 21-25. The correct approach is:
# - Fill NaNs with 0 (assume it's not defective if we don't know)
# - OR impute based on shift_type
# - OR acknowledge this is a missing data problem

# We'll use approach 1 for simplicity:
df['is_defect'] = df['is_defect'].fillna(0)
```

### 5.5 Definition of Done

- [ ] `notebooks/student_challenge.ipynb` runs from top to bottom without kernel crashes
- [ ] Every exercise has a working test cell
- [ ] Tests are clear and fail gracefully with helpful error messages
- [ ] `notebooks/solution.ipynb` contains working code for all exercises
- [ ] Solution notebook has explicit "TRAP" annotations for instructors
- [ ] Mathematical proof: baseline cost < ML model cost (in solution)
- [ ] Both notebooks follow the Portilla Standard format
- [ ] No hardcoded answers in student notebook

---

## Part 6: Integration Checklist

Before considering this complete, verify:

### Data & Scripts
- [ ] `scripts/generate_dirty_data.py` runs and creates `data/raw_returns.csv`
- [ ] Raw CSV has 100,000 rows with all five corruptions
- [ ] Price, dates, categories, and target are properly corrupted
- [ ] Script is documented (inline comments explain why)

### Documentation
- [ ] `docs/scenario_stupid_baseline.md` exists and is complete
- [ ] Business context is clear and motivating
- [ ] Cost matrix covers all four outcomes
- [ ] Three scenarios are described with math
- [ ] Hard ML constraint is stated

### Notebooks
- [ ] `notebooks/student_challenge.ipynb` is self-contained
- [ ] Every exercise has a test cell
- [ ] `notebooks/solution.ipynb` matches structure exactly
- [ ] Solution notebook has instructor annotations
- [ ] Both run from top to bottom without errors

### Pedagogical
- [ ] Students discover that baseline ≈ ML cost
- [ ] Students learn robust data cleaning (not just dropna)
- [ ] Instructor has clear guidance on where traps are
- [ ] The "80/20 chaos" principle is evident throughout

---

## Part 7: Design Principles Recap

### The Teaching Philosophy

1. **Intentional Chaos**: 20% of your material is deliberately broken.
2. **Self-Grading**: Every exercise has a test. Students know immediately if they're right.
3. **Business First**: Teach cost, not accuracy. Teach ROI, not F1 scores.
4. **No Escapes**: Hard constraints (no ML before baseline) prevent cutting corners.
5. **Shared Mystery**: Both student and instructor see the same corruptions, but instructor knows where they are.

### The Cognitive Load

- **Day 1**: "Why is Python throwing errors?"
- **Day 2**: "Why is my model not better than doing nothing?"
- **Day 3+**: "How do I build models that actually solve problems?"

Each question builds understanding through frustrated realizations.

---

## Appendix A: File Structure

```
├── data/
│   └── raw_returns.csv                 (100,000 rows, deliberately dirty)
├── docs/
│   └── scenario_stupid_baseline.md     (Business case & cost matrix)
├── scripts/
│   └── generate_dirty_data.py          (Generates the raw CSV)
├── notebooks/
│   ├── student_challenge.ipynb         (What students see)
│   └── solution.ipynb                  (What instructors see)
└── README.md                           (How to run this)
```

---

## Appendix B: Sample Test Cell Patterns

### Pattern 1: Type Check
```python
assert df['column'].dtype == 'float64', \
    f"Expected float64, got {df['column'].dtype}"
```

### Pattern 2: Value Range Check
```python
assert (df['column'] >= 0).all() and (df['column'] <= 100).all(), \
    "Values out of expected range [0, 100]"
```

### Pattern 3: No Missing Data (After Cleaning)
```python
assert df['column'].isna().sum() == 0, \
    f"Found {df['column'].isna().sum()} NaN values after cleaning"
```

### Pattern 4: Presence Check
```python
assert 'new_column' in df.columns, \
    "Expected column 'new_column' not found"
```

### Pattern 5: Mathematical Validation
```python
assert 2000000 < baseline_cost < 3000000, \
    f"Baseline cost of {baseline_cost} seems incorrect. Check your calculation."
```

---

## Appendix C: Creator Quick Reference

| Component | Purpose | Trap Hidden | Student Sees |
|-----------|---------|-----------|--------------|
| Price corruption (~30%) | Teach type conversion | `.astype()` fails silently | String prices in numeric column |
| Date corruption (~20%) | Teach format handling | Silent `object` dtypes | Mixed date formats |
| Category NaNs (~10%) | Teach categorical validation | `isna()` doesn't catch strings | "null", "N/A", " " values |
| Target NaNs (~40%) | **MAIN TRAP** | `dropna()` deletes defects | Missing labels in outcome |
| Night shift (25%) | Teach basic pattern discovery | Students need to explore grouped data | Conditional probability by shift |
| Amsterdam (20%) | Teach multivariate relationships | Students may ignore location variable | Risk varies by location |
| Interaction (55%) | Teach interaction effects | Students test variables independently | Night + Amsterdam shows multiplicative risk |

---

**Last Updated:** [DATE]  
**Version:** 1.0