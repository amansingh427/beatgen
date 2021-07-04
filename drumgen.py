from midiutil.MidiFile import MIDIFile
import numpy as np
from random import randint, uniform
import os

# sets diretory of timidity and current files
timidity_dir = '/usr/local/Cellar/timidity/2.15.0_1/share/timidity/timidity.cfg'
soundfonts_dir = os.path.realpath(__file__)
soundfonts_dir = soundfonts_dir[:len(soundfonts_dir) - 11]
print(soundfonts_dir)
drums_lines = {'hihatop':58,
               'snare1':51,
               'snare2':52,
               'kick1':48,
               'kick2':49}
# bass_line = 31
hihatcl_line = 31
hihatcl_sf = [f for f in os.listdir(f'{soundfonts_dir}/soundfonts/hihatcl') if f.endswith('sf2')]
drums_sf = [f for f in os.listdir(f'{soundfonts_dir}/soundfonts/drums') if f.endswith('sf2')]
print(hihatcl_sf)
# bass_sf = [f for f in listdir(f'{soundfonts_dir}/bass') if f.endswith('sf2')]

cfg_file = open(timidity_dir)
cfg_lines = cfg_file.readlines()
cfg_file.close()

for d, l in drums_lines.items():
    line = cfg_lines[l].split(' ')
    line[4] = f'\"drums/{drums_sf[randint(0, len(drums_sf) - 1)]}\"'
    cfg_lines[l] = ' '.join(line)

hl = cfg_lines[hihatcl_line].split(' ')
hl[4] = f'\"hihatcl/{hihatcl_sf[randint(0, len(hihatcl_sf) - 1)]}\"'
cfg_lines[hihatcl_line] = ' '.join(hl)

cfg_file = open(timidity_dir, 'w')
new_cfg = ''.join(cfg_lines)
cfg_file.write(new_cfg)
cfg_file.close()

timesig_file = open('timesig.txt', 'r')
timesig = timesig_file.read()
timesig_file.close()
timesig = timesig.split(' ')
channel = 9
duration = 0.5
tempo = int(timesig[0])
velocity = 100
root_note = int(timesig[1])

my_midi = MIDIFile(numTracks=5)
my_midi.addTempo(0, 0, tempo)

'''
# Closed hat track
my_midi.addTrackName(0, 0, 'Closed hat')
hat_track = 0
for x in np.arange(0.0, 16.0, 0.5):
    my_midi.addNote(hat_track, 0, root_note, x, duration, velocity)
'''

# Snare track
my_midi.addTrackName(1, 0, 'Snare')
snare1_track = 1
snare1_note = 40
if randint(1, 4) % 4 == 0:
    snare2_track = 4
    snare2_note = 38
    for x in np.arange(3.5, 16.0, 8.0):
        v = int(velocity / 2)
        my_midi.addNote(snare2_track, channel, snare2_note, x, duration, v)
        my_midi.addNote(snare2_track, channel, snare2_note, x + 1.0, duration, v)
        my_midi.addNote(snare2_track, channel, snare2_note, x + 2.0, duration, v)
for x in np.arange(2.0, 16.0, 4.0):
    my_midi.addNote(snare1_track, channel, snare1_note, x, duration, velocity)

# Kick track
my_midi.addTrackName(2, 0, 'Kick')
kick_track = 2
kick_note = 36
# probs:       0   0.5   1   1.5  2  2.5   3   3.5   4   4.5   5   5.5  6  6.5    7   7.5
kick_probs = [1.0, 0.2, 0.2, 0.6, 0, 0.2, 0.3, 0.2, 0.5, 0.5, 0.3, 0.7, 0, 0.25, 0.6, 0.6]
kick_times = open('kick_times.txt', 'w')
for a in range(2):
    #offset for third and fourth bars
    offset = a * 8
    for x, p in enumerate(kick_probs):
        if uniform(0.0, 1.0) < p:
            time = offset + x / 2
            my_midi.addNote(kick_track, channel, kick_note, time, duration, velocity)
            kick_times.write(f'{time} ')
kick_times.close()

# Open hat track
my_midi.addTrackName(3, 0, 'Open hat')
oh_track = 3
oh_note = 46
for x in np.arange(1.5, 16.0, 4.0):
    my_midi.addNote(oh_track, channel, oh_note, x, 0.25, 50)

with open('drums.mid', 'wb') as output_file:
    my_midi.writeFile(output_file)