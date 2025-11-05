"""
Main Kivy application
"""
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.factory import Factory
from behaviors import HoverBehavior, RippleBehavior
from controller import GameController
from utils import debounce
from kivy.logger import Logger
from screens import (MainMenuScreen, CharacterSelectScreen, DifficultySelectScreen, 
                     GameScreen, StatsScreen, CreditsScreen)

# Set window properties
Window.clearcolor = (0.1, 0.1, 0.12, 1)  # Dark background
Window.size = (1024, 768)


class AnimatedHoverButton(Button, HoverBehavior, RippleBehavior):
    """
    Button with hover animations (scale, color) and ripple effect
    """
    def __init__(self, **kwargs):
        # Store original background if provided, otherwise will use default after super().__init__
        self.original_background = kwargs.get('background_color', None)
        super().__init__(**kwargs)
        # Set original to actual background if not provided
        if self.original_background is None:
            self.original_background = self.background_color[:]
        self.hover_background = [min(1.0, c * 1.2) for c in self.original_background[:3]] + [self.original_background[3]]
        self.base_size = None
        
    def on_enter(self):
        """Hover enter - scale up and brighten"""
        if not self.base_size:
            self.base_size = self.size_hint or (None, None)
        
        # Scale animation
        anim = Animation(
            size_hint=(self.base_size[0] * 1.05 if self.base_size[0] else None, 
                      self.base_size[1] * 1.05 if self.base_size[1] else None),
            background_color=self.hover_background,
            duration=0.2
        )
        anim.start(self)
    
    def on_leave(self):
        """Hover leave - scale down and restore color"""
        if not self.base_size:
            return
            
        anim = Animation(
            size_hint=self.base_size,
            background_color=self.original_background,
            duration=0.2
        )
        anim.start(self)
    
    def on_touch_down(self, touch):
        """Add ripple effect on click"""
        if self.collide_point(*touch.pos):
            self.create_ripple(touch.pos)
        return super().on_touch_down(touch)


class TypewriterLabel(Label):
    """
    Label with typewriter effect support
    """
    pass


class HistoriaPyApp(App):
    """Main application class"""
    
    def build(self):
        """Build the app"""
        # Register custom widgets
        Factory.register('AnimatedHoverButton', cls=AnimatedHoverButton)
        Factory.register('TypewriterLabel', cls=TypewriterLabel)
        
        # Initialize controller
        self.controller = GameController()
        self.selected_character = 'jason'
        
        # Load kv file
        Builder.load_file('views.kv')
        
        # Create screen manager
        sm = ScreenManager(transition=FadeTransition())
        self.controller.screen_manager = sm
        
        # Add screens manually (kv uses @Screen which doesn't auto-add)
        from kivy.uix.screenmanager import Screen
        
        # We need to create a menu screen programmatically or use kv properly
        # For now, load from kv dynamically
        
        Logger.info("HistoriaPy: Application started")
        return sm
    
    def on_start(self):
        """Called when app starts"""
        # Add screens after kv is loaded
        sm = self.root
        
        # Add all screens
        sm.add_widget(MainMenuScreen())
        sm.add_widget(CharacterSelectScreen())
        sm.add_widget(DifficultySelectScreen())
        sm.add_widget(GameScreen())
        sm.add_widget(StatsScreen())
        sm.add_widget(CreditsScreen())
        
        Logger.info("HistoriaPy: App ready")


def main():
    """Main entry point"""
    HistoriaPyApp().run()


if __name__ == '__main__':
    main()
