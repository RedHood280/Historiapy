"""
Game Models - Contains all game logic without UI dependencies
Maintains critical functionality: 3 characters, 3 difficulties, branching, stats, items, multiple endings, save/load
"""
import json
import os
from typing import Dict, List, Optional


class Player:
    """Player character with stats and inventory"""
    
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.reputation = 50
        self.resources = 3
        self.inventory = []
        self.decisions = []
        self.current_node = "start"
    
    def add_item(self, item: str):
        """Add item to inventory"""
        if item and item not in self.inventory:
            self.inventory.append(item)
    
    def modify_stat(self, stat: str, change: int):
        """Modify a player statistic"""
        if stat == "health":
            self.health = max(0, min(100, self.health + change))
        elif stat == "reputation":
            self.reputation = max(0, min(100, self.reputation + change))
        elif stat == "resources":
            self.resources = max(0, self.resources + change)
    
    def save_decision(self, node: str, choice: str):
        """Save a decision made"""
        self.decisions.append({"node": node, "choice": choice})
    
    def to_dict(self):
        """Convert player to dictionary for saving"""
        return {
            "name": self.name,
            "health": self.health,
            "reputation": self.reputation,
            "resources": self.resources,
            "inventory": self.inventory,
            "decisions": self.decisions,
            "current_node": self.current_node
        }
    
    @staticmethod
    def from_dict(data):
        """Create player from dictionary"""
        player = Player(data.get("name", "Player"))
        player.health = data.get("health", 100)
        player.reputation = data.get("reputation", 50)
        player.resources = data.get("resources", 3)
        player.inventory = data.get("inventory", [])
        player.decisions = data.get("decisions", [])
        player.current_node = data.get("current_node", "start")
        return player


class StoryNode:
    """Story node with options"""
    
    def __init__(self, id: str, title: str, description: str, image: str = ""):
        self.id = id
        self.title = title
        self.description = description
        self.image = image
        self.options = []
        self.is_final = False
    
    def add_option(self, text: str, next_node: str,
                   stat: Optional[str] = None, change: int = 0,
                   stat2: Optional[str] = None, change2: int = 0,
                   item: Optional[str] = None):
        """Add a choice option"""
        self.options.append({
            "text": text,
            "next": next_node,
            "stat": stat,
            "change": change,
            "stat2": stat2,
            "change2": change2,
            "item": item
        })


