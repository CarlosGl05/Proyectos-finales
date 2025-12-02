# **Módulo 2: Simulación de Balanceador de Carga (Algoritmo Round Robin)**

---

## **1. Objetivo del Módulo**
En este modulo se espera simular un balanceador de carga utilizando el algoritmo **Round Robin**. El objetivo es distribuir un número determinado de solicitudes entre varios servidores que pueden ser configurados por el usuario o bien usando valores predeterminados.

La simulación permitirá observar la **distribución secuencial y equitativa** de la carga generada por este algoritmo mediante el uso de graficos de barras y reportes estadísticos básicos.

---

## **2. Concepto: Balanceo de Carga Round Robin**
El algoritmo **Round Robin** es uno de los métodos de distribución de carga más simples y utilizados, que, si bien no considera la diferencia de capacidad o carga de los servidores, es muy efectivo en escenarios donde los servidores tienen capaciades similares o incluso iguales, como estaremos simulando en ese caso.

### **Principio de funcionamiento:**
- Mantiene una lista de servidores disponibles.
- Cada nueva solicitud se envía al **siguiente servidor** en la lista.
- Al llegar al final, el algoritmo vuelve al **primer servidor**.

Este método organiza los servidores de forma cíclica, es decir que una vez se llega al último servidor, la siguiente iteración se realizará con el primero de la lista, garantizando una distribución uniforme con el tiempo.

---

## **3. Implementación**

### **3.1 Lenguaje de Implementación**
En esta simulación usamos **Python** debido a la facilidad que ofrece para no solo manipular o simular estructuras de datos, si no también para generar visualizaciones simples en consola o incluso gráficas más avanzadas usando librerías externas como Matplotlib o Seaborn.

En nuestrio caso, nos enfocaremos en una implementación básica que pueda ser ejecutada en cualquier entorno Python sin necesidad de librerías adicionales, por lo que la visualización se realizará mediante gráficos de barras en texto ASCII y una tabla sencilla que muestre la distribución de solicitudes entre los servidores.

---
### **3.2 Estructuras de Datos Clave**

| Componente | Tipo de Dato | Descripción |
|-----------|----------------|-------------|
| **Servidores** | Lista / Array | Identificadores de los servidores (ej.: `["S1", "S2", "S3", "S4"]`). |
| **Nodo** | Índice que apunta al servidor actual. | Permite rastrear el servidor al que se asignará la siguiente solicitud. |
| **Estadísticas** | Diccionario / Mapa | Registra cuántas solicitudes ha recibido cada servidor. |

**Alternativa de simulación:** Se puede implementar una **Lista Enlazada Circular** para modelar de forma natural la rotación continua entre los servidores.
Una forma más sencilla sería usar un array y un índice que se incremente cíclicamente, usando el operador módulo con el numero de servidores disponibles, sin embargio, la lista enlazada circular ofrece una representación más fiel del comportamiento del algoritmo Round Robin por lo que seleccionamos esta opción para la implementación.

### **3.3 Algoritmo de Asignación**
1. Tomar el índice actual `serverIndex`.
2. Asignar la solicitud al servidor correspondiente.
3. Incrementar su contador.
4. Avanzar el índice de manera cíclica
5. Usa una linked list circular para avanzar al siguiente nodo, una vez llega al ulitmo nodo, vuelve al primero.


---

### **3.4 Parámetros de Simulación**
Es importante considerar que en la implementación se pueden ajustar los siguientes parámetros, pero antes cualquier error, el programa usará los siguientes valores predeterminados:
- **REQUESTS:** Total de solicitudes a procesar (10,000 como valor predeterminado).
- **SERVERS:** Número de servidores (5 como valor predeterminado).


---

## **4. Resultados, Reporte Y Visualización**

### **4.1 Reporte de Distribución**
Ejemplo con 10,000 solicitudes y 5 servidores:

| Servidor | Solicitudes | Carga (%) |
|----------|-------------|-----------|
| Servidor 1 | 2000 | 20.00% |
| Servidor 2 | 2000 | 20.00% |
| Servidor 3 | 2000 | 20.00% |
| Servidor 4 | 2000 | 20.00% |
| Servidor 5 | 2000 | 20.00% |
| **TOTAL** | **10000** | **100%** |

> La distribución puede variar ligeramente si la división no es exacta, sin embargo este algoritmo tiende a equilibrar la carga de manera uniforme entre los servidores (máximo una solicitud de diferencia entre servidores).

---

### **4.2 Visualización (Gráfica de Barras)**
- **Eje Y:** Servidores (S1, S2, S3...).
- **Eje X:** Solicitudes asignadas.

La gráfica debe mostrar barras casi del mismo tamaño, reflejando la capacidad que tiene este algoritmo para distribuir la carga de manera igualitaria.

---

## **Ejemplo de Código (Python)**

```python
# Definición de la Simulación
NUM_SERVERS = 5
NUM_REQUESTS = 10000

# 1. Configuración Inicial
servidores = [f"Server_{i+1}" for i in range(NUM_SERVERS)]
estadisticas = {server: 0 for server in servidores}
server_index = 0  # Índice Round Robin

# 2. Bucle de Simulación
for request_id in range(NUM_REQUESTS):
    servidor_actual = servidores[server_index]
    estadisticas[servidor_actual] += 1

    # Avanzar el índice de forma cíclica
    server_index = (server_index + 1) % NUM_SERVERS

# 3. Reporte de Resultados
print("\n--- Reporte de Distribución de Carga (Round Robin) ---")
for server, count in estadisticas.items():
    porcentaje = (count / NUM_REQUESTS) * 100
    print(f"Servidor: {server} | Solicitudes: {count} | Carga: {porcentaje:.2f}%")

```

