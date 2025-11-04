"""
Custom behaviors for widgets - hover, ripple effects, etc.
"""
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ListProperty
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget


class HoverBehavior:
    """
    Hover behavior for widgets - detects mouse enter/leave
    Mix this into any widget class to add hover detection
    """
    hovered = BooleanProperty(False)
    border_point = ListProperty([0, 0])
    
    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)
    
    def on_mouse_pos(self, window, pos):
        """Track mouse position"""
        if not self.get_root_window():
            return
        
        # Check if mouse is inside widget bounds
        inside = self.collide_point(*self.to_widget(*pos))
        
        if inside and not self.hovered:
            self.hovered = True
            self.dispatch('on_enter')
        elif not inside and self.hovered:
            self.hovered = False
            self.dispatch('on_leave')
    
    def on_enter(self):
        """Called when mouse enters widget"""
        pass
    
    def on_leave(self):
        """Called when mouse leaves widget"""
        pass


class RippleBehavior:
    """
    Simple ripple effect behavior for buttons
    Mix this into button widgets for click ripple effect
    """
    ripple_color = ListProperty([1, 1, 1, 0.5])
    ripple_duration = 0.5
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def create_ripple(self, touch_pos):
        """Create ripple effect at touch position"""
        if not self.collide_point(*touch_pos):
            return
            
        with self.canvas.after:
            # Create ripple circle
            ripple_color = Color(*self.ripple_color)
            ripple_size = max(self.width, self.height) * 2
            
            # Center ripple on touch point (convert to widget coordinates)
            local_pos = self.to_widget(*touch_pos)
            ripple = Ellipse(
                pos=(local_pos[0] - ripple_size/2, local_pos[1] - ripple_size/2),
                size=(0, 0)
            )
            
            # Animate ripple expanding and fading
            anim = Animation(
                size=(ripple_size, ripple_size),
                duration=self.ripple_duration
            )
            
            # Fade out color
            color_anim = Animation(
                a=0,
                duration=self.ripple_duration
            )
            
            def cleanup(*args):
                """Remove ripple after animation"""
                self.canvas.after.remove(ripple_color)
                self.canvas.after.remove(ripple)
            
            anim.bind(on_complete=cleanup)
            color_anim.start(ripple_color)
            anim.start(ripple)
