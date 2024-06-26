import pandas as ps
import pycountry
import pgeocode

print("hello world")

data = ps.read_csv("CSV_Files/fall-2022-noaddr.csv")

# read in some column data for zips and country codes
zip_col = data['ZIP']
international_col = data['INTERNATIONAL']
country_col = data['COUNTRY']

# Some items in COUNTRY use two-character indicators, while
# some others use a full country name. We'll run the country name
# ones through
print(set(country_col))

# Remove trailing -00000 and region-specific codes
stripped_zips = map(lambda s: str(s)[:min(5, len(str(s)))], zip_col)

country_col = country_col.map(lambda c: str(c))

count = 0
new_countries = []
for c in country_col:
    if c == "nan":
        country = pycountry.countries.get(alpha_2="us")
    elif len(c) == 2:
        country = pycountry.countries.get(alpha_2=c)
    else:
        country = pycountry.countries.search_fuzzy(c)[0]
    count += 1
    new_countries.append(country.alpha_2)


#for s in set(new_countries):
#    print(s)

coords = []
for country_code, postal_code in zip(new_countries, stripped_zips):
    nomi = pgeocode.Nominatim(country_code)
    postal_code_info = nomi.query_postal_code(postal_code)
    coords.append([postal_code_info.latitude, postal_code_info.longitude])

annville = [[40.32927, -76.51553]] * len(new_countries)
distances_km = pgeocode.haversine_distance(annville, coords)