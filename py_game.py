import random


print("----------------------Welcome to the guessing game------------------\nYou only have 6 attempts\nTry your best as hints are also there!!!")

target_num = random.randint(1,100)
attempt_no = 0

for i in range(6):
    num = int(input("Enter the guessed number:"))
    if num==target_num:
        print("Yeah!!\nWell done")
        print("No of attempts:",attempt_no)
        print("Great Intution") if 0<attempt_no<3 else print("Okay Finely Played")
        print("----------------------------------END------------------------------")
        break
    else:
        print("Try a little higher") if (target_num-num)>0 else print("Try a small number")
    attempt_no+=1
    if i==5:
        print("Better luck next time!!")
        print("----------------------------------END------------------------------")
