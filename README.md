# HistoriaPy - Red Hood Interactive Adventure

Una aventura interactiva basada en los personajes de DC Comics (Red Hood/Robin) con efectos visuales y animaciones mejoradas usando Kivy.

## Características

### Juego
- **3 personajes jugables**: Jason Todd (Red Hood), Dick Grayson (Nightwing), Tim Drake (Red Robin), Damian Wayne (Robin)
- **3 niveles de dificultad**: Fácil (~10-15 min), Normal (~20-30 min), Difícil (~40-60 min)
- **Sistema de branching**: Decisiones que afectan la historia
- **Estadísticas dinámicas**: Salud, Reputación, Recursos
- **Sistema de inventario**: Items coleccionables
- **Múltiples finales**: Diferentes desenlaces según tus decisiones
- **Guardado/Carga**: Persistencia de partidas
- **Autosave**: Guardado automático después de cada decisión

### Efectos Visuales (Nueva Implementación)
- **Botones animados con hover**: Cambio de escala y color al pasar el mouse
- **Efecto typewriter**: Texto que aparece letra por letra con sonido opcional
- **Transiciones suaves**: Cross-fade entre escenas
- **Sistema de sonidos**: Efectos de audio para clicks y transiciones
- **Protección anti-multiclick**: Debounce en botones
- **Cache de recursos**: Carga optimizada de imágenes y sonidos

## Arquitectura

El proyecto sigue el patrón **MVC (Model-View-Controller)** con Kivy:

### Estructura de Archivos

```
historiapy/
├── main.py              # Punto de entrada de la aplicación
├── models.py            # Lógica del juego (NO MODIFICAR)
├── controller.py        # Controlador MVC
├── views.kv             # Interfaz de usuario en Kivy Language
├── behaviors.py         # HoverBehavior y RippleBehavior
├── widgets.py           # AnimatedHoverButton y TypewriterLabel
├── utils.py             # Utilidades (debounce, typewriter_schedule)
├── resources.py         # Gestión de recursos (imágenes, sonidos)
├── Robins.py            # Implementación original en Tkinter (legacy)
├── assets/
│   ├── images/          # Imágenes del juego
│   └── sounds/          # Efectos de sonido (.wav)
│       ├── click.wav    # Sonido de click (opcional)
│       ├── transition.wav # Sonido de transición (opcional)
│       └── type.wav     # Sonido de typewriter (opcional)
└── README.md            # Este archivo
```

### Componentes

#### behaviors.py
- `HoverBehavior`: Detecta entrada/salida del mouse en widgets
- `RippleBehavior`: Proporciona hook para efectos ripple

#### widgets.py
- `AnimatedHoverButton`: Botón con animación de escala/color en hover y press
  - Soporta `tooltip_text` y `anim_duration`
- `TypewriterLabel`: Label con efecto typewriter
  - Soporta `on_complete`, `sound_key`, cancelable

#### utils.py
- `debounce(wait_time)`: Decorador para prevenir multi-click
- `typewriter_schedule()`: Función para crear efecto typewriter
- `play_sound()`: Reproduce efectos de sonido

#### resources.py
- `ResourceManager`: Cache de imágenes, texturas y sonidos
- Métodos: `get_texture()`, `preload_images()`, `preload_sounds()`
- Tolerante a archivos faltantes

#### controller.py
- `GameController`: Coordina modelo y vista
- `play_transition_animation()`: Animación cross-fade
- `choose_option()`: Maneja elección con debounce y autosave

#### views.kv
- Layout: Imagen izquierda (60%), panel derecho (40%)
- Descripción con TypewriterLabel
- Hasta 4 opciones con AnimatedHoverButton
- Stats panel en la parte superior

## Instalación

### Requisitos
- Python 3.8+
- Kivy >= 2.1.0

### Instalar dependencias

```bash
pip install kivy>=2.1.0
```

## Uso

### Ejecutar el juego

```bash
python main.py
```

### Controles
- **Mouse**: Navega por los menús y selecciona opciones
- **Hover**: Pasa el mouse sobre los botones para ver efectos
- **Click**: Selecciona opciones y navega
- **💾**: Guarda la partida
- **🏠**: Vuelve al menú principal

## Desarrollo

### Cambios Implementados

#### 1. behaviors.py (Nuevo)
Comportamientos livianos para detección de hover y ripple:
- `HoverBehavior`: Eventos `on_enter` y `on_leave`
- `RippleBehavior`: Hook `ripple_show()` para efectos personalizados

#### 2. widgets.py (Nuevo)
Widgets personalizados con animaciones:
- `AnimatedHoverButton`: Botón con animaciones de escala/color
  - Hover: escala 1.05x, color más brillante
  - Press: escala 0.95x, color más oscuro
- `TypewriterLabel`: Label con efecto máquina de escribir
  - Configurable: intervalo, sonido, callback de completado
  - Métodos: `cancel_typewriter()`, `skip_to_end()`

