from math import gcd
#Naive implementation to calculate the relative primes of a given number n

def phi(n):
    result = 1
    phi_values = [1]

    for p in range(2, n):
        if gcd(p, n) == 1:
            result =  result + 1
            phi_values.append(p)

    print(phi_values)
    return result

#Driver to test the function above
for i in range(1, 11):
    print("phi(", i, ") = ", phi(i))