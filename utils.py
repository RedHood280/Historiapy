"""
Utility functions and helpers
"""
from functools import wraps
from time import time
from kivy.clock import Clock
from typing import Callable, Optional


# Debounce decorator
def debounce(wait: float = 0.5):
    """
    Decorator that prevents a function from being called more than once every wait seconds
    """
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def debounced(*args, **kwargs):
            current_time = time()
            if current_time - last_called[0] >= wait:
                last_called[0] = current_time
                return func(*args, **kwargs)
        
        return debounced
    return decorator


class TypewriterEffect:
    """
    Enhanced typewriter effect with sound, cancellation, and completion callback
    """
    def __init__(self, text: str, label, interval: float = 0.03, 
                 sound_callback: Optional[Callable] = None,
                 on_complete: Optional[Callable] = None):
        self.text = text
        self.label = label
        self.interval = interval
        self.sound_callback = sound_callback
        self.on_complete = on_complete
        self.current_index = 0
        self.event = None
        self.cancelled = False
        
    def start(self):
        """Start the typewriter effect"""
        self.label.text = ""
        self.current_index = 0
        self.cancelled = False
        self.event = Clock.schedule_interval(self._update, self.interval)
        
    def _update(self, dt):
        """Update callback for each character"""
        if self.cancelled:
            if self.event:
                self.event.cancel()
            return False
            
        if self.current_index < len(self.text):
            self.label.text += self.text[self.current_index]
            self.current_index += 1
            
            # Play typing sound
            if self.sound_callback and self.current_index % 3 == 0:  # Every 3 chars
                self.sound_callback()
            
            return True
        else:
            # Completed
            if self.on_complete:
                self.on_complete()
            return False
    
    def cancel(self):
        """Cancel the typewriter effect"""
        self.cancelled = True
        if self.event:
            self.event.cancel()
            self.event = None
        # Show full text immediately
        self.label.text = self.text
    
    def skip(self):
        """Skip to end of text"""
        self.cancel()


def typewriter_schedule(text: str, label, interval: float = 0.03,
                       sound_callback: Optional[Callable] = None,
                       on_complete: Optional[Callable] = None) -> TypewriterEffect:
    """
    Schedule typewriter effect on a label
    
    Args:
        text: Text to display
        label: Kivy label widget
        interval: Time between characters
        sound_callback: Optional callback for typing sound
        on_complete: Optional callback when complete
    
    Returns:
        TypewriterEffect instance (can be used to cancel/skip)
    """
    effect = TypewriterEffect(text, label, interval, sound_callback, on_complete)
    effect.start()
    return effect
