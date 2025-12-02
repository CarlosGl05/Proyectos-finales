<div align="center">

# ⚡ <span style="color:#61dafb;">ANÁLISIS FORMAL</span>: <span style="color:#ffdd57;">ALGORITMO DE DIJKSTRA</span>

![Static Badge](https://img.shields.io/badge/Algoritmos-Fundamentales-7D3C98?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Camino%20más%20corto-Dijkstra-3498DB?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Complejidad-O(E%20log%20V)-2ECC71?style=for-the-badge)

---

### 🎓 *Departamento de Tecnologías Computacionales*  
### *Instituto Tecnológico y de Estudios Superiores de Monterrey*

</div>

---

## 📝 **Resumen**

Este documento presenta un análisis técnico y formal del **Algoritmo de Dijkstra**, considerado uno de los pilares fundamentales para la resolución del problema del **camino mínimo de origen único** en grafos ponderados sin pesos negativos.  
Su importancia radica en su eficiencia, simplicidad conceptual y aplicabilidad en sistemas reales como navegación satelital, telecomunicaciones, IA y optimización urbana.

---

## 📘 **1. Introducción**

El problema del camino mínimo es esencial dentro de la teoría de grafos y la optimización computacional.  
En 1956, *Edsger W. Dijkstra* formuló un método determinista capaz de calcular el camino más corto en grafos ponderados positivos.  
Hoy en día, sigue siendo la base de algoritmos modernos de ruteo, GPS, redes de datos y modelos de transporte.

---

## 🧠 **2. Fundamentos Teóricos**

### 📌 2.1 Definición del Problema  
Dado un grafo ponderado:

\[
G = (V, E), \quad w(u,v) \ge 0
\]

se busca determinar la distancia mínima desde un nodo origen \(s\) hacia todos los demás nodos del grafo.

---

### 💎 2.2 Operación Fundamental: Relajación

La **relajación** determina si pasar por un nodo intermedio mejora la distancia hacia un vecino:

<div align="center">

$$
\boxed{
d[u] + w(u,v) < d[v] \;\Rightarrow\; d[v] = d[u] + w(u,v)
}
$$

</div>

Esta ecuación constituye la base matemática del algoritmo y es aplicada repetidamente sobre la frontera del grafo.

---

## 🚀 **3. Mecánica del Algoritmo (Estrategia Voraz)**

<div align="center">

| 🔍 Acción | Descripción |
|----------|-------------|
| 🏁 **Definitivos** | Conjunto de nodos con distancia mínima confirmada. |
| 🔭 **Selección Voraz** | Elige el nodo no visitado con menor distancia acumulada. |
| 🕸️ **Expansión** | Relaja las distancias de todos los vecinos del nodo elegido. |

</div>

---

## ⛔ **4. Restricción Fundamental**

<div align="center">

### 🚫 **El algoritmo solo funciona si todos los pesos cumplen:**

\[
w(u,v) \ge 0
\]

Si existen aristas con pesos negativos → se debe emplear **Bellman–Ford**.

</div>

---

## 📊 **5. Complejidad Computacional**

### ⏳ **5.1 Complejidad Temporal**

Usando **listas de adyacencia + heap binario (min-heap)**:

<div align="center">

| Operación | Complejidad | Descripción |
|----------|-------------|-------------|
| Inicialización | \(O(V)\) | Definir distancias iniciales |
| Extraer mínimo | \(O(V \log V)\) | Operaciones del heap |
| Relajación | \(O(E \log V)\) | Actualización de vecinos |
| **TOTAL** | 🚀 **\(O(E \log V)\)** | Escalable para grafos reales |

</div>

---

### 💾 **5.2 Complejidad Espacial**

<div align="center">

| Estructura | Espacio | Descripción |
|------------|---------|-------------|
| Grafo | \(O(V + E)\) | Lista de adyacencia |
| Distancias/Visitados | \(O(V)\) | Arreglos auxiliares |
| Heap | \(O(E)\) | Cola de prioridad |
| **TOTAL** | 💾 **\(O(V + E)\)** | Uso lineal de memoria |

</div>

---

## 🎯 **6. Aplicaciones Reales**

- Sistemas GPS y navegación urbana  
- Redes de comunicaciones (OSPF)  
- Optimización en transporte público  
- IA para pathfinding (A*, videojuegos, robótica)  
- Modelos de análisis urbano (OpenStreetMap, SIG)

---

## 🌍 **7. Créditos Técnicos**

<div align="center">

| Autor | Repositorio | Contribución |
|-------|-------------|-------------|
| **Santi Fiorino** | *maps-pathfinding* | Proyección precisa de mapas OSM |

</div>

Esta referencia es clave para la simulación realista de trayectorias urbanas en este proyecto.

---

## 🏁 **8. Conclusiones**

El algoritmo de Dijkstra combina:

✔ **Eficiencia temporal:** casi lineal en la práctica  
✔ **Robustez matemática:** prueba formal de corrección  
✔ **Escalabilidad:** ideal para grafos grandes  
✔ **Aplicabilidad universal:** desde GPS hasta redes neuronales gráficas

Por ello continúa siendo uno de los algoritmos esenciales dentro de la computación moderna.


<div align="center">


</div>
