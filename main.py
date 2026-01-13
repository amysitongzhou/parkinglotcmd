import yagmail
import random
import math
import datetime
import time
import os
import json
import keyboard
from eyedeaAPI import *


# menu function
def menu():
    print('==================Welcome to the Parking Lot =========================')
    print('----------------------------Contents----------------------------------------')
    print('\t\t\t\t\t\t0.Exit System')
    print('\t\t\t\t\t\t1.Search up a Car')
    print('\t\t\t\t\t\t2.Payment')
    print('\t\t\t\t\t\t3.Add new vehicles')
    print('\t\t\t\t\t\t4.Register Monthly Parking Permits')
    print('----------------------------------------------------------------------------')

def read_json(file_path):
    #with open (path(file_path)) as f:
    f = open(file_path)
    data = json.load(f)
    return data 
def write_json(file_path, name, value):
    f = open(file_path, "r+")
    data = json.load(f)
    data[name] = value
    f.write(json.dumps(data))

 #digital reciept
def notification ():
    sender_email = "amyzhou1102iii@gmail.com"

    sender_password = ""

    reciever_email= str(input("email here:"))

    with open('password.txt',"r",) as f:
        sender_password=f.read()
        
        print(sender_password)

        yag = yagmail.SMTP (user=sender_email, password=sender_password)

        subject = "Parking Reciept"
        contents = ["to be decided."]

        print(yag.send(to=reciever_email,subject=subject,contents=contents))
    #input car info function
def insert():
    while True:
         plate_No = input('Please Enter the License Plate Number：\n')
         if not plate_No:
             break
         car_color = input('The color of the vehicle: \n')
         if not parking_time:
             break
         car = {'color': car_color, 'start_time': datetime.datetime.now()}
         parking_spaces[plate_No]= car
         answer = input('Do you want to add anymore vehicle? (yes/no) \n')
         if answer == 'y' or answer == 'Y':
             continue
         else:
             break
    print('Vehicle info input complete!')
def checkPlate():
    try: 
     
        # Similating the car enter the parking lot
        result = plate_recoginzation ("C:\\website\\plateMNR\\test1.jpg")
        plate_No= result[0].get("anprResult").get("ocrText")
        car_color =result[0].get("mmrResult").get("color")
        if len(parking_spaces)>0 and len(parking_spaces)< total_parking_spaces:
            parking_spaces[plate_No]= {'color':car_color, 'start_time': datetime.datetime.now()}
            print ("A car with the plate " + plate_No + " in " + car_color + "enter the parking lot")
        else: 
            print ("The parking lot is full")
    except:
          print (" An exception occurred in System configuration")

  
def monthly_permit():
    choice = int(input('1: Add a new vehicle \n2: Remove an existing vehicle \n'))
    plate_No = input('Please Enter the License Plate Number：\n')
    try:
        if choice == 1 : 
            monthly_permits.append(plate_No)
        elif choice == 2: 
            monthly_permits.remove(plate_No)
        parking_info["monthly_permits"] = monthly_permits
        write_json ("C:\website\parkinglot\config.json", "monthly_permits",monthly_permits )
    except:
        print ("The system encountered the issue when updating the monthly permits information")
def save ():
    print ("It is here")


def search ():
    plate_No = input('Please Enter the License Plate Number：\n')
    try :
        car = parking_spaces.get(plate_No)
        print ("The vehicle is in the parking lot. The vehicle is in " + car.get("color") + " start time is " + car.get("start_time"))
    except:
        print ("The vehicle isn't found.")
  
#remove the car function 
def payment():
  plate_No = input('Please Enter the License Plate Number：\n')
  total_fee = 0
  if plate_No in monthly_permits :
    return total_fee
  try: 
    car = parking_spaces.get(plate_No)
    parking_time = datetime.datetime.now() - car.get("start_time")
    parking_hours = parking_time.hour

    if (parking_hours > 3):  # It is based on daily rate
        total_fee = parking_hours/24 * daily_rate
    else:
        total_fee = parking_hours * hourly_rate    
    return total_fee * (1+ tax)
  except:
    print ("Please input valid the vehicle's plate number")
    payment ()
def getConfig():
    parking_info = None
    try: 
        parking_info = read_json("C:\website\parkinglot\config.json") 
    except:
          print (" An exception occurred in System configuratoin")
    return parking_info
def main():
         while True:
            #if keyboard.is_pressed("m"): 
                menu()
                try:
                    choice = int(input('Please input your choice\n'))
                    if choice in [0, 1, 2, 3, 4]:
                        if choice == 0:
                            answer = input('Are you sure to exit？y/n\n')
                            if answer == 'y' or answer == 'Y':
                                print('Thank you for using the system！')
                                break  # exit
                            else:
                                continue
                        elif choice == 1:
                            search()
                        elif choice == 2:
                            total_cost= payment()
                            print ("Please pay the parking fee " + total_cost)
                        elif choice == 3:
                            insert()
                        elif choice == 4:
                            monthly_permit()
                except:
                    print("Please input the valid number")
                    main()
            # else:
            #    #checkPlate ()
            #    time.sleep(2)
    

if __name__ == '__main__':
    #initiation
    total_parking_spaces = 0
    tax =0
    hourly_rate = 0
    daily_rate =0
    monthly_permits = {}
    parking_spaces = {}
    parking_info = getConfig()
    if parking_info is not None:
        total_parking_spaces= parking_info.get("parking_space")
        tax = parking_info.get("tax")
        hourly_rate = parking_info.get("hourly_rate")
        daily_rate = parking_info.get("daily_rate")
        monthly_permits= parking_info.get("monthly_permits")
    main()


