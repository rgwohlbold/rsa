import sys
import math
import random

# Class implementing the RSA cryptosystem
# Upon initialization, this randomly generates a RSA key pair
# It provides encrypt(text) and decrypt(num) as its methods designed for external use
class RSA:
    
    # Full alphabet for testing encrypt_to_string and decrypt_from_string
    alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜabcdefghijklmnopqrstuvwxyzäöü1234567890!\"§$%&/()[]={}?\\`´*+~#'-_.:,;<>"

    # Normal alphabet
    #alphabet=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Initialize all instance variables
    def __init__(self, length=5):
        print("Generating primes...")
        self.p = self.random_prime(length)
        self.q = self.random_prime(length)
        print("Calculating n...")
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.d = self.choose_d(self.phi)
        print("Finding inverse...")
        self.e = self.modular_inverse(self.d, self.phi)
        # The number of characters that fit into a block (only if the alphabet size is <=100)
        self.chars_per_block = math.floor(math.log(self.n, 10)) // 2
        # The number of digits that can be encoded. This is one less than the number of digits of n since if it was higher, the program could not guarantee that no block exceeds n
        # The number of digits in an encrypted block is higher since these can have the amount of digits n has, but in a controlled way since the encryption always goes mod n
        self.digits_per_block = math.floor(math.log(self.n, 10))
    

    # Generates random prime number of the desired length inefficiently
    def random_prime(self, length=5):
        i = random.randint(10**length, 10**(length+1))
        while not self.is_prime(i):
            i = random.randint(10**(length-1), 10**length)
        return i

    # Very simple and inefficient primality test
    def is_prime(self,number):
        for i in range(2, math.ceil(math.sqrt(number)) + 1):
            if number % i == 0:
                return False
        return True

    # Calculate modular inverse with Extended Euclidian Algorithm
    def modular_inverse(self, a, b):
        start_b = b
        alpha,s,beta,t = 1,0,0,1
        while b != 0:
            q = a // b
            a, b = b, a % b
            alpha, s = s, alpha - q * s
            #beta, t = t, beta - q * t
        #return (a, alpha, beta)
        return alpha % start_b
   
    # Chooses either 65537 or 17 for d with given phi
    def choose_d(self, phi):
        if phi > 65537 and math.gcd(phi, 65537) == 1:
            return 65537
        elif phi > 17 and math.gcd(phi, 17) == 1:
            return 17
        else:
            raise Error("Invalid phi for this implementation")
   

    # The following encryption and decryption functions are in order of application


    # Splits a string into pieces of length chars_per_block
    def split_string(self, string):
        blocks = []
        for i in range(0, len(string), self.chars_per_block):
            blocks.append(string[i:i+self.chars_per_block])
        return blocks

    # Converts a string into a number
    def string_to_number(self, string):
        result = 0
        for i in string:
            result = result * 100 + self.alphabet.index(i)
        return result
    
    # Encrypts a list of blocks and returns a list of encrypted blocks
    def encrypt_blocks(self, blocks):
        encrypted = []
        for block in blocks:
            encrypted.append(pow(block, self.d, self.n))
        return encrypted
    
    # Concatenates a list of blocks into a single number
    def concat_blocks(self, blocks):
        number = 0
        for block in blocks:
            number = number * (10 ** (self.digits_per_block + 1)) + block
        return number

    # Splits a number into blocks of length self.digits_per_block + 1
    def split_number(self, number):
        factor = 10 ** (self.digits_per_block + 1)
        blocks = []
        while number != 0:
            blocks.append(number % factor)
            number = number // factor
        return blocks[::-1]

    # Decrypt a list of blocks
    def decrypt_blocks(self, blocks):
        decrypted = []
        for block in blocks:
           decrypted.append(pow(block, self.e, self.n)) 
        return decrypted

    # Convert a number to a string given the defined alphabet
    def number_to_string(self, number):
        string = ""
        while number != 0:
            string += self.alphabet[number % 100]
            number = number // 100
        return string[::-1]

    # Concat a list of strings
    def concat_string(self, strings):
        result = ""
        for string in strings:
            result += string
        return result
        
    # Method to encrypt a piece of text
    def encrypt(self, text):
        split = self.split_string(text)
        blocks = []
        for i in split:
            blocks.append(self.string_to_number(i))
        encrypted = self.encrypt_blocks(blocks)
        return self.concat_blocks(encrypted)
    
    # Encrypt to string. Only works reliably with full alphabet
    def encrypt_to_string(self, text):
        assert(len(self.alphabet) == 100)
        num = self.encrypt(text)
        return self.number_to_string(num)
    
    # Decrypt from string. Only works reliably with full alphabet
    def decrypt_from_string(self, text):
        assert(len(self.alphabet) == 100)
        num = self.string_to_number(text)
        return self.decrypt(num)

    # Method to decrypt a piece of text
    def decrypt(self, number):
        blocks = self.split_number(number)
        decrypted = self.decrypt_blocks(blocks)
        strings = []
        for i in decrypted:
            strings.append(self.number_to_string(i))
        return self.concat_string(strings)

    # Returns string representation of instance
    def __str__(self):
        result = "p\t" + str(self.p) + "\n"
        result += "q\t" + str(self.q) + "\n"
        result += "n\t" + str(self.n) + "\n"
        result += "phi\t" + str(self.phi) + "\n"
        result += "d(pub)\t" + str(self.d) + "\n"
        result += "e(priv)\t" + str(self.e)
        return result

# Main RSA test function
def main(text, length=5):
    rsa = RSA(length)
    print()
    # Encrypt number
    enc = rsa.encrypt_to_string(text)
    print(enc)
    dec = rsa.decrypt_from_string(enc)
    print(dec)
    print()
    print(rsa)

# If rsa.py is executed directly, call main()
if __name__ == "__main__":
    # Use given argument as prime length, if available
    if len(sys.argv) > 1:
        length = int(sys.argv[1])
    else:
        length = 5

    text = input("What would you like to encrypt? ") 
    main(text, length) 
