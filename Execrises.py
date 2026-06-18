#Execrise1
check_number = lambda x: "Even" if x %2 ==0 else "odd"
number = int(input("Enter the number:"))
print("Exe1:", check_number(number))
#Execrise2
fruits = ['Cherry','Date','Apple','Mango','DragonFruit']
fruits.sort(key = lambda x: len(x))
print("Exe2:", fruits)
#Excerise3
def fibonacci (n):
    if n<=1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
for i in range(10):
    print("Exe3:", fibonacci(i), end="")