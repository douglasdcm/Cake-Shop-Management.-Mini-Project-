from AdminMenu import CakeShop
from UserMenu import cakeShopUser


def test_cake():
    cake = cakeShopUser()
    cake = CakeShop()
    # assert cake.Add_cart(None) == 42
    assert cake.addCake() == 42