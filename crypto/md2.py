# -*- coding: utf-8 -*-
from __future__ import division

# Permutation of 0..255 constructed from the digits of pi. It gives a "random"
# nonlinear byte substitution operation.
PI_SUBSTITUTION = [
    41, 46, 67, 201, 162, 216, 124, 1, 61, 54, 84, 161, 236, 240, 6, 19, 98,
    167, 5, 243, 192, 199, 115, 140, 152, 147, 43, 217, 188, 76, 130, 202, 30,
    155, 87, 60, 253, 212, 224, 22, 103, 66, 111, 24, 138, 23, 229, 18, 190,
    78, 196, 214, 218, 158, 222, 73, 160, 251, 245, 142, 187, 47, 238, 122,
    169, 104, 121, 145, 21, 178, 7, 63, 148, 194, 16, 137, 11, 34, 95, 33, 128,
    127, 93, 154, 90, 144, 50, 39, 53, 62, 204, 231, 191, 247, 151, 3, 255, 25,
    48, 179, 72, 165, 181, 209, 215, 94, 146, 42, 172, 86, 170, 198, 79, 184,
    56, 210, 150, 164, 125, 182, 118, 252, 107, 226, 156, 116, 4, 241, 69, 157,
    112, 89, 100, 113, 135, 32, 134, 91, 207, 101, 230, 45, 168, 2, 27, 96, 37,
    173, 174, 176, 185, 246, 28, 70, 97, 105, 52, 64, 126, 15, 85, 71, 163, 35,
    221, 81, 175, 58, 195, 92, 249, 206, 186, 197, 234, 38, 44, 83, 13, 110,
    133, 40, 132, 9, 211, 223, 205, 244, 65, 129, 77, 82, 106, 220, 55, 200,
    108, 193, 171, 250, 36, 225, 123, 8, 12, 189, 177, 74, 120, 136, 149, 139,
    227, 99, 232, 109, 233, 203, 213, 254, 59, 0, 29, 57, 242, 239, 183, 14,
    102, 88, 208, 228, 166, 119, 114, 248, 235, 117, 75, 10, 49, 68, 80, 180,
    143, 237, 31, 26, 219, 153, 141, 51, 159, 17, 131, 20,
]


# https://tools.ietf.org/html/rfc1319
def md2(message):
    """ Returns the 16 bytes digest for `message`. """

    # convert to integers
    message = list(map(ord, message))

    # Step 1: Padding is always performed. Pad "i" bytes of value "i", at least
    # 1 and at most 16 bytes.
    pad_size = 16 - (len(message) % 16)
    pad = [pad_size] * pad_size
    message = message + pad

    # Step 2: Append checksum
    checksum = [0] * 16
    previous = 0
    for block_start in range(0, len(message), 16):
        for pos in range(16):
            element = message[block_start + pos]
            previous = checksum[pos] = checksum[pos] ^ PI_SUBSTITUTION[element ^ previous]
    message = message + checksum

    # Step 3/4: Initialize the message digest buffer and compute the digest
    message_digest = [0] * 48
    for block_start in range(0, len(message), 16):
        for pos in range(16):
            message_digest[16 + pos] = message[block_start + pos]
            message_digest[32 + pos] = message_digest[16 + pos] ^ message_digest[pos]

        t = 0
        for round in range(18):
            for pos in range(48):
                t = message_digest[pos] = message_digest[pos] ^ PI_SUBSTITUTION[t]
            t = (t + round) % 256

    return b''.join(map(chr, message_digest[0:16]))


def md2_test():
    assert md2('').encode('hex') == '8350e5a3e24c153df2275c9f80692773'
    assert md2('a').encode('hex') == '32ec01ec4a6dac72c0ab96fb34c0b5d1'
    assert md2('abc').encode('hex') == 'da853b0d3f88d99b30283a69e6ded6bb'
    assert md2('message digest').encode('hex') == 'ab4f496bfb2a530b219ff33031fe06b0'
    assert md2('abcdefghijklmnopqrstuvwxyz').encode('hex') == '4e8ddff3650292ab5a4108c3aa47940b'

    assert md2(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ).encode('hex') == 'da33def2a42df13975352846c30338cd'

    assert md2(
        '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
    ).encode('hex') == 'd5976f79d83d3a0dc9806c3c66f3efd8'
