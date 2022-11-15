import asyncio 
import random
import maskpass
import sqlite3
from datetime import date
import matplotlib.pyplot as m


middle  = 46*" "
database = "database"
conn = sqlite3.connect(database)
cur = conn.cursor()
try:
    cur.execute('CREATE TABLE details (name STRING, account_number INTEGER, password STRING, balance INTEGER, statement STRING, creation_date DATE)')
except:
    print("database exists")
cur.close()

def format_input(ques) : 
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    output = input(string)
    return output

def int_check(answer) :
    answer = str(answer).strip()
    integer = -1
    while integer < 1 :
        try : 
            int(answer)
            integer = int(answer)
        except : 
            centre("Please enter a valid integer !")
            ques = "Enter a number -"
            string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
            answer = input(string) 
            continue
    return int(answer)

def centre(title,symbol=" ",str_end="\n") :
    #aligns the title in centre with symbols around it
    gap = str(symbol)*(64-int((len(title)/2)))
    gap2 = str(symbol)*(128- len(title) - len(gap))
    print(( middle + "|" + gap + title + gap2 + "|" + "\n" + middle + "|" + 128*" " + "|"),end=str_end)

def ans_check(option_list) :

    #prints and detetcs the answers and returns the choose answer
    centre("-","-")
    for i in option_list : 
        centre(symbol=" ", title=(str(option_list.index(i) + 1) + ".) " + str(i)))
    centre("-","-")
    ques = "Choose a option"
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    answer = input(string)
    answer = answer.strip()
    answer = int_check(answer)
    while int(answer) > len(option_list) :
            centre("Not a valid answer !")
            answer = format_input("Choose a option")
            try :
                int(answer) 
            except  :
                answer = int_check(answer)
        
    return option_list[int(answer) - 1]

def format_input(ques):
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    input_ret = input(string)
    return input_ret

def upd_sta(user, update):
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT statement FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchone()
    sta = data[0]

    if sta == "EMPTY" : 
        sta = update + " ON " + str(date.today()) + ","
    else : 
        sta += update + " ON " + str(date.today()) + ","
    cur.execute('UPDATE details SET statement = "{sta}" WHERE account_number = {acc_num}'.format(sta=str(sta),acc_num=user))

    conn.commit()
    cur.close()

async def homescreen(user):
    #printing home bar
    centre(symbol="=", title=" Home Page ")

    #printing and detecting option choices
    option_list = ["Account info check", "Withdraw", "Transfer", "View Statement", "Calculate loan", "Slots", "log out"]
    answer = ans_check(option_list)

    #performing tasks based on choice
    if answer == option_list[0] :
        await acc_info(user)

    elif answer == option_list[1] :
        await withdraw(user)

    elif answer == option_list[2] :
        await transfer(user)

    elif answer == option_list[3] :
        await statement(user)
        
    elif answer == option_list[4] :
        await loan(user)

    elif answer == option_list[5] :
        await slots(user)

    elif answer == option_list[6] :
         centre(symbol="=", title=" You were logged out ")

async def signup(): 
    
    centre(symbol="=", title=" Sign up page ")

    #taking name input
    ques = "Enter your first name : "
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    first_name_input = input(string)

    ques = "Enter your last name : "
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    last_name_input = input(string)
    name_input = first_name_input.capitalize() + " " + last_name_input.capitalize()

    #taking pass input
    ques = "Enter a 6 digit pin"
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    pass_input = maskpass.advpass(prompt=string, mask="*")
    pass_input = int_check(pass_input)
    while len(str(pass_input)) != 6:
        centre("Password is too short")
        ques = "Enter a 6 digit pin"
        string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
        pass_input = maskpass.advpass(prompt=string, mask="*")
        pass_input=int_check(pass_input)
    
    #assigning account number
    acc_num = random.randint(10**8, 10**17)
    
    #assinging balance
    bal = random.randint(10000,10000000)

    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    #storing data
    cur.execute('INSERT INTO details (name, account_number, password, balance, statement, creation_date) VALUES ("{name}", "{acc_num}", "{password}", "{bal}", "EMPTY", "{now}" )'.format(name=name_input,acc_num=acc_num,password=pass_input,bal=bal,now=(date.today())))
    conn.commit()
    cur.close()
    centre(symbol="=", title="")
    
    await login()

