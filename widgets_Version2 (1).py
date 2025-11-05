# widgets.py
"""
Custom UI widgets:
- AnimatedHoverButton: ButtonBehavior + Label + HoverBehavior
  Animates scale and background color on hover/press, exposes tooltip_text property.
- TypewriterLabel: Label that types text with utils.typewriter_schedule and supports on_complete callback.
"""
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock

from behaviors import HoverBehavior
import utils

class AnimatedHoverButton(ButtonBehavior, Label, HoverBehavior):
    scale = NumericProperty(1.0)
    bg_color = ListProperty([0.18, 0.18, 0.18, 1])
    hover_color = ListProperty([0.28, 0.28, 0.28, 1])
    press_color = ListProperty([0.12, 0.12, 0.12, 1])
    tooltip_text = StringProperty('')
    anim_duration = NumericProperty(0.12)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ensure events exist
        self.floating_anim = None
        # Bind our enter/leave to triggers
        self.bind(on_enter=lambda *a: self._on_hover_enter())
        self.bind(on_leave=lambda *a: self._on_hover_leave())

    def _on_hover_enter(self):
        # animate scale up and lighten background
        Animation.cancel_all(self, 'scale')
        Animation.cancel_all(self, 'bg_color')
        Animation(scale=1.04, d=self.anim_duration).start(self)
        Animation(bg_color=self.hover_color, d=self.anim_duration).start(self)

    def _on_hover_leave(self):
        Animation.cancel_all(self, 'scale')
        Animation.cancel_all(self, 'bg_color')
        Animation(scale=1.0, d=self.anim_duration).start(self)
        Animation(bg_color=[0.18, 0.18, 0.18, 1], d=self.anim_duration).start(self)

    def on_press(self):
        # quick press animation
        Animation.cancel_all(self, 'scale')
        Animation(scale=0.98, d=0.06).start(self)
        Animation(bg_color=self.press_color, d=0.06).start(self)
        return super().on_press()

    def on_release(self):
        # restore to hovered or normal state
        if getattr(self, 'hovered', False):
            Animation(scale=1.03, d=0.08).start(self)
            Animation(bg_color=self.hover_color, d=0.08).start(self)
        else:
            Animation(scale=1.0, d=0.08).start(self)
            Animation(bg_color=[0.18, 0.18, 0.18, 1], d=0.08).start(self)
        return super().on_release()


class TypewriterLabel(Label):
    typewriter = BooleanProperty(False)
    full_text = StringProperty('')
    speed = NumericProperty(0.02)
    on_complete = ObjectProperty(None, allownone=True)
    sound_key = StringProperty('assets/sounds/type.wav')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._type_event = None
        # When full_text changes and typewriter is False, show immediately
        self.bind(full_text=self._on_full_text)
        self.bind(typewriter=self._on_typewriter)

    def _on_full_text(self, instance, value):
        if not self.typewriter:
            self.text = value

    def _on_typewriter(self, instance, value):
        # start or stop typing
        if value:
            # cancel previous if any
            if getattr(self, '_type_event', None):
                try:
                    self._type_event.cancel()
                except Exception:
                    pass
                self._type_event = None
            # schedule new typewriter via utils helper
            self._type_event = utils.typewriter_schedule(self, self.full_text, speed=self.speed, sound_key=self.sound_key, on_complete=self._on_complete_internal)
        else:
            # cancel and show full text
            if getattr(self, '_type_event', None):
                try:
                    self._type_event.cancel()
                except Exception:
                    pass
                self._type_event = None
            self.text = self.full_text
            if callable(self.on_complete):
                Clock.schedule_once(lambda dt: self.on_complete(), 0)

    def _on_complete_internal(self):
        self._type_event = None
        if callable(self.on_complete):
            try:
                self.on_complete()
            except Exception:
                pass