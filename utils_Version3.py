# utils.py
"""
Utility helpers: debounce decorator and enhanced typewriter scheduler (with cancel and optional sound callback).
"""
from functools import wraps
import time
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import os

def debounce(wait_seconds):
    """
    Decorator that prevents a function from being called more than once within wait_seconds.
    """
    def decorator(func):
        last_time_attr = '_last_call_' + func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            last = getattr(wrapper, last_time_attr, 0)
            if now - last < wait_seconds:
                return None
            setattr(wrapper, last_time_attr, now)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def _load_sound_once(path):
    # simple caching for tiny UI sounds
    if not hasattr(_load_sound_once, '_cache'):
        _load_sound_once._cache = {}
    cache = _load_sound_once._cache
    if not path or not os.path.exists(path):
        return None
    if path in cache:
        return cache[path]
    s = SoundLoader.load(path)
    if s:
        cache[path] = s
    return s


def typewriter_schedule(label, full_text, speed=0.02, sound_key=None, on_complete=None):
    """
    Animate label text (typewriter effect). Returns the scheduled event (ClockEvent) which can be cancelled.

    Parameters:
    - label: Kivy Label instance (will update label.text)
    - full_text: full string to type
    - speed: seconds per character
    - sound_key: optional path-to-sound or key (if your controller plays sound use callback)
    - on_complete: optional callable to execute when complete
    """
    # Cancel any previous schedule stored on label
    if hasattr(label, '_typewriter_event') and label._typewriter_event:
        try:
            label._typewriter_event.cancel()
        except Exception:
            pass
        label._typewriter_event = None

    label.text = ''
    index = {'pos': 0}

    # Optional tiny typing sound (local path)
    sound = None
    if sound_key and os.path.exists(sound_key):
        sound = _load_sound_once(sound_key)

    def _step(dt):
        if index['pos'] >= len(full_text):
            # complete
            try:
                if callable(on_complete):
                    on_complete()
            except Exception:
                pass
            # cleanup
            if hasattr(label, '_typewriter_event'):
                label._typewriter_event = None
            return False
        index['pos'] += 1
        label.text = full_text[:index['pos']]
        # gentle sound cue
        if sound:
            try:
                sound.stop()
                sound.play()
            except Exception:
                pass
        return True

    event = Clock.schedule_interval(_step, speed)
    # store handle on label for external cancellation
    label._typewriter_event = event
    return event