async def login() :

    centre(symbol="=", title=" Login page ")

    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT account_number, password, name FROM details')
    data = cur.fetchall()
    cur.close()

    id_data = []
    pass_data= []
    name_data= []
    for i in data :
        id_data.append(str(i[0]))
        pass_data.append(str(i[1])) 
        name_data.append(str(i[2]))

    id_trials = 2
    pass_trials = 2

    #checking id
    input_id = format_input("Enter your Account number")
    if input_id in id_data  : 
            index = id_data.index(input_id)

    else:
        while input_id not in id_data and id_trials > 0 :
            centre(" No such ID was found ! you have {trials} trials left ".format(trials=id_trials))
            input_id = format_input("Enter your Account number")
            id_trials -= 1

            if input_id in id_data and id_trials >= 0 : 
                index = id_data.index(input_id)
                break

    if id_trials >= 0 and input_id in id_data  :
        #checking pass
        ques = "Enter your password"
        string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
        input_pass = maskpass.advpass(prompt=string, mask="*")
        if input_pass.lower() != pass_data[index] :

            while input_pass != pass_data[index] and pass_trials > 0 : 

                centre("incorrect password ! you have {trials} trials left ".format(trials=pass_trials))
                ques = "Enter your password"
                string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
                input_pass = maskpass.advpass(prompt=string, mask="*")
                pass_trials -= 1
                if input_pass == pass_data[index] :
                    break
    
        if pass_trials >= 0 and input_pass == pass_data[index] :
            #welcome screen
            if input_id in id_data and input_pass == pass_data[index] :
                centre(symbol="-", title=" Welcome {user} ".format(user=name_data[index]))
                await homescreen(input_id)
        else : 

                centre(symbol="=", title=" You were logged out ")
    else : 
                centre(symbol="=", title=" You were logged out ")

async def acc_info(user):
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT name, balance, creation_date FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchall()
    data = data[0]
    cur.close()

    centre("Account info", "=")
    centre("Name : {name}".format(name=data[0]))
    centre("Account number : {acc_num}".format(acc_num=user))
    centre("Current balance : ₹ {bal}".format(bal=data[1]))
    centre("Account created on : {date}".format(date=data[2]))

    ans_check(option_list=["back"])
    await homescreen(user)

async def withdraw(user):
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT balance, password, statement FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchone()
    bal = int(data[0])
    pas = data[1]
    sta = data[2]

    centre("Current balance : ₹ {bal}".format(bal=bal))

     #checking pass
    pass_trials = 2
    ques = "Enter your password"
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    input_pass = maskpass.advpass(prompt=string, mask="*")
    if input_pass.lower() != pas :

        while input_pass != pas and pass_trials > 0 : 

            centre("incorrect password ! you have {trials} trials left ".format(trials=pass_trials))
            ques = "Enter your password"
            string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
            input_pass = maskpass.advpass(prompt=string, mask="*")
            pass_trials -= 1
            if input_pass == pas :
                break
    if pass_trials >= 0 and input_pass == pas :

        with_input = format_input("Enter the ammount you wish to withraw")
        with_input  = int_check(with_input) 

        if with_input > bal : 
            centre("INSUFFICIENT BALANCE !")
            conn.commit()
            cur.close()
            ans_check(option_list=["back"])
            await homescreen(user)
        else : 
            cur.execute('UPDATE details SET balance = balance - {with_input} WHERE account_number = {acc_num}'.format(with_input=with_input, acc_num=user))
            conn.commit()
            cur.close()

            sta = "₹ {with_input} withdrawn".format(with_input=str(with_input))
            upd_sta(user,sta)

            centre("You withrew ₹ {with_input}......if you're wondering where it went, it went into a virtual blackhole (^_^)".format(with_input=with_input))
            centre("New balance : ₹ {new_bal}".format(new_bal=(bal-with_input)))
            ans_check(option_list=["back"])
            await homescreen(user)
    else : 
        centre("password did not match")
        await homescreen(user)
    conn.commit()
    cur.close()

