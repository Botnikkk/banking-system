import os
try:
    import asyncio 
    import random
    import sqlite3
    from datetime import date
    import matplotlib.pyplot as m
    import botnikkk as n
except :
    os.system('cls')
    print('Installing packages.....')
    os.system(' pip install -r requirements.txt')
    os.system('cls')
    import asyncio 
    import random
    import sqlite3
    from datetime import date
    import matplotlib.pyplot as m
    import botnikkk as n
input('Please enter fullscreen mode for best experience, input any key if you are in fullscreen mode - ')

database = "database"
conn = sqlite3.connect(database)
cur = conn.cursor()
try:
    cur.execute('CREATE TABLE details (name STRING, account_number INTEGER, password STRING, balance INTEGER, statement STRING, creation_date DATE)')
except:
    None
cur.close()

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
    await n.redirect("homescreen")
    os.system('cls')
    n.centre("-","-")
    #printing home bar
    n.centre(symbol="=", title=" Home Page ")

    #printing and detecting option choices
    option_list = ["Account info check", "Withdraw", "Transfer", "View Statement", "Calculate loan", "Slots", "log out"]
    answer = n.ans_check(option_list)

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
         n.centre(symbol="=", title=" You were logged out ")

async def signup(): 
    os.system('cls')
    n.centre("-","-")
    n.centre(symbol="=", title=" Sign up page ")

    #taking name input
    ques = "Enter your first name : "
    first_name_input = n.format_input(ques)

    ques = "Enter your last name : "
    last_name_input = n.format_input(ques)
    
    name_input = first_name_input.capitalize() + " " + last_name_input.capitalize()

    #taking pass input
    
    pass_input = n.format_input('Enter a 6 digit pin - ')
    pass_input = n.int_check(pass_input)
    while len(str(pass_input)) != 6:
        n.centre("Password is too short")
        pass_input = n.format_input('Enter a 6 digit pin - ')
        pass_input = n.int_check(pass_input)
    
    #assigning account number
    acc_num = random.randint(10**8, 10**17)
    n.centre("Your account number is : {num}".format(num=acc_num))
    
    #assinging balance
    bal = random.randint(10000,10000000)

    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    #storing data
    cur.execute('INSERT INTO details (name, account_number, password, balance, statement, creation_date) VALUES ("{name}", "{acc_num}", "{password}", "{bal}", "EMPTY", "{now}" )'.format(name=name_input,acc_num=acc_num,password=pass_input,bal=bal,now=(date.today())))
    conn.commit()
    cur.close()
    n.centre(symbol="=", title="")
    n.centre('Please note/copy your account number as it will not be shown again.')
    n.ans_check(option_list=['Noted'])
    await login()

async def login() :
    await n.redirect("login page")
    os.system('cls')
    n.centre("-","-")
    n.centre(symbol="=", title=" Login page ")

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
    input_id = n.format_input("Enter your Account number")
    if input_id in id_data  : 
            index = id_data.index(input_id)

    else:
        while input_id not in id_data and id_trials > 0 :
            n.centre(" No such ID was found ! you have {trials} trials left ".format(trials=id_trials))
            input_id = n.format_input("Enter your Account number")
            id_trials -= 1

            if input_id in id_data and id_trials >= 0 : 
                index = id_data.index(input_id)
                break

    if id_trials >= 0 and input_id in id_data  :
        #checking pass
        input_pass = n.format_input('Enter your password - ')
        input_pass = str(n.int_check(input_pass))

        if input_pass != pass_data[index] :
            print('incorrect')
            while input_pass != pass_data[index] and pass_trials > 0 : 

                n.centre("incorrect password ! you have {trials} trials left ".format(trials=pass_trials))
                input_pass = n.format_input('Enter your password - ')
                input_pass = str(n.int_check(input_pass))
                pass_trials -= 1
                if input_pass == pass_data[index] :
                    break
        if pass_trials >= 0 and input_pass == pass_data[index] :
            #welcome screen
            if input_id in id_data and input_pass == pass_data[index] :
                n.centre(symbol="-", title=" Welcome {user} ".format(user=name_data[index]))
                await homescreen(input_id)
        else : 

                n.centre(symbol="=", title=" You were logged out ")
    else : 
                n.centre(symbol="=", title=" You were logged out ")

async def acc_info(user):
    os.system('cls')
    n.centre("-","-")
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT name, balance, creation_date FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchall()
    data = data[0]
    cur.close()

    n.centre("Account info", "=")
    n.centre("Name : {name}".format(name=data[0]))
    n.centre("Account number : {acc_num}".format(acc_num=user))
    n.centre("Current balance : ₹ {bal}".format(bal=data[1]))
    n.centre("Account created on : {date}".format(date=data[2]))

    n.ans_check(option_list=["back"])
    await homescreen(user)

