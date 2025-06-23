from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
# from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
import random

Builder.load_file("screens/item_distribution.kv")

RARITY_COLORS = {
    "common": [0.894, 0.894, 0.894],
    "uncommon": [0.251, 0.835, 0.024],
    "rare": [0.518, 0.627, 0.957],
    "epic": [0.906, 0.467, 0.871],
    "legendary": [1, 0.949, 0.4],
}

class ItemDistributionScreen(Screen):
    def on_enter(self):
        self.generate_items()

    def generate_items(self):
        self.ids.item_grid.clear_widgets()
        app = MDApp.get_running_app()
        gm = app.manager
        heroes = gm.player_team
        item_pool = gm.item_pool

        if not heroes:
            print("⚠️ player_team kosong. Pastikan sudah dipilih dari GameManager.")
            return

        items = random.sample(item_pool, 3)

        for item in items:
            receiver = random.choice(heroes)
            color = RARITY_COLORS.get(item.rarity, [1, 1, 1, 1])
            brightness = sum(color[:3]) / 3
            text_color = (0, 0, 0, 1) if brightness > 0.6 else (0, 0, 0, 1)

            box = BoxLayout(orientation='vertical', padding=5, spacing=5, size_hint_y=None, height=180)

            with box.canvas.before:
                Color(*color)
                bg_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[12])

            def bind_rect(rect):
                def update(instance, value):
                    rect.pos = instance.pos
                    rect.size = instance.size
                return update

            box.bind(pos=bind_rect(bg_rect), size=bind_rect(bg_rect))

            box.add_widget(Label(text=item.name, font_size=26, bold=True, color=text_color))
            box.add_widget(Label(
                text=f"Effect: {item.description}",
                font_size=16,
                color=text_color,
                size_hint_x=None,
                width=280,  # sesuaikan lebar box
                text_size=(280, None),  # harus sama dengan width
                halign='center',
                valign='middle'
            ))
            mod_lines = []
            for key, val in item.stat_modifiers.items():
                sign = "+" if val >= 0 else ""
                mod_lines.append(f"{key} {sign}{val}")
            mod_text = ", ".join(mod_lines)

            box.add_widget(Label(
                text=f"Stats: {mod_text}",
                font_size=22,
                color=text_color,
                size_hint_x=None,
                width=280,
                text_size=(280, None),
                halign='center'
            ))            
            box.add_widget(Label(text=f"Rarity: {item.rarity}", font_size=22, color=text_color))
            box.add_widget(Label(text=f"Received by: {receiver.name}", font_size=20, color=text_color))

            receiver.equipped_items.append(item)
            item.apply_to(receiver)

            self.ids.item_grid.add_widget(box)

    def go_to_battle(self):
        self.manager.current = "battle_screen"
