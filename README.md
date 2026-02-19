# GDG Agent - Asistente de Viajes

Agente de viajes inteligente construido con [Google ADK](https://google.github.io/adk-docs/) (Agent Development Kit) y [LiteLLM](https://docs.litellm.ai/), que utiliza el modelo Gemini 3 Flash Preview a traves de OpenRouter.

## Funcionalidades

El agente cuenta con 4 herramientas (tools) que combinan informacion para ayudar a planear viajes:

| Herramienta | Descripcion |
|---|---|
| `get_weather_report` | Clima actual de una ciudad (London, Paris, Tokyo, New York, Campeche) |
| `get_flight_prices` | Precios de vuelos entre ciudades con aerolinea y duracion |
| `get_travel_recommendations` | Atracciones, consejos locales, mejor temporada y presupuesto diario |
| `convert_currency` | Conversion entre divisas (USD, MXN, EUR, GBP, JPY) |

> **Nota:** Todos los datos son mockeados con fines de demostracion.

## Requisitos

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)
- Una API key de [OpenRouter](https://openrouter.ai/)

## Instalacion

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd gdg-agent

# Instalar dependencias con uv
uv sync
```

## Configuracion

Crea el archivo `my_agent/.env` con tu API key de OpenRouter:

```env
OPENROUTER_API_KEY=tu-api-key-aqui
```

## Uso

Ejecuta el agente con el CLI de Google ADK:

```bash
uv run adk run my_agent
```

O para usar la interfaz web:

```bash
uv run adk web my_agent
```

## Estructura del proyecto

```
gdg-agent/
├── my_agent/
│   ├── .env              # Variables de entorno (no commitear)
│   ├── __init__.py
│   └── agent.py          # Definicion del agente y herramientas
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Ejemplo de interaccion

> **Usuario:** Quiero viajar de Campeche a Paris, que me recomiendas?

El agente automaticamente:
1. Consulta el clima en Paris
2. Busca vuelos de Campeche a Paris
3. Muestra recomendaciones turisticas
4. Ofrece convertir precios a MXN
