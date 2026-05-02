from guara import abstract_transaction

import cake


class TransactionException(Exception):
    pass

# Preconditions
class CakeExists(abstract_transaction.AbstractTransaction):
    def do(self, cake_id):
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.split(",")
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
        SIZES = ["s", "m", "l"]
        assert isinstance(cake.cake_id, int), "Cake id should be an integer"
        assert isinstance(cake.flavor, str), "Cake flavor should be a string"
        assert len(cake.flavor) < 25, f"Cake flavor should have less than {MAX_NAME}"
        assert isinstance(cake.price, float), "Cake price should be a float"
        assert isinstance(cake.quantity, int), "Cake quantity should be an integer"
        assert isinstance(cake.flavor, str), "Cake flavor should be a string"
        assert cake.size.lower() in SIZES, f"Cake size should be one of {SIZES}"

class HasEnoughCake(abstract_transaction.AbstractTransaction):
    def do(self, cake_id, quantity):
        with open("cakeData.txt", "r") as fp:
            data = fp.readlines()
        for line in data:
            cake_info = line.strip().split(",")
            if cake_info[0] == str(cake_id):
                available_quantity = int(cake_info[3])
                if available_quantity >= quantity:
                    raise TransactionException("Not enough quantity available for this cake.")


# Actions
class AddCake(abstract_transaction.AbstractTransaction):
    def do(self, cake: cake.Cake):
        with open("cakeData.txt", "a") as fp:
            data = f"{cake.cake_id},{cake.flavor},{cake.size},{cake.quantity},{cake.price:.2f}"
            fp.write(data)
            fp.write("\n")
        return True

class DeleteCake(abstract_transaction.AbstractTransaction):
    def do(self, cake_id):
        allCakes = []
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.split(",")
                if data[0] == str(cake_id):
                    print("Cake with ID {} has been deleted.".format(cake_id))
                else:
                    allCakes.append(line)
        with open("cakeData.txt", "w") as fp:
            fp.write("".join(allCakes))
        return True

class UpdateCake(abstract_transaction.AbstractTransaction):
    def do(self, cake_id, price):
        allcake = []
        with open("cakeData.txt", "r+") as fp:
            for line in fp:
                data = line.split(",")
                if data[0] == str(cake_id):
                    data[4] = f"{price:.2f}"
                allcake.append(",".join(data))
        with open("cakeData.txt", "w") as fp:
            fp.write("\n".join(allcake))
        return True

class AddToCart(abstract_transaction.AbstractTransaction):
    def do(self, cake: cake.Cake):
        total_price = 0
        with open("add_to_cart_data.txt", "a") as cart_file:
            cart_item = [str(cake.cake_id), cake.flavor, cake.size, cake.quantity, f"{total_price:.2f}"]
            cart_file.write(",".join(cart_item))
            cart_file.write("\n")
