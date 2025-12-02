import math
from typing import List, Tuple, Optional

# Implementación de una Lista Enlazada Circular para el load balancer usando Round Robin

class Node: #Clase genera los nodos para representar cada servidor
    """Representa un servidor en la lista enlazada."""
    def __init__(self, server_id: str): #Inicializa el nodo con un ID de servidor y un contador de solicitudes
        self.server_id = server_id
        self.request_count = 0
        self.next: Optional[Node] = None #Puntero al siguiente nodo

class CircularLinkedList: #Clase que implementa la lista enlazada circular para Round Robin
    """Implementación de una Lista Enlazada Circular para el Round Robin."""
    def __init__(self, num_servers: int): #Inicializa la lista con el número de servidores especificado
        self.head: Optional[Node] = None
        self.current_server: Optional[Node] = None
        self._initialize_servers(num_servers) #Llama al método para crear los nodos de servidor

    def _initialize_servers(self, num_servers: int): #Crea los nodos de servidor y los enlaza de forma circular
        """Crea los nodos de servidor y los enlaza de forma circular."""
        if num_servers <= 0: #Si no hay servidores, no hace nada
            return

        # El nombre del primer servidor se genera en el bucle
        current_node = None
        
        for i in range(1, num_servers + 1): #Crea cada nodo de servidor
            new_node = Node(f"S{i}")
            
            if not self.head: #Si es el primer nodo, lo asigna como cabeza y actual servidor
                self.head = new_node #Asigna el primer nodo como cabeza
                self.current_server = new_node #Inicializa el puntero al servidor actual
                current_node = new_node #Establece el nodo actual
            else:
                current_node.next = new_node #Enlaza el nodo actual al nuevo nodo
                current_node = new_node #Actualiza el nodo actual al nuevo nodo
        
        # Cierra el círculo: el último nodo apunta a la cabeza
        if current_node:
            current_node.next = self.head #Cierra el círculo enlazando el último nodo con la cabeza

    def get_next_server(self) -> Node: #Retorna el siguiente servidor en la secuencia Round Robin
        """
        Retorna el servidor actual (apuntado por current_server) 
        y avanza el puntero al siguiente nodo.
        """
        if not self.current_server: #Si no hay servidores, lanza una excepción
            raise Exception("La lista de servidores está vacía.") 
            
        # Almacena el servidor que será retornado
        assigned_server = self.current_server
        
        # Avanza el puntero al siguiente servidor para la próxima solicitud
        self.current_server = self.current_server.next
        
        return assigned_server #Retorna el servidor asignado y avanza al siguiente

    def get_all_servers(self) -> List[Node]: #Retorna una lista de todos los nodos de servidor en la lista
        """Retorna todos los nodos de servidor en orden, útil para reportes."""
        nodes: List[Node] = [] #Lista para almacenar los nodos
        if not self.head:  #Si la lista está vacía, retorna una lista vacía
            return nodes
        
        temp = self.head
        while True:  # Recorre la lista hasta volver a la cabeza
            nodes.append(temp)
            temp = temp.next
            if temp == self.head:
                break
        return nodes

# --- Funciones de Utilidad y Simulación ---

REQUESTS = 10000
SERVERS = 5 #Valores por defecto

def get_user_input() -> Tuple[int, int]: #Solicita al usuario los parámetros de la simulación
    """Solicita al usuario los parámetros de la simulación."""
    print("-" * 50)
    print("SIMULACIÓN DE BALANCEADOR DE CARGA (ROUND ROBIN - LINKED LIST)")
    print("-" * 50)

    try:
        # Usa REQUESTS y SERVERS como valores por defecto si la entrada es vacía
        total_requests = int(input(f"Ingrese el total de solicitudes (por defecto: {REQUESTS}): ") or REQUESTS)
        num_servers = int(input(f"Ingrese el número de servidores (por defecto: {SERVERS}): ") or SERVERS)
    except ValueError:
        print("\n¡Advertencia! Entrada no válida. Usando valores por defecto.")
        total_requests = REQUESTS
        num_servers = SERVERS #Usa valores por defecto en caso de error de entrada
        
    if total_requests <= 0 or num_servers <= 0:
        print("\nError: Tanto las solicitudes como los servidores deben ser mayores a cero.")
        return 0, 0 #Retorna ceros si los valores son inválidos
        
    return total_requests, num_servers

