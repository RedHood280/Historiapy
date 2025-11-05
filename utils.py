"""
utils.py - Utility functions for the Kivy app
"""
import time
from functools import wraps
from kivy.clock import Clock


# Debounce functionality
_debounce_timers = {}


def debounce(wait_time=0.3):
    """
    Decorator that prevents a function from being called more than once
    every wait_time seconds. Useful for preventing multi-click issues.
    
    Args:
        wait_time: Time in seconds to wait between function calls
    """
    def decorator(func):
        @wraps(func)
        def debounced(*args, **kwargs):
            key = id(func)
            
            def call_function(dt):
                _debounce_timers.pop(key, None)
                func(*args, **kwargs)
            
            # Cancel previous timer if exists
            if key in _debounce_timers:
                _debounce_timers[key].cancel()
            
            # Schedule new timer
            _debounce_timers[key] = Clock.schedule_once(call_function, wait_time)
        
        return debounced
    return decorator


# Typewriter effect
_typewriter_cache = {}  # Cache for loaded sounds


class TypewriterSchedule:
    """
    Cancelable typewriter effect scheduler.
    Displays text character by character with optional sound and completion callback.
    """
    def __init__(self, label, full_text, interval=0.05, sound_key=None, on_complete=None):
        """
        Initialize typewriter effect.
        
        Args:
            label: Label widget to display text in
            full_text: Full text to display
            interval: Time between characters in seconds
            sound_key: Optional sound key to play for each character ('type', 'click', etc.)
            on_complete: Optional callback when typing completes
        """
        self.label = label
        self.full_text = full_text
        self.interval = interval
        self.sound_key = sound_key
        self.on_complete = on_complete
        self.current_index = 0
        self.event = None
        self.is_active = True
        
        # Load sound if needed
        self.sound = None
        if sound_key:
            self.sound = self._load_sound(sound_key)
        
        # Start the effect
        self.label.text = ""
        self.event = Clock.schedule_interval(self._add_char, interval)
    
    def _load_sound(self, sound_key):
        """Load and cache sound"""
        global _typewriter_cache
        
        if sound_key in _typewriter_cache:
            return _typewriter_cache[sound_key]
        
        try:
            from kivy.core.audio import SoundLoader
            import os
            
            sound_path = os.path.join('assets', 'sounds', f'{sound_key}.wav')
            if os.path.exists(sound_path):
                sound = SoundLoader.load(sound_path)
                if sound:
                    _typewriter_cache[sound_key] = sound
                    return sound
        except Exception as e:
            print(f"Could not load sound {sound_key}: {e}")
        
        return None
    
    def _add_char(self, dt):
        """Add one character to the label"""
        if not self.is_active:
            return False
        
        if self.current_index < len(self.full_text):
            self.label.text += self.full_text[self.current_index]
            self.current_index += 1
            
            # Play sound if available
            if self.sound:
                try:
                    self.sound.play()
                except:
                    pass
            
            return True  # Continue
        else:
            # Completed
            self.is_active = False
            if self.on_complete:
                self.on_complete()
            return False  # Stop
    
    def cancel(self):
        """Cancel the typewriter effect"""
        self.is_active = False
        if self.event:
            self.event.cancel()
        # Show full text immediately
        self.label.text = self.full_text


def typewriter_schedule(label, full_text, interval=0.05, sound_key=None, on_complete=None):
    """
    Helper function to create a typewriter effect.
    
    Args:
        label: Label widget to display text in
        full_text: Full text to display
        interval: Time between characters in seconds
        sound_key: Optional sound key to play for each character
        on_complete: Optional callback when typing completes
    
    Returns:
        TypewriterSchedule instance (can be used to cancel the effect)
    """
    return TypewriterSchedule(label, full_text, interval, sound_key, on_complete)


# Sound playback helper
def play_sound(sound_key, volume=1.0):
    """
    Play a sound effect.
    
    Args:
        sound_key: Name of the sound file (without .wav extension)
        volume: Volume level (0.0 to 1.0)
    """
    try:
        from kivy.core.audio import SoundLoader
        import os
        
        sound_path = os.path.join('assets', 'sounds', f'{sound_key}.wav')
        if os.path.exists(sound_path):
            sound = SoundLoader.load(sound_path)
            if sound:
                sound.volume = volume
                sound.play()
    except Exception as e:
        print(f"Could not play sound {sound_key}: {e}")
