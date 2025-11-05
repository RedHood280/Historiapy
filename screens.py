"""
Screen classes for the application
"""
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.logger import Logger
from utils import typewriter_schedule


class MainMenuScreen(Screen):
    """Main menu screen"""
    pass


class CharacterSelectScreen(Screen):
    """Character selection screen"""
    
    def select_character(self, character):
        """Store selected character and move to difficulty selection"""
        app = App.get_running_app()
        app.selected_character = character
        Logger.info(f"Character selected: {character}")
        self.manager.current = 'difficulty_select'


class DifficultySelectScreen(Screen):
    """Difficulty selection screen"""
    
    def start_game(self, difficulty):
        """Start game with selected character and difficulty"""
        app = App.get_running_app()
        character = getattr(app, 'selected_character', 'jason')
        
        if app.controller.start_new_game(character, difficulty):
            Logger.info(f"Game started: {character} on {difficulty}")
            self.manager.current = 'game'
            
            # Initialize game screen
            game_screen = self.manager.get_screen('game')
            game_screen.update_display()
        else:
            Logger.error("Failed to start game")


class GameScreen(Screen):
    """Main game screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.typewriter_active = None
    
    def on_enter(self):
        """Called when entering the screen"""
        self.update_display()
    
    def update_display(self):
        """Update the game display with current node"""
        app = App.get_running_app()
        node = app.controller.get_current_node()
        
        if not node:
            Logger.warning("No current node")
            return
        
        # Cancel any active typewriter
        if self.typewriter_active:
            self.typewriter_active.cancel()
        
        # Update title
        self.ids.story_title.text = node.titulo
        
        # Update story text with typewriter effect
        story_label = self.ids.story_text
        
        def on_typewriter_complete():
            app.controller.play_sound("transition.mp3", volume=0.1)
        
        self.typewriter_active = typewriter_schedule(
            node.descripcion,
            story_label,
            interval=0.03,
            sound_callback=None,  # We'll add this when typing.wav exists
            on_complete=on_typewriter_complete
        )
        
        # Update options (max 4)
        option_buttons = [
            self.ids.option1,
            self.ids.option2,
            self.ids.option3,
            self.ids.option4
        ]
        
        for i, btn in enumerate(option_buttons):
            if i < len(node.opciones):
                btn.text = node.opciones[i]["texto"]
                btn.opacity = 1
                btn.disabled = False
            else:
                btn.text = ""
                btn.opacity = 0
                btn.disabled = True
        
        # Update stats
        self.update_stats()
        
        # Check if final node
        if node.es_final:
            self.show_ending()
    
    def update_stats(self):
        """Update player statistics display"""
        app = App.get_running_app()
        stats = app.controller.get_player_stats()
        
        if not stats:
            return
        
        self.ids.player_name.text = stats['nombre']
        self.ids.health_bar.value = stats['salud']
        self.ids.health_text.text = str(stats['salud'])
        self.ids.reputation_bar.value = stats['reputacion']
        self.ids.reputation_text.text = str(stats['reputacion'])
        self.ids.resources_text.text = f"💎 {stats['recursos']}"
    
    def choose_option(self, index):
        """Choose a story option"""
        app = App.get_running_app()
        
        def update_after_transition():
            self.update_display()
        
        # Play transition animation
        app.controller.play_transition_animation(
            self.ids.story_text,
            callback=lambda: app.controller.choose_option(index, update_after_transition)
        )
    
    def show_ending(self):
        """Show ending screen"""
        # For now, just disable options
        for btn_id in ['option1', 'option2', 'option3', 'option4']:
            if btn_id in self.ids:
                self.ids[btn_id].disabled = True


class StatsScreen(Screen):
    """Statistics and inventory screen"""
    
    def on_enter(self):
        """Update stats when entering screen"""
        app = App.get_running_app()
        stats = app.controller.get_player_stats()
        
        if not stats:
            self.ids.stats_content.text = "No hay partida en curso"
            return
        
        # Format stats text
        text = f"""JUGADOR: {stats['nombre']}

ESTADÍSTICAS:
❤️  Salud: {stats['salud']}/100
⭐ Reputación: {stats['reputacion']}/100
💎 Recursos: {stats['recursos']}

INVENTARIO ({len(stats['inventario'])} items):
"""
        for item in stats['inventario']:
            text += f"  • {item}\n"
        
        text += f"\nDECISIONES TOMADAS: {stats['decisiones']}\n"
        
        self.ids.stats_content.text = text


class CreditsScreen(Screen):
    """Credits screen"""
    pass
