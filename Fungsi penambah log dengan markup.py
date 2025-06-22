# battle_log.py (attach ke controller BattleScreen)
from kivy.uix.label import Label
from kivy.metrics import dp
import gui_theme as theme

class BattleLogMixin:
    def write_log(self, text, is_turn_now=False):
        """Tambahkan baris ke log_container"""
        color = theme.HIGHLIGHT if is_turn_now else theme.LIGHT_TEXT
        prefix = "[b]" if is_turn_now else ""
        suffix = "[/b]" if is_turn_now else ""
        markup_text = f"[color={color.hex()}]{prefix}{text}{suffix}[/color]"

        line = Label(text=markup_text,
                     markup=True,
                     size_hint_y=None,
                     halign="left",
                     valign="middle",
                     text_size=(self.width - dp(16), None))
        line.bind(texture_size=lambda s, _v: setattr(s, "height", s.texture_size[1] + dp(4)))
        self.ids.log_container.add_widget(line)
