"""
Custom behaviors for widgets
Provides HoverBehavior and RippleBehavior for enhanced UI interactions
"""
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.animation import Animation


class HoverBehavior:
    """
    Mixin class to add hover detection to widgets.
    Adds 'hovered' property and 'on_enter'/'on_leave' events.
    """
    
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)
    
    def on_mouse_pos(self, *args):
        """Check if mouse is over widget"""
        if not self.get_root_window():
            return
        
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        
        if inside and not self.hovered:
            self.hovered = True
            self.dispatch('on_enter')
        elif not inside and self.hovered:
            self.hovered = False
            self.dispatch('on_leave')
    
    def on_enter(self):
        """Fired when mouse enters widget"""
        pass
    
    def on_leave(self):
        """Fired when mouse leaves widget"""
        pass


class RippleBehavior:
    """
    Mixin class to add ripple effect on press.
    Animates a scale effect when the widget is pressed.
    """
    
    ripple_scale = 1.0
    
    def __init__(self, **kwargs):
        super(RippleBehavior, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        """Handle touch down with ripple effect"""
        if self.collide_point(*touch.pos):
            # Animate scale down
            anim = Animation(ripple_scale=0.95, duration=0.1)
            anim.start(self)
        return super(RippleBehavior, self).on_touch_down(touch)
    
    def on_touch_up(self, touch):
        """Handle touch up - restore scale"""
        if self.collide_point(*touch.pos):
            # Animate scale back up
            anim = Animation(ripple_scale=1.0, duration=0.1)
            anim.start(self)
        return super(RippleBehavior, self).on_touch_up(touch)
