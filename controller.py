"""
Game Controller - MVC Controller layer
Manages game state and coordinates between model and view
"""
from models import GameModel
from resources import get_resource_manager
from utils import debounce
from kivy.animation import Animation
from kivy.clock import Clock


class GameController:
    """
    Main game controller - coordinates between model and view.
    Public API must remain compatible for existing code.
    """
    
    def __init__(self, enable_resources=True):
        self.model = GameModel()
        # Check if we're in headless mode
        import os
        if not enable_resources or os.environ.get('KIVY_NO_ARGS') == '1':
            # Create resource manager with textures disabled for headless testing
            from resources import ResourceManager
            self.resource_manager = ResourceManager(enable_textures=False)
        else:
            self.resource_manager = get_resource_manager()
        self.view = None  # Will be set by the view
        self._transition_in_progress = False
    
    def set_view(self, view):
        """Set the view reference"""
        self.view = view
    
    def new_game(self, character, difficulty, player_name="Player"):
        """
        Start a new game.
        
        Args:
            character: "RedHood", "Nightwing", or "TimDrake"
            difficulty: "easy", "medium", or "hard"
            player_name: Player's name
        """
        self.model.new_game(character, difficulty, player_name)
        
        # Preload some common assets
        self._preload_assets()
        
        return True
    
    def _preload_assets(self):
        """Preload common game assets"""
        try:
            # Preload some common images
            common_images = [
                "crime_alley.png",
                "batman_chase.png",
                "jason_valiente.png",
                "robin_training.png",
                "bludhaven.png",
                "batcave.png"
            ]
            self.resource_manager.preload_images(common_images)
        except Exception as e:
            print(f"Could not preload images (headless mode?): {e}")
        
        try:
            # Preload common sounds
            common_sounds = [
                "click.wav",
                "type.wav"
            ]
            self.resource_manager.preload_sounds(common_sounds)
        except Exception as e:
            print(f"Could not preload sounds: {e}")
    
    @debounce(wait_time=0.5)
    def choose_option(self, option_index):
        """
        Process player's choice (with debounce to prevent double-clicks).
        
        Args:
            option_index: Index of the chosen option
        
        Returns:
            bool: True if choice was successful
        """
        if self._transition_in_progress:
            print("Transition in progress, please wait")
            return False
        
        success = self.model.choose_option(option_index)
        
        if success and self.view:
            # Play transition animation before updating view
            self.play_transition_animation(lambda: self.view.update_display())
        
        return success
    
    def play_transition_animation(self, on_complete=None):
        """
        Play a transition animation (fade effect).
        
        Args:
            on_complete: Callback to execute after animation
        """
        if not self.view:
            if on_complete:
                on_complete()
            return
        
        self._transition_in_progress = True
        
        # Fade out
        fade_out = Animation(opacity=0.3, duration=0.3)
        
        def on_fade_out_complete(widget):
            # Execute the callback (usually updates the display)
            if on_complete:
                try:
                    on_complete()
                except Exception as e:
                    print(f"Error in transition callback: {e}")
            
            # Fade back in
            fade_in = Animation(opacity=1.0, duration=0.3)
            fade_in.bind(on_complete=lambda *args: setattr(self, '_transition_in_progress', False))
            fade_in.start(self.view)
        
        fade_out.bind(on_complete=on_fade_out_complete)
        fade_out.start(self.view)
    
    def get_current_node(self):
        """Get current story node"""
        return self.model.get_current_node()
    
    def get_player(self):
        """Get player object"""
        return self.model.player
    
    def save_game(self, filename="partida_guardada.json"):
        """
        Save game state.
        
        Args:
            filename: Path to save file
        
        Returns:
            bool: True if save was successful
        """
        return self.model.save_game(filename)
    
    def load_game(self, filename="partida_guardada.json"):
        """
        Load game state.
        
        Args:
            filename: Path to save file
        
        Returns:
            bool: True if load was successful
        """
        success = self.model.load_game(filename)
        
        if success and self.view:
            # Update view after loading
            self.view.update_display()
        
        return success
    
    def get_stats_text(self):
        """Get formatted stats text"""
        if not self.model.player:
            return "No active game"
        
        player = self.model.player
        return f"❤️ Health: {player.health}/100  ⭐ Reputation: {player.reputation}/100  💎 Resources: {player.resources}"
    
    def get_inventory_text(self):
        """Get formatted inventory text"""
        if not self.model.player:
            return "Inventory: Empty"
        
        player = self.model.player
        if not player.inventory:
            return "Inventory: Empty"
        
        return "Inventory: " + ", ".join(player.inventory)
    
    def is_game_active(self):
        """Check if a game is currently active"""
        return self.model.player is not None
    
    def is_final_node(self):
        """Check if current node is a final/ending node"""
        node = self.get_current_node()
        return node and node.is_final
