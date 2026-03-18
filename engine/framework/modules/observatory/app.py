#!/usr/bin/env python3
"""
Scholar Observatory - Enhanced Dashboard
Research Mode: Current metrics, alerts, immediate actionables
Planning Mode: Long-term trends, strategic positioning, 5-year trajectory
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import json
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import networkx as nx

# Initialize app with Bootstrap theme (colorblind-friendly colors)
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Data paths
import sys
sys.path.insert(0, str(Path.home() / 'Local/virens/virens/engine/framework/modules/observatory'))
from core.config import config as _obs_config
OBSERVATORY_DIR = Path.home() / 'Local/virens/user1/observatory'
DATA_DIR = _obs_config.observatory_data
PROCESSED_DIR = DATA_DIR / 'processed'

# Colorblind-friendly color scheme (deuteranomaly-safe)
COLORS = {
    'primary': '#0077BB',      # Blue
    'secondary': '#EE7733',    # Orange
    'success': '#009988',      # Teal
    'warning': '#EE3377',      # Magenta
    'info': '#33BBEE',         # Cyan
    'neutral': '#BBBBBB',      # Gray
    'background': '#F8F9FA',
    'text': '#212529'
}

def load_analysis(analysis_type: str) -> dict:
    """Load latest analysis results"""
    file_path = PROCESSED_DIR / f"{analysis_type}_latest.json"
    
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return {}

def create_citation_velocity_timeline(citation_data: dict) -> go.Figure:
    """Timeline visualization of citation velocity"""
    if not citation_data:
        return go.Figure()
    
    fig = go.Figure()
    
    # Mock data for demonstration - replace with historical data
    dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
    citations = [citation_data.get('recent_citations', 0)] * 12  # Simplified
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=citations,
        mode='lines+markers',
        name='Citations',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Citation Velocity Timeline',
        xaxis_title='Date',
        yaxis_title='Citations per Month',
        template='plotly_white',
        height=350
    )
    
    return fig

def create_teaching_research_sankey(teaching_data: dict) -> go.Figure:
    """Sankey diagram showing teaching load → research productivity flow"""
    if not teaching_data or not teaching_data.get('teaching_research_correlation', {}).get('data_sufficient'):
        return go.Figure()
    
    correlation = teaching_data['teaching_research_correlation']
    
    # Simplified Sankey: Course types → Research outputs
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color=COLORS['neutral'], width=0.5),
            label=[
                'English 101',
                'Graduate Seminars',
                'Other Courses',
                'Publications',
                'Research Time'
            ],
            color=[COLORS['warning'], COLORS['success'], COLORS['info'], 
                   COLORS['primary'], COLORS['secondary']]
        ),
        link=dict(
            source=[0, 1, 2, 0, 1],  # Course types
            target=[3, 3, 3, 4, 4],  # Outputs
            value=[
                correlation.get('avg_pubs_with_english_101', 0),
                correlation.get('avg_pubs_without_english_101', 0),
                1,  # Other courses
                5,  # English 101 to research time
                8   # Grad seminars to research time
            ],
            color=[
                f"rgba(238, 51, 119, 0.4)",  # English 101
                f"rgba(0, 153, 136, 0.4)",   # Grad seminars
                f"rgba(51, 187, 238, 0.4)",  # Other
                f"rgba(238, 51, 119, 0.2)",  # English 101 impact
                f"rgba(0, 153, 136, 0.2)"    # Grad seminar impact
            ]
        )
    )])
    
    fig.update_layout(
        title='Teaching Load → Research Productivity Flow',
        height=400,
        font_size=12
    )
    
    return fig

def create_collaboration_network_map(network_data: dict) -> go.Figure:
    """Knowledge map of collaboration network"""
    if not network_data or not network_data.get('strategic_collaborators'):
        return go.Figure()
    
    # Create a simple network visualization
    collaborators = network_data['strategic_collaborators'][:10]  # Top 10
    
    # Build graph
    G = nx.Graph()
    G.add_node('You', size=30)
    
    for collab in collaborators:
        name = collab['name']
        weight = collab['collaboration_count']
        G.add_node(name, size=10 + weight * 2)
        G.add_edge('You', name, weight=weight)
    
    # Get layout
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color=COLORS['neutral']),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_size.append(G.nodes[node]['size'])
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition='top center',
        marker=dict(
            size=node_size,
            color=[COLORS['primary'] if n == 'You' else COLORS['secondary'] for n in G.nodes()],
            line=dict(width=2, color='white')
        )
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title='Collaboration Network Map',
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=450,
        template='plotly_white'
    )
    
    return fig

def create_promotion_timeline(citation_data: dict, teaching_data: dict) -> go.Figure:
    """5-year promotion timeline with milestones"""
    fig = go.Figure()
    
    # Current year to +5 years
    current_year = datetime.now().year
    years = list(range(current_year, current_year + 6))
    
    # Projected h-index trajectory
    current_h = citation_data.get('h_index', 0)
    projected_h = [current_h + i for i in range(6)]
    
    fig.add_trace(go.Scatter(
        x=years,
        y=projected_h,
        mode='lines+markers',
        name='H-Index Projection',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=10)
    ))
    
    # Add milestone markers
    milestones = [
        {'year': current_year + 1, 'event': 'Dept Review', 'y': current_h + 1},
        {'year': current_year + 3, 'event': 'Mid-Cycle Review', 'y': current_h + 3},
        {'year': current_year + 5, 'event': 'Full Prof Application', 'y': current_h + 5}
    ]
    
    for milestone in milestones:
        fig.add_annotation(
            x=milestone['year'],
            y=milestone['y'],
            text=milestone['event'],
            showarrow=True,
            arrowhead=2,
            arrowcolor=COLORS['warning'],
            ax=0,
            ay=-40
        )
    
    fig.update_layout(
        title='5-Year Promotion Timeline & Trajectory',
        xaxis_title='Year',
        yaxis_title='Projected H-Index',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_field_monitoring_dashboard(trend_data: dict) -> html.Div:
    """Dashboard showing journal and keyword monitoring"""
    if not trend_data:
        return html.Div("No trend data available")
    
    journal_activity = trend_data.get('journal_activity', {})
    keyword_trends = trend_data.get('keyword_trends', {})
    
    # Journal activity cards
    journal_cards = []
    for journal, count in journal_activity.items():
        journal_cards.append(
            dbc.Card([
                dbc.CardBody([
                    html.H6(journal, className="card-title"),
                    html.H3(str(count), className="text-primary"),
                    html.P("papers this month", className="text-muted small")
                ])
            ], className="mb-2")
        )
    
    # Keyword trends
    keyword_items = [
        html.Li([
            html.Strong(keyword),
            f": {count} mentions"
        ]) for keyword, count in list(keyword_trends.items())[:10]
    ]
    
    return html.Div([
        html.H4("Journal Monitoring"),
        dbc.Row([
            dbc.Col(card, width=3) for card in journal_cards[:4]
        ]),
        html.Hr(),
        html.H4("Trending Keywords"),
        html.Ul(keyword_items)
    ])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🔭 Scholar Observatory", className="mt-3"),
            html.P(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                   className="text-muted")
        ], width=8),
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button("Research Mode", id="mode-research", 
                          color="primary", className="mt-3"),
                dbc.Button("Planning Mode", id="mode-planning", 
                          color="secondary", outline=True, className="mt-3")
            ])
        ], width=4, className="text-end")
    ]),
    
    html.Hr(),
    
    # Hidden div to store current mode
    html.Div(id='current-mode', style={'display': 'none'}, children='research'),
    
    # Auto-refresh every 5 minutes
    dcc.Interval(id='interval-component', interval=300000, n_intervals=0),
    
    # Dynamic content area
    html.Div(id='dashboard-content')
    
], fluid=True)

@app.callback(
    [Output('mode-research', 'color'),
     Output('mode-research', 'outline'),
     Output('mode-planning', 'color'),
     Output('mode-planning', 'outline'),
     Output('current-mode', 'children')],
    [Input('mode-research', 'n_clicks'),
     Input('mode-planning', 'n_clicks')],
    [State('current-mode', 'children')]
)
def toggle_mode(research_clicks, planning_clicks, current_mode):
    """Handle mode toggle"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return 'primary', False, 'secondary', True, 'research'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'mode-research':
        return 'primary', False, 'secondary', True, 'research'
    else:
        return 'secondary', True, 'primary', False, 'planning'

