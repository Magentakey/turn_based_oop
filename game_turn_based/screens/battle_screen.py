from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.progressindicator import MDLinearProgressIndicator
# from kivy.app import App
from kivymd.app import MDApp
import random

Builder.load_file("screens/battle_screen.kv")

RARITY_COLORS = {
    "common": [0.894, 0.894, 0.894],
    "uncommon": [0.251, 0.835, 0.024],
    "rare": [0.518, 0.627, 0.957],
    "epic": [0.906, 0.467, 0.871],
    "legendary": [1, 0.949, 0.4],
}

class BattleScreen(Screen):
    turn_index = NumericProperty(0)
    players = ListProperty([])
    boss = ObjectProperty(None)
    phase = "hero"
    
    def on_enter(self):
        gm = MDApp.get_running_app().manager
        self.players = gm.player_team
        self.boss = gm.boss
        self.turn_index = 0
        if not gm.round_number or gm.round_number >= 1:
            gm.round_number = gm.next_round()  # satu putaran semua hero + boss 
            # self.ids.turn_info.text += f"Turn info will be shown here\n"
        self.phase_turn = "hero"

        self.update_phase()

    def update_phase(self):
        gm = MDApp.get_running_app().manager
        # gm.round_number = 0
        # gm.current_round_index += 1
        gm.phase_round = gm.round_sequence[gm.current_round_index % len(gm.round_sequence)]
        
        if gm.phase_round == "mobs":
            gm.create_mobs()
            self.mobs = gm.mobs_pool
        elif gm.phase_round == "shop":
            self.go_to_shop()
            
        # self.ids.turn_label.text = f"Turn {gm.round_number}"
        self.update_phase_label()

        # self.update_status_boxes()
        self.update_turn()

    def update_phase_label(self):
        gm = MDApp.get_running_app().manager
        phase_list = gm.round_sequence
        active_index = gm.current_round_index % len(phase_list)

        label_parts = []
        for i, phase in enumerate(phase_list):
            if i == active_index:
                # Tambahkan highlight hijau
                label_parts.append(f"[b][color=00ff00]>> {phase} <<[/color][/b]")
            else:
                label_parts.append(phase)

        full_text = " - ".join(label_parts)
        self.ids.turn_label_.text = full_text

    def update_status_boxes(self):
        gm = MDApp.get_running_app().manager
        # Hapus dan render ulang hero dan boss box tanpa reset turn
        self.ids.hero_box1.clear_widgets()
        self.ids.hero_box2.clear_widgets()
        self.ids.boss_box.clear_widgets()

        print(f"turn index  {self.turn_index}")
        # print(f"mobs pool {gm.mobs_pool}")
        print(f"len mobs pool {len(gm.mobs_pool)}")
        print(f"phase_turn {self.phase_turn}")
        print(f"phase_round {gm.phase_round}")
        print(f"current round index {gm.current_round_index}")
        print(f"round number {gm.round_number}")
        print(f"=============")
        
        if gm.phase_round == "boss":
            # Boss box
            boss_color = RARITY_COLORS.get(self.boss.special_skill.rarity, [0.3, 0.3, 0.3, 1])
            boss_box = BoxLayout(orientation='vertical', padding=5, spacing=5)

            with boss_box.canvas.before:
                Color(*boss_color)
                self.boss_bg = RoundedRectangle(pos=boss_box.pos, size=boss_box.size, radius=[8])
            boss_box.bind(pos=self._update_bg(self.boss_bg), size=self._update_bg(self.boss_bg))

            boss_btn = Button(text=self.boss.name, font_size=22, bold=True,
                            on_release=lambda inst: self.show_boss_popup(self.boss), color=[1,1,1,1])
            boss_box.add_widget(boss_btn)
            boss_box.add_widget(MDLinearProgressIndicator(value=self.boss.hp / self.boss.max_hp * 100, indicator_color=(1,0,0), size_hint=(1,0.2)))
            boss_box.add_widget(MDLinearProgressIndicator(value=self.boss.mp / self.boss.max_mp * 100, indicator_color=(0.482, 0.463, 1), size_hint=(1,0.2)))
            boss_box.add_widget(Label(text=f"Class: {self.boss.hero_class}", color=[0,0,0,1]))
            boss_box.add_widget(Label(text=f"atk: {self.boss.atk}", color=[0,0,0,1]))
            boss_box.add_widget(Label(text=f"DEF: {self.boss.defense}", color=[0,0,0,1]))
            # boss_box.add_widget(Label(text=f"HP: {self.boss.hp}/{self.boss.max_hp}", color=[0,0,0,1]))
            # boss_box.add_widget(Label(text=f"MP: {self.boss.mp}/{self.boss.max_mp}", color=[0,0,0,1]))
            self.ids.boss_box.add_widget(boss_box)
        elif gm.phase_round == "mobs":
            # gm.create_mobs()
            # self.mobs = gm.mobs_pool
            # mobs List
            mobsBoxIndex = 1
            mobsbox1 = BoxLayout(orientation= "vertical", spacing= 10, padding= [5, 5], size_hint= (0.5,0.66), pos_hint= {"center_x": 0.5, "center_y": 0.5})
            if len(gm.mobs_pool) == 5:
                size_hint_mobs = (0.5, 1)
            elif len(gm.mobs_pool) == 4:
                size_hint_mobs = (0.5, 0.66)
            elif len(gm.mobs_pool) <= 3:
                size_hint_mobs = (0.5, 0.33)
            mobsbox2 = BoxLayout(orientation= "vertical", spacing= 10, padding= [5, 5], size_hint= size_hint_mobs, pos_hint= {"center_x": 0.5, "center_y": 0.5})
            for i, mob in enumerate(self.mobs):
                rarity = mob.special_skill.rarity if mob.special_skill else "common"
                mob_color = RARITY_COLORS.get(rarity, [0.5, 0.5, 0.5, 1])
                highlight_color = [0, 0, 0, 1]
                is_dead = mob.hp <= 0

                # Jika hero ini adalah yang sedang mendapat giliran
                if self.phase_turn == "enemy" and i == self.turn_index:
                    # Tambahkan highlight — misal: warna sedikit lebih terang atau border
                    mob_color = [c + 0.2 if c < 0.8 else 1 for c in mob_color]  # highlight
                    highlight_color = [0, 0, 0, 1]
                    
                if is_dead:
                    mob_color = [0.3, 0.3, 0.3, 1]  # abu
                    highlight_color = [0.6, 0.6, 0.6, 1]
                box = BoxLayout(orientation='vertical', padding=5, spacing=3, size_hint=(1,1))
                box.opacity = 0.5 if is_dead else 1.0

                with box.canvas.before:
                    Color(*mob_color)
                    bg = RoundedRectangle(pos=box.pos, size=box.size, radius=[8])
                box.bind(pos=self._update_bg(bg), size=self._update_bg(bg))

                name_text = f">>{mob.name}<<" if self.phase_turn == "enemy" and i == self.turn_index else mob.name
                btn = Button(text=name_text, bold=True, color=[1, 1, 1, 1], disabled=is_dead)
                # btn = Button(text=mob.name, bold=True, color=[1,1,1,1])
                btn.bind(on_release=lambda inst, h=mob: self.show_mob_popup(h))
                box.add_widget(btn)
                
                box.add_widget(MDLinearProgressIndicator(value=mob.hp / mob.max_hp * 100, indicator_color=(1,0,0), size_hint=(1,0.2)))
                box.add_widget(MDLinearProgressIndicator(value=mob.mp / mob.max_mp * 100, indicator_color=(0.482, 0.463, 1), size_hint=(1,0.2)))
                box.add_widget(Label(text=f"Class: {mob.hero_class}", font_size=22, color=highlight_color))
                box.add_widget(Label(text=f"ATK: {mob.atk}", font_size=22, color=highlight_color))
                box.add_widget(Label(text=f"DEF: {mob.defense}", font_size=22, color=highlight_color))
                # box.add_widget(Label(text=f"HP: {mob.hp}/{mob.max_hp}", font_size=22, color=highlight_color))
                # box.add_widget(Label(text=f"MP: {mob.mp}/{mob.max_mp}", font_size=22, color=highlight_color))
                # self.ids.hero_box.add_widget(box)
                
  
                if mobsBoxIndex <= 2:
                    mobsbox1.add_widget(box)
                    mobsBoxIndex += 1
                else:
                    mobsbox2.add_widget(box)
            self.ids.boss_box.add_widget(mobsbox1)
            self.ids.boss_box.add_widget(mobsbox2)
        # Hero boxes
        heroBoxIndex = 1
        for i, hero in enumerate(self.players):
            rarity = hero.special_skill.rarity if hero.special_skill else "common"
            hero_color = RARITY_COLORS.get(rarity, [0.5, 0.5, 0.5, 1])
            highlight_color = [0, 0, 0, 1]
            is_dead_or_escaped = (hero.hp <= 0) or hero.escaped

            if self.phase_turn == "hero" and i == self.turn_index:
                hero_color = [min(c + 0.2, 1.0) for c in hero_color]

            if is_dead_or_escaped:
                hero_color = [0.3, 0.3, 0.3, 1]
                highlight_color = [0.6, 0.6, 0.6, 1]

            box = BoxLayout(orientation='vertical', padding=5, spacing=3, size_hint=(1, 1))
            box.opacity = 0.5 if is_dead_or_escaped else 1.0

            with box.canvas.before:
                Color(*hero_color)
                bg = RoundedRectangle(pos=box.pos, size=box.size, radius=[8])
            box.bind(pos=self._update_bg(bg), size=self._update_bg(bg))

            name_text = f">>{hero.name}<<" if self.phase_turn == "hero" and i == self.turn_index else hero.name
            btn = Button(text=name_text, bold=True, color=[1,1,1,1], disabled=is_dead_or_escaped)
            btn.bind(on_release=lambda inst, h=hero: self.show_player_popup(h))
            box.add_widget(btn)

            box.add_widget(MDLinearProgressIndicator(value=hero.hp / hero.max_hp * 100, indicator_color=(1, 0, 0), size_hint=(1, 0.2)))
            box.add_widget(MDLinearProgressIndicator(value=hero.mp / hero.max_mp * 100, indicator_color=(0.482, 0.463, 1), size_hint=(1, 0.2)))
            box.add_widget(Label(text=f"Class: {hero.hero_class}", font_size=22, color=highlight_color))
            box.add_widget(Label(text=f"ATK: {hero.atk}", font_size=22, color=highlight_color))
            box.add_widget(Label(text=f"DEF: {hero.defense}", font_size=22, color=highlight_color))
            # box.add_widget(Label(text=f"HP: {hero.hp}/{hero.max_hp}", font_size=22, color=highlight_color))
            # box.add_widget(Label(text=f"MP: {hero.mp}/{hero.max_mp}", font_size=22, color=highlight_color))

            if heroBoxIndex <= 3:
                self.ids.hero_box1.add_widget(box)
                heroBoxIndex += 1
            else:
                self.ids.hero_box2.add_widget(box)


    def _update_bg(self, rect):
        def update(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size
        return update

    def update_turn(self):
        gm = MDApp.get_running_app().manager
        self.update_status_boxes()
        if self.phase_turn == "hero":
            while self.turn_index < len(self.players):
                hero = self.players[self.turn_index]
                if hero.is_alive() and not hero.escaped:
                    # gm = MDApp.get_running_app().manager
                    self.ids.turn_label.text = f"Turn {gm.round_number}"
                    # self.ids.turn_info.text = f"Turn {hero.name}"
                    self.show_action_options(hero)
                    # self.update_status_boxes()
                    return  # hanya tampilkan jika valid
                else:
                    self.turn_index += 1  # lewati hero mati/kabur
                    self.update_status_boxes()

            # Kalau semua hero selesai → boss turn
            self.ids.submenu_box.clear_widgets()
            if gm.phase_round == "mobs":
                alive_mobs = [p for p in gm.mobs_pool if p.is_alive()]
                if not alive_mobs:
                    self.ids.turn_info.text += "[b]Semua mobs tidak dapat bertarung![/b]\n"
                    self.game_over()
                    return
                self.phase_turn = "enemy"
                self.turn_index = gm.mobs_pool.index(alive_mobs[0])
                self.update_turn()
            else:
                self.phase_turn = "enemy"
                self.turn_index = 0
                self.update_turn()

        elif self.phase_turn == "enemy":
            if gm.phase_round == "mobs":
                while self.turn_index < len(gm.mobs_pool):
                    mob = gm.mobs_pool[self.turn_index]
                    if mob.is_alive():
                        # gm = MDApp.get_running_app().manager
                        self.ids.turn_label.text = f"Turn {gm.round_number}"
                        self.ids.turn_info.text += f"[b]Turn {mob.name}[/b]\n"
                        self.ids.scroll_log_info.scroll_y = 0
                        
                        btn = Button(text="Next", background_color=(0.4, 0.9, 0.4, 1))
                        btn.bind(on_release=lambda inst: self.btn_mobs_turn(mob))
                        self.ids.action_panel.clear_widgets()
                        self.ids.action_panel.add_widget(btn)
                        # self.do_mobs_turn(mob)
                        # self.ids.turn_info.text = f"Turn {hero.name}"
                        # self.show_action_options(hero)
                        # self.update_status_boxes()
                        return  # hanya tampilkan jika valid
                    else:
                        self.turn_index += 1  # lewati hero mati/kabur
                        self.update_status_boxes()

                # Kalau semua hero selesai → boss turn
                alive_heroes = [p for p in self.players if p.is_alive() and not p.escaped]
                if not alive_heroes:
                    self.ids.turn_info.text += "[b]Semua hero tidak dapat bertarung![/b]\n"
                    self.game_over()
                    return
                self.phase_turn = "hero"
                self.turn_index = self.players.index(alive_heroes[0])
                gm.round_number += 1
                self.update_turn()
            elif gm.phase_round == "boss":
                if self.turn_index < 1:
                    self.ids.turn_label.text = f"Turn {gm.round_number}"
                    self.ids.turn_info.text += f"[b]Turn {self.boss.name}[/b]\n"
                    self.ids.scroll_log_info.scroll_y = 0
                    
                    btn = Button(text="Next", background_color=(0.4, 0.6, 1, 1))
                    btn.bind(on_release=lambda inst: self.btn_boss_turn())
                    self.ids.action_panel.clear_widgets()
                    self.ids.action_panel.add_widget(btn)
                    return
                # Kalau semua hero selesai → boss turn
                alive_heroes = [p for p in self.players if p.is_alive() and not p.escaped]
                if not alive_heroes:
                    self.ids.turn_info.text += "[b]Semua hero tidak dapat bertarung![/b]\n"
                    self.game_over()
                    return
                self.phase_turn = "hero"
                self.turn_index = self.players.index(alive_heroes[0])
                gm.round_number += 1
                self.update_turn()
                # btn = Button(text="Next", background_color=(0.4, 0.9, 0.4, 1))
                # btn.bind(on_release=self.go_to_shop)
                # self.ids.action_panel.clear_widgets()
                # self.ids.action_panel.add_widget(btn)

    def show_action_options(self, hero):
        self.ids.action_panel.clear_widgets()
        self.ids.submenu_box.clear_widgets()

        actions = [
            ("Attack", self.do_attack),
            ("Skills", self.show_skills),
            ("Special", self.show_special),
            ("Restore MP", self.restore_mp),
            ("Retreat", self.retreat)
        ]
        for name, func in actions:
            btn = Button(text=name, background_color=(0.6, 0.6, 0.9, 1))
            btn.bind(on_release=lambda inst, f=func: f(hero))
            self.ids.action_panel.add_widget(btn)

    def show_skills(self, hero):
        self.ids.submenu_box.clear_widgets()
        self.ids.submenu_box.add_widget(
            Button(text="Back", on_release=lambda x: self.show_action_options(hero))
        )

        for skill in hero.skills:
            color = RARITY_COLORS.get(skill.rarity, [0.5, 0.5, 0.5, 1])
            btnText = f"{skill.name}\n({skill.mp_cost} MP)\n[{skill.type} | {skill.target_type}]"
            btn = Button(
                text=btnText,
                background_color=color,
                size_hint_y=1,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            btn.bind(on_release=lambda inst, s=skill: self.use_skill(hero, s))
            self.ids.submenu_box.add_widget(btn)

    def show_special(self, hero):
        self.ids.submenu_box.clear_widgets()
        self.ids.submenu_box.add_widget(Button(text="Back", on_release=lambda x: self.show_action_options(hero)))
        skill = hero.special_skill
        if skill:
            color = RARITY_COLORS.get(skill.rarity, [0.5, 0.5, 0.5, 1])
            btnText = f"{skill.name}\n({skill.mp_cost} MP)\n[{skill.type} | {skill.target_type}]"
            btn = Button(
                text=btnText,
                background_color=color,
                size_hint_y=1,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            btn.bind(on_release=lambda inst: self.use_special(hero, skill))
            self.ids.submenu_box.add_widget(btn)

    def use_skill(self, hero, skill):
        if hero.mp < skill.mp_cost:
            self.ids.turn_info.text += f"{hero.name} tidak punya cukup MP untuk {skill.name}!\n"
            self.ids.scroll_log_info.scroll_y = 0
            return

        gm = MDApp.get_running_app().manager

        # MULTI langsung gunakan
        if skill.target_type == "multi":
            if skill.type in ("healing", "buff"):
                targets = [p for p in self.players if p.is_alive()]
            else:
                if gm.phase_round == "boss":
                    targets = [gm.boss]
                elif gm.phase_round == "mobs":
                    targets = [m for m in gm.mobs_pool if m.is_alive()]
                else:
                    targets = []

            hero.use_skill(skill, targets)
            desc = self.describe_skill_action(hero, skill, targets)
            self.ids.turn_info.text += f"Turn {hero.name}: Skill {skill.name} ({skill.mp_cost} mp)!\n{desc}\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.advance_turn()

        elif skill.target_type == "single":
            self.ids.submenu_box.clear_widgets()
            self.ids.turn_info.text += f"{hero.name} memilih target untuk {skill.name}...\n"
            self.ids.scroll_log_info.scroll_y = 0

            if skill.type in ("healing", "buff"):
                # Tampilkan hero sebagai target
                for target in self.players:
                    if target.is_alive() and not target.escaped:
                        btn = Button(
                            text=f"{target.name} ({target.hp}/{target.max_hp} HP)",
                            size_hint_y=1,
                        )
                        btn.bind(on_release=lambda inst, t=target: self.cast_skill_on_target(hero, skill, t))
                        self.ids.submenu_box.add_widget(btn)
            else:
                # Tampilkan mob atau boss sebagai target
                if gm.phase_round == "boss":
                    target = gm.boss
                    btn = Button(
                        text=f"{target.name} ({target.hp}/{target.max_hp} HP)",
                        size_hint_y=1
                    )
                    btn.bind(on_release=lambda inst, t=target: self.cast_skill_on_target(hero, skill, t))
                    self.ids.submenu_box.add_widget(btn)

                elif gm.phase_round == "mobs":
                    for mob in gm.mobs_pool:
                        if mob.is_alive():
                            btn = Button(
                                text=f"{mob.name} ({mob.hp}/{mob.max_hp} HP)",
                                size_hint_y=1
                            )
                            btn.bind(on_release=lambda inst, t=mob: self.cast_skill_on_target(hero, skill, t))
                            self.ids.submenu_box.add_widget(btn)

    def cast_skill_on_target(self, hero, skill, target):
        hero.use_skill(skill, [target])
        desc = self.describe_skill_action(hero, skill, [target])

        self.ids.turn_info.text += f"Turn {hero.name}: Skill {skill.name} ({skill.mp_cost} mp)!\n{desc}\n"
        self.ids.scroll_log_info.scroll_y = 0
        self.ids.submenu_box.clear_widgets()
        # self.update_status_boxes()
        self.advance_turn()

    def describe_skill_action(self, hero, skill, targets):
        if not targets:
            return "Tidak ada target."

        names = ", ".join(t.name for t in targets)

        if skill.type == "atk":
            if skill.target_type == "multi":
                return f"menyerang semua musuh ({names}) sebesar {skill.power}"
            else:
                target = targets[0]
                damage = skill.power - target.defense
                damage = max(1, damage)
                return f"menyerang {target.name} sebesar {damage}"

        elif skill.type == "healing":
            if skill.target_type == "multi":
                return f"memulihkan semua sekutu ({names}) sebesar {skill.power}"
            else:
                return f"memulihkan {targets[0].name} sebesar {skill.power}"

        elif skill.type == "buff":
            amt = skill.power if skill.power > 0 else int(hero.atk * 0.2)
            if skill.target_type == "multi":
                return f"meningkatkan ATK semua sekutu ({names}) sebesar {amt}"
            else:
                return f"meningkatkan ATK {targets[0].name} sebesar {amt}"

        elif skill.type == "debuff":
            amt = skill.power if skill.power > 0 else int(hero.atk * 0.2)
            if skill.target_type == "multi":
                return f"menurunkan DEF semua musuh ({names}) sebesar {amt}"
            else:
                return f"menurunkan DEF {targets[0].name} sebesar {amt}"

        return "melakukan aksi khusus"

    def use_special(self, hero, special):
        gm = MDApp.get_running_app().manager

        if hero.mp < special.mp_cost:
            self.ids.turn_info.text += f"{hero.name} tidak punya cukup MP untuk {special.name}!\n"
            self.ids.scroll_log_info.scroll_y = 0
            return

        if special.target_type == "multi":
            if special.type in ("healing", "buff"):
                targets = [p for p in self.players if p.is_alive()]
            else:
                if gm.phase_round == "boss":
                    targets = [gm.boss]
                elif gm.phase_round == "mobs":
                    targets = [m for m in gm.mobs_pool if m.is_alive()]
                else:
                    targets = []
            hero.use_special_skill(targets)
            desc = self.describe_skill_action(hero, special, targets)
            self.ids.turn_info.text += f"Turn {hero.name}: Special {special.name} ({special.mp_cost} mp)!\n{desc}\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.advance_turn()

        elif special.target_type == "single":
            self.ids.submenu_box.clear_widgets()
            self.ids.turn_info.text += f"{hero.name} memilih target untuk Special {special.name}...\n"
            self.ids.scroll_log_info.scroll_y = 0

            if special.type in ("healing", "buff"):
                # Pilihan: target hero
                for target in self.players:
                    if target.is_alive() and not target.escaped:
                        btn = Button(
                            text=f"{target.name} ({target.hp}/{target.max_hp} HP)",
                            size_hint_y=1,
                        )
                        btn.bind(on_release=lambda inst, t=target: self.cast_special_on_target(hero, special, t))
                        self.ids.submenu_box.add_widget(btn)

            else:
                # Pilihan: target boss/mobs
                if gm.phase_round == "boss":
                    target = gm.boss
                    btn = Button(
                        text=f"{target.name} ({target.hp}/{target.max_hp} HP)",
                        size_hint_y=1
                    )
                    btn.bind(on_release=lambda inst, t=target: self.cast_special_on_target(hero, special, t))
                    self.ids.submenu_box.add_widget(btn)
                elif gm.phase_round == "mobs":
                    for mob in gm.mobs_pool:
                        if mob.is_alive():
                            btn = Button(
                                text=f"{mob.name} ({mob.hp}/{mob.max_hp} HP)",
                                size_hint_y=1
                            )
                            btn.bind(on_release=lambda inst, t=mob: self.cast_special_on_target(hero, special, t))
                            self.ids.submenu_box.add_widget(btn)

    def cast_special_on_target(self, hero, special, target):
        hero.use_special_skill([target])
        desc = self.describe_skill_action(hero, special, [target])

        self.ids.turn_info.text += f"Turn {hero.name}: Special {special.name} ({special.mp_cost} mp)!\n{desc}\n"
        self.ids.scroll_log_info.scroll_y = 0
        self.ids.submenu_box.clear_widgets()
        self.update_status_boxes()
        self.advance_turn()

    def do_attack(self, hero):
        gm = MDApp.get_running_app().manager

        if gm.phase_round == "boss":
            boss = gm.boss
            hero.attack_target(boss)

            damage = hero.atk - boss.defense
            damage = damage if damage > 0 else 1

            self.ids.turn_info.text += f"Turn {hero.name}: Attack {damage} ke {boss.name}\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.advance_turn()

        elif gm.phase_round == "mobs":
            # Tampilkan submenu pilihan target mob
            self.ids.submenu_box.clear_widgets()
            self.ids.turn_info.text += f"{hero.name} memilih target...\n"
            self.ids.scroll_log_info.scroll_y = 0

            for mob in gm.mobs_pool:
                if mob.is_alive():
                    btn = Button(
                        text=f"{mob.name} ({mob.hp}/{mob.max_hp} HP)",
                        size_hint_y=1
                    )
                    btn.bind(on_release=lambda inst, m=mob: self.attack_mob_target(hero, m))
                    self.ids.submenu_box.add_widget(btn)
                    
    def attack_mob_target(self, hero, mob):
        hero.attack_target(mob)
        damage = hero.atk - mob.defense
        damage = damage if damage > 0 else 1

        self.ids.turn_info.text += f"Turn {hero.name}: Attack {damage} ke {mob.name}\n"
        self.ids.scroll_log_info.scroll_y = 0

        self.ids.submenu_box.clear_widgets()
        # self.update_status_boxes()
        self.advance_turn()

    def restore_mp(self, hero):
        hero.restore_mp()
        self.ids.turn_info.text += f"Turn {hero.name}: Memulihkan MP ke {hero.mp}/{hero.max_mp}\n"
        self.ids.scroll_log_info.scroll_y = 0
        # self.update_status_boxes()
        self.advance_turn()

    def retreat(self, hero):
        hero.retreat()

        self.ids.turn_info.text += f"{hero.name} retreats from battle!\n"
        self.ids.scroll_log_info.scroll_y = 0
        # self.update_status_boxes()
        

        if all(not h.is_alive() or h.escaped for h in self.players):
            self.ids.turn_info.text += "[b]☠️ Semua hero tumbang.[/b]\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.ids.action_panel.clear_widgets()
            self.ids.submenu_box.clear_widgets()
            self.show_end_popup("☠️ Better luck next time...", "Kekalahan")
            return

        self.advance_turn()

    def do_mobs_turn(self, mob):
        gm = MDApp.get_running_app().manager
        alive_heroes = [p for p in self.players if p.is_alive() and not p.escaped]
        alive_mobs = [m for m in gm.mobs_pool if m.is_alive()]

        if not alive_heroes:
            self.ids.turn_info.text += "[b]Semua hero gugur. Mobs menang![/b]\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.game_over()
            return

        if not mob.is_alive():
            self.advance_turn()
            return

        choice = random.randint(1, 100)

        if choice <= 30:
            # Basic attack
            target = random.choice(alive_heroes)
            mob.attack(target)
            damage = max(1, mob.atk - target.defense)
            self.ids.turn_info.text += f"[b]{mob.name} menyerang {target.name} dan memberi {damage} damage![/b]\n"

        elif choice <= 80:
            skill = random.choice(mob.skills)
            if mob.mp >= skill.mp_cost:
                # Pilih target berdasarkan tipe dan target_type
                if skill.type in ("healing", "buff"):
                    if skill.target_type == "multi":
                        targets = alive_mobs
                    else:
                        targets = [mob]
                else:  # atk / debuff
                    if skill.target_type == "multi":
                        targets = alive_heroes
                    else:
                        targets = [random.choice(alive_heroes)]

                skill.use(mob, targets)

                desc = self.describe_skill_action(mob, skill, targets)
                self.ids.turn_info.text += f"[b]{mob.name} menggunakan skill {skill.name} ({skill.mp_cost} MP): {desc}[/b]\n"
            else:
                mob.restore_mp()
                self.ids.turn_info.text += f"[b]{mob.name} kehabisan MP dan memulihkan diri.[/b]\n"

        else:
            # Special skill
            special = mob.special_skill
            if special and mob.mp >= special.mp_cost:
                if special.type in ("healing", "buff"):
                    if special.target_type == "multi":
                        targets = alive_mobs
                    else:
                        targets = [mob]
                else:  # atk / debuff
                    if special.target_type == "multi":
                        targets = alive_heroes
                    else:
                        targets = [random.choice(alive_heroes)]

                special.use(mob, targets)

                desc = self.describe_skill_action(mob, special, targets)
                self.ids.turn_info.text += f"[b]{mob.name} menggunakan SPECIAL {special.name} ({special.mp_cost} MP): {desc}[/b]\n"
            else:
                mob.restore_mp()
                self.ids.turn_info.text += f"[b]{mob.name} kehabisan MP dan memulihkan diri.[/b]\n"

        self.ids.scroll_log_info.scroll_y = 0
        # self.update_status_boxes()
        self.advance_turn()

    def do_boss_turn(self):
        alive_heroes = [p for p in self.players if p.is_alive() and not p.escaped]
        if not alive_heroes:
            self.ids.turn_info.text += "[b]Semua hero telah tumbang. Boss menang![/b]\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.game_over()
            return

        if not self.boss.is_alive():
            self.ids.turn_info.text += "[b]Victory! Boss telah dikalahkan.[/b]\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.ids.action_panel.clear_widgets()
            self.ids.submenu_box.clear_widgets()
            self.show_end_popup("Selamat! Anda menang!", "Kemenangan")
            return

        choice = random.randint(1, 100)

        if choice <= 30:
            # Basic Attack
            target = random.choice(alive_heroes)
            self.boss.attack(target)
            damage = max(1, self.boss.atk - target.defense)
            self.ids.turn_info.text += f"[b]{self.boss.name} menyerang {target.name} sebesar {damage} damage.[/b]\n"

        elif choice <= 80:
            # Use Skill
            skill = random.choice(self.boss.skills)
            if self.boss.mp >= skill.mp_cost:
                targets = []

                if skill.type in ("healing", "buff"):
                    # positif: selalu ke boss sendiri (karena dia sendirian)
                    targets = [self.boss] if skill.target_type == "single" else [self.boss]
                else:
                    # negatif: ke hero (single/multi)
                    if skill.target_type == "single":
                        targets = [random.choice(alive_heroes)]
                    else:
                        targets = alive_heroes

                skill.use(self.boss, targets)
                desc = self.describe_skill_action(self.boss, skill, targets)
                self.ids.turn_info.text += f"[b]{self.boss.name} menggunakan skill {skill.name} ({skill.mp_cost} MP): {desc}[/b]\n"
            else:
                self.boss.restore_mp()
                self.ids.turn_info.text += f"[b]{self.boss.name} memulihkan MP karena kehabisan.[/b]\n"

        else:
            # Use Special Skill
            special = self.boss.special_skill
            if special and self.boss.mp >= special.mp_cost:
                targets = []

                if special.type in ("healing", "buff"):
                    targets = [self.boss] if special.target_type == "single" else [self.boss]
                else:
                    if special.target_type == "single":
                        targets = [random.choice(alive_heroes)]
                    else:
                        targets = alive_heroes

                special.use(self.boss, targets)
                desc = self.describe_skill_action(self.boss, special, targets)
                self.ids.turn_info.text += f"[b]{self.boss.name} menggunakan SPECIAL {special.name} ({special.mp_cost} MP): {desc}[/b]\n"
            else:
                self.boss.restore_mp()
                self.ids.turn_info.text += f"[b]{self.boss.name} memulihkan MP karena kehabisan.[/b]\n"

        self.ids.scroll_log_info.scroll_y = 0
        # self.update_status_boxes()
        self.advance_turn()


    def advance_turn(self):
        if self.phase_turn == "hero":
            self.turn_index += 1
            self.update_turn()
        elif self.phase_turn == "enemy":
            gm = MDApp.get_running_app().manager
            # gm.current_round_index += 1
            # gm.phase_round = gm.round_sequence[gm.current_round_index % len(gm.round_sequence)]
            # self.turn_index = 0

            # if gm.phase_round == "shop":
            #     btn = Button(text="Enter Shop", background_color=(0.9, 0.9, 0.2, 1))
            #     btn.bind(on_release=self.go_to_shop)
            #     self.ids.action_panel.clear_widgets()
            #     self.ids.submenu_box.clear_widgets()
            #     self.ids.action_panel.add_widget(btn)
            if gm.phase_round == "mobs":
                # gm.create_mobs()
                # self.ids.turn_info.text += f"[b]⚔️ Ronde Mobs dimulai![/b]\n"
                # self.ids.scroll_log_info.scroll_y = 0
                self.turn_index += 1
                self.update_turn()
            elif gm.phase_round == "boss":
                # self.ids.turn_info.text += f"[b]👹 Boss {self.boss.name} kembali![/b]\n"
                # self.ids.scroll_log_info.scroll_y = 0
                self.turn_index += 1
                self.update_turn()
            
        self.game_over()

            # self.round_number += 1
            # self.turn_index = 0
            # self.phase = "hero"
            # self.update_turn()

    def game_over(self):
        gm = MDApp.get_running_app().manager

        # 1. Boss dikalahkan → Menang total
        if not self.boss.is_alive():
            self.ids.turn_info.text += "[b]Victory! Boss dikalahkan.[/b]\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.ids.action_panel.clear_widgets()
            self.ids.submenu_box.clear_widgets()
            self.show_end_popup("Selamat! Anda menang!", "Kemenangan")
            return True  # game selesai

        # 2. Semua hero gugur atau kabur → Kalah
        if all(not h.is_alive() or h.escaped for h in self.players):
            self.ids.turn_info.text += "[b]Semua hero telah tumbang.[/b]\n"
            self.ids.scroll_log_info.scroll_y = 0
            self.ids.action_panel.clear_widgets()
            self.ids.submenu_box.clear_widgets()
            self.show_end_popup("Semua hero kalah... Coba lagi!", "Kekalahan")
            return True  # game selesai

        # 3. Ronde mobs berakhir (semua mobs mati)
        if gm.phase_round == "mobs":
            if all(not m.is_alive() for m in gm.mobs_pool):
                self.ids.turn_info.text += "[b]Semua mobs dikalahkan![/b]\n"
                self.ids.scroll_log_info.scroll_y = 0
                self.ids.action_panel.clear_widgets()
                self.ids.submenu_box.clear_widgets()

                # Lanjut ke ronde berikutnya (next phase)
                self.phase_turn = "hero"
                self.turn_index = next(
                    (i for i, h in enumerate(self.players) if h.is_alive() and not h.escaped), 0
                )
                gm.round_number = 1
                gm.current_round_index += 1
                gm.phase_round = gm.round_sequence[gm.current_round_index % len(gm.round_sequence)]
                self.update_phase()
                self.update_turn()
                return False  # lanjut game

        return False  # game masih berjalan

    # def next_turn(self, instance):
    #     self.turn_index = 0
    #     self.phase = "hero"
    #     self.update_turn()

    def btn_mobs_turn(self, mob):
        self.ids.action_panel.clear_widgets()
        self.do_mobs_turn(mob)  
        
    def btn_boss_turn(self):
        self.ids.action_panel.clear_widgets()
        self.do_boss_turn()
           
    def go_to_shop(self):
        gm = MDApp.get_running_app().manager
        gm.create_shop()
        gm.give_income()
        self.turn_index = 0
        self.phase_turn = "hero"
        self.manager.current = "shop_screen"

    def show_mob_popup(self, mob):
        # print(boss)
        content = BoxLayout(orientation="vertical", padding=10, spacing=5)
        info = f"[b]{mob.name}[/b]\n"
        info += f"Class: {mob.hero_class}\n"
        info += f"Type: {mob.special_skill.rarity if mob.special_skill else '-'}\n\n"
        info += f"HP: {mob.hp}/{mob.max_hp}\n"
        info += f"MP: {mob.mp}/{mob.max_mp}\n"
        info += f"ATK: {mob.atk}\n"
        info += f"DEF: {mob.defense}\n\n"

        skill_names = ', '.join([s.name for s in mob.skills]) if mob.skills else "-"
        info += f"Skills: {skill_names}\n\n"
        info += f"Special Skill: {mob.special_skill.name if mob.special_skill else '-'}"

        label = Label(text=info, markup=True)
        content.add_widget(label)

        popup = Popup(title="Mob Info", content=content, size_hint=(0.6, 0.6))
        popup.open()
        
    def show_boss_popup(self, boss):
        # print(boss)
        content = BoxLayout(orientation="vertical", padding=10, spacing=5)
        info = f"[b]{boss.name}[/b]\n"
        info += f"Class: {boss.hero_class}\n"
        info += f"Type: {boss.special_skill.rarity if boss.special_skill else '-'}\n\n"
        info += f"HP: {boss.hp}/{boss.max_hp}\n"
        info += f"MP: {boss.mp}/{boss.max_mp}\n"
        info += f"ATK: {boss.atk}\n"
        info += f"DEF: {boss.defense}\n\n"

        skill_names = ', '.join([s.name for s in boss.skills]) if boss.skills else "-"
        info += f"Skills: {skill_names}\n\n"
        info += f"Special Skill: {boss.special_skill.name if boss.special_skill else '-'}"

        label = Label(text=info, markup=True)
        content.add_widget(label)

        popup = Popup(title="Boss Info", content=content, size_hint=(0.6, 0.6))
        popup.open()

    def show_player_popup(self, player):
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        info = f"[b]{player.name}[/b]\n"
        # info += f"Class: {getattr(player, 'char_class', {player.hero_class})}\n"
        info += f"Class: {player.hero_class}\n"
        info += f"Type: {player.special_skill.rarity if player.special_skill else '-'}\n\n"
        info += f"HP: {player.hp}/{player.max_hp}\n"
        info += f"MP: {player.mp}/{player.max_mp}\n"
        info += f"ATK: {player.atk}\n"
        info += f"DEF: {player.defense}\n\n"

        # skills
        skill_names = ', '.join([s.name for s in player.skills]) if player.skills else "-"
        info += f"Skills: {skill_names}\n\n"

        # special
        info += f"Special Skill: {player.special_skill.name if player.special_skill else '-'}\n\n"

        # items
        if hasattr(player, "equipped_items") and player.equipped_items:
            item_names = ', '.join([item.name for item in player.equipped_items])
            info += f"Items: {item_names}"
        else:
            info += "Items: -"

        label = Label(text=info, markup=True)
        content.add_widget(label)

        popup = Popup(title="Player Info", content=content, size_hint=(0.6, 0.7))
        popup.open()

    def show_end_popup(self, message, title="Game Over"):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        content.add_widget(Label(text=message, font_size=32))

        btn = Button(text="OK", size_hint_y=None, height=40)
        content.add_widget(btn)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 300), auto_dismiss=False)
        btn.bind(on_release=lambda instance: self.end_game(popup))
        popup.open()
        
    def end_game(self, popup):
        popup.dismiss()
        
        gm = MDApp.get_running_app().manager
        gm.round_number = gm.new_round() # reset round/turn
        gm.current_round_index = 0 # reset phase
        self.ids.turn_info.text = f"Turn info will be shown here\n" #reset battle log
        self.ids.scroll_log_info.scroll_y = 1

        self.manager.current = "main_menu"
