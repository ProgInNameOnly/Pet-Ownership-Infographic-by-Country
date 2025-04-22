import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import base64
import os

# Load dataset
df = pd.read_csv("pet_ownership_data_updated.csv")

# Compute average ownership
avg_df = df[['Dog', 'Cat', 'Fish', 'Bird']].mean().reset_index()
avg_df.columns = ['Pet', 'AveragePercentage']
avg_df['AveragePercentage'] = avg_df['AveragePercentage'].round(1)

# Copy country-level data
country_df = df.copy()

# Image encoding function
def encode_image(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    with open(file_path, 'rb') as f:
        data = f.read()
    mime = 'image/png' if ext == '.png' else 'image/jpeg'
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

# Load images from assets/
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
pet_icons = {pet: encode_image(os.path.join(ASSETS_DIR, f"{pet.lower()}.jpg")) for pet in avg_df['Pet']}

flag_map = {}
for country in df['Country']:
    fname = country.replace(' ', '_') + '.png'
    path = os.path.join(ASSETS_DIR, fname)
    flag_map[country] = encode_image(path) if os.path.exists(path) else None

# Initialize app
def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    app.title = "Pet Ownership Infographic"

    pet_options = [{'label': pet, 'value': pet} for pet in avg_df['Pet']]

    def create_avg_chart():
        fig = px.bar(
            avg_df,
            x='Pet',
            y='AveragePercentage',
            text='AveragePercentage',
            title='Average Pet Ownership by Type'
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(
            yaxis_title='Average Ownership (%)',
            xaxis_title='Pet Type',
            height=450,
            margin=dict(t=80, b=40, l=60, r=20),
            title_x=0.5,
            yaxis=dict(range=[0, avg_df['AveragePercentage'].max() + 10])  # Add space above the tallest bar
            )
        return fig

    app.layout = dbc.Container([
        html.H1('Pet Ownership Infographic', className='my-4 text-center'),

        html.H3("Average Ownership by Pet", className='text-center my-3'),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardImg(src=pet_icons[pet], top=True, style={'height':'100px','objectFit':'contain'}),
                    dbc.CardBody([
                        html.H5(pet, className='card-title text-center'),
                        html.P(f"{pct}% avg ownership", className='text-center')
                    ])
                ], className='m-2', style={'width': '160px'}),
                xs=6, sm=4, md=3, lg=2
            )
            for pet, pct in zip(avg_df['Pet'], avg_df['AveragePercentage'])
        ], justify='center'),

        html.Hr(),

        html.H3("Compare Countries", className='text-center my-3'),
        dbc.Row([
            dbc.Col(dcc.Dropdown(id='pet-select', options=pet_options, value=avg_df['Pet'][0], clearable=False), width=6)
        ], justify='center'),

        html.Div(id='top-country-summary', className='text-center my-2'),

        html.Div(
            id='country-row-wrapper',
            children=dbc.Row(id='country-row', className="flex-nowrap"),
            style={"overflowX": "auto", "whiteSpace": "nowrap", "paddingBottom": "1rem"}
        ),

        html.Hr(),

        html.H3("Pet Ownership by Country", className='text-center my-3'),
        dbc.Row(dbc.Col(dcc.Graph(id='choropleth-map'), width=12)),

        html.Hr(),

        html.H3("Overall Pet Ownership Comparison", className='text-center my-3'),
        dbc.Row(dbc.Col(dcc.Graph(figure=create_avg_chart()), width=10), justify='center')

    ], fluid=True)

    # Callback for cards and summary
    @app.callback(
        Output('country-row', 'children'),
        Output('top-country-summary', 'children'),
        Input('pet-select', 'value')
    )
    def update_country_cards(selected_pet):
        cards = []
        for _, row in country_df.iterrows():
            country = row['Country']
            val = int(round(row[selected_pet]))
            img_src = flag_map.get(country) or pet_icons[selected_pet]

            cards.append(
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(src=img_src, top=True, style={'height':'80px','objectFit':'contain'}),
                        dbc.CardBody([
                            html.H6(country, className='card-title text-center',
                                    style={
                                        'fontSize': '0.85rem',
                                        'whiteSpace': 'normal',
                                        'wordWrap': 'break-word',
                                        'lineHeight': '1.2'
                                    }),
                            html.P(f"{val}% {selected_pet} ownership", className='text-center',
                                   style={
                                       'fontSize': '0.8rem',
                                       'marginBottom': '0',
                                       'whiteSpace': 'normal',
                                       'wordWrap': 'break-word'
                                   })
                        ])
                    ], className='m-2', style={'width': '170px', 'minHeight': '200px', 'padding': '5px'}),
                    xs="auto"
                )
            )

        top_country = country_df[['Country', selected_pet]].sort_values(by=selected_pet, ascending=False).iloc[0]
        summary_text = html.Div([
            "🏆 ",
            html.B(top_country['Country']),
            f" has the highest {selected_pet.lower()} ownership at ",
            html.B(f"{int(top_country[selected_pet])}%"),
            "."
        ])
        return cards, summary_text

    # Callback for map
    @app.callback(
        Output('choropleth-map', 'figure'),
        Input('pet-select', 'value')
    )
    def update_map(selected_pet):
        fig = px.choropleth(
            country_df,
            locations="Country",
            locationmode="country names",
            color=selected_pet,
            color_continuous_scale="Blues",
            title=f"{selected_pet} Ownership by Country (%)"
        )
        fig.update_layout(title_x=0.5)
        return fig

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
