from subprocess import Popen
from subprocess import PIPE
from subprocess import run
from datetime import datetime as dt
from time import sleep

orders = {
	'temp': ['vcgencmd', 'measure_temp'],
	'volts': ['vcgencmd', 'measure_volts'],
	'freq': ['vcgencmd', 'measure_clock', 'arm'],
#	 ['vcgencmd', 'commands']
}

# alle gemessenen Temperaturen
temp_all = list()
# aktuelle Temperatur
temp_cur = list()
# maximale gemessene Temperatur
temp_max = float()
# minimale gemessene Temperatur
temp_min = float()
# durchschnittliche  Temperatur
temp_avg = float()


def display_order():
	"""Display info."""
	holder = []
	for order in orders.value():
		Popen(order)
		holder.append(run(order, stdout=PIPE).stdout)
	for stuff in holder:
		print(stuff)


def get_temp():
	"""Get current temperature as dtype float and the time."""
	moment = f'{dt.now().hour}:{dt.now().minute}:{dt.now().second}'  # :{dt.now().microsecond}'
	temp_stdout = str(run(orders['temp'], stdout=PIPE).stdout)
	# print(temp_stdout)
	temp_stdout = temp_stdout.strip()
	temp_stdout = (temp_stdout.split("=")[1])
	# print(type(temp_stdout))
	# print((temp_stdout))
	temp_cur = float(temp_stdout.split("'")[0])
	# print(type(temp_cur))
	return temp_cur, moment

def average(a_list):
	"""Calculate the avarage value of a list."""
	assert [type(each)==float for each in a_list]
	return sum(a_list)/len(a_list)

def calculate_temps(temp_all):
	"""Calculate temperatures."""
	if len(temp_all) == 0:
		raise "The list needs a value."
	if len(temp_all) > 1_000_000:
		print('Die Liste der gesammelten Temperaturen wurde resettet.')
		temp_all = [temp_avg]
	temp_cur, _ = get_temp()
	return temp_cur, max(temp_all), min(temp_all), average(temp_all)


def get_temps(temp_all):
	"""Get temperatures."""
	temperature, _ = get_temp()
	temp_all.append(temperature)
	if len(temp_all) == 1:
		temp_cur = temp_max = temp_min = temp_avg = temperature
		return	temp_cur, temp_max, temp_min, temp_avg

	return calculate_temps(temp_all)


def display_temp():
	"""Display info temperature."""
	temp_cur, temp_max, temp_min, temp_avg = get_temps(temp_all) 
	_, time_cur = get_temp()
	print(f'Temperaturen um {time_cur}:')
	print(f'\tAktuell:\t{temp_cur}°C')
	print(f'\tDurchs.:\t{ round(temp_avg, 1) }°C')
	print(f'\tMaximal:\t{temp_max}°C')
	print(f'\tMinimal:\t{temp_min}°C')


def main():
	"""Loop"""
	print("Monat: {}\nTag: {}\nUhrzeit:{}:{}".format(dt.now().month, dt.now().day, dt.now().hour, dt.now().minute))
	while True:
		print('\n')
	#	display_order()
		print('\n')
		display_temp()
		sleep(25)


if __name__ == "__main__":
	main()

