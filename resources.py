"""
Resource manager for images and sounds with caching and preloading
"""
import os
from typing import Dict, Optional
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader
from kivy.logger import Logger


class ResourceManager:
    """Manage game resources with caching"""
    
    def __init__(self):
        self._texture_cache: Dict[str, CoreImage] = {}
        self._sound_cache: Dict[str, any] = {}
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.sounds_path = os.path.join(os.path.dirname(__file__), "audio")
        
    def get_texture(self, path: str, default: str = ""):
        """
        Get texture from cache or load it
        
        Args:
            path: Path to image file (relative to assets folder)
            default: Default texture if file not found
            
        Returns:
            CoreImage texture or None
        """
        if not path:
            return None
            
        # Check cache first
        if path in self._texture_cache:
            return self._texture_cache[path]
        
        # Try to load
        full_path = os.path.join(self.assets_path, path) if not os.path.isabs(path) else path
        
        if not os.path.exists(full_path):
            Logger.warning(f"ResourceManager: Image not found: {full_path}")
            if default and default != path:
                return self.get_texture(default)
            return None
        
        try:
            texture = CoreImage(full_path)
            self._texture_cache[path] = texture
            return texture
        except Exception as e:
            Logger.error(f"ResourceManager: Error loading image {full_path}: {e}")
            return None
    
    def get_kivy_texture(self, path: str):
        """
        Get Kivy texture object (for use with Image widget)
        
        Args:
            path: Path to image file
            
        Returns:
            Texture object or None
        """
        img = self.get_texture(path)
        return img.texture if img else None
    
    def preload_images(self, paths: list, thumbnail_size: Optional[tuple] = None):
        """
        Preload multiple images into cache
        
        Args:
            paths: List of image paths to preload
            thumbnail_size: Optional (width, height) for thumbnail generation
        """
        for path in paths:
            if path and path not in self._texture_cache:
                self.get_texture(path)
                Logger.info(f"ResourceManager: Preloaded {path}")
    
    def get_sound(self, filename: str):
        """
        Get sound from cache or load it
        
        Args:
            filename: Sound filename (in audio folder)
            
        Returns:
            Sound object or None
        """
        if not filename:
            return None
            
        # Check cache
        if filename in self._sound_cache:
            return self._sound_cache[filename]
        
        # Try to load
        full_path = os.path.join(self.sounds_path, filename) if not os.path.isabs(filename) else filename
        
        if not os.path.exists(full_path):
            Logger.warning(f"ResourceManager: Sound not found: {full_path}")
            return None
        
        try:
            sound = SoundLoader.load(full_path)
            if sound:
                self._sound_cache[filename] = sound
                Logger.info(f"ResourceManager: Loaded sound {filename}")
            return sound
        except Exception as e:
            Logger.error(f"ResourceManager: Error loading sound {full_path}: {e}")
            return None
    
    def play_sound(self, filename: str, volume: float = 1.0):
        """
        Play a sound effect
        
        Args:
            filename: Sound filename
            volume: Volume (0.0 to 1.0)
        """
        sound = self.get_sound(filename)
        if sound:
            sound.volume = volume
            sound.play()
    
    def clear_cache(self):
        """Clear all cached resources"""
        self._texture_cache.clear()
        self._sound_cache.clear()
        Logger.info("ResourceManager: Cache cleared")


# Global instance
resource_manager = ResourceManager()
