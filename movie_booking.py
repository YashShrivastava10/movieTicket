import mysql.connector
import datetime
import random
import json

my_db = mysql.connector.connect(host='localhost', user='root', password='root')
my_cursor = my_db.cursor()
my_cursor.execute('create database MiniProject')
my_db = mysql.connector.connect(host='localhost', user='root', password='root', database='MiniProject')
my_cursor = my_db.cursor()
my_cursor.execute('create table movie_table('
                  'ID int NOT NULL primary key AUTO_INCREMENT, '
                  'Name varchar(30) NOT NULL, '
                  'Movie varchar(30) NOT NULL, '
                  'Ticket_Quantity int, '
                  'Ticket_Price int, '
                  'Combo varchar(20), '
                  'Food_Quantity int,Food_Price int)')


movie = {}
user_dict = {}

while True:
    print(" \nWelcome to MINI PROJECT")
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. Admin")
    print("2. Customer")
    print("3. Exit")
    n1 = int(input("Select a user by entering the number: "))

    if n1 == 1:
        while True:
            print(" \nWelcome Admin")
            print("~~~~~~~~~~~~~~~")
            print("1. Add movies which are currently premiering")
            print("2. Available Movies")
            print("3. Customer details")
            print("4. Logout Admin")
            n2 = int(input("Select an operation by entering the number: "))
            if n2 == 1:
                movie_name = input("Enter movie name: ")
                total_ticket = eval(input("Enter the total number of tickets: "))
                total_price =  eval(input("Enter the price of movie: "))
                movie[movie_name] = [total_ticket, total_price]
            elif n2 == 2:
                print("All available movies:\n", movie)
            elif n2 == 3:
              with open("sample.json", "w") as f:
                json.dump(user_dict, f)
            elif n2 == 4:
                print("You have been logged out.\n")
                break
            else:
              print("Invalid Selection")

    elif n1 == 2:
        user_name = input("Please enter your username: ")
        bag = []
        f = 0
        f1 = 0
        while True:
            print("\nWelcome Dear", user_name)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("1. View all movies")
            print("2. Search movie")
            print("3. Select a movie to book")
            print("4. Cancel the tickets")
            print("5. Print Invoice")
            print("6. Sign out")
            n3 = int(input("Select an operation by entering the number: "))
            if n3 == 1:
                print("All available movies:\n", movie)

            elif n3 == 2:
                search = input("enter the movie: ")
                if search in movie:
                    print("The movie is available.\n")
                else:
                    print("The movie is not available.\n")

            elif n3 == 3:
                f = 1
                m_name = input("Enter the movie name to be booked: ")
                quantity = int(input("Enter the number of tickets: "))
                if m_name in movie:
                  if movie[m_name][0] >= quantity:
                    bag.append(m_name)
                    bag.append(quantity)
                    bag.append(movie[m_name][1])
                    movie[m_name][0] -= quantity
                    total_food_quantity = 0
                    food = input("Do you want enjoy the movie with some snacks (y/n) ? ")
                    if food == 'y':
                      f1 = 1
                      print("\n")
                      print("Combos")
                      print("~~")
                      print("1. Pizza Combo - Rs. 650")
                      print("2. Burger Combo - Rs. 550")
                      print("3. Popcorn Combo - Rs. 300")
                      n31 = eval(input("Select the combo by entering the number: "))
                      food_quantity = eval(input("Enter the quantity: "))
                      bag.append(food_quantity)
                      if n31 == 1:
                        bag.append('Pizza Combo')
                        bag.append(650)
                      elif n31 == 2:
                        bag.append('Burger Combo')
                        bag.append(550)
                      elif n31 == 3:
                        bag.append('Popcorn Combo')
                        bag.append(300)
                      user_dict[user_name] = {
                          'movie': bag[0],
                          'Total number of tickets': bag[1],
                          'Ticket_Price': bag[2],
                          'food_combo': bag[4],
                          'food_quantity': bag[3],
                          'total_food_price':bag[5]
                          }
                      sql = 'insert into movie_table(Name, Movie, Ticket_Quantity, Ticket_Price, Combo, ' \
                            'Food_Quantity, Food_Price) values(%s, %s, %s, %s, %s, %s, %s)'
                      val = (user_name, user_dict[user_name]['movie'], user_dict[user_name]['Total number of tickets'],
                             user_dict[user_name]['Ticket_Price'], user_dict[user_name]['food_combo'],
                             user_dict[user_name]['food_quantity'], user_dict[user_name]['total_food_price'])
                      my_cursor.execute(sql, val)
                      my_db.commit()
                    if f1==0:
                        user_dict[user_name] = {
                         'movie': bag[0],
                         'Total number of tickets': bag[1],
                         'Ticket_Price': bag[2],
                         'food_combo': 0,
                         'food_quantity': 0,
                         'total_food_price':0
                         }
                        sql = 'insert into movie_table(Name, Movie, Ticket_Quantity, Ticket_Price, Combo, ' \
                              'Food_Quantity, Food_Price)values(%s, %s, %s, %s, %s, %s, %s)'
                        val = (user_name, user_dict[user_name]['movie'], user_dict[user_name]['Total number of tickets'],
                               user_dict[user_name]['Ticket_Price'], '', 0, 0)
                        my_cursor.execute(sql, val)
                        my_db.commit()
                else:
                    print("Movie not available\n")

            elif n3 == 4:
              u_id = input("Enter the userid: ")
              if user_name in user_dict:
                otp = random.randrange(1000, 9999)
                print("OTP has been set to ",u_id)
                print("\n")
                print("Your OTP is: ", otp)
                while True:
                  re_otp = eval(input("Enter the OTP: "))
                  if otp == re_otp:
                    print("\nYour ticket has been cancelled succesfully.")
                    movie[user_dict[user_name]['movie']][0] += user_dict[user_name]['Total number of tickets']
                    my_cursor.execute('delete from movie_table where Name = %s',(user_name,))
                    my_db.commit()
                    del user_dict[user_name]
                    break;
                  else:
                    print("\nOTP is incorrect.")
                    print("Please enter the correct OTP.")
              else:
                print("Username is invalid.")

            elif n3 == 5:
              if f == 1:
                sum = 0
                print("\n")
                print("                 Billing Invoice        ")
                print("                 ~~~~~~~~~~~~~~~        ")
                print("Billing date: ", datetime.datetime.now())
                print("Products          Unit Price     Qty    Total")
                print("~~~~~~~~          ~~~~~~~~~~     ~~~    ~~~~~")
                p = bag[0]
                q = bag[1]
                r = bag[2]
                total = q*r
                sum += total
                print(p, "                 ", r,"      ",    q,"    ",total)
              if f1 == 1:
                q = bag[3]
                p = bag[4]
                r = bag[5]
                total = q*r
                sum += total
                print(p, "       ", r,"      ",  q,"    ",total)
              print("------------------------------------------------")
              print("Total price                             ",sum)
              print("------------------------------------------------")
              print("         Thank You For booking the tickets.         \n")

            elif n3 == 6:
              print("\n")
              print("Logging Out..\n")
              print("Developed by - Yash\n")
              break

    elif n1 == 3:
        print("\n")
        print("Software Shutting Down......\n")
        break
    else:
        print("Invalid Selection")
