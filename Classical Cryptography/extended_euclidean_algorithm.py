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