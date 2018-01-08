import sys
import math
import random
# For efficient modular inverse
import gmpy2 as gmpy

class RSA:
    
    alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜabcdefghijklmnopqrstuvwxyzäöü1234567890!\"§$%&/()[]={}?\\`´*+~#'-_.:,;<>"

    # Initialize all instance variables
    def __init__(self, length=5):
        print("Generating primes...")
        self.p = self.random_prime(length)
        self.q = self.random_prime(length)
        print("Calculating n...")
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.choose_e(self.phi)
        print("Finding inverse...")
        self.d = int(gmpy.invert(self.e, self.phi))
        print("Done!")

    # Very simple and inefficient primality test
    def is_prime(self,number):
        for i in range(2, math.ceil(math.sqrt(number)) + 1):
            if number % i == 0:
                return False
        return True
   
    # Generates random prime number of the desired length inefficiently
    def random_prime(self, length=5):
        i = random.randint(10**length, 10**(length+1))
        while not self.is_prime(i):
            i = random.randint(10**(length-1), 10**length)
        return i
   
    # Chooses either 65537 or 17 for e with given phi
    def choose_e(self, phi):
        if phi > 65537 and math.gcd(phi, 65537) == 1:
            return 65537
        elif phi > 17 and math.gcd(phi, 17) == 1:
            return 17
        else:
            raise Error("Invalid phi for this implementation")

    # Decrypts number
    def decrypt_num(self, num):
        return pow(num, self.d, self.n)
    
    # Encrypts number
    def encrypt_num(self, num):
        return pow(num, self.e, self.n)

    def encrypt(self, text):
        nums = self.to_nums(text)

        encrypted = []
        for i in nums:
            encrypted.append(self.encrypt_num(i))
        return encrypted

    def decrypt(self, nums):
        decrypted = []
        for i in nums:
            decrypted.append(self.decrypt_num(i))
        return self.to_string(decrypted)

    def to_string(self, nums):
        length = math.floor(math.log(self.n, 10))    # Find length of public N
        nums_per_block = length // 2                # Every character takes up two digits
        string = ""
        for i in nums:

            temp = ""
            next = i
            for j in range(nums_per_block):
                num = next % 100
                temp += self.alphabet[num]
                next = (next - num) // 100
            string += temp[::-1]
        return string

    
    # Converts a string to a list of numbers with a block length smaller than N
    # Note: Alphabet length currently hardcoded to 2
    def to_nums(self, string):
        length = math.floor(math.log(self.n, 10))    # Find length of public N
        nums_per_block = length // 2                # Every character takes up two digits
        blocks = []
        j = 0
        currentBlock = 0
        for i in string:
            # Shift block to the left and add new number
            currentBlock = currentBlock * 100 + self.alphabet.index(i)
            j += 1
            # Finished block creation, appending it to the list
            if j == nums_per_block:
                blocks.append(currentBlock)
                j = 0
                currentBlock = 0
        while j < nums_per_block and j != 0:
            currentBlock = currentBlock * 100 + 0
            j += 1
            if j == nums_per_block:
                blocks.append(currentBlock)
        return blocks

    # Returns string representation of instance
    def __str__(self):
        result = ""
        result += "p\t" + str(self.p) + "\n"
        result += "q\t" + str(self.q) + "\n"
        result += "n\t" + str(self.n) + "\n"
        result += "phi\t" + str(self.phi) + "\n"
        result += "d(priv)\t" + str(self.e) + "\n"
        result += "e(pub)\t" + str(self.d) + "\n"
        return result


if __name__ == "__main__":
    # Use given argument as prime length, if available
    if len(sys.argv) > 1:
        length = int(sys.argv[1])
    else:
        length = 5

    text = input("What would you like to encrypt? ") 
    
    rsa = RSA(length)

    # Encrypt number
    enc = rsa.encrypt(text)
    print("Encrypted:", enc)
    dec = rsa.decrypt(enc)
    print(dec)
    print(rsa)

