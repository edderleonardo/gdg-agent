import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openrouter/google/gemini-3-flash-preview",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# ---- HERRAMIENTAS (TOOLS) ----
def get_weather_report(city: str) -> dict:
    """Obtiene el clima actual de una ciudad.
    
    Args:
        city: Nombre de la ciudad a consultar.
    Returns:
        dict: Diccionario con 'status' ('success' o 'error') y 'report' con el clima,
              o 'error_message' si la ciudad no está disponible.
    """
    data = {
        "london":   {"temp": 18, "condition": "nublado", "rain_chance": 70},
        "paris":    {"temp": 25, "condition": "soleado",  "rain_chance": 5},
        "tokyo":    {"temp": 22, "condition": "parcialmente nublado", "rain_chance": 20},
        "new york": {"temp": 15, "condition": "ventoso",  "rain_chance": 30},
        "campeche": {"temp": 34, "condition": "caluroso y húmedo", "rain_chance": 60},
    }
    city_lower = city.lower()
    if city_lower in data:
        w = data[city_lower]
        return {
            "status": "success",
            "report": f"{city.title()}: {w['condition']}, {w['temp']}°C, {w['rain_chance']}% de probabilidad de lluvia."
        }
    return {"status": "error", "error_message": f"No hay datos del clima para '{city}'."}


def get_flight_prices(origin: str, destination: str) -> dict:
    """Retorna precios de vuelo mockeados entre dos ciudades.
    
    Args:
        origin: Ciudad de origen.
        destination: Ciudad de destino.
    Returns:
        dict: Precio en USD, duración del vuelo y aerolínea, o error si la ruta no existe.
    """
    routes = {
        ("campeche", "paris"):    {"price": 850,  "duration": "14h",   "airline": "Air France"},
        ("campeche", "london"):   {"price": 780,  "duration": "13h",   "airline": "British Airways"},
        ("campeche", "tokyo"):    {"price": 1100, "duration": "22h",   "airline": "ANA"},
        ("campeche", "new york"): {"price": 420,  "duration": "5h",    "airline": "Delta"},
        ("london",   "paris"):    {"price": 95,   "duration": "1h20m", "airline": "Eurostar"},
    }
    key = (origin.lower(), destination.lower())
    reverse_key = (destination.lower(), origin.lower())

    flight = routes.get(key) or routes.get(reverse_key)
    if flight:
        return {
            "status": "success",
            "origen": origin.title(),
            "destino": destination.title(),
            **flight,
            "precio_usd": flight["price"]
        }
    return {"status": "error", "error_message": f"No se encontraron vuelos de {origin} a {destination}."}


def get_travel_recommendations(city: str) -> dict:
    """Retorna atracciones principales y consejos locales de una ciudad.
    
    Args:
        city: Ciudad sobre la que se quieren recomendaciones.
    Returns:
        dict: Lista de lugares imperdibles, consejo local, mejor temporada y presupuesto diario.
    """
    recommendations = {
        "london": {
            "imperdibles": ["Big Ben", "Museo Británico", "Torre de Londres"],
            "consejo_local": "Consigue una Oyster card para el transporte público, te ahorra bastante dinero.",
            "mejor_temporada": "Primavera (abril-junio)",
            "presupuesto_diario_usd": 120
        },
        "paris": {
            "imperdibles": ["Torre Eiffel", "El Louvre", "Montmartre"],
            "consejo_local": "Reserva la Torre Eiffel en línea con anticipación, las filas son brutales.",
            "mejor_temporada": "Primavera u Otoño",
            "presupuesto_diario_usd": 140
        },
        "tokyo": {
            "imperdibles": ["Shinjuku", "Templo Senso-ji", "Cruce de Shibuya"],
            "consejo_local": "Consigue una tarjeta Suica y descarga Google Translate con japonés offline.",
            "mejor_temporada": "Marzo-Abril (temporada de cerezos)",
            "presupuesto_diario_usd": 100
        },
        "new york": {
            "imperdibles": ["Central Park", "MoMA", "Puente de Brooklyn"],
            "consejo_local": "El metro es barato y llega a todos lados, olvídate de los taxis.",
            "mejor_temporada": "Otoño (septiembre-noviembre)",
            "presupuesto_diario_usd": 200
        },
    }
    city_lower = city.lower()
    if city_lower in recommendations:
        return {"status": "success", "ciudad": city.title(), **recommendations[city_lower]}
    return {"status": "error", "error_message": f"No hay recomendaciones disponibles para '{city}'."}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convierte una cantidad entre divisas usando tipos de cambio mockeados.
    
    Args:
        amount: Cantidad a convertir.
        from_currency: Moneda de origen (ej. 'USD', 'MXN').
        to_currency: Moneda destino (ej. 'EUR', 'JPY').
    Returns:
        dict: Resultado de la conversión con el tipo de cambio aplicado, o error si la moneda no está soportada.
    """
    # Tipos de cambio relativos al USD (mockeados)
    rates = {
        "USD": 1.0,
        "MXN": 17.2,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 149.5,
    }
    from_c = from_currency.upper()
    to_c = to_currency.upper()

    if from_c not in rates or to_c not in rates:
        return {"status": "error", "error_message": f"Moneda no soportada: {from_c} o {to_c}"}

    # Convertir primero a USD como moneda base, luego al destino
    in_usd = amount / rates[from_c]
    converted = in_usd * rates[to_c]
    return {
        "status": "success",
        "original": f"{amount} {from_c}",
        "convertido": f"{converted:.2f} {to_c}",
        "tipo_de_cambio": f"1 {from_c} = {rates[to_c] / rates[from_c]:.4f} {to_c}"
    }


# ---- AGENTE PRINCIPAL ----
root_agent = Agent(
    name="travel_assistant",
    model=model,
    description="Asistente de viajes inteligente que ayuda a planear trips con clima, vuelos, recomendaciones y conversión de divisas.",
    instruction="""
        Eres un asistente de viajes inteligente y amigable.
        Ayudas a los usuarios a planear viajes combinando múltiples fuentes de información.
        
        Cuando el usuario mencione un destino, proactivamente:
        1. Revisa el clima actual
        2. Busca opciones de vuelo si mencionan origen
        3. Da recomendaciones de lugares a visitar
        4. Convierte precios a la moneda que necesiten
        
        Siempre combina la información de múltiples tools para dar una respuesta completa y útil.
        Responde en el mismo idioma que el usuario.
    """,
    tools=[
        get_weather_report,
        get_flight_prices,
        get_travel_recommendations,
        convert_currency,
    ],
)