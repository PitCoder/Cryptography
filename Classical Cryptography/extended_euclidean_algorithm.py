'''
Definition of equations

r = remainder
q = quotient
s = coefficient of a
t = coefficient of b

We represent the calculation of the greatest common divisor as a linear combination
ri = gcd(a,b) = si*a + ti*b = sa + tb

Therefore:
ri-2 = si-2*a + ti-2*b - Equation 1
ri-1 = si-1*a + ti-1*b - Equation 2

Given that a = bq + r, where a = ri-2, b= ri-1
ri-2 = qi-1 * ri-1 + ri
ri = ri-2 - qi-1 * ri-1 - Equation 3

Substituting Eq 1 and Eq 2 on Eq 3
ri = si-2*a + ti-2*b - qi-1 * [si-1*a + ti-1*b ]
ri = [si-2 - qi-1 * si-1]a + [ti-2 - qi-1 * ti-1]b - Equation 4

Where
si = [si-2 - qi-1 * si-1]
ti = [ti-2 - qi-1 * ti-1]

This recursive formula only makes sense when i>=2, thus, the initial values for s0, s1, t0, t1 are trivial:

s0 = 1, t0 = 0
s1 = 0, t1 = 1

Because the gcd(a,1) is 1, therefore s0 = 1 and gdc(a,a) if a, therefore t1 = 1
'''


def eea(r0, r1):
    #Initialization  of coeficients
    s0 = 1; t0 = 0;
    s1 = 0; t1 = 1;

    while r1 != 0:
        temp_r = r1
        r1 = r0 % temp_r
        q = int((r0 - r1) / temp_r)

        temp_s = s1
        s1 = s0 - (q * temp_s)

        temp_t = t1
        t1 = t0 - (q * temp_t)

        #Update of new values
        t0 = temp_t; s0 = temp_s; r0 = temp_r

    return r0, s0, t0


if __name__ == '__main__':
    a, b = str(input("Inserte los valores (a,b): ").replace(" ","")).split(",")
    print("Valor de a: ", a)
    print("Valor de b:", b)

    #Calculando el eea
    gcd, s, t = eea(int(a), int(b))

    #Imprimiendo el resultado
    print("gcd(", a, ",", b, "): ", gcd)
    print("coefficient s: ", s)
    print("coefficient t: ", t)

    #Inverso multiplicativo
    if t >= 0 :
        print("inverse multiplicative: ", t)
    else:
        print("inverse multiplicative: ", int(a) + t)