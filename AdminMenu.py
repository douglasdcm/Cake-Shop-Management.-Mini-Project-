from tabulate import tabulate
import logo
import cake
import AdminLogin
import UserLogin
from transactions import (
    CakeDoesNotExist,
    CakeValuesAreValid,
    AddCake,
    CakeExists,
    DeleteCake,
    UpdateCake
)
from guara import application, it

brain = application.Application()

class CakeShop:
    def addCake(self):
        try:
            cake_id = int(input("Enter cake id: "))
            flavor = input("Enter cake flavor: ")
            size = input("Enter cake size: ")
            quantity = int(input("Number of Quantity: "))
            price = float(input("Enter cake price: "))
            CAKE_info = cake.Cake(cake_id, flavor, size, quantity, price)
            (
                brain.given(CakeValuesAreValid, cake=CAKE_info)
                .and_(CakeDoesNotExist, cake_id=CAKE_info.cake_id)
                .when(AddCake, cake=CAKE_info)
                .expects(it.IsTrue)
            )
        except ValueError:
            print("Invalid Input...")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")

    def displayCake(self):
        try:
            with open("cakeData.txt", "r") as fp:
                data = fp.readlines()

            headers = ["Cake ID", "Cake Name", "Size", "Quantity", "Price"]
            table_data = []
            for line in data:
                cake_info = line.strip().split(",")
                if len(cake_info) == 5:  
                    table_data.append(cake_info)
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except FileNotFoundError:
            print("File does not exist....")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")

    def searchByFlavor(self):
        try:
            flavor = input("Enter cake flavor: ")
            with open("cakeData.txt", "r") as fp:
                data = fp.readlines()
            headers = ["Cake ID", "Cake Name", "Size", "Quantity", "Price"]
            table_data = []
            for line in data:
                cake_info = line.strip().split(",")
                if cake_info[1] == flavor:
                    table_data.append(cake_info)
            if table_data:
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print("Cake is not available...")
        except FileNotFoundError:
            print("File doesn't exist......")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")

    def removeById(self):
        try:
            self.displayCake()
            cake_id = int(input("Enter cake id: "))
            (
                brain.given(CakeExists, cake_id=cake_id)
                .when(DeleteCake, cake_id=cake_id)
                .then(it.IsTrue)
            )
        except FileNotFoundError:
            print("An error occurred while deleting the Cake.")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")

    def updateByID(self):
        try:
            self.displayCake()
            cake_id = int(input("Enter cake id: "))
            price = float(input("Enter a new price of Cake: "))
            (
                brain.given(CakeExists, cake_id=cake_id)
                .when(UpdateCake, cake_id=cake_id, price=price)
                .then(it.IsTrue)
            )
        except FileNotFoundError:
            print("An error occurred while updating the Cake.")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")

    def paymentHistory(self):
        try:
            with open("payment_history.txt", "r") as fp:
                data = fp.readlines()
            headers = ["User ID", "Payment Mode", "Total Price"]
            table_data = []
            for line in data:
                bill_info = line.strip().split(",")  
                if len(bill_info) == 3: 
                    table_data.append(bill_info)
            if table_data:
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print("Payment history is empty.")
        except FileNotFoundError:
            print("File does not exist....")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")

def admin_Menu():
    cake_shop = CakeShop()  
    while True:
        logo.logo_icon()
        print("\t\t1.  Add New Cake.")
        print("\t\t2.  Display All Cakes.")
        print("\t\t3.  Search Cake By Flavor.")
        print("\t\t4.  Remove Cake.")  
        print("\t\t5.  Update Cake Price.")
        print("\t\t6.  View Payment History.")
        print("\t\t7.  Add Admin.")
        print("\t\t8.  Display Admin.")
        print("\t\t9.  Remove Admin.")
        print("\t\t10. Add User.")
        print("\t\t11. Display Users.")
        print("\t\t12. Remove User.")
        print("\t\t13. Exit.")
        try:
            choice = int(input("Enter your Choice (1 to 13): "))
        except ValueError:
            print("Invalid Input...")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")
        else:
            if choice == 1:
                cake_shop.addCake()  
            elif choice == 2:
                cake_shop.displayCake() 
            elif choice == 3:
                cake_shop.searchByFlavor()
            elif choice == 4:
                cake_shop.removeById()
            elif choice == 5:
                cake_shop.updateByID()
            elif choice==6:
                cake_shop.paymentHistory()
            elif choice == 7:
                AdminLogin.addAdmin()
            elif choice == 8:
                AdminLogin.displayAdmin()
            elif choice == 9:
                AdminLogin.removeAdmin()
            elif choice == 10:
                UserLogin.addUser()
            elif choice==11:
                UserLogin.displayUsers()
            elif choice == 12:
                UserLogin.removeUser()
            elif choice == 13:
                print("\nThank You.\n")
                break