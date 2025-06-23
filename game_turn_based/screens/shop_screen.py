from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
# from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty

Builder.load_file("screens/shop_screen.kv")

RARITY_COLORS = {
    "common": [0.894, 0.894, 0.894],
    "uncommon": [0.251, 0.835, 0.024],
    "rare": [0.518, 0.627, 0.957],
    "epic": [0.906, 0.467, 0.871],
    "legendary": [1, 0.949, 0.4],
}

class ShopScreen(Screen):
    selected_hero = None
    
    def on_enter(self):
        self.manager.get_screen("battle_screen").ids.turn_label.text = ""
        gm = MDApp.get_running_app().manager
        gm.shop.refresh_stock()

        self.selected_hero = gm.player_team[0]  # default ke hero pertama
        self.display_heroes()
        self.display_shop_items()
        self.display_hero_items()
        

    def display_heroes(self):
        self.ids.hero_list.clear_widgets()
        gm = MDApp.get_running_app().manager

        alive_heroes = [h for h in gm.player_team if h.is_alive() and not h.escaped]

        # Pastikan selected_hero valid
        if self.selected_hero not in alive_heroes:
            self.selected_hero = alive_heroes[0] if alive_heroes else None

        for hero in alive_heroes:
            btn = Button(
                text=f"{hero.name}\nGold: {hero.gold}",
                size_hint_y=None,
                height=60
            )
            btn.background_color = (0.4, 0.4, 1, 1) if hero == self.selected_hero else (0.3, 0.3, 0.3, 1)
            btn.bind(on_release=lambda inst, h=hero: self.select_hero(h))
            self.ids.hero_list.add_widget(btn)

        self.display_hero_items()  # tampilkan item milik hero yang masih valid

    def select_hero(self, hero):
        self.selected_hero = hero
        self.display_heroes()  # otomatis juga update hero items

    def display_shop_items(self):
        self.ids.shop_items.clear_widgets()
        shop = MDApp.get_running_app().manager.shop
        for item in shop.current_stock:
            self.ids.shop_items.add_widget(self.make_item_box(item, source="shop"))

    def display_hero_items(self):
        self.ids.hero_items.clear_widgets()
        for item in self.selected_hero.equipped_items:
            self.ids.hero_items.add_widget(self.make_item_box(item, source="hero"))

    def make_item_box(self, item, source="shop"):
        if source == "shop":
            box = BoxLayout(orientation='vertical', padding=5, spacing=2, size_hint=(None, None), size=(240, 180))
        else:  # hero item
            box = BoxLayout(orientation='vertical', padding=5, spacing=2, size_hint=(1, None), height=120)
        color = RARITY_COLORS.get(item.rarity, [1, 1, 1, 1])
        brightness = sum(color[:3]) / 3
        text_color = (0, 0, 0, 1) if brightness > 0.6 else (0, 0, 0, 1)

        with box.canvas.before:
            Color(*color)
            bg = RoundedRectangle(pos=box.pos, size=box.size, radius=[10])

        def update_rect(instance, value):
            bg.pos = instance.pos
            bg.size = instance.size

        box.bind(pos=update_rect, size=update_rect)

        box.add_widget(Label(text=item.name, font_size=22, bold=True, color=text_color))
        box.add_widget(Label(text=f"{item.rarity}", font_size=20, color=text_color))
        effect_str = ", ".join([f"{k}: {v:+}" for k, v in item.stat_modifiers.items()])
        box.add_widget(Label(text=effect_str, font_size=18, color=text_color))

        if source == "shop":
            box.add_widget(Label(text=f"{item.price} gold", font_size=18, color=text_color))
            box.bind(on_touch_down=lambda w, t: self.buy_item(item) if w.collide_point(*t.pos) else None)
        elif source == "hero":
            box.add_widget(Label(text="Click to sell", font_size=16, color=text_color))
            box.bind(on_touch_down=lambda w, t: self.confirm_sell(item) if w.collide_point(*t.pos) else None)

        return box

    def buy_item(self, item):
        gm = MDApp.get_running_app().manager
        shop = gm.shop
        player = self.selected_hero

        # Cek kapasitas item terlebih dahulu
        if len(player.equipped_items) >= 5:
            self.show_popup("Inventory Penuh", f"{player.name} sudah membawa 5 item.")
            return

        if item in shop.current_stock:
            index = shop.current_stock.index(item)

            if player.gold < item.price:
                self.show_popup("Gold Kurang", f"{player.name} tidak punya cukup gold.")
                return

            shop.buy(player, index)

            self.display_shop_items()
            self.display_hero_items()
            self.display_heroes()
        else:
            self.show_popup("Item Error", "Item tidak tersedia.")

    def confirm_sell(self, item):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        # item = self.equipped_items.pop(index)
        # item.remove_from(self)
        refund = int(item.price * 0.5)
        # self.gold += refund
        content.add_widget(Label(text=f"Confirm sell? for {refund} gold."))

        btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
        btn_yes = Button(text="Yes", background_color=(0.6, 1, 0.6, 1))
        btn_no = Button(text="No", background_color=(1, 0.4, 0.4, 1))
        btns.add_widget(btn_no)
        btns.add_widget(btn_yes)
        content.add_widget(btns)

        popup = Popup(title="Sell Item", content=content, size_hint=(None, None), size=(300, 200))
        btn_no.bind(on_release=popup.dismiss)

        def do_sell(instance):
            # Proses jual
            gm = MDApp.get_running_app().manager
            shop = gm.shop
            player = self.selected_hero

            if item in player.equipped_items:
                index = player.equipped_items.index(item)
                player.sell_item(index, shop)

                popup.dismiss()
                self.display_hero_items()
                self.display_heroes()
                self.display_shop_items()

        btn_yes.bind(on_release=do_sell)
        popup.open()
        
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message))
        btn = Button(text="OK", size_hint_y=None, height=40)
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 180))
        btn.bind(on_release=popup.dismiss)
        popup.open()
        
    def next_shop(self):
        gm = MDApp.get_running_app().manager
        gm.round_number = 0
        gm.current_round_index += 1
        gm.phase_round = gm.round_sequence[gm.current_round_index % len(gm.round_sequence)]
        self.manager.current = "battle_screen"
