"""
Main Application Entry Point
Kivy-based interactive story game with MVC architecture
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# Import custom widgets so kv loader can find them
from widgets import AnimatedHoverButton, TypewriterLabel
from behaviors import HoverBehavior, RippleBehavior
from controller import GameController
from resources import get_resource_manager


# Define screen classes
class MenuScreen(Screen):
    pass


class CharacterSelectScreen(Screen):
    pass


class DifficultySelectScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class CreditsScreen(Screen):
    pass


class HistoriaPyApp(App):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super(HistoriaPyApp, self).__init__(**kwargs)
        self.controller = GameController()
        self.selected_character = None
        self.screen_manager = None
    
    def build(self):
        """Build the application"""
        # Load kv file
        Builder.load_file('views.kv')
        
        # Create screen manager
        self.screen_manager = ScreenManager(transition=FadeTransition())
        
        # Add screens
        self.screen_manager.add_widget(MenuScreen())
        self.screen_manager.add_widget(CharacterSelectScreen())
        self.screen_manager.add_widget(DifficultySelectScreen())
        self.screen_manager.add_widget(GameScreen())
        self.screen_manager.add_widget(CreditsScreen())
        
        # Set controller's view reference
        self.controller.set_view(self.screen_manager.get_screen('game'))
        
        return self.screen_manager
    
    def show_menu(self):
        """Show main menu"""
        self.screen_manager.current = 'menu'
    
    def show_character_select(self):
        """Show character selection"""
        self.screen_manager.current = 'character_select'
    
    def show_credits(self):
        """Show credits"""
        self.screen_manager.current = 'credits'
    
    def select_character(self, character):
        """
        Handle character selection.
        
        Args:
            character: "RedHood", "Nightwing", or "TimDrake"
        """
        self.selected_character = character
        self.screen_manager.current = 'difficulty_select'
    
    def start_game(self, difficulty):
        """
        Start a new game.
        
        Args:
            difficulty: "easy", "medium", or "hard"
        """
        if not self.selected_character:
            self.show_popup("Error", "Please select a character first")
            return
        
        # Start new game
        self.controller.new_game(self.selected_character, difficulty)
        
        # Switch to game screen and update display
        self.screen_manager.current = 'game'
        self.update_game_display()
    
    def update_game_display(self):
        """Update the game screen with current node info"""
        game_screen = self.screen_manager.get_screen('game')
        node = self.controller.get_current_node()
        
        if not node:
            self.show_popup("Error", "No story node found")
            return
        
        # Update title
        game_screen.ids.title_label.text = node.title
        
        # Update stats
        game_screen.ids.stats_label.text = self.controller.get_stats_text()
        
        # Update inventory
        game_screen.ids.inventory_label.text = self.controller.get_inventory_text()
        
        # Update story text with typewriter effect
        story_label = game_screen.ids.story_label
        story_label.set_text(node.description)
        
        # Update scene image
        resource_manager = get_resource_manager()
        texture = resource_manager.get_texture(node.image)
        game_screen.ids.scene_image.texture = texture
        
        # Clear and rebuild options
        options_box = game_screen.ids.options_box
        options_box.clear_widgets()
        
        for i, option in enumerate(node.options):
            btn = AnimatedHoverButton(
                text=option["text"],
                size_hint_y=None,
                height=50
            )
            btn.bind(on_release=lambda x, idx=i: self.choose_option(idx))
            options_box.add_widget(btn)
        
        # If this is a final node, add "Return to Menu" button
        if node.is_final:
            return_btn = AnimatedHoverButton(
                text="Return to Menu",
                size_hint_y=None,
                height=50
            )
            return_btn.bind(on_release=lambda x: self.show_menu())
            options_box.add_widget(return_btn)
    
    def choose_option(self, option_index):
        """
        Handle option selection.
        
        Args:
            option_index: Index of the chosen option
        """
        success = self.controller.choose_option(option_index)
        
        if not success:
            print("Failed to process choice")
    
    def save_game(self):
        """Save the current game"""
        if not self.controller.is_game_active():
            self.show_popup("Error", "No active game to save")
            return
        
        success = self.controller.save_game()
        
        if success:
            self.show_popup("Success", "Game saved successfully!")
        else:
            self.show_popup("Error", "Failed to save game")
    
    def load_game(self):
        """Load a saved game"""
        success = self.controller.load_game()
        
        if success:
            self.screen_manager.current = 'game'
            self.update_game_display()
            self.show_popup("Success", "Game loaded successfully!")
        else:
            self.show_popup("Error", "No saved game found or failed to load")
    
    def confirm_menu(self):
        """Confirm before returning to menu"""
        if self.controller.is_game_active():
            # Show confirmation popup
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(Label(
                text="Return to menu?\nMake sure to save your progress first!",
                size_hint_y=0.7
            ))
            
            buttons = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.3)
            
            popup = Popup(
                title='Confirm',
                content=content,
                size_hint=(0.6, 0.4)
            )
            
            yes_btn = AnimatedHoverButton(text='Yes')
            yes_btn.bind(on_release=lambda x: (popup.dismiss(), self.show_menu()))
            
            no_btn = AnimatedHoverButton(text='No')
            no_btn.bind(on_release=popup.dismiss)
            
            buttons.add_widget(yes_btn)
            buttons.add_widget(no_btn)
            content.add_widget(buttons)
            
            popup.open()
        else:
            self.show_menu()
    
    def show_popup(self, title, message):
        """
        Show a popup message.
        
        Args:
            title: Popup title
            message: Popup message
        """
        content = Label(text=message)
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.6, 0.4)
        )
        popup.open()
        
        # Auto-dismiss after 2 seconds
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)


def main():
    """Entry point"""
    app = HistoriaPyApp()
    app.run()


if __name__ == '__main__':
    main()