#### 3. utils.py (Actualizado)
Utilidades mejoradas:
- `debounce()`: Decorador para prevenir clicks múltiples
- `typewriter_schedule()`: Función retornable/cancelable
  - Cache de sonidos para mejor rendimiento
  - Soporte para `sound_key` y `on_complete`
- `play_sound()`: Reproduce sonidos si existen

#### 4. resources.py (Actualizado)
Gestión de recursos optimizada:
- `get_texture()`: Obtiene texturas cacheadas
- `preload_images()` y `preload_sounds()`: Precarga tolerante
- `preload_common_assets()`: Precarga sonidos comunes

#### 5. controller.py (Actualizado)
Controlador mejorado:
- `play_transition_animation()`: Cross-fade ligero con sonido
- `choose_option()`: Decorado con `@debounce`
  - Reproduce sonido de click
  - Autosave después de cada elección
  - Callback a UI tras aplicar cambios

#### 6. views.kv (Actualizado)
Interfaz actualizada con widgets animados:
- Layout: 60% imagen, 40% panel de info
- `TypewriterLabel` enlazado a `node.text` con `typewriter: True`
- `AnimatedHoverButton` para opciones y botones UI
- Transiciones en `GameScreen.on_enter` y `update_after_choice`

#### 7. README.md (Este archivo)
Documentación completa con:
- Resumen de cambios
- Estructura del proyecto
- Instrucciones de instalación
- Pasos para probar

## Tests Manuales

### Test 1: Verificar botones con hover
1. Ejecutar `python main.py`
2. Crear nueva partida
3. **Verificar**: Botones cambian escala/color al pasar el mouse
4. **Verificar**: Click produce animación de press

### Test 2: Efecto typewriter
1. Iniciar una partida
2. Observar el panel de descripción
3. **Verificar**: Texto aparece letra por letra
4. **Verificar**: Si existe `assets/sounds/type.wav`, se reproduce sonido

### Test 3: Transiciones
1. En el juego, elegir una opción
2. **Verificar**: Reproducción de sonido de click
3. **Verificar**: Transición suave (fade) mientras cambia la escena
4. **Verificar**: Si existe `assets/sounds/transition.wav`, se reproduce

### Test 4: Stats e inventario
1. Jugar y tomar decisiones
2. **Verificar**: Stats se actualizan correctamente
3. **Verificar**: Items se agregan al inventario
4. **Verificar**: Cambios se muestran en popup

### Test 5: Guardado/Carga
1. Jugar y avanzar en la historia
2. Hacer click en el botón 💾
3. **Verificar**: Mensaje de guardado exitoso
4. Salir y volver al menú
5. Cargar partida
6. **Verificar**: Progreso restaurado correctamente

### Test 6: Múltiples finales
1. Jugar diferentes rutas
2. **Verificar**: Alcanzar diferentes finales según decisiones
3. **Verificar**: Stats finales mostrados correctamente

## Contribuir

Este proyecto es parte de una tarea de mejora de UI/UX. Los cambios se centran en:
- Efectos visuales y animaciones
- **NO** se modifica la lógica de juego en `models.py`
- Se mantiene arquitectura MVC
- Optimizado para desktop

## Comandos Git (Para el PR)

```bash
# Crear rama
git checkout -b feature/ui-visual-effects

# Agregar archivos nuevos/modificados
git add behaviors.py widgets.py utils.py resources.py controller.py views.kv main.py models.py README.md

# Commit
git commit -m "feat: add visual effects and animations to Kivy app

- Add HoverBehavior and RippleBehavior (behaviors.py)
- Add AnimatedHoverButton and TypewriterLabel (widgets.py)
- Enhance utils.py with debounce and typewriter_schedule
- Improve resources.py with texture cache and preload
- Update controller.py with transition animations
- Redesign views.kv with animated widgets
- Create main.py as Kivy entry point
- Update README.md with testing instructions

All critical functionalities maintained:
- 3 characters, 3 difficulties
- Branching storylines
- Stats, inventory, items
- Multiple endings
- Save/load system
- Data persistence"

# Push
git push origin feature/ui-visual-effects

# Abrir PR en GitHub
# Título: "feat: Extend visual effects and animations for Kivy app"
```

## Dependencias

- `kivy>=2.1.0`: Framework principal
- Python standard library: `json`, `os`, `functools`, `time`

## Notas

- Los archivos de sonido son opcionales. El juego funciona sin ellos.
- Las imágenes se cargan desde `assets/images/`
- El guardado se almacena en `partida_guardada.json`
- Compatible con Python 3.8+
- Optimizado para desktop (Windows, macOS, Linux)

## Licencia

Basado en los personajes de DC Comics. Solo para uso educativo.

## Contacto

Para reportar bugs o sugerencias, abrir un issue en el repositorio de GitHub.
