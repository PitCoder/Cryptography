from math import gcd

def phi(n):
    phi_values = [1]
    for p in range(2, n):
        if gcd(p, n) == 1:
            phi_values.append(p)
    return phi_values

if __name__ == '__main__':
    n = int(input("Insert an integer n: "))
    #Then we calculate its relative prime factors
    prime_factors = phi(n)
    print("Prime factors of n: ", prime_factors)

    #We start the constrution of the multiplication table for Zn

    mul_table = []

    #Naive implementation for the construction of the multiplication table
    for i in range(len(prime_factors)):
        a = prime_factors[i]
        table_row = []
        for j in range(len(prime_factors)):
            b = prime_factors[j]
            mul_ab = (a * b) % n
            table_row.append(mul_ab)
        mul_table.append(table_row)

    #Finally we print the result table
    print("Z",n, " multplication table:")
    for row in mul_table:
        print(row)