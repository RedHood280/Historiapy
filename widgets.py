"""
widgets.py - Custom Kivy widgets for the game
"""
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty, NumericProperty, BooleanProperty, 
    ColorProperty, ObjectProperty
)
from kivy.animation import Animation
from behaviors import HoverBehavior
from utils import typewriter_schedule


class AnimatedHoverButton(ButtonBehavior, Label, HoverBehavior):
    """
    Custom button that combines ButtonBehavior, Label, and HoverBehavior.
    Features:
    - Scale and color animation on hover
    - Scale animation on press
    - Optional tooltip text
    - Configurable animation duration
    """
    
    # Properties
    tooltip_text = StringProperty('')
    anim_duration = NumericProperty(0.2)
    hover_scale = NumericProperty(1.05)
    press_scale = NumericProperty(0.95)
    normal_color = ColorProperty([0.8, 0.1, 0.1, 1])  # Red
    hover_color = ColorProperty([1, 0.2, 0.2, 1])  # Brighter red
    press_color = ColorProperty([0.6, 0.05, 0.05, 1])  # Darker red
    
    def __init__(self, **kwargs):
        super(AnimatedHoverButton, self).__init__(**kwargs)
        self.background_color = self.normal_color
        self.color = [1, 1, 1, 1]  # White text
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=self.on_size)
        self._is_pressed = False
    
    def on_size(self, *args):
        """Ensure text wraps properly"""
        self.text_size = self.size
    
    def on_enter(self):
        """Animate on mouse enter"""
        if not self._is_pressed:
            # Scale up
            anim = Animation(
                scale_x=self.hover_scale,
                scale_y=self.hover_scale,
                duration=self.anim_duration
            )
            anim.start(self)
            
            # Color change
            self.background_color = self.hover_color
    
    def on_leave(self):
        """Animate on mouse leave"""
        if not self._is_pressed:
            # Scale back to normal
            anim = Animation(
                scale_x=1.0,
                scale_y=1.0,
                duration=self.anim_duration
            )
            anim.start(self)
            
            # Color back to normal
            self.background_color = self.normal_color
    
    def on_press(self):
        """Animate on button press"""
        self._is_pressed = True
        
        # Scale down
        anim = Animation(
            scale_x=self.press_scale,
            scale_y=self.press_scale,
            duration=self.anim_duration / 2
        )
        anim.start(self)
        
        # Darker color
        self.background_color = self.press_color
    
    def on_release(self):
        """Animate on button release"""
        self._is_pressed = False
        
        # If still hovering, go back to hover state
        if self.hovered:
            anim = Animation(
                scale_x=self.hover_scale,
                scale_y=self.hover_scale,
                duration=self.anim_duration / 2
            )
            anim.start(self)
            self.background_color = self.hover_color
        else:
            # Otherwise, go back to normal
            anim = Animation(
                scale_x=1.0,
                scale_y=1.0,
                duration=self.anim_duration / 2
            )
            anim.start(self)
            self.background_color = self.normal_color


class TypewriterLabel(Label):
    """
    Custom label with typewriter effect.
    Text appears character by character with optional sound and completion callback.
    """
    
    # Properties
    full_text = StringProperty('')
    typewriter = BooleanProperty(False)
    typewriter_interval = NumericProperty(0.05)
    sound_key = StringProperty('')
    on_complete = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(TypewriterLabel, self).__init__(**kwargs)
        self._typewriter_schedule = None
        self.bind(full_text=self._on_full_text_change)
    
    def _on_full_text_change(self, instance, value):
        """Start typewriter effect when full_text changes"""
        if self.typewriter and value:
            self.start_typewriter()
        else:
            self.text = value
    
    def start_typewriter(self):
        """Start the typewriter effect"""
        # Cancel any existing effect
        if self._typewriter_schedule:
            self._typewriter_schedule.cancel()
        
        # Start new effect
        sound_key = self.sound_key if self.sound_key else None
        on_complete = self.on_complete if self.on_complete else None
        
        self._typewriter_schedule = typewriter_schedule(
            label=self,
            full_text=self.full_text,
            interval=self.typewriter_interval,
            sound_key=sound_key,
            on_complete=on_complete
        )
    
    def cancel_typewriter(self):
        """Cancel the typewriter effect and show full text"""
        if self._typewriter_schedule:
            self._typewriter_schedule.cancel()
            self._typewriter_schedule = None
    
    def skip_to_end(self):
        """Skip to the end of the typewriter effect"""
        self.cancel_typewriter()
        self.text = self.full_text
