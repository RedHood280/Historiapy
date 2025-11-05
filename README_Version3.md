```markdown
# Historiapy — Visual Novel (Kivy) — Visual Effects Enhancement

Este conjunto de archivos añade mejoras visuales y widgets animados para que la versión Kivy tenga una presentación más pulida.

Cambios principales:
- Nuevos mixins: HoverBehavior y RippleBehavior (behaviors.py).
- Widgets animados: AnimatedHoverButton y TypewriterLabel (widgets.py).
- Typewriter mejorado: utils.typewriter_schedule con cancelación, callback y soporte de sonido.
- ResourceManager mejorado: get_texture, mejor preload y cache (resources.py).
- GameController: método play_transition_animation para cross-fade ligero (controller.py).
- KV actualizado: usar AnimatedHoverButton y TypewriterLabel en views.kv (reemplaza botones y label antiguos).
- No se modifica models.py (la lógica del juego) y se mantiene la arquitectura MVC / kv / ScreenManager.

Instalación y ejecución rápida
1. Crear entorno virtual
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\\Scripts\\activate    # Windows

2. Instalar dependencias
   pip install kivy

3. Ejecutar la aplicación
   python main.py

Notas
- Coloca tus assets (PNG/WAV) en `assets/images/...` y `assets/sounds/...`. Los sonidos opcionales son:
  - assets/sounds/click.wav
  - assets/sounds/transition.wav
  - assets/sounds/type.wav
- El código tolera la falta de estos archivos y no fallará si no existen.

Cómo probar las mejoras (test rápido)
- Ejecuta python main.py, crea una nueva partida:
  - Los botones deben reaccionar al hover (escala y cambio de color) y al click.
  - El texto muestra efecto typewriter; si `assets/sounds/type.wav` existe reproducirá sonido.
  - Al elegir una opción se reproduce click y la escena cambia con una transición ligera.
  - Stats/inventario se actualizan correctamente.
  - Guardar/cargar funcionan igual que antes.

Archivos añadidos/actualizados en este paquete:
- behaviors.py (nuevo)
- widgets.py (nuevo)
- utils.py (reemplazado)
- resources.py (reemplazado)
- controller.py (reemplazado)
- views.kv (reemplazado)
- README.md (actualizado)

Sugerencia importante:
Si al cargar KV Kivy no encuentra las clases personalizadas (AnimatedHoverButton, TypewriterLabel), añade en main.py al inicio:
```python
from widgets import AnimatedHoverButton, TypewriterLabel
import behaviors
```
Esto registra las clases para que el parser kv las reconozca.
```