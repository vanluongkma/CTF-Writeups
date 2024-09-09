import random
from typing import List, Tuple, Union
from dataclasses import dataclass, field

@dataclass
class Verifier:
    x: int
    y: int
    rs: List[List[Tuple[int, int]]] = field(default_factory=list)
    pairs: List[List[Tuple[int, int]]] = field(default_factory=list)
    num_rounds: int = 0

    def gen_w(self, bit: int, r: int) -> int:
        if bit == 0:
            return pow(r, 2, self.x)
        else:
            return (pow(r, 2, self.x) * self.y) % self.x

    def gen_pairs(self) -> List[Tuple[int, int]]:
        rr = []
        pair = []
        for _ in range(self.num_rounds):
            r1 = self.rand_below(self.x)
            r2 = self.rand_below(self.x)
            a = pow(r1, 2, self.x)
            b = (pow(r2, 2, self.x) * self.y) % self.x

            pair.append((a, b))
            rr.append((r1, r2))
        self.rs.append(rr)
        self.pairs.append(pair)
        return pair

    def respond(self, bit: int, list_i: List[int], r: int) -> List[Union['RpTuple', 'RpNumber']]:
        v = []
        for i, a in enumerate(list_i):
            if a == 0:
                vj = self.rs[-1][i]
                v.append(RpTuple(vj[0], vj[1]))
            elif a == 1:
                if bit == 0:
                    vj = (r * self.rs[-1][i][0]) % self.x
                elif bit == 1:
                    vj = (r * self.rs[-1][i][1] * self.y) % self.x
                v.append(RpNumber(vj))
            else:
                raise ValueError("Invalid input")
        return v

    def get_r(self) -> int:
        return self.rand_below(self.x)

    @staticmethod
    def rand_below(n: int) -> int:
        """Generate a random integer less than n."""
        bit_length = n.bit_length()
        while True:
            y = random.getrandbits(bit_length)
            if y < n:
                return y

@dataclass
class RpTuple:
    a: int
    b: int

@dataclass
class RpNumber:
    n: int