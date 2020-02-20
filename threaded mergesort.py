import concurrent.futures
import random
import datetime
import copy
import matplotlib.pyplot as plt


def selection_sort(data):
	data_sorted = []
	while len(data) != 0:
		smallest_index = get_index_min(data)
		data_sorted.append(data[smallest_index])
		del data[smallest_index]
	return data_sorted


def get_index_min(data):
	smallest_index = 0
	for index in range(1, len(data)):
		if data[index] < data[smallest_index]:
			smallest_index = index
	return smallest_index


def split_data(data, num_sublists):
	sub_size = int(len(data)/num_sublists)
	sub_lists = []
	for i in range(num_sublists):
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


results = []
a = []
for _ in range(10000):
	a.append(random.randrange(1000000))

for thread in range(1, 51):
	print(thread)
	print("start")
	start = datetime.datetime.now()
	merge_sort(copy.deepcopy(a), thread)
	end = datetime.datetime.now()
	print("end")
	b = end-start
	print(b)
	results.append(b)
	
# print(len([i for i in range(1, 51)]))
# print(b)

# plt.plot([i for i in range(1, 51)], b)
# plt.show()






# acopy = copy.deepcopy(a)
# print("start")
# start = datetime.datetime.now()
# list1 = merge_sort(a, 22)
# end = datetime.datetime.now()
# print("end")
# print(end-start)

# f2 = sorted(acopy)

# print(list1==f2)
