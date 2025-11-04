"""
controller.py - Controller layer for the Kivy app (MVC Controller)
"""
from kivy.animation import Animation
from models import GameModel
from utils import debounce, play_sound
from resources import get_resource_manager


class GameController:
    """
    Controller that manages the game logic and coordinates between
    the Model and View layers.
    """
    
    def __init__(self, ui_callback=None):
        """
        Initialize the controller.
        
        Args:
            ui_callback: Callback function to update UI (typically a method from the view)
        """
        self.model = GameModel()
        self.ui_callback = ui_callback
        self.resource_manager = get_resource_manager()
        
        # Preload common assets
        self.resource_manager.preload_common_assets()
    
    def set_ui_callback(self, callback):
        """Set or update the UI callback function"""
        self.ui_callback = callback
    
    def nueva_partida(self, nombre, personaje, dificultad):
        """
        Start a new game.
        
        Args:
            nombre: Player name
            personaje: Character ID ('jason', 'dick', 'tim', 'damian')
            dificultad: Difficulty ('facil', 'normal', 'dificil')
        
        Returns:
            Starting story node
        """
        return self.model.nueva_partida(nombre, personaje, dificultad)
    
    def get_nodo_actual(self):
        """Get the current story node"""
        return self.model.get_nodo_actual()
    
    def get_jugador(self):
        """Get the current player"""
        return self.model.jugador
    
    @debounce(wait_time=0.5)
    def choose_option(self, nodo_actual, opcion):
        """
        Process player's choice with debounce protection.
        
        Args:
            nodo_actual: Current story node
            opcion: Selected option
        """
        # Play click sound
        play_sound('click', volume=0.5)
        
        # Apply the choice
        cambios, siguiente_nodo = self.model.elegir_opcion(nodo_actual, opcion)
        
        # Autosave after choice
        self.model.guardar_partida()
        
        # Update UI through callback
        if self.ui_callback:
            self.ui_callback(siguiente_nodo, cambios)
    
    def play_transition_animation(self, widget, duration=0.3):
        """
        Play a light cross-fade transition animation on a widget.
        
        Args:
            widget: Widget to animate
            duration: Animation duration in seconds
        """
        # Play transition sound
        play_sound('transition', volume=0.3)
        
        # Fade out
        anim_out = Animation(opacity=0, duration=duration / 2)
        
        # Fade in
        anim_in = Animation(opacity=1, duration=duration / 2)
        
        # Chain animations
        anim = anim_out + anim_in
        anim.start(widget)
    
    def guardar_partida(self):
        """Save the game"""
        return self.model.guardar_partida()
    
    def cargar_partida(self):
        """Load a saved game"""
        success = self.model.cargar_partida()
        if success and self.ui_callback:
            nodo = self.model.get_nodo_actual()
            self.ui_callback(nodo, [])
        return success
    
    def get_player_stats(self):
        """Get player statistics"""
        if self.model.jugador:
            return {
                'nombre': self.model.jugador.nombre,
                'salud': self.model.jugador.salud,
                'reputacion': self.model.jugador.reputacion,
                'recursos': self.model.jugador.recursos,
                'inventario': self.model.jugador.inventario,
                'decisiones': len(self.model.jugador.decisiones)
            }
        return None
    
    def preload_image(self, image_name):
        """Preload an image to avoid lag"""
        return self.resource_manager.get_image(image_name)
    
    def get_image_texture(self, image_name):
        """Get texture for an image"""
        return self.resource_manager.get_texture(image_name)
