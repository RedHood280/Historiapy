"""
main.py - Entry point for the Kivy application
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from controller import GameController
from widgets import AnimatedHoverButton
from utils import play_sound
import os


class MenuScreen(Screen):
    """Main menu screen"""
    pass


class CharacterSelectScreen(Screen):
    """Character selection screen"""
    pass


class DifficultySelectScreen(Screen):
    """Difficulty selection screen"""
    pass


class GameScreen(Screen):
    """Main game screen"""
    
    def on_enter(self):
        """Called when entering the game screen"""
        app = App.get_running_app()
        if app.controller:
            # Play transition sound and animation
            play_sound('transition', volume=0.3)
            if self.ids.get('scene_image'):
                app.controller.play_transition_animation(self.ids.scene_image, duration=0.5)
    
    def update_after_choice(self):
        """Called after making a choice"""
        app = App.get_running_app()
        if app.controller:
            # Play transition sound and animation
            play_sound('transition', volume=0.3)
            if self.ids.get('scene_image'):
                app.controller.play_transition_animation(self.ids.scene_image, duration=0.3)


class HistoriaPyApp(App):
    """Main application class"""
    
    selected_character = StringProperty('jason')
    
    def build(self):
        """Build the application"""
        self.title = 'Red Hood - Historia Interactiva'
        
        # Initialize controller
        self.controller = GameController(ui_callback=self.update_game_screen)
        
        # Load kv file
        self.load_kv('views.kv')
        
        # Create screen manager
        sm = ScreenManager()
        
        return sm
    
    def select_character(self, character):
        """Handle character selection"""
        play_sound('click', volume=0.5)
        self.selected_character = character
        self.root.current = 'difficulty_select'
    
    def select_difficulty(self, difficulty):
        """Handle difficulty selection and start game"""
        play_sound('click', volume=0.5)
        
        # Determine character name
        character_names = {
            'jason': 'Jason Todd',
            'dick': 'Dick Grayson',
            'tim': 'Tim Drake',
            'damian': 'Damian Wayne'
        }
        nombre = character_names.get(self.selected_character, 'Héroe')
        
        # Start new game
        nodo = self.controller.nueva_partida(nombre, self.selected_character, difficulty)
        
        # Navigate to game screen
        self.root.current = 'game'
        
        # Update game screen
        if nodo:
            self.update_game_screen(nodo, [])
    
    def update_game_screen(self, nodo, cambios):
        """Update the game screen with new node"""
        if not nodo:
            return
        
        game_screen = self.root.get_screen('game')
        
        # Update player stats
        jugador = self.controller.get_jugador()
        if jugador:
            game_screen.ids.player_name.text = f'👤 {jugador.nombre}'
            game_screen.ids.salud_label.text = f'❤️ {jugador.salud}'
            game_screen.ids.reputacion_label.text = f'⭐ {jugador.reputacion}'
            game_screen.ids.recursos_label.text = f'💎 {jugador.recursos}'
        
        # Update scene
        game_screen.ids.scene_title.text = nodo.titulo
        game_screen.ids.scene_description.full_text = nodo.descripcion
        
        # Update image
        if nodo.imagen:
            image_path = os.path.join('assets', 'images', nodo.imagen)
            if os.path.exists(image_path):
                game_screen.ids.scene_image.source = image_path
            else:
                game_screen.ids.scene_image.source = ''
        else:
            game_screen.ids.scene_image.source = ''
        
        # Update options
        options_container = game_screen.ids.options_container
        options_container.clear_widgets()
        
        if nodo.es_final:
            # Show final screen options
            self.show_final_options(options_container, nodo)
        else:
            # Show normal options
            for i, opcion in enumerate(nodo.opciones, 1):
                btn = AnimatedHoverButton(
                    text=f'{i}. {opcion["texto"]}',
                    size_hint_y=None,
                    height=60
                )
                btn.bind(on_release=lambda x, opt=opcion: self.choose_option(nodo, opt))
                options_container.add_widget(btn)
        
        # Show changes popup if any
        if cambios:
            self.show_changes_popup(cambios)
        
        # Trigger transition animation
        game_screen.update_after_choice()
    
    def show_final_options(self, container, nodo):
        """Show options for final screen"""
        # Show stats
        stats_label = Label(
            text=self.get_final_stats_text(),
            color=[1, 1, 1, 1],
            size_hint_y=None,
            height=100
        )
        container.add_widget(stats_label)
        
        # Nueva partida button
        btn_new = AnimatedHoverButton(
            text='🔄 Nueva Partida',
            size_hint_y=None,
            height=60
        )
        btn_new.bind(on_release=lambda x: self.new_game_from_final())
        container.add_widget(btn_new)
        
        # Menu button
        btn_menu = AnimatedHoverButton(
            text='🏠 Menú Principal',
            size_hint_y=None,
            height=60,
            normal_color=[0.4, 0.1, 0.1, 1]
        )
        btn_menu.bind(on_release=lambda x: self.exit_to_menu())
        container.add_widget(btn_menu)
    
    def get_final_stats_text(self):
        """Get final statistics text"""
        stats = self.controller.get_player_stats()
        if stats:
            return (f"Decisiones: {stats['decisiones']}\n"
                   f"Salud: {stats['salud']}/100\n"
                   f"Reputación: {stats['reputacion']}/100\n"
                   f"Recursos: {stats['recursos']}\n"
                   f"Items: {len(stats['inventario'])}")
        return ""
    
    def choose_option(self, nodo, opcion):
        """Handle option selection (with debounce in controller)"""
        self.controller.choose_option(nodo, opcion)
    
    def show_changes_popup(self, cambios):
        """Show popup with stat changes"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text='Consecuencias:\n\n' + '\n'.join(cambios),
            color=[1, 1, 1, 1]
        )
        content.add_widget(label)
        
        btn = Button(
            text='OK',
            size_hint_y=0.3,
            background_color=[0.87, 0.14, 0.19, 1]
        )
        content.add_widget(btn)
        
        popup = Popup(
            title='Cambios',
            content=content,
            size_hint=(0.6, 0.4)
        )
        btn.bind(on_release=popup.dismiss)
        popup.open()
    
    def save_game(self):
        """Save the current game"""
        play_sound('click', volume=0.5)
        if self.controller.guardar_partida():
            self.show_message('Guardado', 'Partida guardada exitosamente')
        else:
            self.show_message('Error', 'No se pudo guardar la partida')
    
    def load_game(self):
        """Load a saved game"""
        play_sound('click', volume=0.5)
        if self.controller.cargar_partida():
            self.show_message('Éxito', 'Partida cargada correctamente')
            self.root.current = 'game'
        else:
            self.show_message('Error', 'No se encontró ninguna partida guardada')
    
    def confirm_exit_to_menu(self):
        """Show confirmation dialog before exiting to menu"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text='¿Volver al menú principal?\nAsegúrate de guardar tu progreso.',
            color=[1, 1, 1, 1]
        )
        content.add_widget(label)
        
        btn_box = BoxLayout(spacing=10, size_hint_y=0.3)
        
        btn_yes = Button(
            text='Sí',
            background_color=[0.87, 0.14, 0.19, 1]
        )
        btn_no = Button(
            text='No',
            background_color=[0.4, 0.4, 0.4, 1]
        )
        
        btn_box.add_widget(btn_yes)
        btn_box.add_widget(btn_no)
        content.add_widget(btn_box)
        
        popup = Popup(
            title='Confirmar',
            content=content,
            size_hint=(0.6, 0.4)
        )
        
        btn_yes.bind(on_release=lambda x: (popup.dismiss(), self.exit_to_menu()))
        btn_no.bind(on_release=popup.dismiss)
        
        popup.open()
    
    def exit_to_menu(self):
        """Exit to main menu"""
        play_sound('click', volume=0.5)
        self.root.current = 'menu'
    
    def new_game_from_final(self):
        """Start new game from final screen"""
        play_sound('click', volume=0.5)
        self.root.current = 'character_select'
    
    def show_message(self, title, message):
        """Show a simple message popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(text=message, color=[1, 1, 1, 1])
        content.add_widget(label)
        
        btn = Button(
            text='OK',
            size_hint_y=0.3,
            background_color=[0.87, 0.14, 0.19, 1]
        )
        content.add_widget(btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.5, 0.3)
        )
        btn.bind(on_release=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    HistoriaPyApp().run()