## **5. Implementación del algoritmo Round Robin con Lista Enlazada Circular**

### **5.1 Ejemplo de Implementación con Lista Enlazada Circular (Python)**



El siguiente código define:
- La clase `Node`, que representa un servidor.
- La clase `CircularLinkedList`, que implementa el ciclo Round Robin.

```python
class Node:
    def __init__(self, server_id: str):
        self.server_id = server_id
        self.request_count = 0
        self.next: Optional[Node] = None

class CircularLinkedList:
    def __init__(self, num_servers: int):
        self.head: Optional[Node] = None
        self.current_server: Optional[Node] = None
        self._initialize_servers(num_servers)

    def _initialize_servers(self, num_servers: int):
        if num_servers <= 0:
            return

        current_node = None
        for i in range(1, num_servers + 1):
            new_node = Node(f"S{i}")
            if not self.head:
                self.head = new_node
                self.current_server = new_node
                current_node = new_node
            else:
                current_node.next = new_node
                current_node = new_node

        if current_node:
            current_node.next = self.head

    def get_next_server(self) -> Node:
        if not self.current_server:
            raise Exception("Lista de servidores vacía.")
        assigned_server = self.current_server
        self.current_server = self.current_server.next
        return assigned_server

    def get_all_servers(self) -> List[Node]:
        nodes = []
        if not self.head:
            return nodes

        temp = self.head
        while True:
            nodes.append(temp)
            temp = temp.next
            if temp == self.head:
                break
        return nodes
```

---

### **5.2 Simulación del Balanceador Round Robin**
    
```python
def simulate_round_robin(total_requests: int, num_servers: int) -> CircularLinkedList:
    if num_servers <= 0:
        raise ValueError("El número de servidores debe ser positivo.")

    balancer_list = CircularLinkedList(num_servers)

    print(f"
Iniciando simulación: {total_requests:,} solicitudes en {num_servers} servidores...")

    for _ in range(total_requests):
        assigned_server_node = balancer_list.get_next_server()
        assigned_server_node.request_count += 1

    return balancer_list
```

---

### **5.3 Reporte y Visualización ASCII**

```python
def print_results(server_nodes: List[Node], total_requests: int):
    print("
" + "=" * 50)
    print("ESTADÍSTICAS DETALLADAS DE DISTRIBUCIÓN")
    print("=" * 50)

    num_servers = len(server_nodes)
    ideal_load = total_requests / num_servers

    print(f"Total de Solicitudes Procesadas: {total_requests:,}")
    print(f"Total de Servidores: {num_servers}")
    print(f"Carga Ideal: {ideal_load:,.2f} solicitudes")
    print("-" * 50)

    print(f"{'Servidor':<10} | {'Solicitudes':<15} | {'% de Carga':<12}")
    print("-" * 50)

    for node in server_nodes:
        count = node.request_count
        percentage = (count / total_requests) * 100
        print(f"{node.server_id:<10} | {count:<15} | {percentage:8.2f}%")

    print("-" * 50)
```

```python
def print_textual_chart(server_nodes: List[Node], max_width: int = 60):
    print("
" + "=" * 50)
    print("VISUALIZACIÓN DE CARGA (GRÁFICO DE BARRAS)")
    print("=" * 50)

    server_requests = [node.request_count for node in server_nodes]
    server_ids = [node.server_id for node in server_nodes]
    max_requests = max(server_requests)

    for i, count in enumerate(server_requests):
        bar_length = math.ceil((count / max_requests) * max_width) if max_requests > 0 else 0
        bar = "█" * bar_length
        print(f"{server_ids[i]:<10}: {bar:<{max_width}} ({count:,})")
```

---

### **5.4 Función Principal**

```python
def main():
    total_requests, num_servers = REQUESTS, SERVERS
    balancer_list = simulate_round_robin(total_requests, num_servers)
    results_nodes = balancer_list.get_all_servers()

    print_results(results_nodes, total_requests)
    print_textual_chart(results_nodes)

if __name__ == "__main__":
    main()
```

---

## **6. Time Complexity y Análisis final**

- **Time Complexity:** O(N). Si bien las operaciónes de asiganción y cambio de servidor son de tiempo constante O(1), el bucle principal itera N veces para procesar todas las solicitudes, por lo que el tiempo total es lineal respecto al número de solicitudes.

- **Space Complexity:** O(S), donde S es el número de servidores. Se utiliza espacio adicional para almacenar los nodos de la lista enlazada circular.

El modelo de balanceo de carga Round Robin que fue implementado es idea para cualquier escenario donde los aervidores tengan capacidades muy similares, en el caso de que existan diferencias muy grandes, lo mejor sería considerar otros algoritmos de balanceo de carga que tomen en cuenta la carga actual o la capacidad de cada servidor.

El uso de una **circular linked list** permite una representación muy eficiente del funcionamiento cíclico que tiene este algoritomo, facilitando la implementación y la visualización del proceso de asignación de solicitudes.