async def transfer(user):
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT balance, password FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchone()
    bal = int(data[0])
    pas = str(data[1])

    centre("Current balance : ₹ {bal}".format(bal=bal))

     #checking pass
    pass_trials = 2
    ques = "Enter your password"
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    input_pass = maskpass.advpass(prompt=string, mask="*")
    if input_pass.lower() != pas :

        while input_pass != pas and pass_trials > 0 : 

            centre("incorrect password ! you have {trials} trials left ".format(trials=pass_trials))
            ques = "Enter your password"
            string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
            input_pass = maskpass.advpass(prompt=string, mask="*")
            pass_trials -= 1
            if input_pass == pas :
                break
    if pass_trials >= 0 and input_pass == pas :

        tran_input = format_input("Enter the account id you wish to transfer the ammount to")
        tran_input  = int_check(tran_input)

        cur.execute('SELECT name FROM details WHERE account_number = "{acc_num}"'.format(acc_num=tran_input))
        name = cur.fetchone()
        if name is not None : 
            name = name[0]
            centre("Transfering ammount to {name}".format(name=name))

            tran_amm = format_input("Enter the ammount you wish to transfer")
            tran_amm = int_check(tran_amm)

            cur.execute('UPDATE details SET balance = balance + {amm} WHERE account_number = "{num}"'.format(amm=tran_amm,num=tran_input))
            cur.execute('UPDATE details SET balance = balance - {amm} WHERE account_number = "{num}"'.format(amm=tran_amm,num=user))
            
            conn.commit()
            cur.close()

            upd_sta(user=user,update="Transfered ₹ {amm} to {acc}".format(amm=tran_amm, acc=tran_input))
            upd_sta(user=tran_input, update="Recieved ₹ {amm} from {acc}".format(amm=tran_amm, acc=user))
            centre("TRANSACTION SUCCSSESFUL ! your balance now is ₹ {bal}".format())
            ans_check(option_list=["back"])
            await homescreen(user)
        else : 
            centre("TRANSACTION FAILED, USER DOES NOT EXIST")
            await homescreen(user)
    else :
        centre("password did not match")
        await homescreen(user)

async def statement(user): 
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT statement FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchone()
    sta = str(data[0]).split(",")

    for i in sta : 
        centre(i)
    
    ans_check(option_list=["back"])
    await homescreen(user)
    
async def loan(user):
    centre("Which type of interest based loan do you wish to calculate?")
    option_list=["Simple interest", "Amortized loan"]
    ans = ans_check(option_list)
    if  ans == option_list[0] :
        await simple(user)
    else : 
        await amortized(user)

async def simple(user):

    p = int_check(format_input("Enter a principal ammount"))
    r = int_check(format_input("Enter a interest rate"))
    r = (r/100)
    t = int_check(format_input("Enter a time period in years"))
    a = p + (p*r*t)
    

    centre("Total ammount paid : ₹ {a}".format(a=a))
    centre("Principal ammount : ₹ {p}   Ammount paid in interest : ₹ {i}".format(p=p, i=(a-p)))

    option_list=["View pie chat","back"]
    ans = ans_check(option_list)

    if ans == option_list[0]:
        y = [p , (a - p )]
        lper = int((p/a)*100)
        iper = 100 - lper
        labels = ["Loan ammount {lper}%".format(lper=lper) , "Ammount paid in interest {iper}%".format(iper=iper)]
        m.pie(y , labels=labels)
        m.show()

        ans_check(option_list=["back"])

    await homescreen(user)

