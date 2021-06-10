from pygame import mixer
import pygame as pg

mixer.init()
sound_object = mixer.Sound(file='C:\\Users\\ASUS\\PycharmProjects\\pomodoro\\pomodoro\\audios\\notification_iphong_ring.wav')
sound_object.set_volume(0.5)
sound_object.play()
print('When want stop press "s"')
while True:
    user_input = input()
    if user_input == 's':
        break
# test: when set volume maximum -> when play sound -> small, great
# but must have a loop after, as I understand, it will play in the background,
# if the program terminate -> terminate the sound at the same time


