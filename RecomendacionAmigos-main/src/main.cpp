#include <iostream>
#include <limits> // Necesario para la limpieza del buffer (std::numeric_limits)
#include "RedSocial.h" // ¡CORREGIDO! Usamos ruta relativa, gracias al tasks.json

using namespace std;
using namespace RedSocial; // Asumo que Usuario y recomendar están en este namespace

int main() {
    // Crear Usuarios
    Usuario u1("Alice");
    Usuario u2("Bob");
    Usuario u3("Charlie");
    Usuario u4("David");
    Usuario u5("Eve");

    // Intereses
    u1.agregarInteres("Musica");
    u1.agregarInteres("Fitness");
    u1.agregarInteres("Tecnologia");
    u1.agregarInteres("Viajes");

    u2.agregarInteres("Musica");
    u2.agregarInteres("Tecnologia");
    u2.agregarInteres("Cine");
    u2.agregarInteres("Juegos");

    u3.agregarInteres("Fitness");
    u3.agregarInteres("Viajes");
    u3.agregarInteres("Cocina");
    u3.agregarInteres("Juegos");

    u4.agregarInteres("Tecnologia");
    u4.agregarInteres("Musica");
    u4.agregarInteres("Arte");

    u5.agregarInteres("Cocina");
    u5.agregarInteres("Pintura");

    // Amistades
    u1.agregarAmigo(&u2);
    u1.agregarAmigo(&u3);
    u1.agregarAmigo(&u4);

    u2.agregarAmigo(&u1);
    u2.agregarAmigo(&u3);

    u3.agregarAmigo(&u5);

    // Ejecutar recomendaciones
    recomendar(&u1, 2);
    cout << "\n\n======================================" << endl;
    recomendar(&u3, 1);

    cout << "\nPresiona ENTER para salir...";

    // 1. Limpia cualquier entrada anterior en el buffer (evita que se salte la pausa)
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); 
    
    // 2. Espera a que el usuario presione ENTER
    cin.get(); 
    // -----------------------------------------------------------------

    return 0;
}