# *     Project: huffman-code-python
# *      Module: huffman-code
# *      Script: Codeboook.py
# * Description: Core logic of mapping/demapping from finite alphabet.
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


class Codebook:
    def __init__(self):
        self.alphabet = None
        self.tree = None

    @staticmethod
    def _to_bytes(message: str):
        return message.encode(encoding='utf-8', errors='strict')

    @staticmethod
    def _to_string(byte_message:bytes):
        return byte_message.decode(encoding='utf-8', errors='strict')




# TODO: Think about configuration, alphabet definition, update, mapping

# _string = "Some String"
# _string_as_bytes = bytes(_string, 'utf-8')
#bytes(_string="test",_enc='utf-8')