def simulate_round_robin(total_requests: int, num_servers: int) -> CircularLinkedList: #Simula la asignación de solicitudes usando la Lista Enlazada Circular
    """Simula la asignación de solicitudes usando la Lista Enlazada Circular."""
    
    if num_servers <= 0:
        raise ValueError("El número de servidores debe ser positivo.") #Valida el número de servidores

    balancer_list = CircularLinkedList(num_servers) #Crea la lista enlazada circular con los servidores

    print(f"\nIniciando simulación: {total_requests:,} solicitudes en {num_servers} servidores (Linked List)...") 

    for _ in range(total_requests):
        # Obtiene el siguiente servidor en la secuencia cíclica
        assigned_server_node = balancer_list.get_next_server()
        
        # Asignar la solicitud y actualizar estadísticas en el nodo
        assigned_server_node.request_count += 1

    return balancer_list #Retorna la lista enlazada circular con los datos actualizados

def print_textual_chart(server_nodes: List[Node], max_width: int = 60): #Imprime un gráfico de barras ASCII para visualizar la distribución de carga
    """Muestra un gráfico de barras ASCII para visualizar la distribución de carga."""
    print("\n" + "=" * 50)
    print("VISUALIZACIÓN DE CARGA (GRÁFICO DE BARRAS)")
    print("=" * 50)
    
    if not server_nodes:
        return #Retorna si la lista de nodos está vacía

    # Extrae solo el conteo de solicitudes
    server_requests = [node.request_count for node in server_nodes]
    server_ids = [node.server_id for node in server_nodes]

    max_requests = max(server_requests) if server_requests else 0 #Encuentra el máximo número de solicitudes para escalar las barras
    
    for i, count in enumerate(server_requests):
        if max_requests > 0:
            # Calcula la longitud de la barra, redondeando hacia arriba
            bar_length = math.ceil((count / max_requests) * max_width) #Escala la barra proporcionalmente
        else:
            bar_length = 0
            
        bar = "█" * bar_length
        # Alineación y formato de IDs y conteos
        print(f"{server_ids[i]:<10}: {bar:<{max_width}} ({count:,})") #Imprime la barra con el conteo formateado


def print_results(server_nodes: List[Node], total_requests: int): #Imprime un reporte tabular con las estadísticas detalladas
    """Imprime el reporte tabular con las estadísticas detalladas."""
    print("\n" + "=" * 50)
    print("ESTADÍSTICAS DETALLADAS DE DISTRIBUCIÓN")
    print("=" * 50)
    
    if total_requests == 0: #Valida si se procesaron solicitudes
        print("No se procesaron solicitudes.")
        return

    num_servers = len(server_nodes) #Calcula el número de servidores
    ideal_load = total_requests / num_servers #Calcula la carga ideal por servidor
    
    print(f"Total de Solicitudes Procesadas: {total_requests:,}")
    print(f"Total de Servidores: {num_servers}")
    print(f"Carga Ideal (promedio): {ideal_load:,.2f} solicitudes")
    print("-" * 50)

    print(f"{'Servidor':<10} | {'Solicitudes':<15} | {'% de Carga':<12}")
    print("-" * 50)
    
    for node in server_nodes: #Imprime las estadísticas para cada servidor
        count = node.request_count #Obtiene el conteo de solicitudes del nodo
        count_str = f"{count:,}" #Formatea el conteo con comas
        percentage = (count / total_requests) * 100 #Calcula el porcentaje de carga
        print(f"{node.server_id:<10} | {count_str:<15} | {percentage:8.2f}%") 
        
    print("-" * 50)


def main():
    """Función principal para ejecutar la simulación."""
    try:
        total_requests, num_servers = get_user_input() #Obtiene los parámetros de entrada del usuario
        
        if total_requests > 0 and num_servers > 0:
            # La simulación devuelve la instancia de la Linked List
            balancer_list = simulate_round_robin(total_requests, num_servers)
            
            # Recolectar datos de los nodos para los reportes
            results_nodes = balancer_list.get_all_servers()

            print_results(results_nodes, total_requests)
            print_textual_chart(results_nodes)

    except Exception as e: #Manejo general de excepciones
        print(f"\nOcurrió un error en la ejecución: {e}")

if __name__ == "__main__": #Punto de entrada del programa
    main() 