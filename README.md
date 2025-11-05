# Historia Py - Interactive Story Game

An interactive narrative game built with Python and Kivy, featuring multiple characters, branching storylines, and an enhanced UI with visual effects.

## Features

### Core Gameplay
- **3 Playable Characters**: Red Hood (Jason Todd), Nightwing (Dick Grayson), and Red Robin (Tim Drake)
- **3 Difficulty Levels**: Easy, Medium, and Hard with varying complexity
- **Branching Narratives**: Your choices matter and affect the story
- **Stats System**: Health, Reputation, and Resources that change based on decisions
- **Inventory System**: Collect items throughout your journey
- **Multiple Endings**: Different outcomes based on your choices
- **Save/Load System**: Save your progress and continue later

### Visual Enhancements (New!)
- **Animated Hover Buttons**: Buttons change color and scale on hover and press
- **Typewriter Text Effect**: Story text displays gradually with optional typing sound
- **Smooth Transitions**: Fade animations between story nodes
- **Resource Caching**: Images and sounds are preloaded and cached for better performance
- **Graceful Degradation**: Missing assets don't crash the app

### Technical Architecture
- **MVC Design Pattern**: Clean separation between Model, View, and Controller
- **Kivy Framework**: Modern, cross-platform UI framework
- **Custom Widgets**: AnimatedHoverButton and TypewriterLabel for enhanced UX
- **Custom Behaviors**: HoverBehavior and RippleBehavior mixins
- **Debounce Protection**: Prevents accidental double-clicks on buttons
- **Resource Management**: Efficient asset loading and caching

## Installation

### Requirements
- Python 3.7 or higher
- Kivy 2.0 or higher

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/RedHood280/historiapy.git
   cd historiapy
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

## Testing Instructions

### Basic Functionality Test
1. **Start the Game**:
   ```bash
   python main.py
   ```

2. **Test New Game Flow**:
   - Click "New Game" button
   - Verify the button scales and changes color on hover
   - Select a character (Red Hood, Nightwing, or Tim Drake)
   - Select a difficulty (Easy, Medium, or Hard)
   - Verify the game starts and displays the first story node

3. **Test Visual Effects**:
   - **Hover Effect**: Move mouse over buttons and verify they change color
   - **Click Effect**: Click buttons and verify they scale down and play sound (if available)
   - **Typewriter Effect**: Watch story text appear gradually, character by character
   - **Typing Sound**: If `assets/sounds/type.wav` exists, verify typing sound plays
   - **Transitions**: Make choices and verify scene fades out/in smoothly

4. **Test Gameplay**:
   - Make a choice by clicking an option button
   - Verify stats (Health, Reputation, Resources) update correctly
   - Verify inventory shows items when collected
   - Verify the story progresses to the next node
   - Play through to an ending

5. **Test Save/Load**:
   - During gameplay, click "Save" button
   - Verify "Game saved successfully!" message appears
   - Return to main menu
   - Click "Load Game"
   - Verify game resumes from saved position
   - Verify all stats and inventory are preserved

6. **Test Edge Cases**:
   - **Double-Click Prevention**: Rapidly click an option button multiple times
   - Verify only one action is processed (debounce protection)
   - **Missing Assets**: Remove an image file temporarily
   - Verify game shows placeholder instead of crashing
   - **Scene Transitions**: Click options quickly
   - Verify transitions complete before next action

### Visual Regression Testing
- Compare button hover/press animations with previous version
- Verify typewriter speed is comfortable (not too fast/slow)
- Check that fade transitions are smooth
- Ensure text remains readable during animations

### Performance Testing
- Load game and check startup time
- Verify smooth animations without lag
- Check memory usage doesn't grow excessively
- Test with and without asset files present

## File Structure

```
historiapy/
├── main.py              # Application entry point
├── models.py            # Game logic and data models
├── controller.py        # Game controller (MVC)
├── views.kv             # Kivy UI definitions
├── widgets.py           # Custom widgets (AnimatedHoverButton, TypewriterLabel)
├── behaviors.py         # Custom behaviors (HoverBehavior, RippleBehavior)
├── resources.py         # Resource manager for assets
├── utils.py             # Utility functions (debounce, typewriter_schedule)
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── assets/              # Game assets (optional)
│   ├── images/          # Scene images
│   └── sounds/          # Sound effects
└── partida_guardada.json # Save file (created when saving)
```

## Controls

- **Mouse**: Hover over buttons to see hover effect, click to select
- **Keyboard**: No keyboard controls currently (UI is mouse-driven)

## Customization

### Adding New Story Nodes
Edit `models.py` and add nodes to the `_initialize_story()` method:

```python
node = StoryNode("node_id", "Title", "Description", "image.png")
node.add_option("Choice text", "next_node_id", stat="health", change=10)
self.story["node_id"] = node
```

### Adjusting Typewriter Speed
In `widgets.py`, change the `typewriter_interval` property:

```python
typewriter_interval = NumericProperty(0.05)  # Seconds per character
```

### Customizing Button Colors
In `widgets.py`, adjust the color properties:

```python
hover_color = ListProperty([0.8, 0.2, 0.2, 1])  # RGBA
normal_color = ListProperty([0.7, 0.13, 0.13, 1])
press_color = ListProperty([0.5, 0.1, 0.1, 1])
```

## Troubleshooting

### Issue: Buttons don't respond
- Check console for errors
- Ensure Kivy is properly installed
- Verify `views.kv` is in the same directory as `main.py`

### Issue: Images don't appear
- Check that image files exist in `assets/images/` or `imagenes/` directory
- App will show placeholder if images are missing (this is normal)
- Check console for "Image not found" messages

### Issue: No sound effects
- Check that sound files exist in `assets/sounds/` directory
- Verify file format is supported (WAV recommended)
- Sound is optional - game works without it

### Issue: Typewriter effect too slow/fast
- Adjust `typewriter_interval` in `widgets.py`
- Lower value = faster typing, higher value = slower typing

## Known Limitations

- Asset paths are case-sensitive on Linux/Mac
- Sound format support depends on system codecs
- Large images may impact performance

## Credits

- **Game Design**: Interactive narrative framework
- **Programming**: Python + Kivy
- **Architecture**: MVC pattern with custom widgets and behaviors
- **Visual Effects**: Animated buttons, typewriter text, smooth transitions

## License

This project is for educational purposes. Batman and related characters are property of DC Comics.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions, please open an issue on GitHub.

---

**Thank you for playing Historia Py!**
