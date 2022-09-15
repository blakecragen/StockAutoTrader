import time
import datetime as dt
import TextFileEditor

buy_or_sell = [["DOGE",0]]
dataPoints = []
for i in range(0,31):
    dataPoints.append([])
for i in range(0,29):
    dataPoints[i].append(0)
for i in range(1,29):
    dataPoints[i].append(0)
for i in range(1,29):
    dataPoints[i].append(0)
for i in range(1,29):
    dataPoints[i].append(0)
dataPoints[29].append("Half Hour Reference")
dataPoints[29].append(0)
dataPoints[30].append("Hour Reference")
dataPoints[30].append(0)
dataPoints[0][0] = 1
dataPoints.append([])
dataPoints[31].append(0)
dataPoints.append([])
dataPoints[32].append("Counter for Hour/Hr Point")
dataPoints[32].append(0)
dataPoints.append([])
dataPoints[33].append("Delay for buying stock")
dataPoints[33].append(30)
current_time = [["Hours",0],["Min",0],["Seconds",0]]
change_in_percentages = []

def change_in_percentage_2_chosen_pts(point1,point2):
    '''Takes in two points and returns the percentage change'''
    first_taken_point = dataPoints[int(point1)][0]
    secnod_taken_point = dataPoints[int(point2)][0]
    
    if first_taken_point!=0:
        percent_change = 100*(first_taken_point - secnod_taken_point)/first_taken_point
    else:
        percent_change = 0
    return percent_change

def change_in_percentage_2pts():
    '''Takes in two points and returns the percentage change'''
    placeholder = 0
    next_point = dataPoints[0][0]
    first_taken_point = 2
    secnod_taken_point = 1
    if next_point-2 <= 0:
        placeholder = 0
    else:
        first_taken_point = dataPoints[next_point-2][0]
        secnod_taken_point = dataPoints[next_point-1][0]
    if first_taken_point!=0:
        percent_change = 100*(first_taken_point - secnod_taken_point)/first_taken_point
    else:
        percent_change = 0
    return percent_change

def change_in_percentage_halfhr():
    '''Takes in a points and returns the percentage change between it and half
    hr reference'''
    count = dataPoints[0][0]
    if count > 1:
        next_point = dataPoints[0][0]
        first_point = dataPoints[next_point-1][0]
        secnod_point = dataPoints[29][1]

        percent_change = 100*(first_point - secnod_point)/first_point
        return percent_change
    else:
        next_point = 2
        first_point = dataPoints[next_point-1][0]
        secnod_point = dataPoints[29][1]
        if first_point!= 0:
            percent_change = 100*(first_point - secnod_point)/first_point
            return percent_change
        

def change_in_percentage_hr():
    '''Takes in a points and returns the percentage change between it and half
    hr reference'''
    count = dataPoints[0][0]
    if count > 1:
        next_point = dataPoints[0][0]
        if next_point == 1:
            next_point = 2
        first_point = dataPoints[next_point-1][0]
        secnod_point = dataPoints[30][1]

        percent_change = 100*(first_point - secnod_point)/first_point
        return percent_change
    else:
        next_point = 2
        first_point = dataPoints[next_point-1][0]
        secnod_point = dataPoints[29][1]
        if first_point!= 0:
            percent_change = 100*(first_point - secnod_point)/first_point
            return percent_change

def get_current_time():
    time = str(dt.datetime.now().time())
    current_time[0][1] = int(time[:2])
    current_time[1][1] = int(time[3:5])
    current_time[2][1] = float(time[6:])
    return current_time

def store_next_dataPoint(point):
    dataPoints[dataPoints[0][0]][0] = point[0][1]
    current_time = get_current_time()
    dataPoints[dataPoints[0][0]][1] = current_time[0][1]
    dataPoints[dataPoints[0][0]][2] = current_time[1][1]
    dataPoints[dataPoints[0][0]][3] = current_time[2][1]
    if dataPoints[33][1] <=60:
        dataPoints[33][1] = dataPoints[33][1] + 1
    if dataPoints[0][0] == 28:
        dataPoints[0][0] = 1
    else:
        dataPoints[0][0] = dataPoints[0][0]+1
    if int(current_time[1][1]) == 31 or int(current_time[1][1]) == 1:
        dataPoints[32][1] = 0
    if int(current_time[1][1]) == 0 or dataPoints[30][1] == 0:
        if dataPoints[32][1] == 0:
            dataPoints[30][1] = point[0][1]
            TextFileEditor.write("Hour " + current_time[1][0] + " Data Point:")
            TextFileEditor.write(point[0][1])
            dataPoints[30][1] = point[0][1]
            TextFileEditor.write("Half Hour Data Point:")
            TextFileEditor.write(point[0][1])
    if int(current_time[1][1]) == 30 or dataPoints[29][1] == 0:
        if dataPoints[32][1] == 0:
            dataPoints[29][1] = point[0][1]
            TextFileEditor.write("Half Hour Data Point:")
            TextFileEditor.write(point[0][1])
            dataPoints[32][1] = dataPoints[32][1] + 1
    
    
def get_dataPoints():
    return dataPoints

def lowest_percent_relative_to_hr():
    return " "  

def check_percentages():
    half_hour = change_in_percentage_halfhr()
    point1 = dataPoints[0][0]
    if dataPoints[0][0]>=9:
        check_90_seconds = change_in_percentage_2_chosen_pts(dataPoints[0][0]-7,dataPoints[0][0])
    else:
        check_90_seconds = change_in_percentage_2_chosen_pts(28-9+dataPoints[0][0],dataPoints[0][0])
    hour = change_in_percentage_hr()
    change_in_percentages = [["Hour Percent",hour],["Half Hour Percent",half_hour],["90 Second Percent",check_90_seconds]]
    if dataPoints[0][0] > 2:
        immediate_change = change_in_percentage_2_chosen_pts(dataPoints[0][0]-2,dataPoints[0][0])
    else:
        immediate_change = 0
    change_in_percentages.append(["Immediate Change",immediate_change])
    return change_in_percentages

def check_buy_or_sell(current_Percentages,money_available):
    '''Takes in an array of current percentages (originally from check percentages)
    as well as the money available and makes a choice on whether to buy stock or not'''
    if money_available > 0:
        if float(current_Percentages[3][1]) >.1 and float(current_Percentages[2][1]) > .1 and current_Percentages[1][1] > .3:
            buy_or_sell[0][1] = .45
            dataPoints[33][1] = 0
        if float(current_Percentages[3][1]) <-.1 and float(current_Percentages[2][1]) < -.2 and current_Percentages[1][1] < -1:
            buy_or_sell[0][1] = -.4
            dataPoints[33][1] = 0
    return buy_or_sell
        
        

#def set_timer_speed():

#def get_timer_speed():
    
