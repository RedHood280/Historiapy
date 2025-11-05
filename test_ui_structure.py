#!/usr/bin/env python
"""
Test UI structure - validates KV file and widget hierarchy
"""
import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'  # Reduce console output

from kivy.lang import Builder
from kivy.factory import Factory
from main import AnimatedHoverButton, TypewriterLabel
from screens import (MainMenuScreen, CharacterSelectScreen, DifficultySelectScreen,
                     GameScreen, StatsScreen, CreditsScreen)

def test_kv_loading():
    """Test that KV file loads without errors"""
    print("Testing KV file loading...")
    
    # Register custom widgets
    Factory.register('AnimatedHoverButton', cls=AnimatedHoverButton)
    Factory.register('TypewriterLabel', cls=TypewriterLabel)
    
    try:
        # Load KV file
        Builder.load_file('views.kv')
        print("✓ KV file loaded successfully")
        return True
    except Exception as e:
        print(f"✗ KV file loading failed: {e}")
        return False

def test_screen_creation():
    """Test that all screens can be instantiated"""
    print("\nTesting screen creation...")
    
    screens = [
        ("MainMenuScreen", MainMenuScreen),
        ("CharacterSelectScreen", CharacterSelectScreen),
        ("DifficultySelectScreen", DifficultySelectScreen),
        ("GameScreen", GameScreen),
        ("StatsScreen", StatsScreen),
        ("CreditsScreen", CreditsScreen),
    ]
    
    success_count = 0
    for name, screen_class in screens:
        try:
            screen = screen_class()
            print(f"✓ {name} created successfully (name: {screen.name})")
            success_count += 1
        except Exception as e:
            print(f"✗ {name} failed: {e}")
    
    print(f"\n✓ {success_count}/{len(screens)} screens created successfully")
    return success_count == len(screens)

def test_widget_hierarchy():
    """Test widget hierarchy in screens"""
    print("\nTesting widget hierarchy...")
    
    # Create a game screen to check structure
    try:
        game_screen = GameScreen()
        
        # Check for expected IDs
        expected_ids = [
            'player_name', 'health_bar', 'health_text',
            'reputation_bar', 'reputation_text', 'resources_text',
            'story_title', 'story_text',
            'option1', 'option2', 'option3', 'option4'
        ]
        
        found_ids = []
        missing_ids = []
        
        for id_name in expected_ids:
            if id_name in game_screen.ids:
                found_ids.append(id_name)
            else:
                missing_ids.append(id_name)
        
        print(f"✓ Found {len(found_ids)}/{len(expected_ids)} expected widget IDs")
        
        if missing_ids:
            print(f"  Missing IDs: {', '.join(missing_ids)}")
        
        return len(missing_ids) == 0
        
    except Exception as e:
        print(f"✗ Widget hierarchy test failed: {e}")
        return False

def test_button_widgets():
    """Test custom button widgets"""
    print("\nTesting custom widgets...")
    
    try:
        # Test AnimatedHoverButton
        btn = AnimatedHoverButton(text="Test Button")
        print(f"✓ AnimatedHoverButton created")
        print(f"  Properties: text='{btn.text}', hovered={btn.hovered}")
        
        # Test TypewriterLabel
        label = TypewriterLabel(text="Test Label")
        print(f"✓ TypewriterLabel created")
        print(f"  Properties: text='{label.text}'")
        
        return True
        
    except Exception as e:
        print(f"✗ Custom widget test failed: {e}")
        return False

def main():
    """Run all UI structure tests"""
    print("=" * 60)
    print("HISTORIAPY - UI STRUCTURE TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("KV Loading", test_kv_loading()))
    results.append(("Screen Creation", test_screen_creation()))
    results.append(("Widget Hierarchy", test_widget_hierarchy()))
    results.append(("Custom Widgets", test_button_widgets()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
