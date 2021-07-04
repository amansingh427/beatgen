from os import listdir
from midiutil.MidiFile import MIDIFile
import numpy as np
from random import choice, uniform, randint

from numpy.lib.function_base import sinc

soundfonts_dir = "/Users/amansingh/beatgen/soundfonts"
hat_sf = [f for f in listdir(f'{soundfonts_dir}/hihatcl') if f.endswith('sf2')]
hat_line = 31
timidity_dir = '/usr/local/Cellar/timidity/2.15.0_1/share/timidity/timidity.cfg'

cfg_file = open(timidity_dir)
cfg_lines = cfg_file.readlines()
cfg_file.close()

hl = cfg_lines[hat_line].split(' ')
# hl[4] = f'\"hihatcl/{hat_sf[choice(range(len(hat_sf)))]}\"'
hl[4] = f'\"hihatcl/{hat_sf[randint(0, len(hat_sf) - 1)]}\"'
cfg_lines[hat_line] = ' '.join(hl)

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

my_midi = MIDIFile(numTracks=1)
my_midi.addTrackName(0, 0, 'Closed hats')
my_midi.addTempo(0, 0, tempo)
hat_track = 0
hat_channel = 0
hat_duration = 1.0
velocity = 100
eight_note = 0.5
sixteenth_note = 0.25
thirtysecond_note = 0.125

def doublefirst(x):
    my_midi.addNote(hat_track, hat_channel, root_note, x, sixteenth_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note, x + sixteenth_note, sixteenth_note, velocity)
def doublelast(x):
    my_midi.addNote(hat_track, hat_channel, root_note, x + eight_note, sixteenth_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note, x + eight_note + sixteenth_note, sixteenth_note, velocity)
def rootuproll(x):
    my_midi.addNote(hat_track, hat_channel, root_note, x, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note + 2, x + thirtysecond_note, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note + 4, x + sixteenth_note, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note + 4, x + sixteenth_note + thirtysecond_note, thirtysecond_note, velocity)
def rootdownroll(x):
    my_midi.addNote(hat_track, hat_channel, root_note, x, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note - 2, x + thirtysecond_note, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note - 4, x + sixteenth_note, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note - 4, x + sixteenth_note + thirtysecond_note, thirtysecond_note, velocity)
def fastdouble(x):
    my_midi.addNote(hat_track, hat_channel, root_note, x, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note, x + thirtysecond_note, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note, x + sixteenth_note, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note, x + sixteenth_note + thirtysecond_note, thirtysecond_note, velocity)
def fastfirst(x):
    my_midi.addNote(hat_track, hat_channel, root_note, x, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note, x + thirtysecond_note, thirtysecond_note, velocity)
def fastlast(x):
    my_midi.addNote(hat_track, hat_channel, root_note, x + sixteenth_note, thirtysecond_note, velocity)
    my_midi.addNote(hat_track, hat_channel, root_note, x + sixteenth_note + thirtysecond_note, thirtysecond_note, velocity)

patterns = ((doublefirst, 0.3), (doublelast, 0.3), (rootuproll, 0.15), (rootdownroll, 0.15), (fastdouble, 0.2), (fastfirst, 0.25), (fastlast, 0.25))
fast_beat = True if tempo > 155 else False
alt_hats = True if uniform(0.0, 1.0) < 0.2 else False
for x in np.arange(0.0, 16.0, 1.0):
    roll = choice(patterns)
    if uniform(0.0, 1.0) < roll[1]:
        roll[0](x)
    else:
        if alt_hats:
            if fast_beat:
                my_midi.addNote(hat_track, hat_channel, root_note, x, 0.5, velocity)
            else:
                for y in np.arange(x, x + 1, sixteenth_note):
                    my_midi.addNote(hat_track, hat_channel, root_note, x, sixteenth_note, velocity)
        else:
            my_midi.addNote(hat_track, hat_channel, root_note, x, eight_note, velocity)
            my_midi.addNote(hat_track, hat_channel, root_note, x + eight_note, eight_note, velocity)

with open('hatroll.mid', 'wb') as output_file:
    my_midi.writeFile(output_file)