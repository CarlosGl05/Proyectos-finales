#ifndef REDSOCIAL_H
#define REDSOCIAL_H

#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <map>
#include <algorithm>
#include <iomanip>

namespace RedSocial {

using namespace std;

// 1. CLASE USUARIO

class Usuario {
public:
    string nombre; 
    set<string> intereses; // Usamos set para evitar intereses duplicados
    vector<Usuario*> amigos; // Punteros a otros usuarios

    Usuario(const string& n); // Constructor

    void agregarInteres(const string& interes); // Añadir un interés
    void agregarAmigo(Usuario* amigo); // Añadir un amigo
};


// 2. FUNCIONES DEL ALGORITMO

int calcularSimilitud(const Usuario* u1, const Usuario* u2); // Calcula la similitud entre dos usuarios
void recomendar(Usuario* usuario_base, int umbral_similitud = 1); // Genera recomendaciones para un usuario

} 

#endif
