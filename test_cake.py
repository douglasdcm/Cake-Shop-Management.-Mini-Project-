from AdminMenu import CakeShop
from UserMenu import cakeShopUser

# Added just to make the tests easier 
def test_cake():
    cake = CakeShop()
    assert cake.addCake() is None

# Added just to make the tests easier 
def test_cart():
    cake = cakeShopUser()
    assert cake.Add_cart(None) is None