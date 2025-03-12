import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

LOG_FILE = "email_log.csv"

# ✅ Load Email Data
def load_data():
    try:
        return pd.read_csv(LOG_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Subject", "Sender", "Folder", "Score"])

# ✅ Create Dashboard
app = dash.Dash(__name__)

def generate_folder_chart(data):
    folder_counts = data["Folder"].value_counts().reset_index()
    folder_counts.columns = ["Folder", "Count"]
    return px.pie(folder_counts, values="Count", names="Folder", title="📂 Email Distribution by Folder")

def generate_score_chart(data):
    return px.histogram(data, x="Score", nbins=10, title="📊 Email Priority Scores")

app.layout = html.Div(children=[
    html.H1("📬 AI Email Sorting Dashboard"),
    
    html.Div([
        html.H3("📂 Email Distribution"),
        dcc.Graph(id="folder-chart"),
    ]),
    
    html.Div([
        html.H3("📊 Email Priority Scores"),
        dcc.Graph(id="score-chart"),
    ]),

    html.Div([
        html.H3("📧 Recent Classified Emails"),
        dcc.Graph(id="latest-emails"),
    ]),
])

@app.callback(
    [dash.dependencies.Output("folder-chart", "figure"),
     dash.dependencies.Output("score-chart", "figure"),
     dash.dependencies.Output("latest-emails", "figure")],
    [dash.dependencies.Input("folder-chart", "id")]
)
def update_dashboard(_):
    data = load_data()

    folder_chart = generate_folder_chart(data)
    score_chart = generate_score_chart(data)

    latest_emails = data.sort_values(by="Score", ascending=False).head(10)
    latest_emails_fig = px.bar(
        latest_emails,
        x="Score",
        y="Subject",
        color="Folder",
        title="🔍 Recent Emails Sorted"
    )

    return folder_chart, score_chart, latest_emails_fig

if __name__ == "__main__":
    app.run_server(debug=True)
