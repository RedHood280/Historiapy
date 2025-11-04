#!/usr/bin/env python
"""
Test script to verify game logic works correctly
"""
import sys
from models import JuegoAventuraBase

def test_game_initialization():
    """Test game can be initialized"""
    print("Testing game initialization...")
    game = JuegoAventuraBase()
    
    assert game.historia, "Historia should be populated"
    assert game.personajes, "Personajes should be populated"
    
    print(f"✓ Game initialized with {len(game.historia)} story nodes")
    print(f"✓ {len(game.personajes)} characters loaded")
    return game

def test_start_game(game):
    """Test starting a game"""
    print("\nTesting game start...")
    
    # Test Jason Todd easy mode
    success = game.iniciar_juego("jason", "facil")
    assert success, "Should start jason facil game"
    assert game.jugador is not None, "Player should be created"
    assert game.jugador.nombre == "Jason Todd", "Player name should be Jason Todd"
    
    print(f"✓ Started game as {game.jugador.nombre}")
    print(f"✓ Difficulty: {game.dificultad}")
    print(f"✓ Starting node: {game.jugador.nodo_actual}")
    return game

def test_story_navigation(game):
    """Test navigating through story"""
    print("\nTesting story navigation...")
    
    node = game.obtener_nodo_actual()
    assert node is not None, "Should have current node"
    
    print(f"✓ Current node: {node.id}")
    print(f"  Title: {node.titulo}")
    print(f"  Description: {node.descripcion[:100]}...")
    print(f"  Options: {len(node.opciones)}")
    
    if node.opciones:
        # Choose first option
        initial_stats = (game.jugador.salud, game.jugador.reputacion, game.jugador.recursos)
        success = game.elegir_opcion(0)
        assert success, "Should choose option successfully"
        
        print(f"✓ Chose option: {node.opciones[0]['texto']}")
        print(f"  Stats before: Health={initial_stats[0]}, Rep={initial_stats[1]}, Res={initial_stats[2]}")
        print(f"  Stats after: Health={game.jugador.salud}, Rep={game.jugador.reputacion}, Res={game.jugador.recursos}")
        
        new_node = game.obtener_nodo_actual()
        print(f"✓ Moved to node: {new_node.id}")
    
    return game

def test_save_load(game):
    """Test save and load functionality"""
    print("\nTesting save/load...")
    
    # Save game
    success = game.guardar_partida("test_save.json")
    assert success, "Should save game"
    print("✓ Game saved")
    
    # Store current state
    saved_node = game.jugador.nodo_actual
    saved_health = game.jugador.salud
    
    # Create new game instance and load
    game2 = JuegoAventuraBase()
    success = game2.cargar_partida("test_save.json")
    assert success, "Should load game"
    assert game2.jugador.nodo_actual == saved_node, "Should restore node"
    assert game2.jugador.salud == saved_health, "Should restore health"
    
    print(f"✓ Game loaded successfully")
    print(f"  Restored node: {game2.jugador.nodo_actual}")
    print(f"  Restored health: {game2.jugador.salud}")
    
    # Cleanup
    import os
    os.remove("test_save.json")
    
    return game

def test_multiple_characters():
    """Test all character/difficulty combinations"""
    print("\nTesting all character/difficulty combinations...")
    
    characters = ["jason", "nightwing", "tim", "damian"]
    difficulties = ["facil", "normal", "dificil"]
    
    game = JuegoAventuraBase()
    success_count = 0
    
    for char in characters:
        for diff in difficulties:
            success = game.iniciar_juego(char, diff)
            if success:
                success_count += 1
                print(f"✓ {char} + {diff}: OK (node: {game.jugador.nodo_actual})")
            else:
                print(f"✗ {char} + {diff}: FAILED")
    
    print(f"\n✓ Successfully initialized {success_count}/{len(characters) * len(difficulties)} combinations")

def main():
    """Run all tests"""
    print("=" * 60)
    print("HISTORIAPY - GAME LOGIC TEST SUITE")
    print("=" * 60)
    
    try:
        game = test_game_initialization()
        game = test_start_game(game)
        game = test_story_navigation(game)
        game = test_save_load(game)
        test_multiple_characters()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
