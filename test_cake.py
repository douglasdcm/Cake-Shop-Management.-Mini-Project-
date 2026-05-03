from AdminMenu import CakeShop

# Added just to make the tests easier 
def test_cake():
    cake = CakeShop()
    assert cake.addCake() is None