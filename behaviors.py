"""
behaviors.py - Custom Kivy behaviors for hover and ripple effects
"""
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window


class HoverBehavior:
    """
    Lightweight hover behavior that detects mouse enter/leave events.
    Add this to any widget to get hover functionality.
    """
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)
    
    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')
    
    def on_enter(self):
        """Triggered when mouse enters the widget"""
        pass
    
    def on_leave(self):
        """Triggered when mouse leaves the widget"""
        pass


class RippleBehavior:
    """
    Lightweight ripple behavior that provides a hook for ripple effects.
    Override ripple_show() to implement custom ripple animations.
    """
    ripple_duration = 0.5
    ripple_color = [1, 1, 1, 0.3]
    
    def __init__(self, **kwargs):
        super(RippleBehavior, self).__init__(**kwargs)
    
    def ripple_show(self, touch):
        """
        Hook method for showing ripple effect.
        Override this in subclasses to implement custom ripple.
        """
        pass
    
    def on_touch_down(self, touch):
        """Detect touch and trigger ripple"""
        if self.collide_point(*touch.pos):
            self.ripple_show(touch)
        return super(RippleBehavior, self).on_touch_down(touch)
