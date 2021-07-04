echo "Generating a beat..."
python timesiggen.py
echo "Drums..."
python drumgen.py
timidity drums.mid -Ow -o drums.wav
echo "Done. Bass..."
python bassgen.py
timidity bass.mid -Ow -o bass.wav
echo "Done. Hi-hat rolls..."
python hatgen.py
timidity hatroll.mid -Ow -o hatroll.wav
echo "Done. Combining..."
python wavmix.py
mv output.wav bin
echo "Done. Output file is in bin directory."
rm drums.* bass.* kick_times.txt