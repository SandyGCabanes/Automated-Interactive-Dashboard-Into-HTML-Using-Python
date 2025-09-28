# Automated-Interactive-Dashboard-Into-HTML-Using-Python
## Salary Insights Dashboard (Python to HTML)

This dashboard shows what roles, industries, tools, skills, and demographics are most common within each salary range. It’s designed for stakeholders who want to explore compensation patterns interactively—no setup required.

Built in Python using Plotly, the chart is fully self-contained and runs in any browser. The workflow is modular, versioned, and audit-friendly, with explicit salary ordering and dynamic layout updates.  [See the workflow here](workflow_diagram_plotly.txt)

---

## What It Delivers

- Reveals which roles, industries, tools, skills, age groups, and genders are most represented in each salary band  
- Interactive stacked bar chart with dropdown filters  
- Insight summaries embedded in the chart title  
- Exported as a standalone HTML file for direct sharing [HTML file here](index.html)

---

## How Stakeholders Access It

This dashboard is delivered as a single HTML file. Stakeholders can:

- Open it directly via a link [e.g. GitHub Pages]([link here](https://sandygcabanes.github.io/Automated-Interactive-Dashboard-Into-HTML-Using-Python/)) or any internal portal  
- Download the file and view it in any browser—no setup required  

The chart runs locally in Chrome, Edge, Safari, or Firefox. It’s optimized for desktop viewing and presentation use.

---

## Mobile Compatibility

The dashboard can be viewed on tablets and mobile devices, but it’s not optimized for small screens. Font sizes and layout may appear cramped. For full clarity and usability, desktop viewing is recommended.

---

## For Technical Reviewers  
*(Built in Python using a structured, repeatable process—easy to audit, easy to maintain)*
[Python code here](plotly_salary.py)

- Categorical salary ordering via `pd.Categorical`  
  *(Salary ranges are shown in a consistent, logical order)*

- Aggregation logic for both single- and multi-response survey fields  
  *(Handles both single-answer and multi-answer questions correctly)*

- Dynamic layout updates tied to dropdown selection  
  *(Chart title and legend adjust automatically when switching categories)*

- Clean export using `plotly.graph_objects` with CDN bundling  
  *(Final file runs in any browser without setup or installation)*

- All transformations are modular and dictionary-driven for audit traceability  
  *(Every step is structured and transparent—no hidden edits or shortcuts)*

---

## Files Included

- `index.html` — the interactive dashboard  
- `salary_plotly.py` — annotated source script  
- `salary_single_insights.csv` — insight text per category
- `salary_multi_insights.csv` - insight text per category
-  Actual CSV input files are suppressed for privacy reasons 

---

This dashboard was built to make salary data easier to explore, share, and interpret—without sacrificing clarity or control. Every step in the workflow is documented and traceable, so reviewers can understand exactly how the chart was built and what it shows.
