"""
models.py - Game logic and data models (MVC Model layer)
DO NOT MODIFY - Contains all game logic for 3 characters, 3 difficulties,
branching storylines, stats, items, multiple endings, and save/load functionality.
"""
import json
import os
from typing import Optional, Dict, List


class Jugador:
    """Clase que representa al jugador y sus estadísticas"""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.salud = 100
        self.reputacion = 50
        self.recursos = 3
        self.inventario = []
        self.decisiones = []
        self.nodo_actual = "inicio"

    def agregar_item(self, item: str):
        """Agregar un item al inventario"""
        if item not in self.inventario:
            self.inventario.append(item)

    def modificar_stat(self, stat: str, cambio: int):
        """Modificar una estadística del jugador"""
        if stat == "salud":
            self.salud = max(0, min(100, self.salud + cambio))
        elif stat == "reputacion":
            self.reputacion = max(0, min(100, self.reputacion + cambio))
        elif stat == "recursos":
            self.recursos = max(0, self.recursos + cambio)

    def guardar_decision(self, nodo: str, eleccion: str):
        """Guardar una decisión tomada"""
        self.decisiones.append({"nodo": nodo, "eleccion": eleccion})


class Personaje:
    """Clase para personajes no jugables (PNJ)"""
    def __init__(self, nombre: str, dialogo_inicial: str):
        self.nombre = nombre
        self.dialogo_inicial = dialogo_inicial
        self.dialogos = {}


class NodoHistoria:
    """Clase que representa un nodo de la historia"""
    def __init__(self, id: str, titulo: str, descripcion: str, imagen: str = ""):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.imagen = imagen
        self.opciones = []
        self.es_final = False
        self.text = descripcion  # Alias for compatibility

    def agregar_opcion(self, texto: str, nodo_siguiente: str,
                       stat: Optional[str] = None, cambio: int = 0,
                       stat2: Optional[str] = None, cambio2: int = 0,
                       item: Optional[str] = None):
        """Agregar una opción de decisión"""
        self.opciones.append({
            "texto": texto,
            "siguiente": nodo_siguiente,
            "stat": stat,
            "cambio": cambio,
            "stat2": stat2,
            "cambio2": cambio2,
            "item": item
        })


