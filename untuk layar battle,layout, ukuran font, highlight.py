#:import theme gui_theme

<BattleScreen>:
    canvas.before:
        Color:
            rgba: theme.DARK_BG
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(8)
        padding: dp(12)

        # ======= Area Pertempuran (musuh + hero) =======
        BattleArena:   # widget milikmu
            size_hint_y: .55

        # ======= Battle Log  =======
        ScrollView:
            size_hint_y: .30
            do_scroll_x: False

            GridLayout:
                id: log_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(2)

        # ======= Tombol Aksi =======
        ActionBar:     # widget milikmu
            size_hint_y: .15
