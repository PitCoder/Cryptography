#Based on Euler's product formula (Euler's totient function), states that the value of toitent functions is below
#product over all prime factors p of n

#2) Run a loop from 'p' = 2 to sqrt(n), do following for every 'p'.
#     a) If p divides n, then
#           Set: result = result  * (1.0 - (1.0 / (float) p));
#           Divide all occurrences of p in n.

def phi(n):
    phi_values = []
    phi_values.append(1)

    result = n
    p = 2
    while (p * p) <= n:
        if (n % p) == 0:
            while(n % p) == 0:
                n = int(n / p);
            result -= int(result / p);
        p = p + 1

    # If n has a prime factor greater than sqrt(n)
    # (There can be at-most one such prime factor)
    if n > 1:
        result -= int(result / n)
    # 3) Return result
    return result

#Driver code
#1) Initialize : result = n
for n in range(1, 11):
    print("phi(", n, ") = ", phi(n))


