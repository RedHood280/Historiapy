"""
resources.py - Resource management for images, textures, and sounds
"""
import os
from kivy.core.image import Image
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader


class ResourceManager:
    """
    Manages loading and caching of game resources (images, textures, sounds).
    """
    
    def __init__(self):
        self._image_cache = {}
        self._texture_cache = {}
        self._sound_cache = {}
        self.assets_path = 'assets'
        self.images_path = os.path.join(self.assets_path, 'images')
        self.sounds_path = os.path.join(self.assets_path, 'sounds')
        
        # Create asset directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure asset directories exist"""
        for path in [self.assets_path, self.images_path, self.sounds_path]:
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except:
                    pass
    
    def get_image(self, image_name, reload=False):
        """
        Get a cached image or load it.
        
        Args:
            image_name: Name of the image file
            reload: If True, reload the image even if cached
        
        Returns:
            Kivy Image object or None if not found
        """
        if not reload and image_name in self._image_cache:
            return self._image_cache[image_name]
        
        image_path = os.path.join(self.images_path, image_name)
        
        # Try to load the image
        if os.path.exists(image_path):
            try:
                img = Image(image_path)
                self._image_cache[image_name] = img
                return img
            except Exception as e:
                print(f"Error loading image {image_name}: {e}")
        
        return None
    
    def get_texture(self, image_name, reload=False):
        """
        Get a cached texture or load it from an image.
        
        Args:
            image_name: Name of the image file
            reload: If True, reload the texture even if cached
        
        Returns:
            Kivy Texture object or None if not found
        """
        if not reload and image_name in self._texture_cache:
            return self._texture_cache[image_name]
        
        img = self.get_image(image_name, reload)
        if img:
            texture = img.texture
            self._texture_cache[image_name] = texture
            return texture
        
        return None
    
    def get_sound(self, sound_name, reload=False):
        """
        Get a cached sound or load it.
        
        Args:
            sound_name: Name of the sound file (without .wav extension)
            reload: If True, reload the sound even if cached
        
        Returns:
            Kivy Sound object or None if not found
        """
        if not reload and sound_name in self._sound_cache:
            return self._sound_cache[sound_name]
        
        sound_path = os.path.join(self.sounds_path, f'{sound_name}.wav')
        
        # Try to load the sound
        if os.path.exists(sound_path):
            try:
                sound = SoundLoader.load(sound_path)
                if sound:
                    self._sound_cache[sound_name] = sound
                    return sound
            except Exception as e:
                print(f"Error loading sound {sound_name}: {e}")
        
        return None
    
    def preload_images(self, image_names):
        """
        Preload a list of images into cache.
        Tolerant to missing files - will skip any that don't exist.
        
        Args:
            image_names: List of image file names
        """
        for image_name in image_names:
            self.get_image(image_name)
    
    def preload_sounds(self, sound_names):
        """
        Preload a list of sounds into cache.
        Tolerant to missing files - will skip any that don't exist.
        
        Args:
            sound_names: List of sound names (without .wav extension)
        """
        for sound_name in sound_names:
            self.get_sound(sound_name)
    
    def preload_common_assets(self):
        """
        Preload commonly used assets to avoid lag during gameplay.
        """
        # Common sound effects
        common_sounds = ['click', 'transition', 'type']
        self.preload_sounds(common_sounds)
        
        # Add common images here if needed
        # common_images = ['background.png', 'logo.png']
        # self.preload_images(common_images)
    
    def clear_cache(self):
        """Clear all cached resources"""
        self._image_cache.clear()
        self._texture_cache.clear()
        self._sound_cache.clear()
    
    def clear_image_cache(self):
        """Clear only image cache"""
        self._image_cache.clear()
        self._texture_cache.clear()
    
    def clear_sound_cache(self):
        """Clear only sound cache"""
        self._sound_cache.clear()


# Global resource manager instance
_resource_manager = None


def get_resource_manager():
    """Get the global resource manager instance"""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager
