class GameManager:
    ROUND_SEQUENCE = ["mobs", "mobs", "shop", "mobs", "boss"]

    def __init__(self):
        self.current_phase_idx = 0
        self.enemies = []
        self.shop_open = False

    # ---  MAIN LOOP  ---
    def next_turn(self):
        if not self.enemies:               # semua musuh mati?
            self._advance_phase()

    def _advance_phase(self):
        self.current_phase_idx += 1
        if self.current_phase_idx >= len(self.ROUND_SEQUENCE):
            # game selesai / victory screen
            return

        phase = self.ROUND_SEQUENCE[self.current_phase_idx]
        if phase == "shop":
            self._open_shop()
        elif phase == "mobs":
            self._spawn_mobs()
        elif phase == "boss":
            self._spawn_boss()

    # ---  SPAWNERS  ---
    def _spawn_mobs(self):
        self.shop_open = False
        count = random.randint(2, 5)
        self.enemies = [self._random_enemy() for _ in range(count)]

    def _spawn_boss(self):
        self.shop_open = False
        self.enemies = [BossEnemy()]       # implementasi BossEnemy sendiri

    def _open_shop(self):
        self.shop_open = True
        # panggil tampilan shop Kivy-mu
