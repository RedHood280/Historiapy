"""
Utility functions for the game
Includes debounce and typewriter effect scheduling
"""
from functools import wraps
import time
from kivy.clock import Clock


def debounce(wait_time=0.5):
    """
    Decorator to prevent function from being called multiple times rapidly.
    Protects against accidental double-clicks on buttons.
    
    Args:
        wait_time: Minimum time (seconds) between function calls
    """
    def decorator(func):
        last_called = [0.0]  # Use list to allow modification in nested function
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - last_called[0] >= wait_time:
                last_called[0] = current_time
                return func(*args, **kwargs)
            else:
                print(f"Debounced: {func.__name__} called too soon")
                return None
        
        return wrapper
    return decorator


def typewriter_schedule(text, label, interval=0.05, sound_callback=None, on_complete=None):
    """
    Display text gradually with typewriter effect using Kivy's Clock.
    
    Args:
        text: The complete text to display
        label: The label widget to update
        interval: Time between each character (seconds)
        sound_callback: Optional function to call for each character (for typing sound)
        on_complete: Optional callback when text is fully displayed
    
    Returns:
        Function to cancel the scheduled events
    """
    if not text:
        if on_complete:
            on_complete()
        return lambda: None
    
    # Store state
    current_index = [0]
    scheduled_events = []
    
    # Clear label
    label.text = ""
    
    def add_char(dt):
        if current_index[0] < len(text):
            label.text += text[current_index[0]]
            current_index[0] += 1
            
            # Play sound for this character
            if sound_callback:
                try:
                    sound_callback()
                except Exception as e:
                    print(f"Sound callback error: {e}")
        else:
            # Text complete - cancel remaining events and call completion callback
            cancel_typewriter()
            if on_complete:
                try:
                    on_complete()
                except Exception as e:
                    print(f"On complete callback error: {e}")
    
    # Schedule character addition
    event = Clock.schedule_interval(add_char, interval)
    scheduled_events.append(event)
    
    def cancel_typewriter():
        """Cancel all scheduled typewriter events"""
        for evt in scheduled_events:
            evt.cancel()
        scheduled_events.clear()
    
    return cancel_typewriter


def format_stat_text(health, reputation, resources):
    """Format stats for display"""
    return f"❤️ Health: {health}/100  ⭐ Reputation: {reputation}/100  💎 Resources: {resources}"


def safe_file_exists(filepath):
    """Safely check if a file exists without raising exceptions"""
    try:
        import os
        return os.path.exists(filepath)
    except Exception:
        return False
