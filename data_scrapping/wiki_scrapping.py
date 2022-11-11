import requests
from PIL import Image
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
import Levenshtein as lev

# get table with paintings data and clean up data

url = 'https://en.wikipedia.org/wiki/List_of_paintings_by_Paul_Gauguin'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', {'class': "wikitable"})

URL = []
for table in tables:
    temp = table.find_all('a')
    for pic in temp:
        image = pic.find('img')
        if image is not None:
            img = image.get('src')
            URL.append('https:' + img.replace('100px', '350px'))


URL.insert(199, 'nan')

df = pd.DataFrame()
for table in tables:
    temp = pd.read_html(str(table))
    temp = pd.DataFrame(temp[0])
    df = df.append(temp)

df = df.drop(['WIN', 'Picture'], axis=1)
df['URL'] = URL
df = df.astype(str)
df['Museum'] = df['Museum'].apply(lambda a: a[:a.find('[')] + a[a.find(']')+1:] if a.find('[') != -1 else a)
df['Year'] = df['Year'].apply(lambda x: 'nan' if x == '?' else x)
df['Title'] = df['Title'].apply(lambda x: x.replace(' (', r'<br>('))
df['Museum'] = df['Museum'].apply(lambda x: 'Private collection' if (x.find('Private collection') != -1 or \
                                                                     x.find('Private Collection') != -1 or x=='nan' or \
                                                                     x.find('Pierre Rosenberg') != -1 or \
                                                                     x.find('Stavros Niarchos') != -1) else x.strip())
df['Museum'] = df['Museum'].apply(lambda x: x.replace('Currently in ', '') if x.find('Currently in') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: 'Artizon Museum, Tokyo' if x.find('Bridgestone Museum of Art, Tokyo') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: 'Honolulu Museum of Art' if x.find('Honolulu Academy of Arts, Hawaii') != -1 else x)

for s1 in df['Museum']:
    for s2 in df['Museum']:
        diff = lev.jaro(s1, s2)
        if diff >= 0.90 and diff < 1:
            df['Museum'] = df['Museum'].replace(s1, s2)

df['Museum'] = df['Museum'].apply(lambda x: 'Smith College, Northampton, MA' if x.find('Smith College Museum of Art') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: 'National Gallery (Norway), Oslo' if (x.find('National Gallery of Norway, Oslo') != -1 or x.find('National Gallery, Oslo') != -1) else x)
df['Museum'] = df['Museum'].apply(lambda x: 'Ordrupgaard, Denmark' if x.find('Ordrupgaard') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: 'Fogg Museum, Cambridge, MA' if x.find('Fogg') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: 'Barber Institute of Fine Arts, Birmingham' if x.find('Barber') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: 'Mohamed Mahmoud Khalil, Egypt' if x.find('Mohamed Mahmoud Khalil') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Musée d'Art moderne et contemporain de Strasbourg" if x.find('Strasbourg') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Laing Art Gallery" if x.find('Laing') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "National Museum of Western Art, Tokyo" if x.find('The National Museum of Western Art') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Seiji Togo Museum of Art, Tokyo" if x.find('Seiji Togo') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Clark Art Institute, MA" if x.find('Clark Art') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Tehran Museum, Laleh Park" if x.find('Tehran') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "The Phillips Collection Museum" if x.find('Phillips') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Marlborough Gallery" if x.find('Marlborough') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Stiftung Sammlung E. G. Bührle, Zurich" if x.find('Bührle') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Springfield Museum, OH" if x.find('Springfield') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Fukushima Prefectural Museum" if x.find('Fukushima') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "The Courtauld Gallery" if x.find('Courtauld') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Baltimore Museum of Art, MD" if x.find('Baltimore') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Barnes Foundation, PA" if x.find('Barnes') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Musée Malraux" if x.find('Malraux') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Rennes Art Museum" if x.find('Rennes') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Pont-Aven Museum" if x.find('Pont-Aven') != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "d'Orléans Museum" if x.find("d'Orléans") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "La Boverie, Belgium" if x.find("Liège") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Quimper Arts Museum" if x.find("Quimper") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Cleveland Museum of Art" if x.find("Cleveland Museum of Art") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Kunstmuseum Basel" if x.find("Kunstmuseum Basel") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Museum of Grenoble" if x.find("Museum of Grenoble") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Ny Carlsberg Glyptotek" if x.find("Ny Carlsberg Glyptotek") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Pushkin Museum, Moscow" if x.find("Pushkin Museum") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Minneapolis Institute of Art" if x.find("Minneapolis Institute of Art") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Musée d'Orsay, Paris" if x.find("Musée d'Orsay") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Thyssen-Bornemisza Museum, Madrid" if x.find("Museo Thyssen-Bornemisza, Madrid") != -1 else x)
df['Museum'] = df['Museum'].apply(lambda x: "Konstmuseum Gothenburg" if x.find("Gothenburg Museum of Art, Sweden") != -1 else x)

df = df.drop_duplicates(subset="URL")
df = df.reset_index().drop(['index'], axis=1)

df.to_excel('paintings.xlsx')

# get paintings in galleries

df_m = df.where(df['Museum'] != 'Private collection')
df_m = df_m['URL'].dropna()
headers = {'User-Agent': 'My User Agent 1.0'}
for url in df_m:
    img_data = requests.get(url, headers=headers, stream=True).content
    pic = 'paintings/' + str(df_m[df_m==url].index[0]) + '.png'
    with open(pic, 'wb') as f:
        f.write(img_data)

# fix broken pic
img = Image.open('paintings/247.png')
img = img.convert('RGB')
img.save('paintings/247.png')

# get supporting table with gallery name, coordinates and country

locations = [key for key in df['Museum'].unique() if key != 'Private collection']
coord = []

for loc in locations:
    geolocator = Nominatim(user_agent="email@ya.ru")
    location = geolocator.geocode(loc)
    address = geolocator.reverse(f'{location.latitude},{location.longitude}', language='en')
    address = address.raw['address']
    country = address.get('country', '')
    coord.append((loc, location.latitude, location.longitude, country))


coord_df = list(zip(*coord))
galleries = pd.DataFrame({'Museum': coord_df[0],
                          'Latitude': coord_df[1],
                          'Longitude': coord_df[2],
                          'Country': coord_df[3]})

galleries.to_excel('coordinates.xlsx')
