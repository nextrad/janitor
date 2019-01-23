# janitor.py
# script to clear out ADC data files containing just noise
# Brad Kahn
# 06-12-2018

# for every directory containing data:
# 	read NeXtRAD.ini, extract 'PULSES' parameter
# 		determine which band/pol was used based on the 'mode' in the 'PULSES' parameter

#; Polarisation mode parameter decoding
#; ------------------------------------
#; Mode    Freq Band     TxPol   RxPol
#; 0           L           V       V
#; 1           L           V       H
#; 2           L           H       V
#; 3           L           H       H
#; 4           X           V       H,V
#; 5           X           H       H,V

#; PULSE_x   =   [Pulse Width, PRI, Polarisation Mode, Waveform Frequency]
#;       Polarisation Mode   = see "Polarisation mode parameter decoding" table (e.g. '2' for horizontal transmission, vertical reception)
#; PULSES    =   [PULSE_0|PULSE_1|...|PULSE_n], n = number of unique pulses
#PULSES = "10.0,250.0,0,1300.0|10.0,250.0,1,1300.0|10.0,250.0,2,1300.0|10.0,250.0,3,1300.0"


# adc0.dat <-- L Band, Pol depends on mode selection
# adc1.dat <-- X Band, ? Pol
# adc2.dat <-- X Band, ? Pol

import argparse

FILENAME = 'NeXtRAD.ini'

# extract pulses param string from file
def get_pulses_str(filename):
	f = file(filename)
	lines = f.readlines()
	for line in lines:
		if (';' not in line) and ('PULSES' in line):
			return line

# return a list of pulse types given a pulse param string
def decode_pulses_str(pulses_str):
	pulses_list = pulses_str.split('"')
	pulses_list = pulses_list[1]
	pulses_list = pulses_list.split('|')	
	return pulses_list	

# return whether the given pulse str is L or X band
def get_band(pulse_str):
	pulse_list = pulse_str.split(',')
	mode = pulse_list[2]
	if mode in ('0', '1', '2', '3'):
		return 'L'
	elif mode in ('4', '5'):
		return 'X'
	else:
		return ''
		
# delete ADC data based on which band
def clean_up():
	L_band = False
	X_band = False
	
	pulse_list = decode_pulses_str(get_pulses_str(FILENAME))
	for pulse in pulse_list:
		band = get_band(pulse):
			L_band = True
		elif band == 'X Band':
			X_band = True
	
	if L_band and X_band:
		print('Both X and L Bands were used in this experiment')
	elif L_band:
		print('Only L Band used in this experiment')
	elif X_band:
		print('Only X Band used in this experiment')
	else:
		print('Problem: no bands!')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(usage='janitor.py ',
					 				 description='script to clear out ADC data files containing just noise')
	parser.add_argument('--dry-run', '-d',
			    		action='store_true',
			    		default=False,
			    		help='don\'t delete anything, just print out stuff')
	parser.add_argument('--header-file', '-f')

	args = parser.parse_args()

	if args.dry_run is True:
		print('this is a dry run')
