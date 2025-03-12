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

import heapq

class Codebook:
    def __init__(self):
        self.alphabet = None
        self.tree = None

        self.message = None

        self.forward_map = None
        self.backward_map = None

    @staticmethod
    def _to_bytes(message: str):
        return message.encode(encoding='utf-8', errors='strict')

    @staticmethod
    def _to_string(byte_message:bytes):
        return byte_message.decode(encoding='utf-8', errors='strict')

inv_map = dict(zip(my_map.values(), my_map.keys()))

# /**
#  * dictionary // Zuordnungstabelle für das Codebuch
#  */
#  // Diese rekursive Funktion erzeugt das Codebuch für die Huffman-Kodierung und speichert es in der Variable dictionary
#  function createDictionary(node, codeword, dictionary)
#  {
#    if (der Knoten ist node ist leer)
#    {
#        return; // Abbruchbedingung, wenn kein linker oder rechter Teilbaum vorhanden ist
#    }
#    if (node->symbol is kein innerer Knoten, also ein Blatt) // Wenn der Knoten kein innerer Knoten, also ein Blatt ist
#    {
#        dictionary.insert(node->symbol, codeword); // Fügt die Kombination aus Symbol und Codewort dem Codebuch hinzu
#        return; // Verlässt die Funktion
#    }
#    createDictionary(node->left, concat(codeword, "0"), dictionary) // Rekusiver Aufruf für den linken Teilbaum, das Codesymbol 0 für die linke Kante wird angefügt
#    createDictionary(node->right, concat(codeword, "1"), dictionary) // Rekusiver Aufruf für den rechten Teilbaum, das Codesymbol 1 für die rechte Kante wird angefügt
#  }

class HuffmannTree:
    def __init__(self):
        self.heap = None

    ''' 
    Use the min heap structure to fetch left and right node leaves with minimal leftover probability
    '''
    def generate(self, probability:list, symbols:list):
        mapping = dict(zip(probability, symbols))
        demapping = dict(zip(symbols,probability))

        self.heap = probability
        heapq.heapify(self.heap)

        while len(self.heap) > 1:
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)

            top = left + right
            heapq.heappush(self.heap, top)
