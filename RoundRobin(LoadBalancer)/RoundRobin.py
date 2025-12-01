import math
from typing import List, Tuple

REQUESTS = 10000
SERVERS = 5

def get_user_input() -> Tuple[int, int]:
    print("-" * 50)
    print("SIMULACIÓN DE BALANCEADOR DE CARGA (ROUND ROBIN)")
    print("-" * 50)

    try:
        total_requests = int(input(f"Ingrese el total de solicitudes (por defecto: {REQUESTS}): ") or REQUESTS)
        num_servers = int(input(f"Ingrese el número de servidores (por defecto: {SERVERS}): ") or SERVERS)
    except ValueError:
        print("\n¡Advertencia! Entrada no válida.")
        total_requests = REQUESTS
        num_servers = SERVERS
        
    if total_requests <= 0 or num_servers <= 0:
        print("\nError: Tanto las solicitudes como los servidores deben ser mayores a cero.")
        return 0, 0
        
    return total_requests, num_servers

def simulate_round_robin(total_requests: int, num_servers: int) -> List[int]:
    server_requests = [0] * num_servers
    next_server_index = 0

    print(f"\nIniciando simulación: {total_requests:,} solicitudes en {num_servers} servidores...")

    for _ in range(total_requests):
        server_requests[next_server_index] += 1
        next_server_index = (next_server_index + 1) % num_servers

    return server_requests

def print_textual_chart(server_requests: List[int], max_width: int = 60):
    print("\n" + "=" * 50)
    print("VISUALIZACIÓN DE CARGA (GRÁFICO DE BARRAS)")
    print("=" * 50)
    
    if not server_requests:
        return

    max_requests = max(server_requests)
    
    for i, count in enumerate(server_requests):
        if max_requests > 0:
            bar_length = math.ceil((count / max_requests) * max_width)
        else:
            bar_length = 0
            
        bar = "█" * bar_length
        print(f"Servidor {i+1:02d}: {bar:<{max_width}} ({count:,})")


def print_results(server_requests: List[int], total_requests: int):
    print("\n" + "=" * 50)
    print("ESTADÍSTICAS DETALLADAS DE DISTRIBUCIÓN")
    print("=" * 50)
    
    if total_requests == 0:
        print("No se procesaron solicitudes.")
        return

    ideal_load = total_requests / len(server_requests)
    
    print(f"Total de Solicitudes Procesadas: {total_requests:,}")
    print(f"Total de Servidores: {len(server_requests)}")
    print(f"Carga Ideal (promedio): {ideal_load:,.2f} solicitudes")
    print("-" * 50)

    print(f"{'Servidor':<10} | {'Solicitudes':<15} | {'% de Carga':<12}")
    print("-" * 50)
    
    for i, count in enumerate(server_requests):
        count_str = f"{count:,}"
        percentage = (count / total_requests) * 100
        print(f"S{i+1:<9} | {count_str:<15} | {percentage:8.2f}%")
        
    print("-" * 50)


def main():
    total_requests, num_servers = get_user_input()
    
    if total_requests > 0 and num_servers > 0:
        results = simulate_round_robin(total_requests, num_servers)
        print_results(results, total_requests)
        print_textual_chart(results)

if __name__ == "__main__":
    main()