from tabulate import tabulate
from cake import Cake
import logo
from guara import application, it

from transactions import AddToCart, CakeExists, CakeValuesAreValid, HasEnoughCake

brain = application.Application()

class cakeShopUser:
   
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
    
    def Add_cart(self, user_id):
        while True:
            self.displayCake()
            try:
                cake_id = int(input("Enter cake id: "))
                quantity = int(input("Number of Quantity: "))
                cake_ = Cake(cake_id=cake_id, flavor="", size="s", quantity=quantity, price=0)
                (
                    brain.given(CakeExists, cake_id=cake_id)
                    .and_(CakeValuesAreValid, cake=cake_)
                    .and_(HasEnoughCake, cake_id=cake_.cake_id, quantity=cake_.quantity)
                    .when(AddToCart,cake=cake_)
                )
            except Exception as e:
                print("An error occurred:", e)
            add_cake = input("Do you want to add more cake (y or n)? ").lower()
            if add_cake != "y":
                break

    def edit_cart(self, user_id):
        try:
            with open("add_to_cart_data.txt", "r") as cart_file:
                data = cart_file.readlines()

            headers = ["Cake ID", "Cake Name", "Size", "Price", "Quantity", "Total Price"]
            table_data = []
            updated_cart_data = []  

            for line in data:
                cart_item = line.strip().split(",")
                table_data.append(cart_item)

            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            cake_id_to_edit = input("Enter the Cake ID to edit the quantity: ")
            new_quantity = int(input("Enter the new quantity: "))

            for cart_item in table_data:
                if cart_item[0] == cake_id_to_edit:
                    old_quantity = int(cart_item[3])
                    cart_item[3] = str(new_quantity)
                    new_total_price = float(cart_item[2]) * new_quantity  
                    cart_item[4] = f"{new_total_price:.2f}"
                updated_cart_data.append(",".join(cart_item))

            with open("add_to_cart_data.txt", "w") as cart_file:
                cart_file.write("\n".join(updated_cart_data))

            with open("cakeData.txt", "r") as cake_file:
                cake_data = cake_file.readlines()

            updated_cake_data = []
            for line in cake_data:
                cake_info = line.strip().split(",")
                if cake_info[0] == cake_id_to_edit:
                    available_quantity = int(cake_info[3]) + old_quantity - new_quantity
                    cake_info[3] = str(available_quantity)
                updated_cake_data.append(",".join(cake_info))

            with open("cakeData.txt", "w") as cake_file:
                cake_file.write("\n".join(updated_cake_data))

            print("Cart item updated successfully.")

        except FileNotFoundError:
            print("Cart is empty.")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found...")

    def getBill(self, user_id):
        try:
            with open("add_to_cart_data.txt", "r") as cart_file:
                data = cart_file.readlines()

            headers = ["Cake ID", "Cake Name", "Size", "Quantity", "Price"]
            table_data = []
            total_price = 0.0
            for line in data:
                cart_item = line.strip().split(",")
                total_price += float(cart_item[-1])
                table_data.append(cart_item)
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print("\t\t\t\t\t\t\t Total:", total_price)
            print("\t\t\t\t\t\t\t\b18% GST:", total_price * 0.18)
            print("\t\t\t\t\t\tPayable Amount:", total_price + (total_price * 0.18))
        except FileNotFoundError:
            print("Cart is empty.")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found...")
        else:
            try:
                payment_mode = int(input("What is your Payment Mode\n1. Cash\n2. Online or Card\nEnter 1 or 2: "))
            except ValueError:
                print("Invalid Inputs...")
            except:
                print("Error 404: Error Not Found...")
            else:
                if payment_mode == 1:
                    payment_type = "Cash"
                elif payment_mode == 2:
                    payment_type = "Online or Card"
                else:
                    print("Wrong Input.")
                    return 

                with open("add_to_cart_data.txt", "w") as cart_file:
                    cart_file.truncate(0)  

                data = f"{user_id},{payment_type},{total_price + (total_price * 0.18)}"
                with open("payment_history.txt", "a") as fp:
                    fp.write(data)
                    fp.write("\n")

def user_Menu(user_id): 
    cake_shop_user = cakeShopUser()  
    while True:
        logo.logo_icon()
        print("\t\t1. Display All Cakes.")
        print("\t\t2. Search Cake By Flavor.")
        print("\t\t3. Add to Cart.")
        print("\t\t4. Edit Cart.")
        print("\t\t5. Get a Bill.")
        print("\t\t6. Exit to Main Menu.")  
        try:
            choice = int(input("Enter your Choice (1 to 6): "))
        except ValueError:
            print("Invalid Input...")
        except Exception as e:
            print("An error occurred:", e)
        except:
            print("Error 404: Error Not Found.")
        else:
            if choice == 1:
                cake_shop_user.displayCake()
            elif choice == 2:
                cake_shop_user.searchByFlavor()
            elif choice == 3:
                cake_shop_user.Add_cart(user_id)
            elif choice == 4:
                cake_shop_user.edit_cart(user_id)
            elif choice == 5:
                cake_shop_user.getBill(user_id)
            elif choice == 6:
                print("\n\t\tThank You for Shopping.\n\t\tVisit Again...!\n")
                break
