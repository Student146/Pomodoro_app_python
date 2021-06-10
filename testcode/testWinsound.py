import winsound
import os
from audios import SOUNDFILE

dirname = os.path.dirname(__file__)
print(dirname)
winsound.PlaySound(SOUNDFILE,
                       winsound.SND_ASYNC | winsound.SND_LOOP)
while True:
    continue