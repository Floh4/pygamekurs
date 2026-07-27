import random
random_number = random.randint(1, 4)
# Schau mit match, ob random_number 1, 2, 3 oder 4 ist und schreibe dementsprechent etwas ins Terminal

# * Lösungen

match random_number:
    case 1:
        print("Hallo, die nummer ist:", random_number)
    case 2:
        print("Hallo, die nummer ist:", random_number)
    case 3:
        print("Hallo, die nummer ist:", random_number)
    case 4:
        print("Hallo, die nummer ist:", random_number)