async def withdraw(user):
    os.system('cls')
    n.centre("-","-")
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT balance, password, statement FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchone()
    bal = int(data[0])
    pas = str(data[1])
    sta = data[2]

    n.centre("Current balance : ₹ {bal}".format(bal=bal))

     #checking pass
    pass_trials = 2
    input_pass = n.format_input('Enter your password - ')
    input_pass = str(n.int_check(input_pass))
    if input_pass != pas :

        while input_pass != pas and pass_trials > 0 : 

            n.centre("incorrect password ! you have {trials} trials left ".format(trials=pass_trials))
            input_pass = n.format_input('Enter your password - ')
            input_pass = str(n.int_check(input_pass))
            pass_trials -= 1
            if input_pass == pas :
                break
    if pass_trials >= 0 and input_pass == pas :

        with_input = n.format_input("Enter the ammount you wish to withraw")
        with_input  = n.int_check(with_input) 

        if with_input > bal : 
            n.centre("INSUFFICIENT BALANCE !")
            conn.commit()
            cur.close()
            n.ans_check(option_list=["back"])
            await homescreen(user)
        else : 
            cur.execute('UPDATE details SET balance = balance - {with_input} WHERE account_number = {acc_num}'.format(with_input=with_input, acc_num=user))
            conn.commit()
            cur.close()

            sta = "₹ {with_input} withdrawn".format(with_input=str(with_input))
            upd_sta(user,sta)

            n.centre("You withrew ₹ {with_input}......if you're wondering where it went, it went into a virtual blackhole (^_^)".format(with_input=with_input))
            n.centre("New balance : ₹ {new_bal}".format(new_bal=(bal-with_input)))
            n.ans_check(option_list=["back"])
            await homescreen(user)
    else : 
        n.centre("password did not match")
        await homescreen(user)
    conn.commit()
    cur.close()

async def transfer(user):
    os.system('cls')
    n.centre("-","-")
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT balance, password FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchone()
    bal = int(data[0])
    pas = str(data[1])

    n.centre("Current balance : ₹ {bal}".format(bal=bal))

    #checking pass
    pass_trials = 2
    input_pass = n.format_input('Enter your password - ')
    input_pass = str(n.int_check(input_pass))
    if input_pass != pas :

        while input_pass != pas and pass_trials > 0 : 

            n.centre("incorrect password ! you have {trials} trials left ".format(trials=pass_trials))
            input_pass = n.format_input('Enter your password - ')
            input_pass = str(n.int_check(input_pass))
            pass_trials -= 1
            if input_pass == pas :
                break
    if pass_trials >= 0 and input_pass == pas :

        tran_input = n.format_input("Enter the account id you wish to transfer the ammount to")
        tran_input  = n.int_check(tran_input)

        cur.execute('SELECT name FROM details WHERE account_number = "{acc_num}"'.format(acc_num=tran_input))
        name = cur.fetchone()
        if name is not None : 
            name = name[0]
            n.centre("Transfering ammount to {name}".format(name=name))

            tran_amm = n.format_input("Enter the ammount you wish to transfer")
            tran_amm = n.int_check(tran_amm)

            cur.execute('UPDATE details SET balance = balance + {amm} WHERE account_number = "{num}"'.format(amm=tran_amm,num=tran_input))
            cur.execute('UPDATE details SET balance = balance - {amm} WHERE account_number = "{num}"'.format(amm=tran_amm,num=user))
            
            conn.commit()
            cur.close()

            upd_sta(user=user,update="Transfered ₹ {amm} to {acc}".format(amm=tran_amm, acc=tran_input))
            upd_sta(user=tran_input, update="Recieved ₹ {amm} from {acc}".format(amm=tran_amm, acc=user))
            n.centre("TRANSACTION SUCCSSESFUL ! your balance now is ₹ {bal}".format(bal=bal-tran_amm))
            n.ans_check(option_list=["back"])
            await homescreen(user)
        else : 
            n.centre("TRANSACTION FAILED, USER DOES NOT EXIST")
            await homescreen(user)
    else :
        n.centre("password did not match")
        await homescreen(user)

async def statement(user):
    os.system('cls') 
    n.centre("-","-")
    #opening the file
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT statement FROM details WHERE account_number = "{acc_num}"'.format(acc_num=user))
    data = cur.fetchone()
    sta = str(data[0]).split(",")

    for i in sta : 
        n.centre(i)
    
    n.ans_check(option_list=["back"])
    await homescreen(user)
    
async def loan(user):
    os.system('cls')
    n.centre("-","-")
    n.centre("Which type of interest based loan do you wish to calculate?")
    option_list=["Simple interest", "Amortized loan"]
    ans = n.ans_check(option_list)
    if  ans == option_list[0] :
        await simple(user)
    else : 
        await amortized(user)

