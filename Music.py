from pygame import mixer
import settingsdata

class Music:
    def __init__(self, track):
         super().__init__()
         self.track = track
         mixer.init()
         mixer.music.load(self.track)
         mixer.music.set_volume(settingsdata.volumes[0] * settingsdata.volumes[1])
         mixer.music.play()