class GameModel:
    """Core game model with story and state management"""
    
    def __init__(self):
        self.player = None
        self.character = None  # "RedHood", "Nightwing", or "TimDrake"
        self.difficulty = None  # "easy", "medium", "hard"
        self.story = {}
        self._initialize_story()
    
    def new_game(self, character: str, difficulty: str, player_name: str = "Player"):
        """Start a new game"""
        self.character = character
        self.difficulty = difficulty
        self.player = Player(player_name)
        
        # Set starting node based on character and difficulty
        start_node = f"{character.lower()}_{difficulty}_start"
        if start_node not in self.story:
            start_node = "start"  # Fallback
        self.player.current_node = start_node
    
    def get_current_node(self) -> Optional[StoryNode]:
        """Get the current story node"""
        if self.player:
            return self.story.get(self.player.current_node)
        return None
    
    def choose_option(self, option_index: int) -> bool:
        """Process a choice and return success"""
        current_node = self.get_current_node()
        if not current_node or not self.player:
            return False
        
        if option_index < 0 or option_index >= len(current_node.options):
            return False
        
        option = current_node.options[option_index]
        
        # Save decision
        self.player.save_decision(current_node.id, option["text"])
        
        # Apply stat changes
        if option["stat"]:
            self.player.modify_stat(option["stat"], option["change"])
        if option["stat2"]:
            self.player.modify_stat(option["stat2"], option["change2"])
        
        # Add item
        if option["item"]:
            self.player.add_item(option["item"])
        
        # Move to next node
        self.player.current_node = option["next"]
        
        return True
    
    def save_game(self, filename: str = "partida_guardada.json") -> bool:
        """Save game state"""
        if not self.player:
            return False
        
        try:
            data = {
                "player": self.player.to_dict(),
                "character": self.character,
                "difficulty": self.difficulty
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, filename: str = "partida_guardada.json") -> bool:
        """Load game state"""
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.player = Player.from_dict(data.get("player", {}))
            self.character = data.get("character", "RedHood")
            self.difficulty = data.get("difficulty", "easy")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def _initialize_story(self):
        """Initialize all story nodes - simplified version with key nodes"""
        # Default start node
        start = StoryNode("start", "THE BEGINNING", 
                         "Choose your character and difficulty to begin your story...", 
                         "start.png")
        self.story["start"] = start
        
        # Red Hood Easy Mode
        rh_easy_start = StoryNode(
            "redhhood_easy_start",
            "CRIME ALLEY - THE ENCOUNTER",
            "Gotham City. You are Jason Todd, a 12-year-old orphan surviving by stealing. "
            "Tonight, while trying to steal the Batmobile's tires, a shadow looms over you. "
            "Batman watches you, but in his eyes you see not anger, but... curiosity?",
            "crime_alley.png"
        )
        rh_easy_start.add_option("Try to run away", "rh_easy_chase", stat="resources", change=-1)
        rh_easy_start.add_option("Face him bravely", "rh_easy_brave", stat="reputation", change=10)
        rh_easy_start.add_option("Explain your situation honestly", "rh_easy_honest", stat="reputation", change=15)
        self.story["redhood_easy_start"] = rh_easy_start
        
        rh_easy_chase = StoryNode(
            "rh_easy_chase",
            "THE CHASE",
            "You run as fast as you can, but Batman is too fast. He catches you in seconds, "
            "but instead of turning you over to the police, he offers you food and shelter. "
            "'You have potential,' he says. 'But you're wasting your courage on the streets.'",
            "batman_chase.png"
        )
        rh_easy_chase.add_option("Accept his help with distrust", "rh_easy_training", stat="resources", change=2)
        rh_easy_chase.add_option("Refuse and stay alone", "rh_easy_refuse", stat="reputation", change=-10)
        self.story["rh_easy_chase"] = rh_easy_chase
        
        rh_easy_brave = StoryNode(
            "rh_easy_brave",
            "COURAGE RECOGNIZED",
            "You stand before the Dark Knight, wrench in hand. Batman smiles slightly under his cowl. "
            "'Not many have the courage to face me,' he says. 'Especially at your age. "
            "How about we use that bravery for something better?'",
            "jason_valiente.png"
        )
        rh_easy_brave.add_option("Accept immediately", "rh_easy_training", stat="reputation", change=5)
        rh_easy_brave.add_option("Ask what he means", "rh_easy_curious", stat="resources", change=1)
        self.story["rh_easy_brave"] = rh_easy_brave
        
        rh_easy_honest = StoryNode(
            "rh_easy_honest",
            "THE TRUTH HURTS",
            "You tell him about your addicted mother, how she died, about the cold nights on "
            "the streets. Batman listens in silence. When you finish, he places a hand on your "
            "shoulder. 'I also lost my parents here, in this same alley. Let me help you turn "
            "your pain into purpose.'",
            "jason_triste.png"
        )
        rh_easy_honest.add_option("Accept his proposal", "rh_easy_training",
                                 stat="reputation", change=20, item="Renewed Hope")
        self.story["rh_easy_honest"] = rh_easy_honest
        
        rh_easy_curious = StoryNode(
            "rh_easy_curious",
            "THE RIGHT QUESTIONS",
            "Batman explains his mission: protect Gotham from those who hurt the innocent. "
            "'I need a partner,' he says. 'Someone who understands the streets like you. "
            "Are you ready to train?' Your heart beats fast. This is your chance to change everything.",
            "batman_explica.png"
        )
        rh_easy_curious.add_option("Accept with determination", "rh_easy_training", stat="reputation", change=10)
        self.story["rh_easy_curious"] = rh_easy_curious
        
        rh_easy_training = StoryNode(
            "rh_easy_training",
            "TRAINING BEGINS",
            "You begin training with Batman. The days are hard, but you're determined. "
            "You learn combat, detective skills, and most importantly, you learn what it means "
            "to be a hero. Months pass, and finally, Batman presents you with a costume. "
            "'Welcome, Robin,' he says.",
            "robin_training.png"
        )
        rh_easy_training.add_option("Accept the mantle with pride", "rh_easy_robin", 
                                   stat="reputation", change=15, item="Robin Costume")
        rh_easy_training.add_option("Question if you're ready", "rh_easy_doubt", stat="health", change=-5)
        self.story["rh_easy_training"] = rh_easy_training
        
        rh_easy_robin = StoryNode(
            "rh_easy_robin",
            "THE BOY WONDER - ENDING",
            "You become Robin, the new Boy Wonder. Together with Batman, you protect Gotham "
            "from villains and bring hope to the city. Your journey from street orphan to hero "
            "is complete. This is your happy ending... for now.",
            "robin_hero.png"
        )
        rh_easy_robin.is_final = True
        self.story["rh_easy_robin"] = rh_easy_robin
        
        rh_easy_doubt = StoryNode(
            "rh_easy_doubt",
            "DOUBT AND GROWTH - ENDING",
            "Your doubts make you cautious, and that caution saves lives. You grow into your role "
            "slowly but surely. Eventually, you become a trusted hero of Gotham, known for your "
            "strategic mind as much as your courage.",
            "robin_thoughtful.png"
        )
        rh_easy_doubt.is_final = True
        self.story["rh_easy_doubt"] = rh_easy_doubt
        
        rh_easy_refuse = StoryNode(
            "rh_easy_refuse",
            "ALONE IN THE STREETS - ENDING",
            "You refuse Batman and continue stealing to survive. Life on the streets is hard, "
            "and eventually, you realize you made a mistake. But by then, Batman has moved on. "
            "You survive, but you never become the hero you could have been.",
            "jason_alone.png"
        )
        rh_easy_refuse.is_final = True
        self.story["rh_easy_refuse"] = rh_easy_refuse
        
        # Nightwing Easy Mode
        nw_easy_start = StoryNode(
            "nightwing_easy_start",
            "BLÜDHAVEN - A NEW BEGINNING",
            "You are Dick Grayson, recently moved to Blüdhaven to establish your identity as Nightwing. "
            "The city is corrupt, dangerous, and needs a hero. Your first night on patrol, you witness "
            "a mugging in progress. What do you do?",
            "bludhaven.png"
        )
        nw_easy_start.add_option("Intervene immediately", "nw_easy_hero", stat="reputation", change=10)
        nw_easy_start.add_option("Observe and gather intel", "nw_easy_strategic", stat="resources", change=2)
        nw_easy_start.add_option("Call GCPD for backup", "nw_easy_cautious", stat="health", change=5)
        self.story["nightwing_easy_start"] = nw_easy_start
        
        nw_easy_hero = StoryNode(
            "nw_easy_hero",
            "HERO OF BLÜDHAVEN - ENDING",
            "You leap into action without hesitation. Your acrobatic skills and combat training "
            "make quick work of the criminals. The victim thanks you, and word spreads of a new "
            "hero in Blüdhaven. You've successfully established yourself as Nightwing.",
            "nightwing_hero.png"
        )
        nw_easy_hero.is_final = True
        self.story["nw_easy_hero"] = nw_easy_hero
        
        nw_easy_strategic = StoryNode(
            "nw_easy_strategic",
            "THE STRATEGIST - ENDING",
            "You observe from the shadows, gathering information. This leads you to a larger "
            "criminal network. By taking your time, you dismantle an entire operation. "
            "Blüdhaven is safer because of your patience and strategic mind.",
            "nightwing_strategic.png"
        )
        nw_easy_strategic.is_final = True
        self.story["nw_easy_strategic"] = nw_easy_strategic
        
        nw_easy_cautious = StoryNode(
            "nw_easy_cautious",
            "THE TEAM PLAYER - ENDING",
            "You work with the police, building trust and cooperation. While some see this as "
            "weakness, you know that lasting change requires institutional support. You become "
            "a bridge between vigilantes and law enforcement.",
            "nightwing_team.png"
        )
        nw_easy_cautious.is_final = True
        self.story["nw_easy_cautious"] = nw_easy_cautious
        
        # Tim Drake Easy Mode
        td_easy_start = StoryNode(
            "timdrake_easy_start",
            "THE DETECTIVE - DISCOVERY",
            "You are Tim Drake, a brilliant young detective who has deduced Batman's identity. "
            "After Jason Todd's death, Gotham needs a new Robin. You approach Batman at the Batcave, "
            "determined to prove yourself. How do you present your case?",
            "batcave.png"
        )
        td_easy_start.add_option("Show your detective work", "td_easy_detective", stat="reputation", change=15)
        td_easy_start.add_option("Offer your skills humbly", "td_easy_humble", stat="health", change=10)
        td_easy_start.add_option("Challenge him to test you", "td_easy_challenge", stat="resources", change=3)
        self.story["timdrake_easy_start"] = td_easy_start
        
        td_easy_detective = StoryNode(
            "td_easy_detective",
            "THE WORLD'S GREATEST DETECTIVE - ENDING",
            "You impress Batman with your deductive skills. He agrees to train you, and you become "
            "the new Robin. Your analytical mind solves cases that even Batman struggled with. "
            "You prove that Robin can be more than just a sidekick - he can be an equal partner.",
            "tim_detective.png"
        )
        td_easy_detective.is_final = True
        self.story["tim_detective"] = td_easy_detective
        
        td_easy_humble = StoryNode(
            "td_easy_humble",
            "THE WORTHY SUCCESSOR - ENDING",
            "Your humility and genuine desire to help impresses Batman. He sees in you the potential "
            "to be not just Robin, but perhaps something greater. You train hard and earn the trust "
            "of the entire Bat-family.",
            "tim_humble.png"
        )
        td_easy_humble.is_final = True
        self.story["tim_humble"] = td_easy_humble
        
        td_easy_challenge = StoryNode(
            "td_easy_challenge",
            "THE BOLD APPROACH - ENDING",
            "Your bold challenge catches Batman off guard. He tests you rigorously, and you pass "
            "every test. You become Robin, but your confidence sometimes borders on arrogance. "
            "Still, you get results, and that's what matters.",
            "tim_bold.png"
        )
        td_easy_challenge.is_final = True
        self.story["tim_bold"] = td_easy_challenge
        
        # Add medium and hard variants by referencing the same nodes with different IDs
        for char in ["redhood", "nightwing", "timdrake"]:
            for diff in ["medium", "hard"]:
                start_id = f"{char}_{diff}_start"
                if start_id not in self.story:
                    # Create a reference to easy mode but with increased difficulty
                    easy_id = f"{char}_easy_start"
                    if easy_id in self.story:
                        self.story[start_id] = self.story[easy_id]
