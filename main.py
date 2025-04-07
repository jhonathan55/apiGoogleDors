import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from dotenv import load_dotenv
import logging
from typing import List, Dict, Optional

# ---------------- Configuración de Logging ----------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------- Cargar variables de entorno ----------------
def load_env_variables() -> Optional[Dict[str, str]]:
    load_dotenv()
    api_key = os.getenv('API_KEY_SEARCH_GOOGLE')
    search_engine_id = os.getenv('SEARCH_ENGINE_ID')

    if not api_key or not search_engine_id:
        logging.error("API Key o Search Engine ID no encontrados en el archivo .env")
        return None
    logging.info("API Key y Search Engine ID cargados correctamente.")
    return {
        'api_key': api_key,
        'search_engine_id': search_engine_id
    }

# ---------------- Realizar búsqueda en Google ----------------
def perform_google_search(api_key: str, search_engine_id: str, query: str, start: int = 1, lang: str = "lang_es") -> Optional[List[Dict]]:
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "start": start,
        "lr": lang
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Levanta HTTPError si la respuesta no es 200
        data = response.json()
        return data.get("items", [])

    except ConnectionError:
        logging.error("Error de conexión: no se pudo resolver el nombre del host o no hay red.")
    except Timeout:
        logging.error("La solicitud ha superado el tiempo de espera.")
    except RequestException as e:
        logging.error(f"Ocurrió un error en la solicitud HTTP: {e}")
    except ValueError as e:
        logging.error(f"Error al parsear la respuesta JSON: {e}")
    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
    
    return None


# ---------------- Mostrar resultados ----------------
def display_results(results: List[Dict]) -> None:
    for result in results:
        print("------- Nuevo resultado -------")
        print(f"Título: {result.get('title')}")
        print(f"Descripción: {result.get('snippet')}")
        print(f"Enlace: {result.get('link')}")
        print("-------------------------------")
        
# ---------------- Ejecución Principal ----------------
def main():
    env_vars = load_env_variables()
    if not env_vars:
        return
    query = 'filetype:sql "MySQL dump" (pass|password|passwd|pwd)'
    results = perform_google_search(env_vars['api_key'], env_vars['search_engine_id'], query)

    if results:
        display_results(results)
    else:
        logging.info("No se encontraron resultados o ocurrió un error durante la búsqueda.")
    

if __name__ == "__main__":
    main()


