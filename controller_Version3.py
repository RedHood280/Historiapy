# controller.py
"""
GameController: mediates between the GameModel and Kivy UI.
Added: play_transition_animation(widget) to provide light cross-fade.
"""
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
import os
import time

from utils import debounce

class GameController:
    def __init__(self, model, app):
        self.model = model
        self.app = app
        self._debounce_state = {}
        # pre-load interface sounds
        self.sounds = {
            'click': SoundLoader.load('assets/sounds/click.wav') if os.path.exists('assets/sounds/click.wav') else None,
            'transition': SoundLoader.load('assets/sounds/transition.wav') if os.path.exists('assets/sounds/transition.wav') else None,
            'type': SoundLoader.load('assets/sounds/type.wav') if os.path.exists('assets/sounds/type.wav') else None,
        }

    def play_sound(self, key):
        s = self.sounds.get(key)
        if s:
            try:
                s.volume = 0.6
                s.stop()
                s.play()
            except Exception:
                pass

    def start_new_game(self, player_key, difficulty_key):
        self.play_sound('transition')
        self.model.new_game(player_key, difficulty_key)
        return self.model.get_current_node()

    @debounce(0.4)
    def choose_option(self, idx, ui_callback=None):
        # quick visual transition on main area if available
        try:
            # attempt to find main_area widget and animate opacity for a cross-fade feel
            main_area = getattr(self.app.root, 'ids', {}).get('screen_manager')
            # Not guaranteed; safe-guard
        except Exception:
            main_area = None

        # Apply choice (this mutates model)
        choice = self.model.choose(idx)
        node = self.model.get_current_node()

        # Play a small transition animation if possible (UI will handle most)
        # We just play sound here
        self.play_sound('click')

        # Auto-save after each choice
        try:
            self.model.save()
        except Exception:
            pass

        # Callback to UI to update visuals (async safe)
        if ui_callback:
            Clock.schedule_once(lambda dt: ui_callback(choice, node), 0)
        return choice, node

    def save_game(self, path=None, auto=False):
        saved_path = self.model.save(path)
        if not auto:
            self.play_sound('click')
        return saved_path

    def load_game(self, path=None):
        loaded = self.model.load(path)
        return loaded

    def get_progress(self):
        return self.model.quick_progress()

    def get_palette(self):
        player = self.model.session.get('player')
        return self.app.palette_for(player) if player else self.app.palette_for('jason')

    def preload_images(self):
        self.app.resources.preload_all(self.model)

    def play_transition_animation(self, widget, duration=0.28):
        """
        Lightweight cross-fade animation for a target widget (animates opacity down/up).
        """
        try:
            Animation.cancel_all(widget, 'opacity')
            half = duration / 2.0
            Animation(opacity=0.6, d=half).start(widget)
            Clock.schedule_once(lambda dt: Animation(opacity=1.0, d=half).start(widget), half)
            # play transition sound if present
            self.play_sound('transition')
        except Exception:
            pass