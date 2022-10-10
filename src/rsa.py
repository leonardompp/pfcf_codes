import argparse
import re
from Crypto.Util import number
import math
import textwrap


def gcdExtended(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1

    r, s1, t1 = gcdExtended(b % a, a)

    # Update x and y using results of recursive
    # call
    s = t1 - (b // a) * s1
    t = s1

    return r, s, t

def encode_text_to_int(text):
    # Default encoding is UTF-8
    int_text  = int.from_bytes(text.encode(), byteorder='big')
    return int_text

def decode_int_to_text(decimal_number):
    byte_length = math.ceil(decimal_number.bit_length() / 8)
    # Default encoding is UTF-8
    return decimal_number.to_bytes(byte_length, byteorder='big').decode()

def main(plaintext):

    # KEY GENERATION
    print("KEY GENERATION PHASE")
    # 1)
    # Using RSA with 1024 bit primes
    p = number.getPrime(1024)
    q = number.getPrime(1024)
    N = p*q
    print(f"""
        1) Alice generates a pair of two large integers p and q:
        p = {p}
        q = {q}
        Alice then calculates N = p x q:
        N = {N}
        """)
    # 2)
    phi = (p-1)*(q-1)
    print(f"""
        2) Alice calculates phi(N) = (p-1)x(q-1):
        phi(N) = {phi}
        """)
    # 3)
    # Constant prime number chosen for simplicity. Doesn't cause problems
    a = 65537
    print(f"""
        3) Alice calculates a such that gcd(a, phi(N)) = 1:
        a              = {a}
        gcd(a, phi(N)) = {math.gcd(a, phi)}
        """)
    # 4)
    _, b, _ = gcdExtended(a, phi)
    print(f"""
        4) Alice calculates b such that a x b congruent 1 (mod phi(N)):
        b                  = {b}
        (a x b) mod phi(N) = {(a*b)%phi}
        """)

    # 5)
    print(f"""
        5) Alice sends values (N, a) over the network and saves (p, q, b) for herself
        """)

    # MESSAGE EXCHANGE
    print("MESSAGE EXCHANGE PHASE")
    # 6)
    print(f"""
        6) Bob gets (N, a) and can now construct ring (Z_N, oplus, otimes), upon which he will build his algebra 
        """)

    # 7)
    int_plaintext = encode_text_to_int(plaintext)
    print(f"""
        7) Bob encodes his message to a number x in Z_N using some encoding scheme (UTF-8 here):
        Bob's message       = {plaintext}
        Encoded plaintext x = {int_plaintext}
        In Z_N?             = {int_plaintext < N}
        """)

    # 8)
    int_ciphertext = pow(int_plaintext, a, N)
    print(f"""
        8) Bob calculates ciphertext y in Z_N by taking y = x^a:
        Encoded ciphertext y = {int_ciphertext}
        """)

    # 9)
    print(f"""
        9) Bob sends y over the network to Alice
        """)

    # 10)
    int_plaintext_line = pow(int_ciphertext, b, N)
    print(f"""
        10) Alice receives y and calculates x' = y^b:
        Encoded plaintext x' = {int_plaintext_line}
        """)

    # 11)
    plaintext_line = decode_int_to_text(int_plaintext_line)
    print(f"""
        10) Alice decodes her plaintext using the same encoding scheme (UTF-8 here):
        Alice's message = {plaintext_line}
        Equal to Bob's  = {plaintext_line == plaintext}
        """)






if __name__ == "__main__":
    # Script instruction
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
        """
        This script implements the RSA cryptosystem in order to exemplify its operation \n
        The procedures here should be used for illustration purposes only \n
        ** THIS IS NOT A SECURE IMPLEMENTATION OF RSA ** \n
        """),
        epilog=textwrap.dedent(
        """
        Example usage: python src/rsa.py attack at dawn
        """),
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('message', nargs='*', default='', type=str, help='The message to be transmitted. Only a-zA-Z0-9 characters allowed')
    args = parser.parse_args()
    message = args.message

    # Remove non-alphanum and join with spaces for the code
    filtered = [re.sub('[^A-Za-z0-9]+', '', part) for part in message]
    # Remove all '' elements from list. Avoids growing list needlessly
    filtered = list(filter(lambda a: a != '', filtered))
    message_sent = str.join(" ",filtered)
    # Call the RSA
    main(message_sent)

