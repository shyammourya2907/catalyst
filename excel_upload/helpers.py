from excel_upload.models import Company


def get_cities_states():

    cities = []
    states = []
    for comp in Company.objects.all():
        if comp.locality != 'nan':
            parts = [part.strip(' ') for part in comp.locality.split(',')]
            city = parts[0]
            state = parts[1]

            if city not in cities:
                cities.append(city)

            if state not in states:
                states.append(state)
    print(cities)
    print(states)