async def amortized(user):
    p = int_check(format_input("Enter a principal ammount"))
    r = int_check(format_input("Enter a interest rate"))
    r = (r/100)
    t = int_check(format_input("Enter a time period in years"))

    a =  int((p*r*((1 + r)**t))/(((1 + r)**t) - 1))
    i = int(p*r)
    p = int(a - i) 
    
    a = int(a)
    centre("Total ammount paid : ₹ {a}".format(a=a))
    centre("Principal repayment : ₹ {p}   Ammount paid in interest : ₹ {i}".format(p=p, i=i))

    option_list=["View pie chat","back"]
    ans = ans_check(option_list)

    if ans == option_list[0]:
        y = [p , i]
        lper = int((p/a)*100)
        iper = 100 - lper
        labels = ["Loan ammount {lper}%".format(lper=lper) , "Ammount paid in interest {iper}%".format(iper=iper)]
        m.pie(y , labels=labels)
        m.show()

        ans_check(option_list=["back"])
    
    await homescreen(user)

async def slots(user):
    await roll(user)
    option_list=["roll again", "back"]
    ans = ans_check(option_list)
    while ans == option_list[0]:
        await roll(user)
        option_list=["roll again", "back"]
        ans = ans_check(option_list)
    
    await homescreen(user)

async def roll(user):

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute('SELECT balance FROM details WHERE account_number = {user}'.format(user=user))
    bal = cur.fetchone()
    bal = bal[0]

    centre("SLOTS",symbol="=")
    amm = int(format_input("Enter the ammount you wish to bet"))
    if amm <= bal : 
        for i in range(270) :
            await asyncio.sleep(0.001)
            if i < 70 :
                a = random.randint(1,7)
            if i < 130 : 
                b = random.randint(1,7)
            c = random.randint(1,7)
            title = "| {a} | {b} | {c} |".format(a=a,b=b,c=c)
            symbol = " "
            gap = str(symbol)*(64-int((len(title)/2)))
            gap2 = str(symbol)*(128- len(title) - len(gap))
            print(( middle + "|" + gap + title + gap2 + "|"),end='\r')
        centre(title)

        if a == b == c == 7  :

            centre("CONGRATULATIONS ! you've hit a jackpot !")
            cur.execute('UPDATE details SET balance = balance + {amm} WHERE account_number = "{user}"'.format(amm=2*amm, user=user))
            centre("You won ₹ {amm}".format(amm=2*amm))
            conn.commit()
            cur.close()
            upd_sta(user,"Won ₹ {amm} in slots".format(amm=2*amm))

        elif a == b == c :

            centre("You didn't hit the jackpot but u didn't loose any money !")
            conn.commit()
            cur.close()

        elif a == b or b == c or c == a :

            centre("You hit the half jackpot ! you only lost half of your money !")
            cur.execute('UPDATE details SET balance = balance - {amm} WHERE account_number = "{user}"'.format(amm=int(amm/2), user=user))
            centre("You lost ₹ {amm}".format(amm=str(int(amm/2))))
            conn.commit()
            cur.close()
            upd_sta(user,"Lost ₹ {amm} in slots".format(amm=int(amm/2)))

        else : 

            centre("OUCH! you could not hit the jackpot !")
            cur.execute('UPDATE details SET balance = balance - {amm} WHERE account_number = "{user}"'.format(amm=amm, user=user))
            centre("You lost ₹ {amm}".format(amm=amm))
            conn.commit()
            cur.close()
            upd_sta(user,"Lost ₹ {amm} in slots".format(amm=amm))
    else :
        centre("NOT ENOUGH BALANCE !")


#cool entry screen 
file = open("design.txt",encoding= "utf8")
lines = file.readlines()
file.close()

#forever running loop for the game
while 1 < 2 :
    string = ""
    for i in  lines : 
        print(middle + i.strip('\n'))
    centre("Are you a existing user ?")
    answer  = ans_check(option_list=["yes", "no", "exit bank"])   
    if answer == "yes" :
        asyncio.run(login())
    elif answer == "no" :
        asyncio.run(signup())
    else :
        centre(" Exited the bank ","=")
        break
