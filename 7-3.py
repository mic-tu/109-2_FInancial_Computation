import datetime

ticket_num = int(input())  # 票數
nums = input().split(',')
people_num = int(nums[0])  # 人數
level_num = int(nums[1])  # 會員等級數

levels = input().split(',')  # 等級
level_ticket = input().split(',')  # 每個等級可買票數
for i in range(level_num):
	level_ticket[i] = int(level_ticket[i])

start = datetime.datetime.strptime(input(), "%Y-%m-%d %H:%M:%S")  # 開始售票時間
level_day = input().split(',')  # 售票區間
for i in range(level_num):
	level_day[i] = int(level_day[i])

if people_num == 0:
	print(ticket_num)
else:
	people_time = input().split(',')  # 人數購票時間
	for i in range(people_num):
		people_time[i] = datetime.datetime.strptime(people_time[i], "%Y-%m-%d %H:%M:%S")

	people = input().split(',')  # 人數編號

	people_level = input().split(',')  # 人數等級

	people_pur = input().split(',')  # 購票數
	for i in range(people_num):
		people_pur[i] = int(people_pur[i])

	people_data = []
	for i in range(people_num):
		people_data.append([people_time[i], people[i], people_level[i], people_pur[i]])
	people_data.sort()  # people_data將會以訂票順序排序，像[datetime.datetime(2005, 5, 3, 1, 0), '-11', 'common', 2]

	for a in range(level_num):
		for i in range(people_num):
			if levels[a] == people_data[i][2]:
				if level_ticket[a] < people_data[i][3]:
					people_data[i][3] = level_ticket[a]

	level_list = []
	for a in range(level_num):
		accepted = []
		for i in range(a + 1):
			accepted.append(levels[i])
		level_list.append(accepted)

	output_list = []
	for a in range(level_num):
		for i in range(people_num):
			if datetime.timedelta(0) <= (people_data[i][0] - start) <= datetime.timedelta(days = level_day[a]) and people_data[i][2] in level_list[a] and people_data[i] not in output_list:
				output_list.append(people_data[i])

	output = []
	pur_list = []  # 購買過的人的編號
	for i in range(len(output_list)):
		if output_list[i][1] not in pur_list:
			if ticket_num - output_list[i][3] >= 0:
				output.append([output_list[i][1], output_list[i][3]])
				ticket_num -= output_list[i][3]
				pur_list.append(output_list[i][1])
			elif ticket_num > 0 and ticket_num - output_list[i][3] <= 0:
				output.append([output_list[i][1], ticket_num])
				ticket_num -= ticket_num
				pur_list.append(output_list[i][1])
			else:
				break
	print(ticket_num)
	for i in range(len(output)):
		print(output[i][0] + ':' + str(output[i][1]))