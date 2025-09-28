# Create plots with plotly inline and export to html

# %%
# 0. Import packages
import os
import pandas as pd
import plotly.graph_objects as go


# %%
# 0. Load main data, generaltools, whatused
csv_df_dir = "csv_outputs_dir"
df_single = pd.read_csv(os.path.join(csv_df_dir, "df_single.csv"))
df_generaltools = pd.read_csv(os.path.join(csv_df_dir, "generaltools.csv"))
df_whatused = pd.read_csv(os.path.join(csv_df_dir, "whatused.csv"))

# %%
# 1. Left join for salary stacked bar chart
df_merged = (
    pd.merge(df_single, df_whatused, how='left', on='resp_id')
      .merge(df_generaltools, how='left', on='resp_id')
)

# %%
# 2. Salary as x axis, order, pd.Categorical
# Define salary order in the x axis
salary_order = [
    "15K or less",
    "15K+ to 25K",
    "25K+ to 35K",
    "35K+ to 45K",
    "45K+ to 55K",
    "55K+ to 65K",
    "65K+ to 75K",
    "75K+ to 85K",
    "85K+ to 95K",
    "95K+ to 100K",
    "a. 100K+ to 125K",
    "b. 125K+ to 250K",
    "c. 250K+"
]

# Ensure salary column is categorical with correct order
df_merged["salary"] = pd.Categorical(
    df_merged["salary"],
    categories=salary_order,
    ordered=True
)

# %%
# 3. Split categories into single-response and multi-response
single_response_cats = [
    "age_grp", "careerstg", "datarole_grpd", "educstat",
    "employertype", "gender", "industry", "sitework"
]

multi_response_cats = [
    "generaltools", "whatused"
]

label_map = {
    "age_grp": "Age Group",
    "careerstg": "Career Stage",
    "datarole_grpd": "Datarole Group",
    "educstat": "Education Status",
    "employertype": "Employer Type",
    "gender": "Gender",
    "generaltools": "General Tools",
    "industry": "Industry",
    "sitework": "Site Work",
    "whatused": "Skills"
}

# %%
# 4. Aggregate counts per category, grouped by salary
# Single-response: count unique respondents per (salary, category value)
agg_data_single = {}
for cat in single_response_cats:
    counts = (
        df_merged.groupby(["salary", cat])["resp_id"]
        .nunique()
        .reset_index(name="count")
    )
    agg_data_single[cat] = counts

# Multi-response: count mentions per (salary, category value)
agg_data_multi = {}
for cat in multi_response_cats:
    counts = (
        df_merged.groupby(["salary", cat])
        .size()
        .reset_index(name="count")
    )
    agg_data_multi[cat] = counts

# Load insights CSVs
single_insights = pd.read_csv("salary_single_insights.csv")
multi_insights = pd.read_csv("salary_multi_insights.csv")

single_insights_map = dict(zip(single_insights["cat"], single_insights["insight"]))
multi_insights_map = dict(zip(multi_insights["cat"], multi_insights["insight"]))





# %%
# 5. Build single-response stacked bar chart

# Initialize figure
fig_single = go.Figure()

# Pre-compute trace_counts and total_traces
trace_counts_single = [agg_data_single[cat][cat].nunique() for cat in single_response_cats]
total_traces_single = sum(trace_counts_single)

# Prepare dropdown buttons
buttons_single = []
trace_index = 0


for i, (cat, n_vals) in enumerate(zip(single_response_cats, trace_counts_single)):
    counts = agg_data_single[cat]
    # Add traces for each value in the category
    for val in sorted(counts[cat].dropna().unique()):
        subset = counts[counts[cat] == val]
        fig_single.add_trace(
            go.Bar(
                hovertemplate='n=%{y}<br>%{fullData.name}<extra></extra>',
                x=subset["salary"],
                y=subset["count"],
                name=str(val),
                visible=(i == 0)  # show only first category initially
            )
        )
    # Visibility mask for the dropdown state
    mask = [False] * total_traces_single
    for j in range(n_vals):
        mask[trace_index + j] = True
    
    # Insight for single response
    insight_text = single_insights_map.get(cat, "") 
    # Layout updates per dropdown selection
    layout_update = {
        "title": {"text": f"Salary Distribution by {label_map[cat]} - {insight_text}"},
        "legend": {"title": {"text": label_map[cat]}, "y": 0.85},
        "xaxis": {"categoryorder": "array", "categoryarray": salary_order}
    }

    buttons_single.append({
        "label": label_map[cat],
        "method": "update",
        "args": [{"visible": mask}, layout_update]
    })

    trace_index += n_vals

