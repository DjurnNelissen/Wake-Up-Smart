#!/usr/bin/python

import sys
sys.path.insert(0, '../python')

import common, json, wave, pyaudio
from subprocess import call

c = common.common()

call(["amixer", "-D", "pulse", "sset", "Master", str(c.get_setting_value('alarmVolume')) + "%"])

chunk = 1024

p = pyaudio.PyAudio()

f = c.get_setting_value('alarmFile')
m = wave.open(f)

s = p.open(
    format = p.get_format_from_width(m.getsampwidth()),
    channels = m.getnchannels(),
    rate = m.getframerate(),
    output=True
)

data = m.readframes(chunk)

while data:
    s.write(data)
    data = m.readframes(chunk)

s.stop_stream()
s.close()
p.terminate()

print("Content-type: application/json\n")
print(json.dumps({'succes': True}, default=str))
