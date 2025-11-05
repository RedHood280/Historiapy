# Testing Guide for HistoriaPy

## Quick Start

### 1. Install Dependencies
```bash
pip install kivy>=2.1.0
```

### 2. Run Automated Tests (No Display Needed)
```bash
python3 << 'EOF'
from models import GameModel
game = GameModel()
print(f"✅ Loaded {len(game.historia)} story nodes")
print(f"✅ Loaded {len(game.personajes)} characters")

# Test game start
nodo = game.nueva_partida("Test Player", "jason", "facil")
print(f"✅ Game starts: {nodo.titulo}")
print(f"✅ {len(nodo.opciones)} options available")

# Test save/load
game.guardar_partida()
print("✅ Save successful")

game2 = GameModel()
game2.cargar_partida()
print(f"✅ Load successful: {game2.jugador.nombre}")

print("\n🎉 All tests passed!")
EOF
```

### 3. Run Full App (Requires Display)
```bash
python main.py
```

## Manual Testing Checklist

### Menu Screen
- [ ] Title displays correctly ("RED HOOD")
- [ ] "NUEVA PARTIDA" button has hover effect
- [ ] "CARGAR PARTIDA" button has hover effect
- [ ] "SALIR" button works
- [ ] All buttons animate on hover (scale up)
- [ ] All buttons animate on click (scale down)

### Character Select Screen
- [ ] 4 character buttons visible
- [ ] Each button has correct color
  - Red Hood: Red (#C00000)
  - Nightwing: Blue (#00529B)
  - Red Robin: Green (#319C00)
  - Robin: Gold (#FFD700)
- [ ] Hover effects work on all buttons
- [ ] Clicking advances to difficulty select

### Difficulty Select Screen
- [ ] 3 difficulty buttons visible
- [ ] Correct difficulty descriptions
  - Fácil: ~10-15 min
  - Normal: ~20-30 min
  - Difícil: ~40-60 min
- [ ] Hover effects work
- [ ] Clicking starts game

### Game Screen - Layout
- [ ] Stats panel at top shows:
  - [ ] Player name (👤)
  - [ ] Health (❤️)
  - [ ] Reputation (⭐)
  - [ ] Resources (💎)
  - [ ] Save button (💾)
  - [ ] Menu button (🏠)
- [ ] Image panel (60% width, left side)
- [ ] Info panel (40% width, right side)
  - [ ] Scene title in red
  - [ ] Scene description with typewriter effect
- [ ] Options panel at bottom (up to 4 options)

### Game Screen - Functionality
- [ ] Scene image loads (or shows placeholder)
- [ ] Title displays correctly
- [ ] **Typewriter effect**: Description appears letter by letter
- [ ] Option buttons display correctly
- [ ] Hover effects on option buttons
- [ ] Clicking option advances story
- [ ] Stats update after choice
- [ ] Popup shows stat changes
- [ ] Save button works
- [ ] Menu button shows confirmation dialog

### Transitions
- [ ] Scene image fades on scene change
- [ ] Smooth transition between screens
- [ ] No lag or stuttering

### Sound Effects (if .wav files present)
- [ ] `click.wav`: Plays on button click
- [ ] `transition.wav`: Plays on scene change
- [ ] `type.wav`: Plays during typewriter effect

### Game Logic
- [ ] Stats increase/decrease correctly
  - [ ] Health (0-100)
  - [ ] Reputation (0-100)
  - [ ] Resources (can go negative in some cases)
- [ ] Items added to inventory
- [ ] Decisions tracked
- [ ] Multiple paths available
- [ ] Different endings reachable

### Save/Load System
- [ ] Clicking 💾 saves game
- [ ] "Guardado exitoso" message appears
- [ ] Returning to menu preserves save
- [ ] "CARGAR PARTIDA" loads saved game
- [ ] All stats restored correctly
- [ ] Current node restored correctly
- [ ] Inventory restored

### Edge Cases
- [ ] Clicking button multiple times doesn't cause issues (debounce works)
- [ ] Missing images show placeholder
- [ ] Missing sounds don't cause errors
- [ ] Invalid save file handled gracefully
- [ ] Rapid navigation doesn't cause crashes

## Performance Tests

### Load Time
- [ ] App starts in < 3 seconds
- [ ] Story nodes load in < 1 second
- [ ] Character select appears instantly
- [ ] Game screen loads in < 0.5 seconds

### Memory Usage
- [ ] Memory stays stable during gameplay
- [ ] No memory leaks after 10+ scene changes
- [ ] Image cache doesn't grow indefinitely

### Animation Performance
- [ ] Hover animations are smooth (60 FPS)
- [ ] Typewriter effect is consistent
- [ ] Transition animations are fluid
- [ ] No dropped frames during normal use

## Regression Tests

### All Characters
Test each character starts correctly:
- [ ] Jason Todd (Red Hood)
- [ ] Dick Grayson (Nightwing)
- [ ] Tim Drake (Red Robin)
- [ ] Damian Wayne (Robin)

### All Difficulties
Test each difficulty starts correctly:
- [ ] Fácil (Easy)
- [ ] Normal (Normal)
- [ ] Difícil (Hard)

### All Story Paths
Verify major branches work:
- [ ] Jason - Facil path
- [ ] Jason - Normal path (Death in the Family)
- [ ] Jason - Dificil path (Under the Red Hood)
- [ ] Other characters have starting nodes

## Bug Report Template

If you find a bug, report with this format:

```
**Bug**: [Short description]

**Steps to Reproduce**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result**: [What should happen]

**Actual Result**: [What actually happened]

**Environment**:
- OS: [Windows/Mac/Linux]
- Python: [Version]
- Kivy: [Version]

**Screenshots**: [If applicable]

**Logs**: [Error messages or console output]
```

## Success Criteria

✅ All automated tests pass
✅ All manual tests pass
✅ No errors in console
✅ Smooth user experience
✅ All 733 story nodes accessible
✅ All game features work as expected

## Quick Verification Command

```bash
# One-liner to verify installation
python -c "from models import GameModel; g=GameModel(); assert len(g.historia)==733; print('✅ Installation verified!')"
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'kivy'"
**Solution**: Install Kivy with `pip install kivy>=2.1.0`

### Error: "Couldn't connect to X server"
**Solution**: This is normal in headless environments. The app needs a display to run.

### Warning: "Could not load sound X"
**Solution**: Sounds are optional. Place .wav files in `assets/sounds/` or ignore the warning.

### Error: Image not found
**Solution**: Place images in `assets/images/` or they'll show as placeholders.

## Additional Resources

- Full documentation: See `README.md`
- PR details: See `PR_DESCRIPTION.md`
- Test script: Run `python test_app.py`
