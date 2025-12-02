import osmnx as ox
import random
import heapq
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os
import imageio.v2 as imageio
import shutil

# Cargamos el grafo de la ciudad con OSMnx

# Cargamos la lactitud y longitud del centro de la ciudad de León, Gto, Mexico
center_point = (21.122, -101.680)  # latitude, longitude
G = ox.graph_from_point(center_point, dist=7000, network_type="drive") # Cargamos 7 km cuadrados alrededor del punto central

G = ox.project_graph(G) # Proyectamos el grafo a un sistema de coordenadas 2D adecuado para cálculos de distancia

# Parametros de salida
fps = 40
size = 10
animation = True
frames_folder = "a_star"

# Global variables
stage = "finding"
os.makedirs(frames_folder, exist_ok=True)
frame_count = 0

# Limpiamos los atributos de velocidad y peso de las aristas
for u, v, key, data in G.edges(keys=True, data=True):
    maxspeed = 60 # Velocidad por defecto en km/h
    if "maxspeed" in data: # Si existe el atributo de velocidad máxima
        val = data['maxspeed'] # Puede ser una lista o un string
        if isinstance(val, list): # Si es una lista, tomamos el valor mínimo

            # Extraemos los dígitos y convertimos a entero
            val = min([int(''.join(filter(str.isdigit, s))) for s in val]) 
        elif isinstance(val, str): # Si es un string, extraemos los dígitos y convertimos a entero
            val = int(''.join(filter(str.isdigit, val))) # Extraemos los dígitos y convertimos a entero
        maxspeed = val # Actualizamos la velocidad máxima
    data["maxspeed"] = maxspeed # Guardamos la velocidad máxima en la arista
    # Calculamos el peso de la arista en función de la longitud y la velocidad máxima
    data["weight"] = data["length"] / maxspeed

# Style utils
def style_unvisited_edge(edge):
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 0.2
    G.edges[edge]["linewidth"] = 0.5

def style_visited_edge(edge):
    G.edges[edge]["color"] = "#d36206"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_active_edge(edge):
    G.edges[edge]["color"] = '#e8a900'
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_path_edge(edge):
    G.edges[edge]["color"] = "white"
    G.edges[edge]["alpha"] = 1
    G.edges[edge]["linewidth"] = 1

def style_start_end(node):
    G.nodes[node]["highlight"] = True
    G.nodes[node]["size"] = 35 
    G.nodes[node]["color"] = "#FFFFFF"

# Obteniendo la posicion de cada Nodo (x, y)
pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

# Construyendo los puentes de las aristas
edges_lines = [] # Lista de coordenadas de las aristas
edges_keys = [] # Lista de llaves de las aristas

# Recorremos las aristas del grafo
for u, v, key, data in G.edges(keys=True, data=True):
    edges_keys.append((u,v,key)) # Guardamos la llave de la arista
    if 'geometry' in data: # Si la arista tiene geometria (curva)
        coords = list(data['geometry'].coords) # Obtenemos las coordenadas de la curva
    else: # Si la arista es recta
        coords = [pos[u], pos[v]] # Obtenemos las coordenadas de los nodos
    edges_lines.append(coords) # Guardamos las coordenadas de la arista

# Crear LineCollection para las aristas del grafo para que sea más eficiente
lc = LineCollection(edges_lines,
                    colors=[G.edges[e].get('color', '#d36206') for e in edges_keys],
                    linewidths=[G.edges[e].get('linewidth',0.5) for e in edges_keys],
                    alpha=[G.edges[e].get('alpha',0.2) for e in edges_keys])

# parametros del plot
fig, ax = plt.subplots(figsize=(size,size))
fig.patch.set_facecolor("#18080e")
ax.set_facecolor("#18080e")    

# Agregamos la coleccion de lineas al plot
ax.add_collection(lc)
ax.set_xlim(min(x for x, y in pos.values()), max(x for x, y in pos.values()))
ax.set_ylim(min(y for x, y in pos.values()), max(y for x, y in pos.values()))
ax.axis('off')

# Funcion para guardar cada frame
def save_frame(step):
    global frame_count, stage # almacenamiento del numero de frame y etapa actual

