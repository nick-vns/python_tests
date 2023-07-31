number_1 = int(input("Enter first number: "))
number_2 = int(input("Enter second number: "))

sum_sub = input("Would you like to add or subtract? Enter '+' or '-' ")

add = number_1 + number_2
sub = number_1 - number_2

if sum_sub == "-" and sub < 0:
    print("Your result is negative ", sub)
elif sum_sub == "-" and sub >= 0:
    print("Your result is positive ", sub)

elif sum_sub == '+':
    print("Your result is ", add)
else:
    print("Ops, your forgot to specify an action. ")
