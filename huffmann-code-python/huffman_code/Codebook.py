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

# class Codebook:
#     def __init__(self):
#         self.counterObj = None
#         self.nodes = []
#         self.mapping = {}
#         self.demapping = {}
#         self.tree = HuffmannTree()
#         self.codeword = None
#         self.message = None
#
#     def fit_from_message(self, message: str):
#         """Build internal statistics and tree from a raw message."""
#         self.message = message
#         self.counterObj = Counter(message)
#         self._build_tree()
#
#     def fit_from_stats(self, stats: dict):
#         """Rebuild from externally provided statistics."""
#         self.counterObj = Counter(stats)
#         self._build_tree()
#
#     def _build_tree(self):
#         self.nodes.clear()
#         occurrence = sorted(self.counterObj.items(), key=lambda x: (x[1], x[0]))
#         total = sum(self.counterObj.values())
#         for symbol, count in occurrence:
#             node = Node()
#             node.set_symbol(symbol)
#             node.set_probability(count / total)
#             self.nodes.append(node)
#         self.tree.generate(self.nodes)
#         self.mapping = {n.get_symbol(): n.get_code() for n in self.nodes if n.get_symbol() is not None}
#         self.demapping = {v: k for k, v in self.mapping.items()}
#
#     def map(self, message: str | None = None) -> str:
#         if message:
#             self.message = message
#         if not self.message or not self.mapping:
#             raise RuntimeError("Codebook not yet initialized with message or statistics.")
#         self.codeword = ''.join(self.mapping[s] for s in self.message)
#         return self.codeword
#
#     def demap(self, codeword: str | None = None) -> str:
#         if codeword:
#             self.codeword = codeword
#         if not self.codeword or not self.demapping:
#             raise RuntimeError("Codebook not yet initialized with statistics.")
#         decoded, buffer = [], ""
#         for bit in self.codeword:
#             buffer += bit
#             if buffer in self.demapping:
#                 decoded.append(self.demapping[buffer])
#                 buffer = ""
#         return ''.join(decoded)

class Codebook:
    def __init__(self) -> None:
        self.role = None        # 'tx' or 'rx' role as codebook lives at runtime as two separated instances
        self.codeword = None
        self.message = None

        self.counterObj = None
        self.nodes = []
        self.mapping = {}
        self.demapping = {}
        self.tree = HuffmannTree()

    @classmethod
    def from_message(cls, message: str) -> "Codebook":
        obj = cls()
        obj.role = 'tx'
        obj.message = message
        counter = Counter(message)
        obj.counterObj = counter
        obj.start()
        obj.tree.generate(obj.nodes)
        return obj

    @classmethod
    def from_stats(cls, symbol_stats: dict) -> "Codebook":
        obj = cls()
        obj.role = 'rx'
        counter = Counter(symbol_stats)
        obj.counterObj = counter
        obj.start()
        obj.tree.generate(obj.nodes)
        return obj

    @staticmethod
    def _to_bytes(message: str):
        return message.encode(encoding='utf-8', errors='strict')

    @staticmethod
    def _to_string(byte_message:bytes):
        return byte_message.decode(encoding='utf-8', errors='strict')

    def _print_codeword(self):
        print(self.codeword)

    def map(self) -> str:
        symbol_to_code = {node.get_symbol(): node.get_code() for node in self.nodes if node.get_symbol() is not None}
        self.mapping = symbol_to_code
        self.codeword = ''.join(symbol_to_code[s] for s in self.message)
        return self.codeword

    def demap(self) -> str:
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
        self.root = None

    def generate(self, nodes: list):
        counter = itertools.count()         # Unique sequence number
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
