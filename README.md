# FE5108 Midterm Group Project

**From the Mutual-Fund Theorem to the Security Market Line: does the theory survive real data?**

Due: **Sunday 18 October 2026, 23:59 (Singapore time)**

> **New here? Open the folder [`Read it before you do!`](./Read%20it%20before%20you%20do!) first.**
> It contains the project handout and the one-page-per-person guide to who does what.

## Who owns which file

Only edit the files next to your letter.

```
fe5108-midterm/
├── README.md                    # A   how to run, data files, package versions
├── requirements.txt             # A   package versions
├── run_all.py                   # A   single entry point: runs every script below in order
│
├── Read it before you do!/      # everyone reads, nobody edits
│   ├── midterm_project_handout.pdf
│   └── FE5108_Midterm_Who_Does_What.pdf
│
├── data/
│   ├── raw/                     # A   raw CSVs, downloaded once, never edited
│   └── clean/                   # A   the one shared monthly-returns file
│
├── src/
│   ├── config.py                # A   shared settings: sample period, tickers, paths, plot style
│   ├── data_prep.py             # A   download and clean the data
│   ├── stage1_portfolio.py      # B   Stage 1: tangency vs value weights
│   ├── stage2_capm.py           # C   Stage 2: CAPM regressions and the SML
│   ├── stage3_factors.py        # D   Stage 3: add size / value / momentum factors
│   └── stage4_roll.py           # E   Stage 4: rerun Stage 2 with another market index
│
├── output/
│   ├── figures/                 # all charts, e.g. fig_1b_weights.png
│   └── tables/                  # all tables, e.g. tab_2a_capm.csv
│
└── report/
    ├── 0_exec_summary.md        # E   one-page summary
    ├── 1_stage1.md              # B
    ├── 2_stage2.md              # C
    ├── 3_stage3.md              # D
    ├── 4_memo.md                # E   two-page memo to the committee
    └── appendix.md              # E   contribution statement, AI-use note
```

## What each person does

| Person | Job | Code | Report section |
|---|---|---|---|
| **A** | Get the data ready; make all the code run at the end | `config.py`, `data_prep.py`, `run_all.py` | `README.md` |
| **B** | Stage 1: the best portfolio vs the real market | `stage1_portfolio.py` | `1_stage1.md` |
| **C** | Stage 2: test CAPM | `stage2_capm.py` | `2_stage2.md` |
| **D** | Stage 3: add factors | `stage3_factors.py` | `3_stage3.md` |
| **E** | Stage 4: memo, summary, final report | `stage4_roll.py` | `0_exec_summary.md`, `4_memo.md`, `appendix.md` |

Step-by-step tasks for each person are in `FE5108_Midterm_Who_Does_What.pdf`.

## Key dates

| When | What |
|---|---|
| Fri 9 Oct | A delivers the clean returns file |
| Mon 12 Oct | B, C, D have their tables and charts. Meeting 1 (evening) |
| Thu 15 Oct | All written sections go to E. Meeting 2 |
| Fri 16 Oct | E finishes the full report. A tests all code from zero |
| Sat 17 Oct | Everyone proofreads and signs the contribution statement |
| Sun 18 Oct | Submit before 23:59 |

## Rules for everyone

1. Run `git pull` before you start working, every time.
2. Only edit your own code file and your own report section.
3. Read data only from `data/clean/`. Do not download your own copy.
4. Save every chart to `output/figures/` and every table to `output/tables/`.
5. Do not share this code or text with other groups.

## How to run

*(A fills this in: setup steps, data files, package versions.)*

```bash
pip install -r requirements.txt
python run_all.py
```
