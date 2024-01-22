import pickle

# Leer el objeto desde el archivo
with open('datos/datos_7001to8000.pkl', 'rb') as archivo:
    resultados_finales = pickle.load(archivo)

# Imprimir el objeto leído
for titulo, artista in resultados_finales:
    print(f"Artista de '{titulo}': {artista}")