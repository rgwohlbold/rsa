def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a

def extended(a,b):
    alpha,s,beta,t = 1,0,0,1
    while b != 0:
        q = a // b
        a, b = b, a % b
        alpha, s = s, alpha - q * s
        beta, t = t, beta - q * t
    return (a, alpha, beta)

p = 13
q = 17
n = p * q
phi = (p-1) * (q - 1)
d = 17
print("gcd(d,phi)", gcd(phi, d))
alpha = extended(d, phi)[1]
one = alpha * d % phi
print(one)
print("modular inverse to d mod phi", alpha)
