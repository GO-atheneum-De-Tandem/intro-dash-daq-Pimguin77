import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# =========================================================
# CSV rechtstreeks van GitHub lezen
# =========================================================

url = "https://raw.githubusercontent.com/USERNAME/REPOSITORY/main/immigrati.csv"

df = pd.read_csv(
    url,
    sep=";",
    encoding="latin-1"
)

# =========================================================
# Kolom numeriek maken
# =========================================================

df["Numero Immigrati"] = pd.to_numeric(
    df["Numero Immigrati"],
    errors="coerce"
)

# =========================================================
# Pivot tabel maken
# =========================================================

df_pivot = df.pivot_table(
    index="Anno",
    columns="Cittadinanza",
    values="Numero Immigrati",
    aggfunc="sum",
    fill_value=0
)

# =========================================================
# Lijst van jaren ophalen
# =========================================================

years = df_pivot.index.tolist()

# =========================================================
# Dash app maken
# =========================================================

app = Dash(__name__)

# =========================================================
# Layout van dashboard
# =========================================================

app.layout = html.Div([

    # Titel
    html.H1(
        "Aantal immigranten per land",
        style={
            "textAlign": "center"
        }
    ),

    # Jaar slider
    dcc.Slider(
        id="year-slider",

        min=min(years),
        max=max(years),

        step=1,

        value=min(years),

        # Labels op slider
        marks={
            int(year): str(year)
            for year in years[::2]
        }
    ),

    # Grafiek
    dcc.Graph(
        id="bar-chart"
    )

])

# =========================================================
# Callback voor interactieve grafiek
# =========================================================

@app.callback(
    Output("bar-chart", "figure"),
    Input("year-slider", "value")
)

def update_graph(selected_year):

    # Data selecteren voor gekozen jaar
    data = (
        df_pivot.loc[selected_year]
        .sort_values(ascending=False)
        .head(10)
    )

    # Plotly bar chart maken
    fig = px.bar(

        x=data.values,
        y=data.index,

        orientation="h",

        # Verschillende kleuren
        color=data.index,

        # Waarden tonen op bars
        text=data.values,

        # Titel
        title=f"Aantal immigranten - {selected_year}"
    )

    # Layout aanpassen
    fig.update_layout(

        xaxis_title="Aantal immigranten",
        yaxis_title="Land",

        # Grootste bovenaan
        yaxis=dict(
            autorange="reversed"
        )
    )

    return fig

# =========================================================
# App starten
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
