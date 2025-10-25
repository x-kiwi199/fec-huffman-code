# *     Project: huffman-code-python
# *      Module: huffman_code
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
from collections import Counter
import itertools

class Codebook:
    def __init__(self, message: str = None, symbol_stats: dict = None) -> None:
        if message:
            self.message = message
            self.counterObj = Counter(self.message)
        elif symbol_stats:
            self.message = None
            self.counterObj = Counter(symbol_stats)
        else:
            raise ValueError("Either message or symbol_stats must be provided.")

        self.codeword = None
        self.tree = HuffmannTree()
        self.nodes = []
        self.mapping = None
        self.demapping = None

        self.start()
        self.tree.generate(self.nodes)


    @staticmethod
    def _to_bytes(message: str):
        return message.encode(encoding='utf-8', errors='strict')

    @staticmethod
    def _to_string(byte_message:bytes):
        return byte_message.decode(encoding='utf-8', errors='strict')

    def _print_codeword(self):
        print(self.codeword)

    def map(self):
        symbol_to_code = {node.get_symbol(): node.get_code() for node in self.nodes if node.get_symbol() is not None}
        self.mapping = symbol_to_code
        self.codeword = ''.join(symbol_to_code[s] for s in self.message)
        return self.codeword

    def demap(self):
        code_to_symbol = {node.get_code(): node.get_symbol() for node in self.nodes if node.get_symbol() is not None}
        buffer = ""
        decoded = []
        for bit in self.codeword:
            buffer += bit
            if buffer in code_to_symbol:
                decoded.append(code_to_symbol[buffer])
                buffer = ""
        self.message = ''.join(decoded)
        return self.message

    def start(self):
        occurrence = sorted(self.counterObj.items(), key=lambda x: (x[1], x[0]))  # sort by frequency, then symbol
        total = sum(self.counterObj.values())
        for symbol, count in occurrence:
            node = Node()
            node.set_symbol(symbol)
            node.set_probability(count / total)
            self.nodes.append(node)


# self.counterObj.elements()
# statistics = counterObj.elements()
# inv_map = dict(zip(my_map.values(), my_map.keys()))
#         mapping = dict(zip(probability, symbols))
#         # demapping = dict(zip(symbols, probability))

class Node:
    def __init__(self) -> None:
        self.probability = None
        self.symbol = None
        self.code = None
        self.left = None
        self.right = None

    def set_probability(self, probability: float):
        self.probability = probability

    def get_probability(self):
        return self.probability

    def set_symbol(self, symbol:str):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol

    def set_code(self, code:str):
        self.code = code

    def get_code(self):
        return self.code

class HuffmannTree:
    def __init__(self) -> None:
        self.heap = None

    ''' 
    Use the min heap structure to fetch left and right node leaves with minimal leftover probability
    '''


    def generate(self, nodes: list):
        counter = itertools.count()  # Unique sequence number
        heap = [[node.get_probability(), next(counter), node] for node in nodes]
        heapq.heapify(heap)

        while len(heap) > 1:
            left_prob, _, left_node = heapq.heappop(heap)
            right_prob, _, right_node = heapq.heappop(heap)

            parent = Node()
            parent.set_probability(left_prob + right_prob)
            parent.set_symbol(None)
            parent.left = left_node
            parent.right = right_node

            heapq.heappush(heap, [parent.get_probability(), next(counter), parent])

        _, _, root = heap[0]
        self.root = root
        self._assign_codes(self.root)

    def _assign_codes(self, node, code=""):
        if node.get_symbol() is not None:
            node.set_code(code)
            return
        self._assign_codes(node.left, code + "0")
        self._assign_codes(node.right, code + "1")


