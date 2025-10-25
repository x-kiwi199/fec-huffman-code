# *     Project: huffman-code-python
# *      Module: -
# *      Script: main.py
# * Description: Demonstration of Forward-Error-Correction (FEC) encoder/decoder usage. Communication link system module abstraction.
# *              [message (cleartext) -> encoder -> codeword (encoded) -> decoder -> message(recovered)]
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

import sys
import argparse
import logging
from collections import Counter
from huffman_code import Encoder, Decoder

def main() -> int:
    parser = argparse.ArgumentParser(description="Test standard encoder/decoder framework based on Huffmann code")
    parser.add_argument("-d","--data", type=str,
                        default="Hello, World! 'utf-8' text-encoded message!",
                        help="verify correct feed trough of DATA",
                        required=False)
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()

    # Setup basic logging
    logger = logging.getLogger("MAIN")
    logging.basicConfig(
        level=logging.DEBUG,  # or logging.DEBUG
        format='%(asctime)s [%(name)s][%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logger.info("Running application...")

    # Cleartext message input from commandline argument
    original_message = args.data

    # Initialize Encoder and Decoder
    encoder = Encoder()
    decoder = Decoder()

    # Run real test
    codeword = encoder.encode(message=original_message)
    alphabet_soup = dict(Counter(original_message))
    decoded_message = decoder.decode(codeword=codeword, alphabet_soup=alphabet_soup)

    try:
        if original_message != decoded_message:
            logging.error("FAILURE! Decoded message does not match the original.")
            logging.error(f"original message: {original_message}")
            logging.error(f"decoded message: {decoded_message}")
            return 1  # non-zero indicates error
        else:
            logger.info("SUCCESS! Message correctly recovered.")
            return 0
    except Exception as e:
        logger.exception(f"Unexpected runtime error: {e}")
        return 2  # non-zero indicates error
    finally:
        logger.info("Closing application.")

if __name__ == "__main__":
    sys.exit(main())