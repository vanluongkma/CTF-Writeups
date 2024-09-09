import random
from typing import List

class Prover:
    def __init__(self, x: int, y: int, n: int):
        self.x = x
        self.y = y
        self.num_rounds = n
        self.list_i = []

    def gen_list_i(self) -> List[int]:
        list_i = [random.randint(0, 1) for _ in range(self.num_rounds)]
        return list_i