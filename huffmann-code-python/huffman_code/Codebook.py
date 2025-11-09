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
import itertools
from collections import Counter
from typing import Optional, Dict, List, Tuple, cast

class Codebook:
    def __init__(self) -> None:
        self.role: Optional[str] = None  # 'tx' or 'rx'
        self.codeword: Optional[str] = None
        self.message: Optional[str] = None

        self.counterObj: Optional[Counter[str]] = None
        self.nodes: List[Node] = []
        self.mapping: Dict[str, str] = {}
        self.demapping: Dict[str, str] = {}
        self.tree = HuffmannTree()

    @classmethod
    def from_message(cls, message: str) -> "Codebook":
        obj = cls()
        obj.role = 'tx'
        obj.message = message
        obj.counterObj = Counter(message)
        obj.start()
        obj.tree.generate(obj.nodes)
        return obj

    @classmethod
    def from_stats(cls, symbol_stats: Dict[str, int]) -> "Codebook":
        obj = cls()
        obj.role = 'rx'
        counter = Counter(symbol_stats)
        obj.counterObj = counter
        obj.start()
        obj.tree.generate(obj.nodes)
        return obj

    @staticmethod
    def _to_bytes(message: str) -> bytes:
        return message.encode(encoding='utf-8', errors='strict')

    @staticmethod
    def _to_string(byte_message:bytes) -> str:
        return byte_message.decode(encoding='utf-8', errors='strict')

    def _print_codeword(self) -> None:
        print(self.codeword)

    def map(self) -> str:
        if self.message is None:
            raise ValueError("Message not initialized.")

        symbol_to_code: Dict[str, str] = {}
        for node in self.nodes:
            sym = node.get_symbol()
            code = node.get_code()
            if sym is not None and code is not None:
                symbol_to_code[sym] = code

        self.mapping = symbol_to_code
        self.codeword = ''.join(symbol_to_code[s] for s in self.message)
        return self.codeword

    def demap(self) -> str:
        if self.codeword is None:
            raise ValueError("Codeword not initialized.")

        code_to_symbol: Dict[str, str] = {}
        for node in self.nodes:
            sym = node.get_symbol()
            code = node.get_code()
            if sym is not None and code is not None:
                code_to_symbol[code] = sym

        buffer = ""
        decoded: List[str] = []
        for bit in self.codeword:
            buffer += bit
            if buffer in code_to_symbol:
                decoded.append(code_to_symbol[buffer])
                buffer = ""
        self.message = "".join(decoded)
        return self.message

    def start(self) -> None:
        if self.counterObj is None:
            raise ValueError("counterObj not initialized.")

        occurrence = sorted(self.counterObj.items(), key=lambda x: (x[1], x[0]))  # sort by frequency, then symbol
        total: float = float(sum(self.counterObj.values()))
        for symbol, count in occurrence:
            node = Node()
            node.set_symbol(symbol)
            node.set_probability(count / total)
            self.nodes.append(node)

class Node:
    def __init__(self) -> None:
        self.probability: Optional[float] = None
        self.symbol: Optional[str] = None
        self.code: Optional[str] = None
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

    def set_probability(self, probability: float) -> None:
        self.probability = probability

    def get_probability(self) -> float:
        if self.probability is None:
            raise ValueError("Node probability not set")
        return self.probability

    def set_symbol(self, symbol: Optional[str]) -> None:
        self.symbol = symbol

    def get_symbol(self) -> Optional[str]:
        return self.symbol

    def set_code(self, code: str) -> None:
        self.code = code

    def get_code(self) -> Optional[str]:
        return self.code

class HuffmannTree:
    def __init__(self) -> None:
        self.heap: list[list[float | int | Node]] | None = None
        self.root: Node | None = None

    def generate(self, nodes: list[Node]) -> None:
        counter = itertools.count()         # Unique sequence number
        heap = [[node.get_probability(), next(counter), node] for node in nodes]
        heapq.heapify(heap)

        while len(heap) > 1:
            left_tuple = cast(tuple[float, int, Node], heapq.heappop(heap))
            right_tuple = cast(tuple[float, int, Node], heapq.heappop(heap))
            left_prob, _, left_node = left_tuple
            right_prob, _, right_node = right_tuple

            parent = Node()
            parent.set_probability(left_prob + right_prob)
            parent.set_symbol(None)
            parent.left = left_node
            parent.right = right_node

            heapq.heappush(heap, [parent.get_probability(), next(counter), parent])

        root_tuple = cast(tuple[float, int, Node], heap[0])
        _, _, self.root = root_tuple
        self._assign_codes(self.root)

    def _assign_codes(self, node: Node | None, code: str="") -> None:
        if node is None:
            return
        if node.get_symbol() is not None:
            node.set_code(code)
            return
        self._assign_codes(node.left, code + "0")
        self._assign_codes(node.right, code + "1")
