'''
Specification of Trivium
    Register Length     Feedback Bit        Feedforward Bit     AND inputs
A       93                  69                  66                91,92
B       84                  78                  69                82,83
C       111                 87                  66               109,110

#Input of each register
Cn+1 xor 69 -> A0
An+1 xor 78 -> B0
Bn+1 xor 87 -> C0

#Output of each register
An xor(91 and 92) xor 66 -> An+1
Bn xor(82 and 83) xor 69 -> Bn+1
Cn xor(109 and 110) xor 66 -> Cn+1

#Key stream generation
An+1 xor Bn+1 xor Cn+1 -> Si

'''

if __name__ == '__main__':
    print("Hello Triviumm")