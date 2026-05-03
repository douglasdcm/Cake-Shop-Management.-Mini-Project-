from guara import abstract_transaction

import cake


class TransactionException(Exception):
    pass

# Preconditions
class CakeExists(abstract_transaction.AbstractTransaction):
    def do(self, cake_id):
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.replace("\n", "").split(",")
                if data[0] == str(cake_id):
                    return
        raise TransactionException("Cake not found") 

class CakeDoesNotExist(abstract_transaction.AbstractTransaction):
    def do(self, cake_id):
        try:
            CakeExists().do(cake_id)
        except TransactionException:
            return
        raise TransactionException("Cake already exists")

class CakeValuesAreValid(abstract_transaction.AbstractTransaction):
    def do(self, cake: cake.Cake):
        MAX_NAME = 25
        MIN_QUANTITY = MIN_PRICE = 0
        SIZES = ["s", "m", "l"]
        assert isinstance(cake.cake_id, int), "Cake id should be an integer"
      
        assert isinstance(cake.flavor, str), "Cake flavor should be a string"
        assert len(cake.flavor) < 25, f"Cake flavor should have less than {MAX_NAME}"
      
        assert isinstance(cake.price, float), "Cake price should be a float"
        assert cake.price > 0, f"Cake price should higher than {MIN_PRICE}"
      
        assert isinstance(cake.quantity, int), "Cake quantity should be an integer"
        assert cake.quantity > 0, f"Cake quantity should be higher than {MIN_QUANTITY}"
      
        assert cake.size.lower() in SIZES, f"Cake size should be one of {SIZES}"

class CartValuesAreValid(abstract_transaction.AbstractTransaction):
    def do(self, cake_id, quantity):
        MIN_QUANTITY = 0
        assert isinstance(cake_id, int), "Cake id should be an integer"

        assert isinstance(quantity, int), "Cake quantity should be an integer"
        assert quantity > 0, f"Cake quantity should be higher than {MIN_QUANTITY}"

class HasEnoughCake(abstract_transaction.AbstractTransaction):
    def do(self, cake_id, quantity):
        with open("cakeData.txt", "r") as fp:
            data = fp.readlines()
        for line in data:
            cake_info = line.strip().split(",")
            if cake_info[0] == str(cake_id):
                available_quantity = int(cake_info[3])
                if available_quantity < quantity:
                    raise TransactionException("Not enough quantity available for this cake.")
                return


# Actions
class AddCake(abstract_transaction.AbstractTransaction):
    def do(self, cake: cake.Cake):
        with open("cakeData.txt", "a") as fp:
            data = f"{cake.cake_id},{cake.flavor},{cake.size.upper()},{cake.quantity},{cake.price:.2f}\n"
            fp.write(data)
        return True

class DeleteCake(abstract_transaction.AbstractTransaction):
    def do(self, cake_id):
        allCakes = []
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.replace("\n", "").split(",")
                if data[0] == str(cake_id):
                    print("Cake with ID {} has been deleted.".format(cake_id))
                else:
                    allCakes.append(line)
        with open("cakeData.txt", "w") as fp:
            for cake in allCakes:
                fp.write(f"{cake}\n")
        return True

class UpdateCake(abstract_transaction.AbstractTransaction):
    def do(self, cake_id, price=None, quantity=None):
        allcake = []
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.replace("\n", "").split(",")
                if data[0] == str(cake_id):
                    if price:
                        data[4] = f"{price:.2f}"
                    if quantity:
                        data[3] = f"{quantity}"
                allcake.append(",".join(data))
        with open("cakeData.txt", "w") as fp:
            for item in allcake:
                fp.write(f"{item}\n")
        return True

class UpdateCakeStock(abstract_transaction.AbstractTransaction):
    def do(self, cake_id, quantity, with_operation):
        allcake = []
        assert with_operation.lower() in ["add", "remove"], "Operation in stock should be 'add' or 'remove'"
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.replace("\n", "").split(",")
                if data[0] == str(cake_id):
                    if with_operation == "remove":
                        if quantity:
                            new = int(data[3]) - quantity
                            data[3] = str(new)
                    if with_operation == "add":
                        if quantity:
                            new = int(data[3]) + quantity
                            data[3] = str(new)
                allcake.append(",".join(data))
        with open("cakeData.txt", "w") as fp:
            for item in allcake:
                fp.write(f"{item}\n")
        return True

class AddToCart(abstract_transaction.AbstractTransaction):
    def do(self, cake_id, quantity):
        total_price = 0
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.replace("\n", "").split(",")
                if data[0] == str(cake_id):
                    cake_ = cake.Cake(data[0], data[1], data[2], quantity, float(data[4]))
                    break
        with open("add_to_cart_data.txt", "a") as cart_file:
            total_price = float(cake_.price * cake_.quantity)
            cart_item = f'{str(cake_.cake_id)},{cake_.flavor},{cake_.size},{str(cake_.quantity)},{total_price:.2f}\n'
            cart_file.write(cart_item)
    