# Control de la frecuencia de guardado de frames según la etapa
    if stage == "finding": # Durante la búsqueda
        if step % 35 != 0: # Guardar cada 35 pasos para reducir la cantidad de frames
            return    
    elif stage == "reconstructing": # Durante la reconstrucción del camino
        if step % 1 != 0: # Guardar cada paso
            return 
        # Si el stage es igual a "found", no hacemos nada especial
    elif stage == "found":
        pass

    # Actualizamos los estilos de las aristas en la LineCollection
    lc.set_color([G.edges[e].get('color', '#d36206') for e in edges_keys])
    lc.set_linewidth([G.edges[e].get('linewidth',0.5) for e in edges_keys])
    lc.set_alpha([G.edges[e].get('alpha',0.2) for e in edges_keys])

    # Limpiamos el eje y lo redibujamos para el nuevo frame
    ax.cla()
    ax.set_facecolor("#18080e")
    ax.add_collection(lc)
    ax.set_xlim(min(x for x, y in pos.values()), max(x for x, y in pos.values()))
    ax.set_ylim(min(y for x, y in pos.values()), max(y for x, y in pos.values()))
    ax.axis('off')

    # Dibujamos los nodos visitados y destacados
    visited = [n for n, data in G.nodes(data=True) if data.get("visited")]
    highlighted = [n for n, data in G.nodes(data=True) if data.get("highlight")]
    if highlighted:
        ax.scatter([pos[n][0] for n in highlighted],
                   [pos[n][1] for n in highlighted],
                   s=[G.nodes[n].get("size", 25) for n in highlighted],
                   c=[G.nodes[n].get("color", "#FFFFFF") for n in highlighted],
                   zorder=3)

    # Anotamos las distancias en los nodos visitados cada cierto intervalo
    annotate_every = 10
    # Recorremos los nodos visitados
    for i, n in enumerate(visited):
        if i % annotate_every == 0: # Anotamos cada 'annotate_every' nodos
            dist = G.nodes[n].get("distance") # Obtenemos la distancia del nodo
            if dist is not None and dist != float("inf"): # Si la distancia es válida
                 # Intentamos anotar la distancia en el nodo
                try:
                    ax.text(pos[n][0], pos[n][1], f"{dist:.1f}", color='white', fontsize=6, zorder=4) # Anotamos la distancia en el nodo
                except Exception:
                    pass

    # Guardamos el frame como imagen PNG
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.savefig(os.path.join(frames_folder, f"frame_{frame_count:05d}.png"),
                dpi=160, facecolor=fig.get_facecolor(), transparent=False)
    frame_count += 1

# Dijkstra's Algorithm
def dijkstra(orig, dest, isAnimate=False):
    global stage
    stage = "finding"

    # Cambio de estado de los nodos para el algoritmo
    for node in G.nodes:
        G.nodes[node]["visited"] = False
        G.nodes[node]["distance"] = float("inf")
        G.nodes[node]["previous"] = None
        G.nodes[node]["size"] = 0

    # Algoritmo de configuración inicial
    for edge in G.edges:
        style_unvisited_edge(edge) # Estilo de arista no visitada

    G.nodes[orig]["distance"] = 0 # Distancia del nodo origen a 0
    style_start_end(orig) # Estilo del nodo inicio
    style_start_end(dest) # Estilo del nodo destino
    pq = [(0, orig)] # Cola de prioridad inicializada con el nodo origen
    step = 0 # Contador de pasos

    while pq: # Mientras haya nodos en la cola de prioridad
        _, node = heapq.heappop(pq) # Sacamos el nodo con la distancia mínima

        if node == dest: # Si llegamos al nodo destino
            stage = "found" # Cambiamos el estado a encontrado
            if isAnimate: # Si se está animando
                for _ in range(int(fps*0.8)): # Guardamos varios frames para pausar en el destino
                    save_frame(step) # Guardamos el frame actual
            else: 
                save_frame(step) # Guardamos el frame actual
            return step # Retornamos el número de pasos
        
        # saltamos nodos ya visitados
        if G.nodes[node]["visited"]: 
            continue
        G.nodes[node]["visited"] = True # Marcamos el nodo como visitado
        
        # Relajamos las aristas adyacentes
        for edge in G.out_edges(node, keys=True):
            style_visited_edge(edge) # Estilo de arista visitada
            neighbor = edge[1] # Nodo vecino
            weight = G.edges[edge]["weight"] # Peso de la arista

            # Relajación del algoritmo de Dijkstra
            if G.nodes[neighbor]["distance"] > G.nodes[node]["distance"] + weight: # Si encontramos una distancia menor
                # Actualizamos la distancia y el nodo previo
                G.nodes[neighbor]["distance"] = G.nodes[node]["distance"] + weight
                G.nodes[neighbor]["previous"] = node # Actualizamos el nodo previo

                # Añadimos el vecino a la cola de prioridad
                heapq.heappush(pq, (G.nodes[neighbor]["distance"], neighbor)) 

                # Actualizamos el estilo de la arista activa
                for edge2 in G.out_edges(neighbor, keys=True):
                    style_active_edge(edge2)
        
        # Plot frame para animación
        if isAnimate:
            save_frame(step)
        step += 1
    return step


