import xmltodict

filename = "5.osm"

def parse_osm_police_stations_xmltodict(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        doc = xmltodict.parse(f.read())

    police_stations = []

    nodes = doc.get('osm', {}).get('node', [])
    if not isinstance(nodes, list):
        nodes = [nodes]

    for node in nodes:
        tags = node.get('tag', [])
        if not isinstance(tags, list):
            tags = [tags]

        is_police = False
        name = None
        addr_street = None
        addr_housenumber = None
        addr_city = None

        for tag in tags:
            k = tag.get('@k')
            v = tag.get('@v')
            if k == 'amenity' and v == 'police':
                is_police = True
            elif k == 'name':
                name = v
            elif k == 'addr:street':
                addr_street = v
            elif k == 'addr:housenumber':
                addr_housenumber = v
            elif k == 'addr:city':
                addr_city = v

        if is_police:
            address_parts = []
            if addr_city:
                address_parts.append(addr_city)
            if addr_street:
                address_parts.append(addr_street)
            if addr_housenumber:
                address_parts.append(addr_housenumber)
            address = ', '.join(address_parts) if address_parts else (name or "адрес не указан")

            police_stations.append({
                'address': address,
                'name': name
            })

    return police_stations

def main():

    try:
        stations = parse_osm_police_stations_xmltodict(filename)
    except Exception as e:
        print(f"ошибка: {e}")

    stations_sorted = sorted(stations, key=lambda x: x['address'])

    print(f"\nколичество полицейских участков: {len(stations_sorted)}")
    print("\nсписок в алфавитном порядке по адресу:")
    k = 0
    for station in stations_sorted:
        k += 1
        if station['name'] and station['name'] != station['address']:
            print(f"{k}) адрес:{station['address']}, ({station['name']})")
        else:
            print(f"{k}) {station['address']}")

if __name__ == "__main__":
    main()