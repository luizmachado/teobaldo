import os
import requests
import json
from langchain_core.tools import tool

# Chave Routes API
maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

# Endpoint google
url = "https://routes.googleapis.com/directions/v2:computeRoutes"

# Cabeçalho da requisição
headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": maps_api_key,
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
}

@tool
def get_route_and_polyline_metric(origin, destination):
    """
    Útil para  encontrar uma rota de carro entre um ponto de origem e um de destino.
    Esta ferramenta retorna os resultados no sistema métrico (quilômetros).
    Retorna um resumo legível da rota e uma string 'polyline' codificada que representa a geometria do caminho.
    """
    
    # URL da API do Google Maps
    api_url = "https://maps.googleapis.com/maps/api/directions/json"
    
    # Parâmetros para a requisição
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "units": "metric",  
        "language": "pt-BR",
        "key": maps_api_key
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # OK' significa que encontrou uma rota.
        if data["status"] != "OK":
            return {"error": f"Não foi possível encontrar uma rota. Status da API: {data.get('status')}"}

        # Extrai a primeira rota, apenas um trecho
        route = data["routes"][0]
        leg = route["legs"][0] 
        
        # Extrai as informações já no sistema métrico
        distance = leg["distance"]["text"]
        duration = leg["duration"]["text"]
        route_summary_text = route.get("summary", "N/A")
        
        # Cria o resumo final em português
        summary = (f"A rota de {origin} para {destination} tem {distance} "
                   f"e leva aproximadamente {duration}. "
                   f"A principal via é {route_summary_text}.")
        
        # Extrai a polyline codificada
        polyline = route["overview_polyline"]["points"]
        
        return {"summary": summary, "polyline": polyline}

    except requests.exceptions.RequestException as e:
        return {"error": f"Erro de conexão ao chamar a API do Google Maps: {e}"}
    except (KeyError, IndexError):
        # Ocorre se a estrutura da resposta JSON for inesperada
        return {"error": "Não foi possível processar a resposta da API do Google Maps. Formato inesperado."}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado: {str(e)}"}

if __name__ == "__main__":
    origem_teste = "Araguaína, TO"
    destino_teste = "Pinheiros, SP"
    print(f"\nBuscando rota de '{origem_teste}' para '{destino_teste}'...")

    resultado = get_route_and_polyline_metric.invoke({
    "origin": origem_teste, 
    "destination": destino_teste
    })
        
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
