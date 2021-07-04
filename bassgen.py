import os
from random import randint, uniform
from midiutil.MidiFile import MIDIFile
import numpy as np

soundfonts_dir = f'{os.path.realpath(__file__)}'
soundfonts_dir = soundfonts_dir[:len(soundfonts_dir) - 11] + '/soundfonts'
bass_sf = [f for f in os.listdir(f'{soundfonts_dir}/bass') if f.endswith('sf2')]
bass_line = 31
timidity_dir = '/usr/local/Cellar/timidity/2.15.0_1/share/timidity/timidity.cfg'

cfg_file = open(timidity_dir)
cfg_lines = cfg_file.readlines()
cfg_file.close()

bl = cfg_lines[bass_line].split(' ')
bl[4] = f'\"bass/{bass_sf[randint(0, len(bass_sf) - 1)]}\"'
cfg_lines[bass_line] = ' '.join(bl)

cfg_file = open(timidity_dir, 'w')
new_cfg = ''.join(cfg_lines)
cfg_file.write(new_cfg)
cfg_file.close()

timesig_file = open('timesig.txt', 'r')
timesig = timesig_file.read()
timesig_file.close()
timesig = timesig.split(' ')
tempo = int(timesig[0])
root_note = int(timesig[1])

def bass_note():
    r = randint(1,7)
    note = root_note - 36
    if r % 5 == 0:
        return note + 3
    elif r % 6 == 0:
        return note - 1
    elif r % 7 == 0:
        return note + 7
    return note

my_midi = MIDIFile(numTracks=1)
my_midi.addTrackName(0, 0, 'Bass')
my_midi.addTempo(0, 0, tempo)
bass_track = 0
bass_channel = 0
bass_duration = 1.0
velocity = 100
kick_times_file = open('kick_times.txt', 'r')
text = kick_times_file.read()
kick_times_file.close()
kick_times = text.split(' ')[:-1]
for time in kick_times:
    if uniform(0.0, 1.0) < 0.8:
        my_midi.addNote(bass_track, bass_channel, bass_note(), float(time), bass_duration, velocity)

with open('bass.mid', 'wb') as output_file:
    my_midi.writeFile(output_file)