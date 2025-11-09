# *     Project: huffman-code-python
# *      Module: huffman_code
# *      Script: Encoder.py
# * Description: Forward-Error-Correction (FEC) encoder, system module abstraction of communication link, message (input) -> codeword (output)
# *
# *  Created on: Feb 24, 2025
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

import logging
from .Codebook import Codebook

class Encoder:
    def __init__(self) -> None:
        self.message: str | None = None

        self.codebook: Codebook | None = None
        self.codeword: str | None = None

        self.logger = logging.getLogger("ENCODER")
        self.logger.debug("Initializing encoder")

    def encode(self, message:str) -> str:
        self.message = message
        if self.codebook is None:
            self.codebook = Codebook.from_message(message=message)
        else:
            self.codebook = Codebook() # dummy
            self.logger.warning("Codebook update mechanism not yet implemented")
        self.codeword = self.codebook.map()
        self.logger.debug(f"> tx_message: {self.message}")
        self.logger.debug(f"> codeword: {self.codeword}")
        return self.codeword
