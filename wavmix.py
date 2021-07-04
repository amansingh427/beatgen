from pydub import AudioSegment

dir = '/Users/amansingh/beatgen'
drums = AudioSegment.from_file(f'{dir}/drums.wav')
bass = AudioSegment.from_file(f'{dir}/bass.wav')
hats = AudioSegment.from_file(f'{dir}/hatroll.wav')
bassndrums = drums.overlay(bass)
combined = bassndrums.overlay(hats)

combined.export(f'{dir}/output.wav', format='wav')