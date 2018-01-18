#!/usr/bin/python3
import sys
import random
import math


def sieve(n):
    # Every number is assumed prime except 0 and 1
    numbers = [False, False] + [True] * (n-2)
    print("Numbers appended")
    for i in range(int(math.sqrt(n))+1):
        if not numbers[i]:
            continue                    # Do not do anything if i is not prime
        for j in range(i**2, n, i):
            numbers[j] = False          # Mark every multiple as not prime
    print("Filter finished")
    res = []
    for i in range(n):
        if numbers[i]:
            res.append(i)
    return res


def main(length):
    primes = sieve(10**(length + 1))
    print("Finished generating")
    num = random.choice(primes)
    while num < 10**length:
        num = random.choice(primes)
    print(num)
    

main(7)

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         length = int(sys.argv[1])
#     else:
#         length = 5
#     main(length)
