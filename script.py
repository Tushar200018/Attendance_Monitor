import pandas as pd
import csv
import pathlib
import os
import numpy as np
import datetime


base_dir = pathlib.Path().absolute()
input_file = pd.read_csv(os.path.join(base_dir,'raw_attendance.csv'))

Time_stamps = []

for i in input_file['Timestamp']:
	curr_datetime = datetime.datetime.strptime(i,'%m/%d/%Y, %I:%M:%S %p')
	Time_stamps.append(curr_datetime)

input_file['Timestamp'] = Time_stamps	

input_file = input_file.sort_values(by=['Full Name','Timestamp'], ascending = True)
input_file = input_file.reset_index(drop = True)

input_file = input_file.groupby('Full Name')

output_df = pd.DataFrame()
Output_Names = []
Output_EntryNum = []
Output_Stamps = []
Output_Total_Time = []
Output_Status = []

Meeting_end_Time = datetime.datetime(hour = 12,minute = 30,second = 59,day = 26,month =9,year =2020)

for names, group in input_file:
	# print(names)
	Output_Names.append(names)
	total_time = datetime.timedelta()
	# print(group)
	joined = False
	prev_time = 0
	dropped = []
	stamp_list = []

	for i in group.index:
		if joined:
			if group['User Action'][i]=='Joined' or group['User Action'][i]=='Joined before':
				# gotta drop this row
				dropped.append(i)
			else:
				total_time+=(group['Timestamp'][i]-prev_time)

				stamp_list.append(str(prev_time.time())+','+str(group['Timestamp'][i].time())+','+str(group['Timestamp'][i]-prev_time)[7:])
				joined = not joined
		else:
			if group['User Action'][i]=='Left':
				# gotta drop
				dropped.append(i)
			else:
				prev_time = group['Timestamp'][i]
				# print(prev_time.time())
				joined = not joined	

	if joined:
		total_time+=(Meeting_end_Time-prev_time)
		stamp_list.append(str(prev_time.time())+','+str(Meeting_end_Time)+','+str(Meeting_end_Time-prev_time)[7:])


	
	group = group.drop(dropped)

	if total_time>=datetime.timedelta(minutes = 40):
		Output_Status.append("Present")
	else:
		Output_Status.append("Absent")	

	Output_Total_Time.append(str(total_time)[7:])
	Output_Stamps.append(stamp_list)

	# print(str(total_time)[7:])	
	# break


output_df['Name'] = Output_Names

for i in Output_Names:
	Output_EntryNum.append(i.partition('_')[2])

output_df['Entry Number'] = Output_EntryNum
output_df['Timestamp'] = Output_Stamps
output_df['Total Time'] = Output_Total_Time
output_df['Status'] = Output_Status

print(output_df)

output_df.to_csv(r'output.csv')
# print(Output_Stamps)
# print(input_file.get_group('zwwCXzrFgt_9217TZY2307'))

# print(input_file.names)
