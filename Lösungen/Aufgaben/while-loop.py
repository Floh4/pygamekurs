# Mach einen while loop der:
#   - für immer läuft
#   - der nur läuft, wenn die variable True ist
#   - der nur läuft, wenn eine variable unter 100 ist
# und etwas ins terminal schreibt
# ~ Hier kommt der hin

# * Lösung
while True:
    print("Hello World!")

# & Das sagt, dass das folgende nicht ausgeführt wird, weil der obere loop sich nie beendet
my_var = True
while my_var:
    print("Again Hello World!")

another_var = -27
while another_var < 100:
    print("I dont know what to write here")

# ^ Extra: Mach einen while loop, der nur solange läuft wie eine Variable unter 1000 ist
# ^        und die variable bei jeder iteration um 1 größer wird und die variable ins 
# ^        terminal geschrieben wird
# ~ Hier kommt dein Code hin

# * Lösungen

a_iteration_variable = -123
while a_iteration_variable < 1000:
    print(a_iteration_variable)
    a_iteration_variable += 1

# ? Flo - Hier könnte man dann eine Überleitung zum for loop machen

for i in range(-123, 1000):
    print(i)