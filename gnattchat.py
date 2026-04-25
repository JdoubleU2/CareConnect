import pandas as pd
import plotly.express as px

# Define the roadmap data
roadmap = [
    {"Task": "Project requirements & AI/LLM research", "Start": "2024-09-01", "Finish": "2024-09-30"},
    {"Task": "LLM training research", "Start": "2024-10-01", "Finish": "2024-10-31"},
    {"Task": "Snowflake training & data collection", "Start": "2024-11-01", "Finish": "2024-12-31"},
    {"Task": "Github repo & preprocessing scripts", "Start": "2025-01-01", "Finish": "2025-01-31"},
    {"Task": "First finetune (Colab) & pipeline", "Start": "2025-02-01", "Finish": "2025-02-14"},
    {"Task": "Transition to Snowflake Snowpark", "Start": "2025-02-15", "Finish": "2025-04-14"},
    {"Task": "Test finetunes & preprocessing overhaul", "Start": "2025-03-01", "Finish": "2025-03-15"},
    {"Task": "Integrated fine-tuning pipeline", "Start": "2025-03-15", "Finish": "2025-03-31"},
    {"Task": "Finetune Careconnect-llama3.2-3b-8b", "Start": "2025-03-15", "Finish": "2025-04-14"},
    {"Task": "Finetune gemma3", "Start": "2025-03-20", "Finish": "2025-04-10"},
    {"Task": "Github/docs & Careconnect finetune", "Start": "2025-04-01", "Finish": "2025-04-14"},
    {"Task": "Careconnect evaluation & backend", "Start": "2025-04-15", "Finish": "2025-04-21"},
    {"Task": "Website cleanup & hosting", "Start": "2025-04-22", "Finish": "2025-04-30"},
    {"Task": "Final Presentation", "Start": "2025-05-05", "Finish": "2025-05-05"},
]

# Create DataFrame
df = pd.DataFrame(roadmap)

# Create Gantt chart
fig = px.timeline(
    df,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Task",
    title="CareConnect Roadmap Gantt Chart",
    labels={"Task": "Milestone"},
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_yaxes(autorange="reversed")  # Tasks from top to bottom
fig.update_layout(
    showlegend=False,
    title_font_size=28,
    xaxis_title="Date",
    yaxis_title="",
    plot_bgcolor="white",
    font=dict(size=16),
    margin=dict(l=20, r=20, t=80, b=20)
)

# Save as high-quality PNG
fig.write_image("roadmap_gantt.png", width=1400, height=800, scale=3)

print("Gantt chart saved as 'roadmap_gantt.png'.")
