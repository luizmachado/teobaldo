import json
from langchain_core.tools import tool
from shapely.geometry import Point, LineString
import polyline as polyline_decoder
from app.tools.geo import km_to_degrees

# Carrega dados dos parceiros
with open('src/data/partners.json', 'r', encoding='utf-8') as f:
    partners_data = json.load(f)["estabelecimentos"]

@tool
def find_partners_on_route(route_polyline, partner_type, search_radius_km=5.0):
    """
    Encontra estabelecimentos parceiros de um determinado tipo (ex: 'Posto de Combustível', 'Restaurante')
    ao longo de uma rota. Requer uma 'polyline' codificada da rota e um raio de busca em km.
    """
    try:
        # Decodifica polyline
        decoded_coords = polyline_decoder.decode(route_polyline)

        # Cria uma linha com os pontos da rota e inverte lat/lon
        route_linestring = LineString([(lon, lat) for lat, lon in decoded_coords])

        # Cria o buffer em graus
        buffer_dist_degrees = km_to_degrees(search_radius_km)
        search_area = route_linestring.buffer(buffer_dist_degrees)

        # Lista de parceiros encontrados
        found_partners = []

        for partner in partners_data:
            # Se partner_type for especificado, filtra, caso contrário, inclui todos
            if not partner_type or partner["tipo"].lower() == partner_type.lower():
                loc = partner["localizacao"]
                partner_point = Point(loc["longitude"], loc["latitude"])
                if search_area.intersects(partner_point):
                    found_partners.append({
                        "nome": partner["nome"],
                        "tipo": partner["tipo"],
                        "endereco": loc["endereco"]
                    })

        if not found_partners:
            return {"message": "Nenhum parceiro encontrado na rota especificada."}

        return found_partners

    except Exception as e:
        return [{"error": f"Erro ao processar busca de parceiros: {str(e)}"}]