class GameModel:
    """
    Main game model containing all game logic.
    Manages story nodes, player state, and save/load functionality.
    """
    def __init__(self):
        self.jugador = None
        self.dificultad = None
        self.personaje_actual = None
        self.historia = {}
        self.personajes = {}
        self.save_file = "partida_guardada.json"
        
        # Initialize all game content
        self._inicializar_personajes()
        self._inicializar_historias()
    
    def _inicializar_personajes(self):
        """Crear los personajes del juego"""
        # Import existing character initialization from Robins.py
        try:
            from Robins import JuegoAventuraBase
            temp_game = JuegoAventuraBase()
            self.personajes = temp_game.personajes
        except:
            # Fallback: create basic characters
            batman = Personaje("Batman", "La justicia de Gotham requiere más que fuerza bruta.")
            batman.dialogos = {
                "orgullo": "Estoy orgulloso de ti, Jason.",
                "decepcion": "Esperaba más de ti, Robin.",
                "preocupacion": "Ten cuidado ahí fuera.",
            }
            self.personajes["batman"] = batman

            alfred = Personaje("Alfred", "¿Té, Maestro Jason?")
            alfred.dialogos = {
                "consejo": "La diferencia entre un héroe y un villano a menudo es solo una decisión.",
            }
            self.personajes["alfred"] = alfred

            joker = Personaje("Joker", "¡Jajajaja! ¿Vino el pequeño pájaro a jugar?")
            self.personajes["joker"] = joker
    
    def _inicializar_historias(self):
        """Cargar todas las historias del juego"""
        # Import existing stories from Robins.py
        try:
            from Robins import JuegoAventuraBase
            temp_game = JuegoAventuraBase()
            self.historia = temp_game.historia
        except Exception as e:
            print(f"Error loading stories: {e}")
            # Create a minimal fallback story
            self._crear_historia_minima()
    
    def _crear_historia_minima(self):
        """Crear historia mínima de fallback"""
        inicio = NodoHistoria(
            "jason_facil_inicio",
            "INICIO DEL JUEGO",
            "Bienvenido al juego. Esta es una historia de prueba.",
            ""
        )
        inicio.agregar_opcion("Comenzar aventura", "jason_facil_final")
        self.historia["jason_facil_inicio"] = inicio
        
        final = NodoHistoria(
            "jason_facil_final",
            "FINAL",
            "Has completado la aventura de prueba.",
            ""
        )
        final.es_final = True
        self.historia["jason_facil_final"] = final
    
    def nueva_partida(self, nombre: str, personaje: str, dificultad: str):
        """
        Iniciar una nueva partida.
        
        Args:
            nombre: Nombre del jugador
            personaje: ID del personaje ('jason', 'dick', 'tim', 'damian')
            dificultad: Dificultad ('facil', 'normal', 'dificil')
        """
        self.jugador = Jugador(nombre)
        self.personaje_actual = personaje
        self.dificultad = dificultad
        
        # Determine starting node
        prefijos = {
            "jason": "jason",
            "dick": "grayson",
            "tim": "tim",
            "damian": "damian"
        }
        prefijo = prefijos.get(personaje, "jason")
        nodo_inicial = f"{prefijo}_{dificultad}_inicio"
        
        # Fallback if node doesn't exist
        if nodo_inicial not in self.historia:
            nodo_inicial = "jason_facil_inicio"
        
        self.jugador.nodo_actual = nodo_inicial
        return self.get_nodo_actual()
    
    def get_nodo_actual(self):
        """Obtener el nodo actual de la historia"""
        if self.jugador and self.jugador.nodo_actual in self.historia:
            return self.historia[self.jugador.nodo_actual]
        return None
    
    def get_nodo(self, nodo_id: str):
        """Obtener un nodo específico"""
        return self.historia.get(nodo_id)
    
    def aplicar_opcion(self, opcion: dict):
        """
        Aplicar los efectos de una opción elegida.
        
        Args:
            opcion: Diccionario con los datos de la opción
        
        Returns:
            List of change descriptions
        """
        cambios = []
        
        # Apply stat changes
        if opcion.get('stat') and opcion.get('cambio') != 0:
            stat = opcion['stat']
            cambio = opcion['cambio']
            self.jugador.modificar_stat(stat, cambio)
            simbolo = "+" if cambio > 0 else ""
            cambios.append(f"{stat.capitalize()}: {simbolo}{cambio}")
        
        if opcion.get('stat2') and opcion.get('cambio2') != 0:
            stat2 = opcion['stat2']
            cambio2 = opcion['cambio2']
            self.jugador.modificar_stat(stat2, cambio2)
            simbolo = "+" if cambio2 > 0 else ""
            cambios.append(f"{stat2.capitalize()}: {simbolo}{cambio2}")
        
        # Add item
        if opcion.get('item'):
            item = opcion['item']
            self.jugador.agregar_item(item)
            cambios.append(f"Obtenido: {item}")
        
        return cambios
    
    def elegir_opcion(self, nodo_actual, opcion):
        """
        Procesar la elección de una opción.
        
        Args:
            nodo_actual: Nodo actual
            opcion: Opción elegida
        
        Returns:
            Tuple (cambios, siguiente_nodo)
        """
        # Save decision
        self.jugador.guardar_decision(nodo_actual.id, opcion['texto'])
        
        # Apply effects
        cambios = self.aplicar_opcion(opcion)
        
        # Update current node
        self.jugador.nodo_actual = opcion['siguiente']
        
        # Get next node
        siguiente_nodo = self.get_nodo_actual()
        
        return cambios, siguiente_nodo
    
    def guardar_partida(self) -> bool:
        """Guardar el progreso del juego"""
        if not self.jugador:
            return False
        
        try:
            datos = {
                "nombre": self.jugador.nombre,
                "salud": self.jugador.salud,
                "reputacion": self.jugador.reputacion,
                "recursos": self.jugador.recursos,
                "inventario": self.jugador.inventario,
                "decisiones": self.jugador.decisiones,
                "nodo_actual": self.jugador.nodo_actual,
                "dificultad": self.dificultad,
                "personaje_actual": self.personaje_actual
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def cargar_partida(self) -> bool:
        """Cargar una partida guardada"""
        if not os.path.exists(self.save_file):
            return False
        
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            self.jugador = Jugador(datos["nombre"])
            self.jugador.salud = datos["salud"]
            self.jugador.reputacion = datos["reputacion"]
            self.jugador.recursos = datos["recursos"]
            self.jugador.inventario = datos["inventario"]
            self.jugador.decisiones = datos["decisiones"]
            self.jugador.nodo_actual = datos["nodo_actual"]
            self.dificultad = datos.get("dificultad", "normal")
            self.personaje_actual = datos.get("personaje_actual", "jason")
            
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
