# Quick Start Guide - HistoriaPy Kivy

## For End Users

### Installation
```bash
# Clone repository
git clone https://github.com/RedHood280/historiapy.git
cd historiapy

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### First Time Playing
1. Click "🎮 NUEVA PARTIDA"
2. Choose your Robin (try Jason Todd first)
3. Select difficulty (start with Fácil)
4. Read the story and make choices
5. Watch your stats change
6. Save your progress with 💾 button
7. View inventory with 📊 button

## For Developers

### Project Structure
```
main.py       → App entry, custom widgets
models.py     → Game logic (733 story nodes)
controller.py → State management
screens.py    → Screen controllers
views.kv      → UI layouts
utils.py      → Helpers (typewriter, debounce)
resources.py  → Asset management
behaviors.py  → Hover, ripple behaviors
```

### Testing
```bash
# Test game logic
python test_game_logic.py

# Test UI (needs display)
python test_ui_structure.py

# Quick validation
python -c "import models; print('OK')"
```

### Adding a New Screen

1. **Create screen class** (screens.py):
```python
class MyNewScreen(Screen):
    def on_enter(self):
        """Called when screen becomes active"""
        pass
```

2. **Define layout** (views.kv):
```yaml
<MyNewScreen>:
    name: 'my_screen'
    BoxLayout:
        Label:
            text: 'Hello World'
```

3. **Register screen** (main.py):
```python
def on_start(self):
    sm = self.root
    sm.add_widget(MyNewScreen())
```

4. **Navigate to it**:
```python
app.root.current = 'my_screen'
```

### Adding Visual Effects

#### Hover Effect
```python
# In Python
class MyButton(Button, HoverBehavior):
    def on_enter(self):
        # Mouse entered
        pass
    
    def on_leave(self):
        # Mouse left
        pass
```

#### Animation
```python
from kivy.animation import Animation

# Fade out
anim = Animation(opacity=0, duration=0.5)
anim.start(widget)
```

#### Typewriter
```python
from utils import typewriter_schedule

effect = typewriter_schedule(
    "Your text here",
    label_widget,
    interval=0.03
)
```

### Modifying Story Content

All story content is in `models.py`, in these methods:
- `inicializar_historias()` - Jason Todd stories
- `inicializar_historias_nightwing()` - Dick Grayson stories  
- `inicializar_historias_tim_drake()` - Tim Drake stories
- `inicializar_historias_damian_wayne()` - Damian Wayne stories

Example of adding a story node:
```python
# In models.py, inside appropriate method
new_node = NodoHistoria(
    "jason_facil_new_scene",
    "NEW SCENE TITLE",
    "Description of what happens...",
    "scene_image.png"
)
new_node.agregar_opcion(
    "Choice text",
    "next_node_id",
    stat="salud",
    cambio=10,
    item="New Item"
)
self.historia["jason_facil_new_scene"] = new_node
```

### Debugging

#### Enable verbose logging:
```python
# In main.py, at top
import os
os.environ['KIVY_LOG_LEVEL'] = 'debug'
```

#### Check game state:
```python
# In any screen
app = App.get_running_app()
print(app.controller.game.jugador.salud)
print(app.controller.game.jugador.inventario)
```

#### Test specific character/difficulty:
```python
from models import JuegoAventuraBase
game = JuegoAventuraBase()
game.iniciar_juego("jason", "facil")
node = game.obtener_nodo_actual()
print(node.titulo)
print(node.descripcion)
```

### Common Issues

#### "Module not found"
```bash
pip install -r requirements.txt
```

#### "Couldn't connect to X server"
- Normal in headless environment
- App works fine with display

#### "Story node not found"
- Check character name mapping (nightwing → grayson)
- Verify node ID in models.py

#### Animations not working
- Check if Window is available
- Try on system with display

### Performance Tips

1. **Preload images:**
```python
from resources import resource_manager
resource_manager.preload_images([
    "scene1.png",
    "scene2.png"
])
```

2. **Limit typewriter speed:**
```python
# Faster typing = less CPU
typewriter_schedule(text, label, interval=0.05)  # vs 0.03
```

3. **Disable animations if slow:**
```python
# In views.kv
AnimatedHoverButton:
    # Comment out animations in on_enter/on_leave
```

### Customization

#### Change color scheme (views.kv):
```yaml
#:set COLOR_PRIMARY 0.2, 0.6, 0.8, 1  # Blue theme
#:set COLOR_SECONDARY 0.1, 0.3, 0.5, 1
```

#### Modify button style:
```yaml
<AnimatedHoverButton>:
    font_size: '20sp'  # Larger text
    background_color: 0.5, 0.5, 0.5, 1  # Gray background
```

#### Change window size (main.py):
```python
Window.size = (1280, 720)  # 720p
Window.size = (1920, 1080)  # 1080p
```

### Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

### Resources

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Kivy Examples](https://kivy.org/doc/stable/examples/gen__index.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Questions?

Check:
1. README.md - User documentation
2. IMPLEMENTATION.md - Technical details
3. GitHub Issues - Report bugs
4. Code comments - Inline documentation

---
**Happy coding! 🦇**
