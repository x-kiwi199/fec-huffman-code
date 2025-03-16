# *     Project: huffman-code-python
# *      Module: -
# *      Script: main.py
# * Description: Demonstration of Forward-Error-Correction (FEC) encoder/decoder usage. Communication link system module abstraction.
# *              [message (unencrypted) -> encoder -> codeword (encrypted) -> decoder -> message(recovered)]
# *
# *       Usage: python main.py -h, --h
#                python main.py -d, --data "12345abc..."
# *
# *  Created on: Mar 16, 2025
# *      Author: Vivian Becher
# *     Contact: x-kiwi199@web.de
# *     License: [The Unlicense]
# -----------------------------------------------------------------------
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <https://unlicense.org/>
# -----------------------------------------------------------------------


import argparse
from huffman_code import Encoder, Decoder

def main():
    parser = argparse.ArgumentParser(description="Test standard encoder/decoder framework based on Huffmann code")
    parser.add_argument("-d","--data", type=str,
                        default="Hello, World! Unencrypted 'utf-8' encoded message!",
                        help="verify correct feed trough of DATA",
                        required=True)
    args = parser.parse_args()

    # Unencrypted message input as commandline argument
    original_message = args.data

    # Initialize Encoder and Decoder
    encoder = Encoder()
    decoder = Decoder()

    # Run real test
    codeword = encoder.encode(original_message)
    # TODO: Missing codebook instance separation. Or statistics sharing mechanism
    decoded_message = decoder.decode(codebook=encoder.codebook, codeword=codeword)

    print(f"original message: {original_message}")
    print(f"decoded message: {decoded_message}")

    assert original_message == decoded_message, "Decoded data does not match the original!"

if __name__ == "__main__":
    main()