# Reconstruyendo el camino desde el destino al origen
def reconstruct_path(orig, dest, isAnimate=False, algorithm=None):
    global stage # Estado actual
    stage = "reconstructing" # Cambiamos el estado a reconstrucción    
    # Apagamos todas las aristas
    for edge in G.edges:
        style_unvisited_edge(edge)
    dist = 0
    speeds = []
    curr = dest
    step = 0

    # Vamos a través de los nodos previos desde el destino al origen
    while curr != orig:
        prev = G.nodes[curr]["previous"] # Nodo previo
        if prev is None: # Si no hay nodo previo, el destino es inalcanzable
            print("Unnaccessible goal")
            return
        
        # Estilizamos la arista del camino
        for key in G[prev][curr]:
            # Aplicamos el estilo de camino
            style_path_edge((prev,curr,key))
            if algorithm: # Si se especifica un algoritmo, contamos el uso de la arista
                G.edges[(prev,curr,key)][f"{algorithm}_uses"] = G.edges[(prev,curr,key)].get(f"{algorithm}_uses",0)+1
        dist += G.edges[(prev,curr,0)]["length"] # Sumamos la distancia de la arista
        speeds.append(G.edges[(prev,curr,0)]["maxspeed"]) # Guardamos la velocidad de la arista
        curr = prev # Avanzamos al nodo previo
        if isAnimate: # Si se está animando
            save_frame(step) # Guardamos el frame actual
        step += 1 # Contador de pasos
    
    # Distancia en km
    dist /= 1000

    print(f"Distance: {dist} km") # Distancia total
    print(f"Avg. speed: {sum(speeds)/len(speeds)}") # Velocidad promedio 
    print(f"Total time: {dist/(sum(speeds)/len(speeds)) * 60} min") # Tiempo total en minutos

    stage = "found" # Cambiamos el estado a encontrado
    save_frame(step) # Guardamos el frame final
    

# Genera el video a partir de los frames guardados
def generate_video(frames_folder, output_video):

    # Obtener lista de frames ordenados para el video
    frames = sorted([
    os.path.join(frames_folder, f)
    for f in os.listdir(frames_folder)
    if f.endswith(".png")
    ])

    # Crear el video usando imageio
    with imageio.get_writer(output_video, fps=fps, codec='libx264') as writer:
        for frame in frames:
            writer.append_data(imageio.imread(frame)) # Agregar frame al video

    print("Video generado exitosamente:", output_video) # Mensaje de éxito

    # Finalmente, eliminamos la carpeta de frames para limpiar
    shutil.rmtree(frames_folder)
    print("Carpeta de frames eliminada.")

# Seleccionamos nodos de inicio y fin de forma aleatoria
nodes = list(G.nodes) # Lista de nodos del grafo
if len(nodes) < 15:
    print("El grafo tiene menos de 15 nodos. Ajusta el parámetro 'center_point' o la distancia de búsqueda.")
    raise SystemExit(1)

# Seleccionamos dos nodos aleatorios diferentes
start = random.choice(nodes)
end = random.choice(nodes)
while end == start: # Aseguramos que el nodo de fin sea diferente al de inicio
    end = random.choice(nodes)


print(f"Start node: {start}  End node: {end}")

total_steps = dijkstra(start, end, isAnimate=animation)
reconstruct_path(start, end, isAnimate=animation, algorithm='dijkstra')

if animation:
    generate_video(frames_folder, "animation_final_definitivo.mp4")