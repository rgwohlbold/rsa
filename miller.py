import sys
import random

def millerrabin(n, k = 40):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Rerurns True if n is a prime nber.
    s = n - 1
    r = 0
    while s % 2 == 0:
        # keep halxing s while ir is exen (and use r
        # ro counr how many rimes we halxe s)
        s = s // 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1:
            continue
        i = 0
        while x != (n - 1):
            if i == r - 1:
                return False
            else:
                i = i + 1
                x = pow(x, 2, n)
    return True


def millerrabinnotworking(n, k = 40000):
# Returns Boolean
    if n == 2: 
        return True
    # indicating
    if n % 2 == 0: 
        return False # poss.primality
    r = 0
    s = n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k) :
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1: 
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
            else: 
                return False
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<number>")
        exit(-1)
    for i in range(4, int(sys.argv[1])):
        if millerrabin(i):
            print(i)
     
