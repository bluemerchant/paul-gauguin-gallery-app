from flask import Flask, render_template
import folium
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    coordinates = pd.read_excel('coordinates.xlsx')
    grouped = coordinates.groupby('Country')

    groups = []

    m = folium.Map(location=(25, 100), min_zoom=2, width=1200, height=500, control_scale=True, zoom_start=2, max_bounds=True)

    for group_name, group_data in grouped:
        groups.append(folium.FeatureGroup(f'{group_name} ({len(group_data)})', show=False))
        for i in range(len(group_data)):
            html = """
            <iframe src=\"""" + f"static/{group_data.iloc[i]['Museum']}.html" + """\" width="500" height="300" frameborder="0">
            """

            popup = folium.Popup(folium.Html(html, script=True))
            folium.Marker([group_data.iloc[i]['Latitude'], group_data.iloc[i]['Longitude']], \
                          popup=popup, icon=folium.Icon(icon='museum', prefix='fa')).add_to(groups[-1])
        groups[-1].add_to(m)

    folium.LayerControl().add_to(m)
    m.save('templates/map.html')
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
