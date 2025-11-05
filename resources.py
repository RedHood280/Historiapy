"""
Resource Manager - Handles images and sounds with caching
Preloads and caches assets, handles missing files gracefully
"""
import os
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader
from kivy.graphics.texture import Texture
from io import BytesIO


class ResourceManager:
    """Manages game resources (images, sounds) with caching and preloading"""
    
    def __init__(self):
        self.image_cache = {}
        self.sound_cache = {}
        self.texture_cache = {}
        self._placeholder_texture = None
    
    def get_texture(self, image_path, width=400, height=300):
        """
        Get texture for an image, with caching and placeholder fallback.
        
        Args:
            image_path: Path to image file (e.g., "assets/images/scene.png")
            width: Desired width
            height: Desired height
        
        Returns:
            Kivy Texture object
        """
        cache_key = f"{image_path}_{width}_{height}"
        
        # Return cached texture if available
        if cache_key in self.texture_cache:
            return self.texture_cache[cache_key]
        
        # Try to load the image
        full_path = image_path
        if not os.path.isabs(image_path):
            # Try common asset locations
            for base_dir in ["assets/images", "imagenes", "images", "."]:
                test_path = os.path.join(base_dir, image_path)
                if os.path.exists(test_path):
                    full_path = test_path
                    break
        
        texture = None
        if os.path.exists(full_path):
            try:
                # Load image
                core_image = CoreImage(full_path)
                texture = core_image.texture
                
                # Cache the texture
                self.texture_cache[cache_key] = texture
                print(f"Loaded texture: {image_path}")
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")
                texture = self._get_placeholder_texture(width, height)
        else:
            print(f"Image not found: {full_path}, using placeholder")
            texture = self._get_placeholder_texture(width, height)
        
        return texture
    
    def _get_placeholder_texture(self, width=400, height=300):
        """Create a placeholder texture for missing images"""
        if self._placeholder_texture is None:
            # Create a simple colored texture as placeholder
            size = (width, height)
            # Create RGB data (dark gray)
            data = bytes([30, 30, 30] * (width * height))
            
            texture = Texture.create(size=size)
            texture.blit_buffer(data, colorfmt='rgb', bufferfmt='ubyte')
            self._placeholder_texture = texture
        
        return self._placeholder_texture
    
    def preload_images(self, image_paths, width=400, height=300):
        """
        Preload multiple images into cache.
        
        Args:
            image_paths: List of image paths to preload
            width: Desired width
            height: Desired height
        """
        loaded = 0
        for image_path in image_paths:
            try:
                self.get_texture(image_path, width, height)
                loaded += 1
            except Exception as e:
                print(f"Error preloading {image_path}: {e}")
        
        print(f"Preloaded {loaded}/{len(image_paths)} images")
    
    def get_sound(self, sound_path):
        """
        Get a sound object, with caching.
        Returns None if sound file doesn't exist.
        
        Args:
            sound_path: Path to sound file (e.g., "assets/sounds/click.wav")
        
        Returns:
            Kivy Sound object or None
        """
        # Return cached sound if available
        if sound_path in self.sound_cache:
            return self.sound_cache[sound_path]
        
        # Try to load the sound
        full_path = sound_path
        if not os.path.isabs(sound_path):
            # Try common asset locations
            for base_dir in ["assets/sounds", "audio", "sounds", "."]:
                test_path = os.path.join(base_dir, sound_path)
                if os.path.exists(test_path):
                    full_path = test_path
                    break
        
        if os.path.exists(full_path):
            try:
                sound = SoundLoader.load(full_path)
                if sound:
                    self.sound_cache[sound_path] = sound
                    print(f"Loaded sound: {sound_path}")
                    return sound
                else:
                    print(f"Could not load sound: {full_path}")
            except Exception as e:
                print(f"Error loading sound {full_path}: {e}")
        else:
            print(f"Sound not found: {full_path}")
        
        return None
    
    def preload_sounds(self, sound_paths):
        """
        Preload multiple sounds into cache.
        
        Args:
            sound_paths: List of sound paths to preload
        """
        loaded = 0
        for sound_path in sound_paths:
            try:
                sound = self.get_sound(sound_path)
                if sound:
                    loaded += 1
            except Exception as e:
                print(f"Error preloading {sound_path}: {e}")
        
        print(f"Preloaded {loaded}/{len(sound_paths)} sounds")
    
    def play_sound(self, sound_path, volume=1.0):
        """
        Play a sound if it exists.
        
        Args:
            sound_path: Path to sound file
            volume: Volume level (0.0 to 1.0)
        """
        sound = self.get_sound(sound_path)
        if sound:
            try:
                sound.volume = volume
                sound.play()
            except Exception as e:
                print(f"Error playing sound {sound_path}: {e}")
    
    def clear_cache(self):
        """Clear all cached resources"""
        self.image_cache.clear()
        self.sound_cache.clear()
        self.texture_cache.clear()
        print("Resource cache cleared")


# Global singleton instance
_resource_manager = None


def get_resource_manager():
    """Get the global ResourceManager instance"""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager
