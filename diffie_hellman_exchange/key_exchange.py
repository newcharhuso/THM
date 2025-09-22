import random


def isPrime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n % f == 0:
            return False
        if n % (f + 2) == 0:
            return False
        f += 6
    return True


primes = [i for i in range(0, 100) if isPrime(i)]

# A large prime number (small here for the sake of the example)
p = random.choice(primes)
# A large prime number  as generator (small here for the sake of the example)
g = random.choice(primes)

while g > p or g == p:
    g = random.choice(primes)
# random integers for alice and bob
a = random.randint(0, 100)
b = random.randint(0, 100)

A = g**a  # Alice pub key
B = g**b  # Bob pub key

# They send each other their public keys
# Alice to calculate shared secret
shared_secret_a = B**a
shared_secret_a = shared_secret_a % p
print(f"The secret key alice found: {shared_secret_a} ")


# Bob to calculate shared secret
shared_secret_b = A**b
shared_secret_b = shared_secret_b % p
print(f"The secret key bob found: {shared_secret_b} ")

print(shared_secret_a == shared_secret_b)
