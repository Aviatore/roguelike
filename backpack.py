from engine import Weapon, Clothes, Alcohol

#weapons
stick = Weapon("w1", "stick", 10, 2)
empty_bottle = Weapon("w2", "empty bottle", 15, 4)
stone = Weapon("w3", "stone", 20, 8)
baseball = Weapon("w4", "baseball", 40, 30)

#pants
dirty_pants = Clothes("p1", "dirty pants", 1, 1)
short_trousers = Clothes("p2", "short trousers", 5, 10)
ripped_jeans = Clothes("p3", "ripped jeans", 10, 20)
suit_pants = Clothes("p4", "suit pants", 30, 40)

#shoes
sandals = Clothes("s1", "sandals", 5, 10)
sneakers = Clothes("s2", "sneakers", 10, 20)
elegant_shoes = Clothes("s3", "elegant shoes", 20, 40)

#body
old_leaky_t_shirt = Clothes("b1", "old leaky t-shirt", 1, 1)
clean_t_shirt = Clothes("b2", "clean t-shirt", 5, 10)
fake_leather_jacket = Clothes("b3", "fake leather jacket", 10, 20)
old_suit = Clothes("b4", "old suit", 40, 60)

#alco
beer = Alcohol("a1", "beer", 5, 5)
wine = Alcohol("a2", "wine", 12, 10)
small_vodka = Alcohol("a3", "small vodka", 20, 15)
vodka = Alcohol("a4", "vodka", 40, 25)