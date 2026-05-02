from AdminMenu import CakeShop
from UserMenu import cakeShopUser


def test_cake():
    cake = cakeShopUser()
    assert cake.Add_cart() == 42