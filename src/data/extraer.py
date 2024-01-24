import concurrent.futures
import requests
import numpy as np
import time
import pickle
import requests

def obtener_artista_y_genero_por_titulo(titulo_cancion, api_key):
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.search",
        "track": titulo_cancion,
        "api_key": api_key,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Verificar si la respuesta tiene resultados
    if "results" in data and "trackmatches" in data["results"]:
        trackmatches = data["results"]["trackmatches"]
        
        # Obtener el primer resultado (asumiendo que es el más relevante)
        if "track" in trackmatches and trackmatches["track"]:
            primer_resultado = trackmatches["track"][0]
            artista = primer_resultado.get("artist", "Desconocido")
            
            # Obtener información adicional sobre el artista y la canción
            artista_info = obtener_info_artista(artista, api_key)
            genero = artista_info.get("genero", "Desconocido")
            
            return {"artista": artista, "genero": genero}

    return {"artista": "Desconocido", "genero": "Desconocido"}

def obtener_info_artista(artista, api_key):
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getinfo",
        "artist": artista,
        "api_key": api_key,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Verificar si la respuesta tiene información sobre el artista
    if "artist" in data:
        artista_info = data["artist"]
        genero = artista_info.get("tags", {}).get("tag", [])
        
        # Obtener el primer género (asumiendo que es el más relevante)
        genero = genero[0]["name"] if genero else "Desconocido"
        
        return {"genero": genero}

    return {"genero": "Desconocido"}

def obtener_artista_por_titulo(titulo_cancion, api_key):
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.search",
        "track": titulo_cancion,
        "api_key": api_key,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Verificar si la respuesta tiene resultados
    if "results" in data and "trackmatches" in data["results"]:
        trackmatches = data["results"]["trackmatches"]
        
        # Obtener el primer resultado (asumiendo que es el más relevante)
        if "track" in trackmatches and trackmatches["track"]:
            primer_resultado = trackmatches["track"][0]
            artista = primer_resultado.get("artist", "Desconocido")
            return artista

    return "Desconocido"

# Función que realiza una consulta en un lote
def consultar_lote(titulos, api_key):
    resultados = []
    for titulo in titulos:
      result = obtener_artista_y_genero_por_titulo(titulo, api_key)
      resultados.append({'titulo':titulo, 'data':result})
    return resultados


def create_data_music(lotes, name, api_key_lastfm):
     # Realizar consultas en paralelo utilizando concurrent.futures.ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = list(executor.map(lambda lote: consultar_lote(lote, api_key_lastfm), lotes))

    # Combinar los resultados de todos los lotes
    resultados_finales = [resultado for sublist in resultados for resultado in sublist]

    route='datos/'+name+'.pkl'
    with open(route, 'wb') as archivo:
        pickle.dump(resultados_finales, archivo)

def main():
   # Registrar el tiempo de finalización
    data_array = np.load('./spotify.npy', allow_pickle=True)
    valor_nativo = data_array.item()
    api_key_lastfm = "d4a9079efcaec92a90657b01b8cf7786"

    for x in range(10):
        newValor=[]
        initValue=x*1000
        finalValue=(x+1)*1000
        for j in range(initValue, finalValue):
            newValor.append(valor_nativo[j])
        name='datosT_'+str(initValue+1)+'to'+ str(finalValue)
        create_data_music(newValor, name,api_key_lastfm)
main()