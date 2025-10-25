import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

# Load dataset
df = px.data.gapminder()

# Initialize app
app = dash.Dash(__name__)

# --- Chart Functions ---
def create_population_chart(continent, year):
    dff = df[(df['continent'] == continent) & (df['year'] == year)]
    fig = px.bar(
        dff,
        x='country',
        y='pop',
        title=f"Population in {continent} ({year})",
        color='country',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0A0F24',
        plot_bgcolor='#0A0F24',
        font=dict(color='#00FFFF', family='Orbitron, sans-serif')
    )
    return fig


def create_gdp_chart(continent, year):
    dff = df[(df['continent'] == continent) & (df['year'] == year)]
    fig = px.scatter(
        dff,
        x='gdpPercap',
        y='lifeExp',
        size='pop',
        color='country',
        title=f"GDP vs Life Expectancy ({continent}, {year})",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        size_max=60
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0A0F24',
        plot_bgcolor='#0A0F24',
        font=dict(color='#00FFFF', family='Orbitron, sans-serif')
    )
    return fig


def create_lifeexp_chart(continent, year):
    dff = df[(df['continent'] == continent) & (df['year'] == year)]
    fig = px.line(
        dff,
        x='country',
        y='lifeExp',
        title=f"Life Expectancy in {continent} ({year})",
        color='country',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0A0F24',
        plot_bgcolor='#0A0F24',
        font=dict(color='#00FFFF', family='Orbitron, sans-serif')
    )
    return fig


def create_world_map(year):
    dff = df[df['year'] == year]
    fig = px.scatter_geo(
        dff,
        locations="iso_alpha",
        color="lifeExp",
        hover_name="country",
        size="pop",
        projection="natural earth",
        title=f"🌍 World Map of Population & Life Expectancy ({year})",
        color_continuous_scale="Tealgrn"
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0A0F24',
        font=dict(color='#00FFFF', family='Orbitron, sans-serif')
    )
    return fig


# --- Layout ---
app.layout = html.Div([
    html.H1(
        "🌌 Futuristic Global Insights Dashboard 🌍",
        style={'textAlign': 'center', 'color': '#00FFFF', 'fontFamily': 'Orbitron, sans-serif'}
    ),

    html.Div([
        html.Label("Select Continent:", style={'color': '#00FFFF'}),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': c, 'value': c} for c in df['continent'].unique()],
            value='Asia',
            clearable=False,
            style={'backgroundColor': '#111', 'color': '#00FFFF'}
        ),
    ], style={'width': '50%', 'margin': 'auto', 'padding': '10px'}),

    html.Div([
        html.Label("Select Year:", style={'color': '#00FFFF'}),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            step=5,
            value=df['year'].max(),
            marks={str(year): str(year) for year in df['year'].unique()},
        ),
    ], style={'width': '80%', 'margin': 'auto', 'padding': '20px'}),

    # Tabs for navigation
    dcc.Tabs(id='tabs', value='tab-data', children=[
        dcc.Tab(label='📊 Data Table', value='tab-data', style={'backgroundColor': '#0A0F24', 'color': '#00FFFF'}),
        dcc.Tab(label='👥 Population', value='tab-population', style={'backgroundColor': '#0A0F24', 'color': '#00FFFF'}),
        dcc.Tab(label='💰 GDP', value='tab-gdp', style={'backgroundColor': '#0A0F24', 'color': '#00FFFF'}),
        dcc.Tab(label='❤️ Life Expectancy', value='tab-lifeexp', style={'backgroundColor': '#0A0F24', 'color': '#00FFFF'}),
        dcc.Tab(label='🌍 World Map', value='tab-map', style={'backgroundColor': '#0A0F24', 'color': '#00FFFF'}),
    ], style={'fontFamily': 'Orbitron, sans-serif', 'borderBottom': '2px solid #00FFFF'}),

    html.Div(id='tabs-content', style={'padding': '20px'})
], style={'backgroundColor': '#02040F', 'minHeight': '100vh', 'padding': '30px'})


# --- Callback for Tabs ---
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    Input('continent-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_tab_content(tab, continent, year):
    dff = df[(df['continent'] == continent) & (df['year'] == year)]

    if tab == 'tab-data':
        return dash_table.DataTable(
            data=dff.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in dff.columns],
            style_table={'overflowX': 'auto', 'backgroundColor': '#0A0F24'},
            style_header={'backgroundColor': '#00FFFF', 'color': '#0A0F24', 'fontWeight': 'bold'},
            style_cell={'backgroundColor': '#0A0F24', 'color': '#00FFFF', 'fontFamily': 'Orbitron, sans-serif'},
            page_size=10
        )

    elif tab == 'tab-population':
        return dcc.Graph(figure=create_population_chart(continent, year))

    elif tab == 'tab-gdp':
        return dcc.Graph(figure=create_gdp_chart(continent, year))

    elif tab == 'tab-lifeexp':
        return dcc.Graph(figure=create_lifeexp_chart(continent, year))

    elif tab == 'tab-map':
        return dcc.Graph(figure=create_world_map(year))

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)