@app.callback(
    Output('dashboard-content', 'children'),
    [Input('current-mode', 'children'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(mode, n_intervals):
    """Update dashboard based on mode"""
    # Load all analysis data
    citation_data = load_analysis('citation_analysis')
    trend_data = load_analysis('trend_analysis')
    network_data = load_analysis('network_analysis')
    teaching_data = load_analysis('teaching_analysis')
    
    if mode == 'research':
        return create_research_mode_view(
            citation_data, trend_data, network_data, teaching_data
        )
    else:
        return create_planning_mode_view(
            citation_data, trend_data, network_data, teaching_data
        )

def create_research_mode_view(citation_data, trend_data, network_data, teaching_data):
    """Research Mode: Current activity, alerts, immediate actions"""
    
    # Alert banner
    alerts = []
    if citation_data.get('burst_detected'):
        alerts.append(
            dbc.Alert([
                html.H4("🎉 Citation Burst Detected!", className="alert-heading"),
                html.P(f"Paper: {citation_data.get('burst_paper', 'Unknown')}")
            ], color="success")
        )
    
    # Citation velocity indicator
    velocity = citation_data.get('citation_velocity', 0)
    velocity_color = 'success' if velocity > 0 else 'warning' if velocity == 0 else 'danger'
    
    return html.Div([
        # Alerts
        html.Div(alerts) if alerts else None,
        
        # Key metrics row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Citations This Week"),
                        html.H2(citation_data.get('recent_citations', 0)),
                        html.P(f"Velocity: {velocity:+d}", 
                               className=f"text-{velocity_color}")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("H-Index"),
                        html.H2(citation_data.get('h_index', 0)),
                        html.P("Current", className="text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Collaborators"),
                        html.H2(network_data.get('total_collaborators', 0)),
                        html.P("Active", className="text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Teaching Load"),
                        html.H2(teaching_data.get('course_distribution', {}).get('total_courses', 0)),
                        html.P("This semester", className="text-muted")
                    ])
                ])
            ], width=3)
        ], className="mb-4"),
        
        # Main visualization
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=create_citation_velocity_timeline(citation_data))
            ], width=12)
        ], className="mb-4"),
        
        # Field monitoring
        create_field_monitoring_dashboard(trend_data)
    ])

def create_planning_mode_view(citation_data, trend_data, network_data, teaching_data):
    """Planning Mode: Long-term trends, strategic positioning, trajectory"""
    
    return html.Div([
        # 5-year timeline
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=create_promotion_timeline(citation_data, teaching_data))
            ], width=12)
        ], className="mb-4"),
        
        # Teaching-Research Sankey
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=create_teaching_research_sankey(teaching_data))
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=create_collaboration_network_map(network_data))
            ], width=6)
        ], className="mb-4"),
        
        # Strategic recommendations
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("Strategic Recommendations")),
                    dbc.CardBody([
                        html.Ul([
                            html.Li(rec) for rec in 
                            teaching_data.get('recommendations', [])
                        ])
                    ])
                ])
            ])
        ])
    ])

if __name__ == '__main__':
    print("🔭 Scholar Observatory starting...")
    print("   Research Mode: Current activity & alerts")
    print("   Planning Mode: Strategic trajectory & long-term view")
    print("")
    print("   Archive: http://localhost:5555")
    print("   Network: http://archive.local:5555")
    print("")

    app.run(host="0.0.0.0", port=5555, debug=False)
