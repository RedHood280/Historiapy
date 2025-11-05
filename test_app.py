"""
test_app.py - Manual testing script for the Kivy app

This script can be run on a system with a display to test the UI.
Run: python test_app.py

Tests performed:
1. UI loads correctly
2. Buttons respond to hover
3. Character selection works
4. Difficulty selection works
5. Game starts and displays correctly
6. TypewriterLabel shows text progressively
7. Options are clickable and advance the game
8. Stats update correctly
9. Save/load functionality works
"""
import os
import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import behaviors
        import widgets
        import utils
        import resources
        import models
        import controller
        import main
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_models():
    """Test the game models"""
    print("\nTesting models...")
    try:
        from models import GameModel
        
        game = GameModel()
        print(f"✅ Loaded {len(game.historia)} story nodes")
        print(f"✅ Loaded {len(game.personajes)} characters")
        
        # Test starting a game
        nodo = game.nueva_partida("Test Player", "jason", "facil")
        if nodo:
            print(f"✅ Game started successfully: {nodo.titulo}")
        else:
            print("❌ Failed to start game")
            return False
        
        # Test save/load
        if game.guardar_partida():
            print("✅ Save successful")
            
            game2 = GameModel()
            if game2.cargar_partida():
                print("✅ Load successful")
            else:
                print("❌ Load failed")
                return False
        else:
            print("❌ Save failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Model error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui():
    """Test the UI (requires display)"""
    print("\n" + "="*60)
    print("MANUAL UI TESTING")
    print("="*60)
    print("""
To test the UI, run: python main.py

Then perform these manual tests:

1. MENU SCREEN
   ✓ Buttons change color/size on hover
   ✓ "NUEVA PARTIDA" button works
   ✓ "CARGAR PARTIDA" button works (after save)
   ✓ "SALIR" button exits the app

2. CHARACTER SELECT
   ✓ All 4 character buttons visible
   ✓ Hover effects work
   ✓ Clicking a character advances to difficulty select

3. DIFFICULTY SELECT
   ✓ 3 difficulty buttons visible
   ✓ Hover effects work
   ✓ Clicking difficulty starts the game

4. GAME SCREEN
   ✓ Stats panel shows at top (name, health, reputation, resources)
   ✓ Scene image loads (or shows placeholder if missing)
   ✓ Title shows in red
   ✓ Description appears with typewriter effect
   ✓ Options appear as buttons below
   ✓ Hover effects on option buttons
   ✓ Clicking option advances story
   ✓ Stats update after choices
   ✓ Popup shows stat changes
   ✓ Save button (💾) works
   ✓ Menu button (🏠) works

5. FINAL SCREEN
   ✓ Final stats displayed
   ✓ "Nueva Partida" button works
   ✓ "Menú Principal" button works

6. SOUND EFFECTS (if .wav files exist)
   ✓ Click sound on buttons
   ✓ Transition sound when changing scenes
   ✓ Typewriter sound (type.wav) during text display

7. ANIMATIONS
   ✓ Buttons scale up on hover
   ✓ Buttons scale down on press
   ✓ Scene image fades in/out on transitions
   ✓ Smooth color transitions on buttons
    """)

def main():
    print("="*60)
    print("HISTORIAPY - TEST SUITE")
    print("="*60)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return False
    
    # Test models
    if not test_models():
        print("\n❌ Model tests failed")
        return False
    
    # Show UI testing instructions
    test_ui()
    
    print("\n" + "="*60)
    print("✅ All automated tests passed!")
    print("="*60)
    print("\nTo run the app with UI: python main.py")
    print("To test without display: See instructions above")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
