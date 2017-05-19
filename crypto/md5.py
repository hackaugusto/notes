
HIGH_BIT = 128

# https://tools.ietf.org/html/rfc1321
def md5(message):
    original_message = message

    # convert to integers
    message = list(map(ord, message))

    # step 1: Append Padding Bits
    pad_length = 64 - ((len(original_message) + 8) % 64)
    pad = [HIGH_BIT] + [0] * (pad_length - 1)
    message = message + pad

    # step 2: Append Length
    length = len(original_message)
    len_pad = list()
    while length and len(len_pad) < 8:
        len_pad.append(length % 256)
        length = length >> 8
    message = message + len_pad

    # step 3: Initialize MD Buffer
    buffer = [
          1,  23,  45,  67,
         89, 172, 205, 239,
        154, 220, 189,  98,
         76,  54,  32,  10,
    ]

    for word_start in range(0, len(message), 64):
        pass


def md5_test():
    md5('') == 'd41d8cd98f00b204e9800998ecf8427e'
    md5('a') == '0cc175b9c0f1b6a831c399e269772661'
    md5('abc') == '900150983cd24fb0d6963f7d28e17f72'
    md5('message digest') == 'f96b697d7cb7938d525a2f31aaf161d0'
    md5('abcdefghijklmnopqrstuvwxyz') == 'c3fcd3d76192e4007dfb496cca67e13b'

    md5(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ) == 'd174ab98d277d9f5a5611c2c9f419d9f'

    md5(
        '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
    ) == '57edf4a22be3c955ac49da2e2107b67a'