async def simple(user):
    os.system('cls')
    n.centre("-","-")

    p = n.int_check(n.format_input("Enter a principal ammount"))
    r = n.int_check(n.format_input("Enter a interest rate"))
    r = (r/100)
    t = n.int_check(n.format_input("Enter a time period in years"))
    a = p + (p*r*t)
    

    n.centre("Total ammount paid : ₹ {a}".format(a=a))
    n.centre("Principal ammount : ₹ {p}   Ammount paid in interest : ₹ {i}".format(p=p, i=(a-p)))

    option_list=["View pie chat","back"]
    ans = n.ans_check(option_list)

    if ans == option_list[0]:
        y = [p , (a - p )]
        lper = int((p/a)*100)
        iper = 100 - lper
        labels = ["Loan ammount {lper}%".format(lper=lper) , "Ammount paid in interest {iper}%".format(iper=iper)]
        m.pie(y , labels=labels)
        m.show()

        n.ans_check(option_list=["back"])

    await homescreen(user)

async def amortized(user):
    os.system('cls')
    n.centre("-","-")
    p = n.int_check(n.format_input("Enter a principal ammount"))
    r = n.int_check(n.format_input("Enter a interest rate"))
    r = (r/100)
    t = n.int_check(n.format_input("Enter a time period in years"))

    a =  int((p*r*((1 + r)**t))/(((1 + r)**t) - 1))
    i = int(p*r)
    p = int(a - i) 
    
    a = int(a)
    n.centre("Total ammount paid : ₹ {a}".format(a=a))
    n.centre("Principal repayment : ₹ {p}   Ammount paid in interest : ₹ {i}".format(p=p, i=i))

    option_list=["View pie chat","back"]
    ans = n.ans_check(option_list)

    if ans == option_list[0]:
        y = [p , i]
        lper = int((p/a)*100)
        iper = 100 - lper
        labels = ["Loan ammount {lper}%".format(lper=lper) , "Ammount paid in interest {iper}%".format(iper=iper)]
        m.pie(y , labels=labels)
        m.show()

        n.ans_check(option_list=["back"])
    
    await homescreen(user)

async def slots(user):
    await roll(user)
    option_list=["roll again", "back"]
    ans = n.ans_check(option_list)
    while ans == option_list[0]:
        await roll(user)
        option_list=["roll again", "back"]
        ans = n.ans_check(option_list)
    
    await homescreen(user)

async def roll(user):
    os.system('cls')
    n.centre("-","-")
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute('SELECT balance FROM details WHERE account_number = {user}'.format(user=user))
    bal = cur.fetchone()
    bal = bal[0]

    n.centre("SLOTS",symbol="=")
    amm = int(n.format_input("Enter the ammount you wish to bet"))
    if amm <= bal : 
        for i in range(270) :
            await asyncio.sleep(0.01)
            if i < 70 :
                a = random.randint(1,7)
            if i < 130 :
                b = random.randint(1,7)
            c = random.randint(1,7)
            title = "| {a} | {b} | {c} |".format(a=a,b=b,c=c)
            n.centre(title,str_end='\r')
        n.centre(title)

        if a == b == c == 7  :

            n.centre("CONGRATULATIONS ! you've hit a jackpot !")
            cur.execute('UPDATE details SET balance = balance + {amm} WHERE account_number = "{user}"'.format(amm=2*amm, user=user))
            n.centre("You won ₹ {amm}".format(amm=2*amm))
            conn.commit()
            cur.close()
            upd_sta(user,"Won ₹ {amm} in slots".format(amm=2*amm))

        elif a == b == c :

            n.centre("You didn't hit the jackpot but u didn't loose any money !")
            conn.commit()
            cur.close()

        elif a == b or b == c or c == a :

            n.centre("You hit the half jackpot ! you only lost half of your money !")
            cur.execute('UPDATE details SET balance = balance - {amm} WHERE account_number = "{user}"'.format(amm=int(amm/2), user=user))
            n.centre("You lost ₹ {amm}".format(amm=str(int(amm/2))))
            conn.commit()
            cur.close()
            upd_sta(user,"Lost ₹ {amm} in slots".format(amm=int(amm/2)))

        else : 

            n.centre("OUCH! you could not hit the jackpot !")
            cur.execute('UPDATE details SET balance = balance - {amm} WHERE account_number = "{user}"'.format(amm=amm, user=user))
            n.centre("You lost ₹ {amm}".format(amm=amm))
            conn.commit()
            cur.close()
            upd_sta(user,"Lost ₹ {amm} in slots".format(amm=amm))
    else :
        n.centre("NOT ENOUGH BALANCE !")

#cool entry screen 
file = open("design.txt",encoding= "utf8")
lines = file.readlines()
file.close()
#forever running loop for the game
while 1 < 2 :
    middle = n.get_alignments()["left_align"]
    os.system('cls')
    string = ""
    for i in  lines : 
        print(middle*" " + i.strip('\n'))
    n.centre("Are you a existing user ?")
    answer  = n.ans_check(option_list=["yes", "no", "exit bank"])   
    if answer == "yes" :
        asyncio.run(login())
    elif answer == "no" :
        asyncio.run(signup())
    else :
        n.centre(" Exited the bank ","=")
        break
    
