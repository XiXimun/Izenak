# raw geojson files frm: https://www.data.gouv.fr/fr/datasets/carte-des-departements-2-1/

import pandas as pd
import plotly.express as px
import json
import numpy as np
from geojson import dump


file = './data/carte-de-france-et-outre-mers.json'

with open(file) as f:
    geojson = json.load(f)

# refactor dict
for feature in geojson['features']:
    if 'Code Dept' in feature['properties']:
        code = feature['properties'].pop('Code Dept')
        str_code = str(code)
        if str_code[0] == '0':
            str_code = str_code[1:]
        feature['properties']['code'] = str_code

# merge 2 corsican departments
for feature in geojson['features']:
    if 'code' in feature['properties']:
        if feature['properties']['code'] == '2A':
            haute_corse = feature
        if feature['properties']['code'] == '2B':
            corse_du_sud = feature

corse = {
    "type": "Feature",
    "geometry": {
        "type": "MultiPolygon",
        "coordinates": [haute_corse['geometry']['coordinates'], corse_du_sud['geometry']['coordinates']]
    },
    "properties": {
        "D\u00e9partement": "CORSE",
        "R\u00e9gion": "CORSE",
        "Territoire": "FRANCE DOM",
        "code": "20"
    },
    "id": "020"
}

geojson['features'].remove(haute_corse)
geojson['features'].remove(corse_du_sud)
geojson['features'].append(corse)

df = pd.DataFrame([x['properties'] for x in geojson['features'] if 'Département' in x['properties']])
df['rand'] = np.random.randint(0, 10, df.shape[0]).astype('str')
print(df)

fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    featureidkey='properties.code',
    locations='code',
    color='rand',
    center={"lat": 46.5, "lon": 2.4},
    zoom=4.4,
    mapbox_style="white-bg",
    opacity=1.,
    hover_name='Département'
    # color_continuous_scale=color_continuous_scale
)

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
)

fig.show()

with open('./data/carte-de-france-et-outre-mers-new.geojson', 'w') as f:
   dump(geojson, f)
