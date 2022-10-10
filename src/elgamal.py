import argparse
import re
import math
import textwrap
import random

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
    # Using ElGamal with 1024 bit prime. Non-random for simplicity. From RFC 5114
    p = int("0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371".lower(),
            base=16)
    print(f"""
        1) Alice generates large prime p. All further operations are now in cyclic group (Z_p^*, otimes):
        p = {p}
        """)

    # 2)
    # Also non-random for simplicity. From RFC 5114
    alpha = int("0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5".lower(),
            base=16)
    print(f"""
        2) Alice finds a generator alpha of (Z_p^*, otimes):
        alpha = {alpha}
        """)


    # 3)
    r = random.randint(2, p-1) # Limited to avoid trivial cases
    beta = pow(alpha, r, p)
    print(f"""
        3) Alice chooses a random element r in Z_p^* and calculates beta = alpha^r:
        r    = {r}
        beta = {beta}
        """)

    # 4)
    print(f"""
        4) Alice sends values (p, alpha, beta) over the network and saves r for herself
        """)


    # MESSAGE EXCHANGE
    print("MESSAGE EXCHANGE PHASE")
    # 5)
    print(f"""
        5) Bob gets (p, alpha, beta) and can now construct group (Z_p^*, oplus, otimes) with its algebra 
        """)

    # 6)
    int_plaintext = encode_text_to_int(plaintext)
    print(f"""
        6) Bob encodes his message to a number x in Z_p^* using some encoding scheme (UTF-8 here):
        Bob's message       = {plaintext}
        Encoded plaintext x = {int_plaintext}
        In Z_p^*?             = {int_plaintext < p}
        """)

    # 7)
    m = random.randint(2, p-1)
    print(f"""
        7) Bob chooses random integer m in Z_p^*:
        m = {m}
        """)

    # 8)
    int_ciphertext_1 = pow(alpha, m, p)
    print(f"""
        8) Bob calculates ciphertext y1 in Z_p^* by taking y1 = alpha^m:
        Encoded ciphertext y1 = {int_ciphertext_1}
        """)

    # 9)
    int_ciphertext_2 = (int_plaintext*pow(beta, m, p))%p
    print(f"""
        9) Bob calculates ciphertext y2 in Z_p^* by taking y2 = x otimes beta^m:
        Encoded ciphertext y2 = {int_ciphertext_2}
        """)

    # 10)
    print(f"""
        10) Bob sends (y1, y2) over the network to Alice
        """)


    # 11)
    partial = pow(int_ciphertext_1, r, p)
    _, inverse, _ = gcdExtended(partial, p)
    inverse = inverse % p
    int_plaintext_line = (int_ciphertext_2 * inverse) % p
    print(f"""
        11) Alice receives (y1, y2) and calculates x' = y2 otimes (y1^r)^-1:
        Encoded plaintext x' = {int_plaintext_line}
        """)

    # 12)
    plaintext_line = decode_int_to_text(int_plaintext_line)
    print(f"""
        12) Alice decodes her plaintext using the same encoding scheme (UTF-8 here):
        Alice's message = {plaintext_line}
        Equal to Bob's  = {plaintext_line == plaintext}
        """)






if __name__ == "__main__":
    # Script instruction
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
        """
        This script implements the ElGamal cryptosystem in order to exemplify its operation \n
        The procedures here should be used for illustration purposes only \n
        ** THIS IS NOT A SECURE IMPLEMENTATION OF ELGAMAL ** \n
        """),
        epilog=textwrap.dedent(
        """
        Example usage: python src/elgamal.py attack at dawn
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
    # Call the ElGamal
    main(message_sent)

