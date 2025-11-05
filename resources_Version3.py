# resources.py
"""
ResourceManager: caching images and textures. Adds get_texture for quick access
and a more robust preload_all that tolerates missing files.
"""
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader
from kivy.uix.image import AsyncImage
import os

class ResourceManager:
    def __init__(self):
        self._image_cache = {}
        self._texture_cache = {}
        self._sound_cache = {}

    def load_image(self, path):
        """
        Return CoreImage instance (cached). If file missing return None.
        """
        if not path:
            return None
        if path in self._image_cache:
            return self._image_cache[path]
        if not os.path.exists(path):
            return None
        try:
            img = CoreImage(path)
            self._image_cache[path] = img
            return img
        except Exception:
            # fallback: return None
            return None

    def get_texture(self, path):
        """
        Return a Kivy texture object for faster drawing (cached).
        """
        if not path:
            return None
        if path in self._texture_cache:
            return self._texture_cache[path]
        try:
            ci = self.load_image(path)
            if ci:
                tex = ci.texture
                self._texture_cache[path] = tex
                return tex
        except Exception:
            pass
        return None

    def load_sound(self, path):
        if not path:
            return None
        if path in self._sound_cache:
            return self._sound_cache[path]
        if not os.path.exists(path):
            return None
        s = SoundLoader.load(path)
        self._sound_cache[path] = s
        return s

    def preload_all(self, model):
        # Iterate story nodes and preload images/textures
        for diff, story in model.stories.items():
            for node in story.values():
                img = node.get('image')
                if img:
                    try:
                        # prefer texture caching
                        self.get_texture(img)
                    except Exception:
                        pass
        # preload some common UI sounds if they exist
        for sname in ['assets/sounds/click.wav', 'assets/sounds/transition.wav', 'assets/sounds/type.wav']:
            if os.path.exists(sname):
                try:
                    self.load_sound(sname)
                except Exception:
                    pass