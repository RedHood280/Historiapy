# HistoriaPy: Los Robins

Una aventura narrativa interactiva basada en el universo de Batman, desarrollada con Kivy.

## 🎮 Características

### Funcionalidades Principales
- **3 Personajes Jugables**:
  - Jason Todd (El Segundo Robin)
  - Dick Grayson (Nightwing)
  - Tim Drake (El Tercer Robin)
  - Damian Wayne (El Cuarto Robin)

- **3 Niveles de Dificultad**:
  - Fácil: Historia más directa con final feliz
  - Normal: Decisiones más complejas
  - Difícil: Múltiples finales posibles

- **Sistema de Juego Completo**:
  - Narrativa ramificada con múltiples caminos
  - Sistema de estadísticas (Salud, Reputación, Recursos)
  - Sistema de inventario con ítems coleccionables
  - Múltiples finales basados en tus decisiones
  - Sistema de guardado/carga de partidas
  - Persistencia de progreso

### Mejoras Visuales (Kivy)

#### Efectos y Animaciones
- **HoverBehavior**: Detección de entrada/salida del ratón en widgets
- **AnimatedHoverButton**: Botones con reacciones al hover y click
  - Transiciones de color suaves
  - Efecto de escala al pasar el ratón
  - Animaciones fluidas usando Kivy Animation
- **Efecto Typewriter Mejorado**:
  - Texto que aparece letra por letra
  - Cancelación y salto de animación
  - Soporte para sonido de tipeo (opcional)
  - Callback al completar
- **Transiciones de Escena**:
  - Fade overlay para cambios de pantalla
  - Cross-fade entre nodos de historia
  - Animaciones suaves entre estados

#### Características de UI
- **Debounce en Botones**: Previene clicks múltiples accidentales
- **Cache de Recursos**: Gestión eficiente de imágenes y sonidos
- **Tooltips**: Información adicional en botones (propiedad tooltip_text)
- **Efectos Ripple**: Feedback visual al hacer click
- **Interfaz Responsiva**: Layout adaptable y moderno

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/RedHood280/historiapy.git
cd historiapy
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `kivy>=2.3.0` - Framework de UI
- `pillow>=10.0.0` - Procesamiento de imágenes
- `pygame>=2.5.0` - Reproducción de audio

3. **Ejecutar el juego**:
```bash
python main.py
```

## 🎯 Cómo Jugar

1. **Menú Principal**: 
   - Nueva Partida: Comienza una nueva aventura
   - Cargar Partida: Continúa desde donde lo dejaste
   - Créditos: Información del juego

2. **Selección de Personaje**:
   - Elige tu Robin favorito
   - Cada personaje tiene su propia historia única

3. **Selección de Dificultad**:
   - Fácil: Ideal para primera partida
   - Normal: Balance de desafío
   - Difícil: Múltiples caminos y finales

4. **Durante el Juego**:
   - Lee la historia que aparece con efecto typewriter
   - Elige entre las opciones presentadas (máximo 4)
   - Observa cómo tus decisiones afectan las estadísticas
   - Usa el botón 💾 para guardar tu progreso
   - Usa el botón 📊 para ver inventario y estadísticas

5. **Finales**:
   - Cada combinación de personaje y dificultad tiene finales únicos
   - Tus decisiones determinan el destino de tu Robin

## 📁 Estructura del Proyecto

```
historiapy/
├── main.py              # Punto de entrada de la aplicación
├── models.py            # Lógica del juego y datos de historia
├── controller.py        # Controlador de estado y transiciones
├── views.kv            # Diseño de interfaz en Kivy language
├── screens.py          # Clases de pantallas
├── utils.py            # Utilidades (typewriter, debounce)
├── resources.py        # Gestor de recursos (imágenes, sonidos)
├── behaviors.py        # Comportamientos personalizados (hover, ripple)
├── requirements.txt    # Dependencias del proyecto
├── README.md          # Este archivo
├── assets/            # Recursos gráficos (futuro)
├── audio/             # Archivos de audio
└── Robins.py          # Versión original tkinter (referencia)
```

## 🛠️ Arquitectura Técnica

### Separación de Capas
- **Models** (models.py): Lógica pura del juego, sin dependencias de UI
- **View** (views.kv): Diseño visual declarativo en Kivy language
- **Controller** (controller.py): Mediador entre modelo y vista
- **Utils & Behaviors**: Componentes reutilizables

### Características Técnicas Implementadas

1. **Sistema de Recursos**:
   - Cache de texturas para rendimiento
   - Preloading de assets
   - Método `get_kivy_texture()` para widgets de imagen

2. **Animaciones**:
   - `Animation` de Kivy para transiciones suaves
   - Canvas instructions para overlays
   - Efectos visuales sin bloqueo

3. **Audio** (Opcional):
   - Soporte para efectos de sonido
   - Reproducción con pygame
   - Configuración de volumen

4. **Persistencia**:
   - Guardado en JSON
   - Carga automática de partidas anteriores

## 🧪 Testing Manual

Para verificar que todas las funcionalidades están operativas:

1. **Test de Navegación**:
   - Navega por todos los menús
   - Verifica hover effects en botones
   - Confirma transiciones suaves

2. **Test de Gameplay**:
   - Inicia una partida con cada personaje
   - Prueba cada nivel de dificultad
   - Verifica que el efecto typewriter funciona
   - Confirma que las opciones responden correctamente

3. **Test de Stats**:
   - Observa cambios en salud, reputación, recursos
   - Verifica que los ítems se agregan al inventario
   - Confirma que la pantalla de stats muestra todo correctamente

4. **Test de Persistencia**:
   - Guarda una partida
   - Cierra la aplicación
   - Vuelve a abrir y carga la partida
   - Verifica que el estado se restauró correctamente

## 📝 Cambios Respecto a la Versión Original

### De tkinter a Kivy
- Migración completa de UI de tkinter a Kivy
- Mantenimiento de TODA la lógica del juego
- Mejoras visuales significativas

### Nuevas Características
- Efectos hover en botones
- Animaciones de transición
- Efecto typewriter mejorado con callbacks
- Sistema de recursos con cache
- Behaviors reutilizables
- Ripple effects
- Mejor feedback visual

### Preservado
- ✅ 3 personajes con historias completas
- ✅ 3 niveles de dificultad
- ✅ Sistema de branching narrativo
- ✅ Sistema de stats completo
- ✅ Sistema de inventario
- ✅ Múltiples finales
- ✅ Guardado y carga de partidas
- ✅ Todas las 10,000+ líneas de contenido narrativo

## 🤝 Contribuciones

Este proyecto es una demostración de migración de tkinter a Kivy manteniendo toda la funcionalidad existente y añadiendo mejoras visuales modernas.

## 📄 Licencia

Basado en personajes de DC Comics. Este es un proyecto educativo/de demostración.

## 🐛 Problemas Conocidos

- Los assets visuales (imágenes de escenas) necesitan ser añadidos en `assets/images/`
- Los sonidos opcionales deben colocarse en `audio/` (typing.wav, transition.mp3, etc.)
- En entornos headless, Kivy requiere configuración adicional para renderizado offscreen

## 📞 Contacto

Para reportar issues o sugerencias, usa el sistema de issues de GitHub.

---

**¡Disfruta tu aventura como Robin en Gotham City!** 🦇
