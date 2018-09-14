import common, pygame

pygame.init()

pygame.mixer.music.load(c.get_setting_value('alarmFile'))
pygame.mixer.music.set_volume(c.get_setting_value('alarmVolume'))

pygame.mixer.music.play(1)

print("Content-type: application/json\n")
print(json.dumps({'succes': True}, default=str))