# Initial layout
fig_single.update_layout(
    hoverlabel=dict(
        bgcolor='white',
        font_size=16),
    paper_bgcolor='white',
    plot_bgcolor='white',   
    updatemenus=[
        dict(
            active=0,
            buttons=buttons_single,
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top"
        )
    ],
    barmode="stack",
    title={
        "text": f"Salary Distribution by {label_map[single_response_cats[0]]} — "
                f"{single_insights_map.get(single_response_cats[0], '')}"
    },
    xaxis_title="Salary Range",
    yaxis_title="Number of Respondents",
    legend_title=label_map[single_response_cats[0]],
    xaxis={"categoryorder": "array", "categoryarray": salary_order},
    width=1100,
    height=750,
    margin=dict(l=40, r=200, t=80, b=40),
    legend=dict(
        yanchor="top",
        y=0.85,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255,255,255,0.5)",
        font=dict(size=10)
    )
)

fig_single.show()
fig_single.write_html("salary_chart_single.html", include_plotlyjs="cdn")




# %%
# 6. Build multi-response stacked bar chart

# Initialize figure
fig_multi = go.Figure()

# Pre-compute trace_counts and total_traces
trace_counts_multi = [agg_data_multi[cat][cat].nunique() for cat in multi_response_cats]
total_traces_multi = sum(trace_counts_multi)

# Prepare dropdown buttons
buttons_multi = []
trace_index = 0

for i, (cat, n_vals) in enumerate(zip(multi_response_cats, trace_counts_multi)):
    counts = agg_data_multi[cat]
    # Add traces for each value in the category
    for val in sorted(counts[cat].dropna().unique()):
        subset = counts[counts[cat] == val]
        fig_multi.add_trace(
            go.Bar(
                hovertemplate='n=%{y}<br>%{fullData.name}<extra></extra>',
                x=subset["salary"],
                y=subset["count"],
                name=str(val),
                visible=(i == 0)  # show only first category initially
            )
        )
    # Visibility mask for the dropdown state
    mask = [False] * total_traces_multi
    for j in range(n_vals):
        mask[trace_index + j] = True

    # Get insight for multi_response
    insight_text = multi_insights_map.get(cat, "")

    # Layout updates per dropdown selection
    layout_update = {
        "title": {"text": f"Salary Distribution by {label_map[cat]} - {insight_text}"},
        "legend": {"title": {"text": label_map[cat]}, "y": 0.85},
        "xaxis": {"categoryorder": "array", "categoryarray": salary_order}
    }

    buttons_multi.append({
        "label": label_map[cat],
        "method": "update",
        "args": [{"visible": mask}, layout_update]
    })

    trace_index += n_vals

# Initial layout
fig_multi.update_layout(
    hoverlabel=dict(
        bgcolor='white',
        font_size=16),
    paper_bgcolor='white',
    plot_bgcolor='white',
    updatemenus=[
        dict(
            active=0,
            buttons=buttons_multi,
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top"
        )
    ],
    barmode="stack",
    title={
        "text": f"Salary Distribution by {label_map[multi_response_cats[0]]} — "
                f"{multi_insights_map.get(multi_response_cats[0], '')}"
    },
    xaxis_title="Salary Range",
    yaxis_title="Number of Mentions",
    legend_title=label_map[multi_response_cats[0]],
    xaxis={"categoryorder": "array", "categoryarray": salary_order},
    width=1100,
    height=750,
    margin=dict(l=40, r=200, t=80, b=40),
    legend=dict(
        yanchor="top",
        y=0.85,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255,255,255,0.5)",
        font=dict(size=10)
    )
    )

fig_multi.show()
fig_multi.write_html("salary_chart_multi.html", include_plotlyjs="cdn")






# %%
# 7. Combine all figures into one HTML using plotly.io
import plotly.io as pio

# Export each figure to a string instead of a file
html_single = pio.to_html(fig_single, include_plotlyjs='cdn', full_html=False)
html_multi = pio.to_html(fig_multi, include_plotlyjs=False, full_html=False)

# Wrap them in one HTML page
combined_html = f"""
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cdn.plot.ly/plotly-2.27.1.min.js"></script>
</head>
<body>
  <h4>Single-response Salary Chart - scroll down for multi-response breaks</h4>
  {html_single}
  <h4>Multi-response Salary Chart - scroll up for single-response breaks</h4>
  {html_multi}
</body>
</html>
"""

with open("salary_charts_combined.html", "w", encoding="utf-8") as f:
    f.write(combined_html)



