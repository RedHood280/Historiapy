"""
Game controller - manages game state, transitions, and UI updates
"""
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from models import JuegoAventuraBase
from resources import resource_manager
from utils import debounce
from kivy.logger import Logger


class GameController:
    """Main game controller"""
    
    def __init__(self, screen_manager=None):
        self.game = JuegoAventuraBase()
        self.screen_manager = screen_manager
        self.current_screen = None
        self.typewriter_effect = None
        
    def start_new_game(self, character: str, difficulty: str):
        """Start a new game with selected character and difficulty"""
        # Map nightwing to grayson for story nodes
        char_map = {
            'nightwing': 'grayson',
            'jason': 'jason',
            'tim': 'tim',
            'damian': 'damian'
        }
        story_char = char_map.get(character, character)
        
        success = self.game.iniciar_juego(story_char, difficulty)
        if success:
            Logger.info(f"GameController: Started new game - {character} on {difficulty}")
            return True
        Logger.error(f"GameController: Failed to start game - {character} on {difficulty}")
        return False
    
    def get_current_node(self):
        """Get current story node"""
        return self.game.obtener_nodo_actual()
    
    @debounce(wait=0.5)
    def choose_option(self, option_index: int, callback=None):
        """
        Choose a story option
        
        Args:
            option_index: Index of the option to choose
            callback: Optional callback after transition
        """
        if self.game.elegir_opcion(option_index):
            Logger.info(f"GameController: Option {option_index} chosen")
            
            # Play transition sound
            self.play_sound("transition.mp3", volume=0.3)
            
            if callback:
                callback()
            return True
        return False
    
    def save_game(self):
        """Save current game state"""
        return self.game.guardar_partida()
    
    def load_game(self):
        """Load saved game state"""
        return self.game.cargar_partida()
    
    def get_player_stats(self):
        """Get current player statistics"""
        if not self.game.jugador:
            return None
        
        return {
            'nombre': self.game.jugador.nombre,
            'salud': self.game.jugador.salud,
            'reputacion': self.game.jugador.reputacion,
            'recursos': self.game.jugador.recursos,
            'inventario': self.game.jugador.inventario,
            'decisiones': len(self.game.jugador.decisiones)
        }
    
    def play_transition_animation(self, target_widget, callback=None):
        """
        Play transition animation (fade out/in)
        
        Args:
            target_widget: Widget to animate
            callback: Function to call mid-transition
        """
        # Fade out
        fade_out = Animation(opacity=0, duration=0.3)
        
        def on_fade_out_complete(*args):
            # Call callback at mid-point
            if callback:
                callback()
            
            # Fade in
            fade_in = Animation(opacity=1, duration=0.3)
            fade_in.start(target_widget)
        
        fade_out.bind(on_complete=on_fade_out_complete)
        fade_out.start(target_widget)
    
    def play_sound(self, sound_name: str, volume: float = 1.0):
        """
        Play a sound effect
        
        Args:
            sound_name: Name of the sound file
            volume: Volume level (0.0 to 1.0)
        """
        resource_manager.play_sound(sound_name, volume)
    
    def get_typing_sound_callback(self):
        """Get callback for typing sound effect"""
        def play_typing_sound():
            self.play_sound("typing.wav", volume=0.2)
        return play_typing_sound
