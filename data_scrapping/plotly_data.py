from PIL import Image
import pandas as pd
import plotly.graph_objects as go
from math import ceil
import numpy as np

# prepare data

paintings = pd.read_excel('paintings.xlsx')
coordinates = pd.read_excel('coordinates.xlsx')

dashboard = pd.merge(paintings.reset_index(), coordinates.reset_index(), on=["Museum"], how="inner").set_index( \
    ["index_x"]).drop(['Unnamed: 0_x', 'index_y', 'Unnamed: 0_y'], axis=1).sort_index()

dashboard["x"] = np.nan
dashboard["y"] = np.nan

for museum in coordinates["Museum"]:
    temp = dashboard[(dashboard['Museum'] == str(museum))]
    recs = len(temp)
    rows, cols = ceil(recs/5), 5
    x, y, ids = [], [], temp.index.tolist()
    for i in range(recs):
        col = (i+1) % 5 if (i+1) % 5 != 0 else 5
        row = ceil((i+1) / 5)
        dashboard.at[ids[i], 'x'] = col
        dashboard.at[ids[i], 'y'] = row

dashboard.to_excel('dashboard.xlsx')

# construct plotly graphs -> html

dashboard = pd.read_excel('dashboard.xlsx')

for museum in coordinates["Museum"]:
    df_gallery = dashboard[(dashboard['Museum'] == str(museum))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode='markers', x=df_gallery['x'], y=df_gallery['y'], name="Year<br>Title", \
                         customdata = np.stack((df_gallery['Year'], df_gallery['Title']), axis=-1), \
                         hovertemplate = ('%{customdata[0]}<br>'+ '%{customdata[1]}<br>'), \
                         marker=dict(size=20), showlegend=False))
    fig.update_traces(marker_color="rgba(0,0,0,0)", marker={'size': 30})
    for i in range(len(df_gallery)):
        img = f"paintings/{df_gallery.iloc[i]['index_x']}.png"
        fig.add_layout_image(
            dict(
                source=Image.open(img), xref="x", yref="y", sizex=0.9, sizey=0.9,
                xanchor="center",
                yanchor="middle",
                x=df_gallery.iloc[i]['x'],
                y=df_gallery.iloc[i]['y'],
                sizing="contain",
                opacity=0.8,
                layer="above"
            )
        )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), yaxis_range=[0, max(df_gallery['y'])+1], xaxis_range=[0, max(df_gallery['x'])+1], \
                      title_text=f"{museum}<br>{df_gallery.iloc[0]['Country']}", title_x=0.5, showlegend=False)

    fig.write_html("static/"+str(museum)+".html")
