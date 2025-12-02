#include "C:\Programacion\RecomendacionAmigos\include\RedSocial.h"

namespace RedSocial {

//Implementación de la clase Usuario

Usuario::Usuario(const string& n) : nombre(n) {} // Constructor
 
void Usuario::agregarInteres(const string& interes) { // Añadir un interés
    intereses.insert(interes); // set evita duplicados automáticamente
}

void Usuario::agregarAmigo(Usuario* amigo) { // Añadir un amigo
    if (amigo != this) { // Evitar agregarse a uno mismo
        for (Usuario* a : amigos) { // Evitar duplicados
            if (a == amigo) return; // Condición para validar si ya es amigo
        }
        amigos.push_back(amigo); // Agregar nuevo amigo
    }
}

// Funciones del Algoritmo

int calcularSimilitud(const Usuario* u1, const Usuario* u2) { // Calcula la similitud entre dos usuarios
    int similitud = 0;  // Contador de intereses compartidos
    for (const string& interes : u1->intereses) { // Iterar sobre intereses del primer usuario
        if (u2->intereses.count(interes)) { // Verificar si el segundo usuario tiene el mismo interés
            similitud++; // Incrementar contador si hay coincidencia
        }
    }
    return similitud; // Devolver el total de intereses compartidos
}

void recomendar(Usuario* usuario_base, int umbral_similitud) { // Genera recomendaciones para un usuario
    using std::cout; 
    using std::endl;

    cout << "\n🌟 **Recomendaciones para " << usuario_base->nombre << "** 🌟" << endl; 
    cout << "--------------------------------------" << endl;

    map<string, int> recomendaciones_conteo; // Mapa para contar recomendaciones

    vector<Usuario*> amigos_cercanos; // Amigos con similitud suficiente
    cout << "👥 Amigos cercanos (Similitud >= " << umbral_similitud << "):" << endl;

    for (Usuario* amigo : usuario_base->amigos) { // Iterar sobre amigos
        int sim = calcularSimilitud(usuario_base, amigo);// Calcular similitud

        if (sim >= umbral_similitud) {// Verificar umbral
            amigos_cercanos.push_back(amigo);// Agregar a amigos cercanos
            cout << "  - " << amigo->nombre // Mostrar amigo cercano
                 << " (Similitud: " << sim << " intereses compartidos)" << endl;

            for (const string& interes : amigo->intereses) { // Iterar sobre intereses del amigo
                if (usuario_base->intereses.find(interes) == usuario_base->intereses.end()) { // Si el usuario base no tiene este interés
                    recomendaciones_conteo[interes]++; // Contar recomendación
                }
            }
        }
    }

    if (amigos_cercanos.empty()) { // Vlidar no hay amigos cercanos
        cout << "  (No se encontraron amigos con similitud suficiente.)" << endl;
    }

    vector<pair<int, string>> recomendaciones_ordenadas; // Vector para ordenar recomendaciones
    for (const auto& par : recomendaciones_conteo) { // Convertir mapa a vector para ordenar
        recomendaciones_ordenadas.push_back({par.second, par.first}); // Par (conteo, interés)
    }

    sort(recomendaciones_ordenadas.rbegin(), recomendaciones_ordenadas.rend()); // Ordenar de mayor a menor

    cout << "\n💡 Intereses recomendados:" << endl;
    if (recomendaciones_ordenadas.empty()) { // Validar no hay recomendaciones
        cout << "  (No hay intereses nuevos para recomendar.)" << endl;
    } else { // Mostrar hasta 5 recomendaciones
        int count = 0;
        for (const auto& par : recomendaciones_ordenadas) { // Iterar sobre recomendaciones ordenadas
            if (count >= 5) break; // Limitar a 5 recomendaciones
            cout << "  - **" << par.second 
                 << "** (Visto en " << par.first << " amigos cercanos)" << endl;
            count++;
        }
    }
}

} // namespace RedSocial
