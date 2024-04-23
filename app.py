# Omisha Mondal om4kud
from dash import Dash, html, dcc, dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Read in the data
data = pd.read_csv('data.csv')

# Uses a stylesheet
stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/quartz/bootstrap.min.css']

app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# Functions for the range sliders (price)

# first range slider
def create_pm():
    return {str(price): {'label': str(price), 'style': {'color': 'black'}} for price in range(int(data['Price'].min()), int(data['Price'].max()), 100)}

# second range slider
def create_marks():
    return {str(price): {'label': str(price), 'style': {'color': 'black'}} for price in range(int(data['Price'].min()), int(data['Price'].max()), 100)}

# Make the layout
app.layout = html.Div(style={'backgroundColor': 'rgba(0,0,0,0)', 'padding': '20px'}, children=[
    html.H1("Day Trader Graphs", style={'textAlign': 'center', 'marginBottom': '20px'}), 
    
    # Top row - this will have the Best / Worst Stocks
    html.Div([
        html.Div([
            html.H2("", id='best-worst-title', style={'textAlign': 'center', 'marginBottom': '10px', 'color': 'green'}),
            dcc.RadioItems(
                id='radio-best-worst', 
                options=[
                    {'label': 'Best Stocks', 'value': 'best'}, # When best radio button is clicked, best will be shown with green title
                    {'label': 'Worst Stocks', 'value': 'worst'}     # When worst radio button is clicked, worst will be shown with red title
                ],
                value='best',
                labelStyle={'display': 'block'}
            ),
        ], style={'marginBottom': '20px', 'textAlign': 'center'}), # puts radio buttons in center
    ], style={'margin': 'auto', 'textAlign': 'center', 'marginBottom': '20px', 'width': '90%'}),
    
    # top row data table for best / worst
    html.Div([
        
        # Data table - translucent
        html.Div([
            dash_table.DataTable(
                id='top-stocks-table',
                columns=[
                    {"name": i, "id": i} for i in data.columns
                ],
                style_data={ # actual data will be black
                    'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                    'color': 'black'
                },
                style_header={
                    'backgroundColor': 'rgba(0, 0, 0, 0.7)', # sets opacity 
                    'fontWeight': 'bold'
                },
                style_cell_conditional=[ #keeps text within the cells
                    {
                        'if': {'column_id': 'Symbol'},
                        'textAlign': 'center'
                    }
                ]
            )
        ], style={'width': '100%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '10px'}), # makes sure to take up entire width of pg
        
    ], style={'margin': 'auto', 'textAlign': 'center', 'marginBottom': '20px', 'width': '90%'}), # sets this apart from rest

    # middle row
    html.Div([
        
        # Bubble Plot of Market Cap vs Price vs PE Ratio
        html.Div([
            dcc.Dropdown(
                id='company-symb',
                options=[
                    {'label': symbol, 'value': symbol} for symbol in data['Symbol'].unique()
                ],
                value=[symbol for symbol in data['Symbol'].unique()[:3]], # default selection is first 3 symbols
                multi=True,
                style={'color': 'black', 'marginBottom': '10px'}
            ),
            dcc.Graph(id='bubble-plot'),
        ], style={'width': '50%', 'display': 'inline-block', 'margin': 'auto', 'textAlign': 'center'}),
        
        # PE Ratio Graph with Price Range Slider
        html.Div([
            dcc.RangeSlider(
                id='price-range-slider',
                min=data['Price'].min(),
                max=data['Price'].max(),
                step=0.1,
                value=[data['Price'].min(), data['Price'].max()], 
                marks=create_pm()  # Uses a function to create marks on the range slider
            ),
            dcc.Graph(id='pe-ratio-graph')
        ], style={'width': '50%', 'display': 'inline-block', 'margin': 'auto', 'textAlign': 'center'}),
        
    ], style={'margin': 'auto', 'textAlign': 'center', 'marginBottom': '20px', 'width': '90%'}), 

    # bottom row
    html.Div([
        
        # Grouped bar graph Price, Change, and PE Ratio
        html.Div([
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label': name, 'value': name} for name in data['Name'].unique()],
                # Default names of 1st, 6th, and last stocks hence why using .unique
                value=[
                    data['Name'].unique()[0],
                    data['Name'].unique()[5],
                    data['Name'].unique()[-1]
                ],  
                multi=True,  # Allows for multiple selections
                style={'color': 'black', 'marginBottom': '10px'}  # Make text color black so it is visible
            ),
            dcc.Graph(id='grouped-bar-chart')
        ], style={'width': '50%', 'display': 'inline-block', 'margin': 'auto', 'textAlign': 'center'}), # want 50/50 here so graphs are side by side
        
        # Scatter plot Change vs. PE Ratio with Price Range Slider
        html.Div([
            dcc.RangeSlider(
                id='price-range-slider-scatter',
                min=data['Price'].min(),
                max=data['Price'].max(),
                step=0.1,
                value=[data['Price'].min(), data['Price'].max()],
                marks=create_marks() # Uses a function to create marks on the range slider, similar to above
            ),
            dcc.Graph(id='scatter-plot')
        ], style={'width': '50%', 'display': 'inline-block', 'margin': 'auto', 'textAlign': 'center'}),
    ], style={'margin': 'auto', 'textAlign': 'center', 'marginBottom': '20px', 'width': '90%'})
])


# Radio Button Title Callbacks
@app.callback(
    [Output('best-worst-title', 'children'), # children element https://dash.plotly.com/dash-ag-grid/column-groups
     Output('best-worst-title', 'style')],
    [Input('radio-best-worst', 'value')]
)
def update_title(value):
    title_text = "Best Stocks of the Day"
    title_color = {'textAlign': 'center', 'marginBottom': '10px', 'color': 'rgb(0, 255, 0)'} # using rgb for a more vibrant shade of green

    if value == 'worst':
        title_text = "Worst Stocks of the Day"
        title_color['color'] = 'red' # shows red when it is the worst stocks

    return title_text, title_color

# Stocks Callbacks
@app.callback(
    Output('top-stocks-table', 'data'),
    [Input('radio-best-worst', 'value')]
)
# In order to determine whether a stock pick is good or bad, multiply price times market cap. These often tell how good the stock is doing.
def update_stocks_table(value):
    # If value is best: choose top 5 stocks based on highest multiplied score 
    if value == 'best':
        data['pmc'] = data['Price'] * data['Market Cap']
        temp = data.sort_values(by='pmc', ascending=False).head(5) # creates a temp column for the values
        temp = temp.drop(columns=['pmc'])  # drops temp column

    # If value is worst: choose top 5 stocks based on highest multiplied score
    elif value == 'worst':
        # Select the bottom 5 stocks based on a combined score of price and market cap
        data['pmc'] = data['Price'] * data['Market Cap']
        temp = data.sort_values(by='pmc', ascending=True).head(5) # creates a temp column for the values
        temp = temp.drop(columns=['pmc'])  # drops temp column
    
    return temp.to_dict('records')


# Bubble plot callback
@app.callback(
    Output('bubble-plot', 'figure'),
    [Input('company-symb', 'value')]
)
def update_bubble_plot(chose_symb):
    filtered_data = data[data['Symbol'].isin(chose_symb)]
    fig = px.scatter(filtered_data, x='Price', y='Market Cap', size='PE Ratio',
                     color='PE Ratio', hover_name='Symbol', title='Market Cap vs Price by PE Ratio Bubble Plot')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')  # make the background transparent
    return fig


# Histogram callback
@app.callback(
    Output('pe-ratio-graph', 'figure'),
    [Input('price-range-slider', 'value')]
)
def update_histogram(price_range):
    filtered_data = data[(data['Price'] >= price_range[0]) & (data['Price'] <= price_range[1])]
    fig = px.histogram(filtered_data, x='PE Ratio', title='Distribution of PE Ratio by Price')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')  # make the background transparent
    return fig


# Groouped bar chart callback
@app.callback(
    Output('grouped-bar-chart', 'figure'),
    [Input('name-dropdown', 'value')]
)
def update_grouped_bar_graph(chose_names):
    filtered_data = data[data['Name'].isin(chose_names)]
    fig = px.bar(filtered_data, x='Price', y='Change', color='Market Cap',
                 barmode='group', labels={'Price': 'Price', 'Change': 'Change', 'Market Cap': 'Market Cap'},
                 title='Price, Change, and Market Cap Bar Chart')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')  # make the background transparent
    return fig

# Scatter plot callback
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('price-range-slider-scatter', 'value')]
)
def update_scatter_plot(price_range):
    filtered_data = data[(data['Price'] >= price_range[0]) & (data['Price'] <= price_range[1])]
    fig = px.scatter(filtered_data, x='Change', y='PE Ratio', color='Price',
                     hover_name='Symbol', title='Change vs PE Ratio by Price')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')  # make the background transparent
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
