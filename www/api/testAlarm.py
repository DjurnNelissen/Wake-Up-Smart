#!/usr/bin/python

import sys
sys.path.insert(0, '../python')

import common, json, time, wave, pyaudio

c = common.common()
chunk = 1024

p = pyaudio.PyAudio()

f = c.get_setting_value('alarmFile')
m = wave.open(f)

s = p.open(
format = p.get_format_from_width(m.getsampwidth()),
channels = m.getnchannels(),
rate = m.getframerate(),
ourput=True
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
