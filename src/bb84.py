import argparse
import random
import textwrap

def main(key_size):
    # Definitions
    computational_basis = ['|0>', '|1>']
    hadamard_basis = ['|+>', '|->']

    # Alice
    key = []
    base = []
    states = []
    for i in range(key_size):
        key.append(random.randint(0, 1))
        base.append(random.randint(0, 1))
        if base[i] == 0:
            choices = computational_basis
        else:
            choices = hadamard_basis
        states.append(choices[key[i]])

    # Bob
    base_line = []
    key_line = []
    for i in range(key_size):
        base_line.append(random.randint(0, 1))
        if base_line[i] == 0:
            if states[i] in computational_basis:
                key_line.append(computational_basis.index(states[i]))
            else:
                key_line.append(random.randint(0, 1))
        else:
            if states[i] in hadamard_basis:
                key_line.append(hadamard_basis.index(states[i]))
            else:
                key_line.append(random.randint(0, 1))

    # Key comparison
    red_key = []
    red_key_line = []
    for i in range(key_size):
        if base[i] == base_line[i]:
            red_key.append(key[i])
            red_key_line.append(key_line[i])
        else:
            red_key.append('_')
            red_key_line.append('_')


    # Show results
    print(f"Alice generated key        : {''.join([str(x) for x in key])}")
    print(f"Alice generated base       : {''.join([str(x) for x in base])}")
    print(f"Alice encoded key in states: {''.join([str(x) for x in states])}")
    print(f"Bob generated base'        : {''.join([str(x) for x in base_line])}")
    print(f"Bob decoded key'           : {''.join([str(x) for x in key_line])}")
    print(f"================ Comparing bits of base and base' ================")
    print(f"Alice gets reduced key     : {''.join([str(x) for x in red_key])}")
    print(f"Bob gets reduced key'      : {''.join([str(x) for x in red_key_line])}")





if __name__ == "__main__":
    # Script instruction
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
        """
        This script implements the BB-84 protocol in order to exemplify its operation \n
        The procedures here should be used for illustration purposes only \n
        ** THIS IS NOT A SECURE IMPLEMENTATION OF BB-84 ** \n
        """),
        epilog=textwrap.dedent(
        """
        Example usage: python src/bb84.py -n 10
        """),
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-n', nargs=1, type=int, help='Number of bits in the key-string to be transmitted', required=True)
    args = parser.parse_args()
    n = abs(args.n[0])

    # Call the BB84
    main(n)