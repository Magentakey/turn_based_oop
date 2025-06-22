from kivy.core.audio import SoundLoader
hit_sfx = SoundLoader.load("assets/sfx/hit.wav")

def play_hit():
    if hit_sfx: hit_sfx.play()
