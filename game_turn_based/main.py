# from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.main_menu import MainMenuScreen
from screens.hero_result import HeroResultScreen
from screens.item_distribution import ItemDistributionScreen
from screens.battle_screen import BattleScreen
from screens.shop_screen import ShopScreen
from game_manager import GameManager
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import NoTransition



class RPGApp(MDApp):
    def build(self):
        self.manager = GameManager()
        self.bgm = None  # untuk menyimpan musik aktif

        # sm = ScreenManager()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(HeroResultScreen(name='hero_result'))
        sm.add_widget(ItemDistributionScreen(name='item_distribution'))
        sm.add_widget(BattleScreen(name='battle_screen'))
        sm.add_widget(ShopScreen(name='shop_screen'))
        return sm

    def play_music(self, file_path, loop=True):
        from kivy.core.audio import SoundLoader

        # Stop jika sedang ada musik
        if self.bgm:
            self.bgm.stop()

        # Load dan play musik baru
        self.bgm = SoundLoader.load(file_path)
        if self.bgm:
            self.bgm.loop = loop
            self.bgm.play()

if __name__ == "__main__":
    RPGApp().run()
