
def find_partner(industry, location):
    """Mock de busca por instituições credenciadas."""
    return {
        "industry": industry,
        "location": location,
        "partners": [
            {"name": "Empresa Alpha", "rating": 4.7},
            {"name": "Negócios Beta", "rating": 4.5},
        ]
    }

def get_weather(location):
    """Mock de consulta do clima em uma localidade."""
    return {
        "location": location,
        "temperature_c": 26,
        "condition": "Parcialmente nublado",
        "forecast": [
            {"day": "Hoje", "temp": 26, "condition": "Sol com nuvens"},
            {"day": "Amanhã", "temp": 24, "condition": "Chuva leve"},
        ]
    }


def get_route_info(origin, destination):
    """Mock de rota entre duas localidades."""
    return {
        "origin": origin,
        "destination": destination,
        "distance_km": 12.5,
        "duration_min": 25,
        "route_summary": f"Rota simulada entre {origin} e {destination}."
    }


