import concurrent.futures
from random import randrange
from datetime import datetime
from copy import deepcopy
import matplotlib.pyplot as plt


def selection_sort(data):
	"""
	Data: Een lijst met ints.
	Returns: Data gesorteerd met selection_sort.
	"""
	data_sorted = []
	while len(data) != 0:
		smallest_index = get_index_min(data)
		data_sorted.append(data[smallest_index])
		del data[smallest_index]
	return data_sorted


def get_index_min(data):
	"""
	Data: Een lijst met ints.
	Returns: De index van het kleinste getal uit de lijst.
	"""
	smallest_index = 0
	for index in range(1, len(data)):
		if data[index] < data[smallest_index]:
			smallest_index = index
	return smallest_index


def split_data(data, num_sub_lists):
	"""
	Data: Een lijst met getallen.
	Num_sublists
	"""
	sub_size = int(len(data)/num_sub_lists)
	sub_lists = []
	for i in range(num_sub_lists):
		sub_list = data[:sub_size]
		sub_lists.append(sub_list)
		del data[:sub_size]

	while len(data) != 0:
		for sub_list in sub_lists:
			if len(data) == 0:
				break
			sub_list.append(data[0])
			del data[0]
	return sub_lists


def delete_empty_sub_lists(sub_lists):
	"""
	Deze functie krijgt een 2d lijst met getallen
	Deze functie verwijderd de lege sublijsten
	en geeft 
	"""
	to_delete = []
	for i in range(len(sub_lists)):
		if len(sub_lists[i]) == 0:
			to_delete.append(i)
	for elem in to_delete:
		del sub_lists[elem]
	return sub_lists


def count_elem_sub_lists(sub_lists):
	sum = 0
	for i in range(len(sub_lists)):
		sum += len(sub_lists[i])
	return sum


def merge_sort(data, num_threads):
	sub_lists = split_data(data, num_threads)
	sub_lists_sorted = []
	data_sorted = []
	with concurrent.futures.ThreadPoolExecutor() as executor:
		for i in range(num_threads):
			t_sub_list = executor.submit(selection_sort, sub_lists[i])
			sub_lists_sorted.append(t_sub_list.result())

	while count_elem_sub_lists(sub_lists_sorted) != 0:
		sub_lists_sorted = delete_empty_sub_lists(sub_lists_sorted)
		next_elem = []
		for i in range(len(sub_lists_sorted)):
			if len(sub_lists_sorted[i]) != 0:
				next_elem.append(sub_lists_sorted[i][0])
		smallest_index = get_index_min(next_elem)
		data_sorted.append(next_elem[smallest_index])
		del sub_lists_sorted[smallest_index][0]
	return data_sorted


def main(len_list, num_threads_list, show_plot):
	time_results = []
	random_list = []
	for _ in range(len_list):
		random_list.append(randrange(1000000))

	print("merge_sort will be tested with a list of {} elements.". format(len_list))
	print("----------------------------------------------------------------")
	for thread in num_threads_list:
		print("merge_sort started with {} thread(s).".format(thread))
		start = datetime.now()
		merge_sort(deepcopy(random_list), thread)
		end = datetime.now()
		time = end-start
		print("merge_sort ended with a total runtime of {} seconds.".format(time.total_seconds()))
		time_results.append(time.total_seconds())
		print("----------------------------------------------------------------")
	print("merge_sort loop is ended")

	if show_plot:
		plt.plot([i for i in num_threads_list], time_results)
		plt.title("Performance merge_sort algoritme. {} willekeurige elementen".format(len_list))
		plt.xlabel("Aantal threads waarmee merge_sort mee uitgevoerd is")
		plt.ylabel("Aantal secondes dat het algoritme er over gedaan heeft")
		plt.show()


# (1e parameter)  geef hier de totale lengte van de lijst die gesorteerd moet worden, 
# (2e parameter) geef hier een range of lijst die aangeeft met hoeveel threads het algoritme steeds uitgevoerd moet worden
# (3e parameter) geef hier aan of je een grafiek getoond wil hebben van de resultaten
main(10000, range(10,11), True)
