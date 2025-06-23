from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
# from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_file("screens/main_menu.kv")

class MainMenuScreen(Screen):
  # app = MDApp.get_running_app()

  def on_enter(self):
    MDApp.get_running_app().play_music("assets/sound/the_path_of_the_goblin_king.mp3")
    
    self.ids.change_mode.clear_widgets()
    
    self.ids.change_mode.add_widget(Button(text="Play",
                                    font_size= 30,
                                    color= (0,0,0,1),
                                    bold= True,
                                    italic= True,
                                    background_normal= "",
                                    background_color= (0.82, 0.776, 1, 1),
                                    on_release=lambda inst: self.on_play()))

  def on_play(self):


    self.ids.change_mode.clear_widgets()
    box = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=15)

    box.add_widget(Button(text= "normal",
                font_size= 24,
                size_hint= (0.5, 1),
                color= (0,0,0,1),
                bold= True,
                italic= True,
                background_normal= "",
                background_color= (0.82, 0.776, 1, 1),
                on_release=lambda inst: self.mode_normal()))
    box.add_widget(Button(text= "overgeared",
                font_size= 24,
                color= (0,0,0,1),
                size_hint= (0.5, 1),
                bold= True,
                italic= True,
                background_normal= "",
                background_color= (0.82, 0.776, 1, 1),
                on_release=lambda inst: self.mode_overgeared()))
    self.ids.change_mode.add_widget(box)
  def mode_normal(self):
    app = MDApp.get_running_app()
    app.manager.init_skills_and_items()
    app.manager.create_heroes_and_bosses()
    
    app.play_music("assets/sound/the_path_of_the_goblin_king.mp3")

    self.manager.current = "hero_result"
  def mode_overgeared(self):
    app = MDApp.get_running_app()
    app.manager.init_skills_and_items()
    app.manager.create_heroes_op_and_bosses()
    
    app.play_music("assets/sound/the_path_of_the_goblin_king.mp3")

    self.manager.current = "hero_result"
    # print("Test")
    # box.add_widget(MDLinearProgressIndicator(value=hero.hp / hero.max_hp * 100, indicator_color=(1, 0, 0), size_hint=(1, 0.2)))
    # box.add_widget(MDLinearProgressIndicator(value=hero.mp / hero.max_mp * 100, indicator_color=(0.482, 0.463, 1), size_hint=(1, 0.2)))
    # box.add_widget(Label(text=f"Class: {hero.hero_class}", font_size=22, color=highlight_color))
    # box.add_widget(Label(text=f"ATK: {hero.atk}", font_size=22, color=highlight_color))
    # box.add_widget(Label(text=f"HP: {hero.hp}/{hero.max_hp}", font_size=22, color=highlight_color))
    # box.add_widget(Label(text=f"MP: {hero.mp}/{hero.max_mp}", font_size=22, color=highlight_color))

    # if heroBoxIndex <= 3:
    #     self.ids.hero_box1.add_widget(box)
    #     heroBoxIndex += 1
    # else:
    #     self.ids.hero_box2.add_widget(box)

    # Ganti musik

  def on_exit(self):
    MDApp.get_running_app().stop()
