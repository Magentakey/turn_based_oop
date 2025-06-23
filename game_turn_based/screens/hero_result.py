from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
# from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

Builder.load_file("screens/hero_result.kv")

RARITY_COLORS = {
    "common": [0.894, 0.894, 0.894],
    "uncommon": [0.251, 0.835, 0.024],
    "rare": [0.518, 0.627, 0.957],
    "epic": [0.906, 0.467, 0.871],
    "legendary": [1, 0.949, 0.4],
}

class HeroResultScreen(Screen):
    def on_enter(self):
        self.display_heroes()

    def display_heroes(self):
        self.ids.hero_grid1.clear_widgets()
        self.ids.hero_grid2.clear_widgets()
        gm = MDApp.get_running_app().manager
        self.heroes = gm.hero_pool

        heroGridIndex = 1
        for hero in self.heroes:
            color = RARITY_COLORS.get(hero.special_skill.rarity, [1, 1, 1, 1])
            brightness = sum(color[:3]) / 3
            text_color = (0, 0, 0, 1) if brightness > 0.6 else (0, 0, 0, 1)

            box = BoxLayout(orientation='vertical', padding=5, spacing=5, size_hint_y= 1)

            with box.canvas.before:
                Color(*color)
                bg_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[12])

            def bind_rect(rect):
                def update_rect(instance, value):
                    rect.pos = instance.pos
                    rect.size = instance.size
                return update_rect

            box.bind(pos=bind_rect(bg_rect), size=bind_rect(bg_rect))

            skill_names = ", ".join([s.name for s in hero.skills])
            special_name = hero.special_skill.name if hero.special_skill else "-"

            for label_text in [
                hero.name,
                f"Class: {getattr(hero, 'hero_class', 'Hero')}", f"Type: {hero.special_skill.rarity}", "",
                f"HP: {hero.hp}", f"MP: {hero.mp}", f"ATK: {hero.atk}", f"DEF: {hero.defense}", "",
                f"skills: {skill_names}", "",
                f"special skill: {special_name}",
            ]:
                box.add_widget(Label(text=label_text, font_size=22, text_size= (300, None), halign='center', valign='middle', color=text_color, bold=True))
            if heroGridIndex <= 3:
                self.ids.hero_grid1.add_widget(box)
                heroGridIndex += 1
            else:
                self.ids.hero_grid2.add_widget(box)
                

    def go_to_item_distribution(self):
        gm = MDApp.get_running_app().manager
        gm.player_team = gm.hero_pool
        self.manager.current = "item_distribution"
