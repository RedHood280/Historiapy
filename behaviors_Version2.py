# behaviors.py
"""
Hover and small visual behavior mixins for Kivy widgets.

Provides:
- HoverBehavior: dispatches on_enter/on_leave events when mouse moves over widget.
- RippleBehavior: small placeholder for future ripple effects (simple interface).
"""
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher

class HoverBehavior(EventDispatcher):
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        # Ensure the widget using this mixin calls super().__init__()
        super().__init__(**kwargs)
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        # bind once; multiple bindings safe
        Window.bind(mouse_pos=self._on_mouse_pos)

    def _on_mouse_pos(self, window, pos):
        # Only consider widgets already in the window
        root = getattr(self, 'get_root_window', lambda: None)()
        if not root:
            return
        try:
            inside = self.collide_point(*self.to_widget(*pos))
        except Exception:
            # Some composite widgets may not implement to_widget; fallback
            inside = self.collide_point(*pos)
        if inside and not self.hovered:
            self.hovered = True
            self.dispatch('on_enter')
        elif not inside and self.hovered:
            self.hovered = False
            self.dispatch('on_leave')

    def on_enter(self, *args):
        # override in user class
        pass

    def on_leave(self, *args):
        # override in user class
        pass


class RippleBehavior:
    """
    Placeholder/small helper for ripple visuals.
    You can extend this to draw a ripple canvas instruction when pressed.
    This is intentionally lightweight and non-blocking.
    """
    def start_ripple(self, touch_pos, duration=0.35):
        # Implementations can override to draw ripple at touch_pos
        return None