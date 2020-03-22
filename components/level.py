import sound_manager.sound_manager as sm

sound = sm.init_son()
level_up_sounds = sound.get('level_up')[0]


class Level:
    def __init__(self, current_level=1, current_xp=0, level_up_base=200, level_up_factor=150):
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor

    @property
    def experience_to_next_level(self):
        return self.level_up_base + self.current_level * self.level_up_factor

    def add_xp(self, xp):
        self.current_xp += xp
        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1
            level_up_sound = sm.Son(level_up_sounds)
            level_up_sound.playpause()
            return True
        else:
            return False
