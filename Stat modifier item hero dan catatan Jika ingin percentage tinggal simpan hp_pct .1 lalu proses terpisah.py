class Item:
    def __init__(self, name, modifiers=None, slot="misc"):
        # modifiers: dict stat→nilai (+ atau ×)
        self.modifiers = modifiers or {}

class Character:
    ...
    def equip(self, item):
        self.equipment[item.slot] = item
        self._recalc_stats()

    def _recalc_stats(self):
        # reset ke base
        self.current_stats = self.base_stats.copy()
        for itm in self.equipment.values():
            for stat, val in itm.modifiers.items():
                self.current_stats[stat] += val
