import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# CSV rechtstreeks van GitHub lezen
url = "url = "https://raw.githubusercontent.com/GO-atheneum-De-Tandem/intro-dash-daq-Pimguin77/refs/heads/master/immigrati_00003_stranieri_seriecittaprovenienza%20(1).csv""

df = pd.read_csv(
    url,
    sep=";",
    encoding="latin-1"
)

# Kolom numeriek maken
df["Numero Immigrati"] = pd.to_numeric(
    df["Numero Immigrati"],
    errors="coerce"
)

# Pivot tabel maken
df_pivot = df.pivot_table(
    index="Anno",
    columns="Cittadinanza",
    values="Numero Immigrati",
    aggfunc="sum",
    fill_value=0
)

# Jaren ophalen
years = df_pivot.index.tolist()

# Dash app maken
app = Dash(__name__)

# Layout
app.layout = html.Div([

    html.H1("Aantal immigranten per land"),

    dcc.Slider(
        id="year-slider",
        min=min(years),
        max=max(years),
        step=1,
        value=min(years),
        marks={
            int(year): str(year)
            for year in years[::2]
        }
    ),

    dcc.Graph(id="bar-chart")

])

# Callback
@app.callback(
    Output("bar-chart", "figure"),
    Input("year-slider", "value")
)

def update_graph(selected_year):

    data = (
        df_pivot.loc[selected_year]
        .sort_values(ascending=False)
        .head(10)
    )

    fig = px.bar(
        x=data.values,
        y=data.index,
        orientation="h",
        color=data.index,
        text=data.values,
        title=f"Aantal immigranten - {selected_year}"
    )

    fig.update_layout(
        xaxis_title="Aantal immigranten",
        yaxis_title="Land",
        yaxis=dict(autorange="reversed")
    )

    return fig

# App starten
if __name__ == "__main__":
    app.run(debug=True)
