"""
Custom widgets for the game UI
Includes AnimatedHoverButton with hover/press effects and TypewriterLabel
"""
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from behaviors import HoverBehavior, RippleBehavior
from resources import get_resource_manager


class AnimatedHoverButton(HoverBehavior, RippleBehavior, Button):
    """
    Button with hover and press animations.
    Changes color on hover and scales on press.
    """
    
    hover_color = ListProperty([0.8, 0.2, 0.2, 1])  # Lighter red on hover
    normal_color = ListProperty([0.7, 0.13, 0.13, 1])  # Normal red
    press_color = ListProperty([0.5, 0.1, 0.1, 1])  # Darker red on press
    
    def __init__(self, **kwargs):
        super(AnimatedHoverButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = self.normal_color
        self._original_size = None
        self._is_pressed = False
    
    def on_enter(self):
        """Animate color change on hover"""
        if not self._is_pressed:
            Animation(background_color=self.hover_color, duration=0.2).start(self)
    
    def on_leave(self):
        """Animate color back to normal"""
        if not self._is_pressed:
            Animation(background_color=self.normal_color, duration=0.2).start(self)
    
    def on_press(self):
        """Handle press - change color and play sound"""
        super(AnimatedHoverButton, self).on_press()
        self._is_pressed = True
        
        # Color change
        Animation(background_color=self.press_color, duration=0.1).start(self)
        
        # Play click sound if available
        resource_manager = get_resource_manager()
        resource_manager.play_sound("click.wav", volume=0.5)
    
    def on_release(self):
        """Handle release - restore hover color"""
        super(AnimatedHoverButton, self).on_release()
        self._is_pressed = False
        
        # Restore to hover color if still hovering, else normal
        target_color = self.hover_color if self.hovered else self.normal_color
        Animation(background_color=target_color, duration=0.2).start(self)


class TypewriterLabel(Label):
    """
    Label that displays text gradually with typewriter effect.
    Supports optional typing sound and completion callback.
    """
    
    full_text = ""
    typewriter_interval = NumericProperty(0.05)  # Seconds between characters
    on_complete_callback = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(TypewriterLabel, self).__init__(**kwargs)
        self._cancel_typewriter = None
        self._current_index = 0
        self._scheduled_event = None
        self._typing_sound = None
        
        # Try to load typing sound
        resource_manager = get_resource_manager()
        self._typing_sound = resource_manager.get_sound("type.wav")
    
    def set_text(self, text, on_complete=None):
        """
        Set text to display with typewriter effect.
        
        Args:
            text: Full text to display
            on_complete: Callback function to call when text is fully displayed
        """
        # Cancel any existing typewriter effect
        self.cancel_typewriter()
        
        # Store full text and callback
        self.full_text = text
        self.on_complete_callback = on_complete
        
        # Reset state
        self.text = ""
        self._current_index = 0
        
        # Start typewriter effect
        if text:
            self._scheduled_event = Clock.schedule_interval(
                self._add_character, 
                self.typewriter_interval
            )
    
    def _add_character(self, dt):
        """Add one character to displayed text"""
        if self._current_index < len(self.full_text):
            self.text += self.full_text[self._current_index]
            self._current_index += 1
            
            # Play typing sound (every 2nd character to avoid overwhelming)
            if self._typing_sound and self._current_index % 2 == 0:
                try:
                    self._typing_sound.volume = 0.3
                    self._typing_sound.play()
                except Exception as e:
                    print(f"Error playing typing sound: {e}")
        else:
            # Text complete
            self.cancel_typewriter()
            if self.on_complete_callback:
                try:
                    self.on_complete_callback()
                except Exception as e:
                    print(f"Error in on_complete callback: {e}")
    
    def cancel_typewriter(self):
        """Cancel the typewriter effect and show full text immediately"""
        if self._scheduled_event:
            self._scheduled_event.cancel()
            self._scheduled_event = None
        
        # Show full text
        if self.full_text and self.text != self.full_text:
            self.text = self.full_text
    
    def skip_to_end(self):
        """Skip animation and show full text immediately"""
        self.cancel_typewriter()
        if self.on_complete_callback:
            try:
                self.on_complete_callback()
            except Exception as e:
                print(f"Error in on_complete callback: {e}")
