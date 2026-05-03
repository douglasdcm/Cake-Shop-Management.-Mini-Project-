from tabulate import tabulate

def user_login():
    try:
        user_id = input("\nEnter a User ID: ")
        with open("user_log.txt", "r") as fp:
            data = fp.readlines()
        for line in data:
            user_info = line.strip().split(",")
            if user_info[0] == user_id:
                user_pass = input("Enter a  User Password: ")
                if user_info[1] == user_pass:
                    print("\nWelcome", user_id, "\n")
                    return user_id  
    except FileNotFoundError:
        print("File does not exist....")
    except Exception as e:
        print("An error occurred:", e)
    return None

def addUser():
    try:
        with open("user_log.txt", "r") as user_file:
            existing_users = [line.strip().split(",")[0] for line in user_file.readlines()]

        while True:
            new_user_id = input("Enter a unique User ID: ")
            if new_user_id in existing_users:
                print("User ID already exists. Please enter a unique User ID.")
                continue
            new_password = input("Enter a password: ")

            new_user_data = f"{new_user_id},{new_password}"  
            with open("user_log.txt", "a") as user_file:
                user_file.write(new_user_data + "\n")
            print("User added successfully.")
            break

    except Exception as e:
        print("An error occurred:", e)
    except:
        print("Error 404: Error Not Found...")

def displayUsers():
    try:
        with open("user_log.txt", "r") as user_file:
            data = user_file.readlines()

        user_ids = [line.strip().split(",")[0] for line in data]

        if user_ids:
            headers = ["User ID"]
            table_data = [[user_id] for user_id in user_ids]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("No users found.")
    except FileNotFoundError:
        print("File does not exist.")
    except Exception as e:
        print("An error occurred:", e)

def removeUser():
    try:
        displayUsers()
        user_id=input("Enter a User ID: ")
        allUser = []
        found = False
        with open("user_log.txt", "r+") as fp:
            for line in fp:
                data = line.split(",")
                if data[0] == str(user_id):
                    found = True
                    print("User ID {} has been deleted.".format(user_id))
                else:
                    allUser.append(line)
        with open("user_log.txt", "w") as fp:
            fp.write("".join(allUser))
        if not found:
            print("User ID {} not found.".format(user_id))
    except FileNotFoundError:
        print("An error occurred while deleting the Cake.")
    except Exception as e:
        print("An error occurred:", e)
    except:
        print("Error 404: Error Not Found.")
