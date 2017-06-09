# -*- coding: utf-8 -*-


multiplier = 25214903917  # 0x5DEECE66DL
addend = 11  # 0xBL
precision_mask = 2 ** 48 - 1
int32_mask = 2 ** 32 - 1


def next_seed(seed):
    """ Returns a 48 bit seed number to be used in the data generation. """
    # (seed * 0x5DEECE66DL + 0xBL) & ((1L << 48) - 1)
    return (seed * multiplier + addend) & precision_mask


def next_int(seed, bits=32):
    """ Uses at most 32 bits out of the seed's higher bits to create a random integer. """
    bits = max(1, min(bits, 32))

    # (int)(seed >>> (48 - bits)).
    shift = (48 - bits) & int32_mask
    return seed >> shift


def find_seed(first, second):
    """ Brute force the seed from the generated sequence `first` and `second`. """

    seed_higher_bits = first << 16
    for lower_hexted in range(2 ** 16 - 1):
        guess = seed_higher_bits + lower_hexted

        if next_int(next_seed(guess)) == second:
            return guess


def previous_seed(seed):
    """ Compute the previous seed based on the current one, used to rework the
    all the history from the brute forced seed.
    """
    assert multiplier & 1, 'last bit of the multiplier must be set'
    previous_seed = 0

    seed -= addend
    seed += 2 ** 96  # add a really high bit to avoid negative numbers
    for bit_position in range(48):
        bit = seed & (1 << bit_position)
        if bit:
            previous_seed += bit
            seed -= multiplier << bit_position

    return previous_seed


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('seed', type=int)
    args = parser.parse_args()
    seed = args.seed

    first = next_int(seed)
    seed = next_seed(seed)
    second = next_int(seed)

    print(find_seed(first, second))


if __name__ == '__main__':
    main()
