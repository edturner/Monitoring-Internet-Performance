from ip2geotools.databases.noncommercial import DbIpCity
import folium
import math


def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


ips = [
    "139.222.0.1",
    "193.62.92.126",
    "146.97.130.237",
    "146.97.35.217",
    "146.97.33.5",
    "146.97.33.22",
    "146.97.33.42",
    "146.97.35.190",
    "162.158.32.34",
    "162.158.32.45",
    "104.21.12.211"
]


def get_geolocation(ip):
    try:
        response = DbIpCity.get(ip, api_key='free')
        return (response.latitude, response.longitude), f"{response.city}, {response.region}, {response.country}"
    except Exception as e:
        print(f"Could not get geolocation for IP {ip}: {e}")
        return None, None


m = folium.Map(location=[0, 0], zoom_start=2)
map_locations = []
total_distance = 0

for ip in ips:
    location, tooltip = get_geolocation(ip)
    if location:
        if map_locations:
            # Calculate distance from last valid location
            last_location = map_locations[-1]
            total_distance += haversine(last_location[0], last_location[1], location[0], location[1])
        map_locations.append(location)
        folium.Marker(location, popup=f"<i>{ip}</i>", tooltip=tooltip).add_to(m)

if len(map_locations) > 1:
    folium.PolyLine(map_locations, color="blue", weight=2.5, opacity=1).add_to(m)

if map_locations:
    m.location = map_locations[0]

m.save("traceroute_map_with_lines.html")
print(f"Total distance covered: {total_distance:.2f} km")
