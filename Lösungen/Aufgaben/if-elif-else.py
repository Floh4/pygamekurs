# Mach eine Variable mit den Wert 5. Dann schau ob die Variable:
#   - unter 0 ist
#   - 0 ist
#   - über 0 ist
# ~ Hier kommt der Code hin

# * Lösungen

my_var = 5
if my_var < 0:
    print("es ist negativ!")
elif my_var == 0:
    print("es ist null")
elif my_var > 0:
    print("es ist positiv")
else:
    print("es ist weder positiv, noch negativ, noch null")