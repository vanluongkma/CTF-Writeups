import os
import random
from typing import List, Tuple
from dataclasses import dataclass
from pathlib import Path

# Utility functions (equivalent to the Rust module `utils`)
def bytes_to_bigint(bytes_data: bytes) -> int:
    """Convert a byte array to an integer."""
    return int.from_bytes(bytes_data, byteorder='big')

def rand_below(n: int) -> int:
    """Generate a random integer less than n."""
    bit_length = n.bit_length()
    while True:
        y = random.getrandbits(bit_length)
        if y < n:
            return y

def convert_rp_to_string(v: List['Rp']) -> List[str]:
    """Convert a list of Rp objects to a list of strings."""
    normal_numbers = []
    for item in v:
        if isinstance(item, RpTuple):
            normal_numbers.append(f"({item.a}, {item.b})")
        elif isinstance(item, RpNumber):
            normal_numbers.append(f"{item.n}")
    return normal_numbers

# Classes equivalent to the Rust modules

@dataclass
class Prover:
    x: int
    y: int
    num_rounds: int

    def gen_list_i(self) -> List[int]:
        """Generate a list of random bits (0 or 1) of length num_rounds."""
        return [random.randint(0, 1) for _ in range(self.num_rounds)]

@dataclass
class Verifier:
    x: int
    y: int
    rs: List[List[Tuple[int, int]]] = field(default_factory=list)
    pairs: List[List[Tuple[int, int]]] = field(default_factory=list)
    num_rounds: int = 0

    def gen_w(self, bit: int, r: int) -> int:
        """Generate w based on the bit value and r."""
        if bit == 0:
            return pow(r, 2, self.x)
        else:
            return (pow(r, 2, self.x) * self.y) % self.x

    def gen_pairs(self) -> List[Tuple[int, int]]:
        """Generate pairs of values."""
        rr = []
        pair = []
        for _ in range(self.num_rounds):
            r1 = rand_below(self.x)
            r2 = rand_below(self.x)
            a = pow(r1, 2, self.x)
            b = (pow(r2, 2, self.x) * self.y) % self.x

            pair.append((a, b))
            rr.append((r1, r2))
        self.rs.append(rr)
        self.pairs.append(pair)
        return pair

    def respond(self, bit: int, list_i: List[int], r: int) -> List['Rp']:
        """Generate a list of responses based on the bit, list_i, and r."""
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
        """Get a random value below x."""
        return rand_below(self.x)

@dataclass
class RpTuple:
    a: int
    b: int

@dataclass
class RpNumber:
    n: int

def main():
    flag = b"KMACTF{*******************************************}"
    num_flag = bytes_to_bigint(flag)

    num_rounds = num_flag.bit_length()

    folder_name = "Log"

    # Create the folder if it doesn't exist
    Path(folder_name).mkdir(parents=True, exist_ok=True)

    print(f"Number of rounds: {num_rounds}")

    x = int("106276637345585586395178695555113419125706596151484787339368729136766801222943")
    y = int("67502870359608496464376733754660348616157530226832182619029429292243849029379")

    prover = Prover(x, y, num_rounds)
    verifier = Verifier(x, y, num_rounds)

    for i in range(num_rounds):
        file_name = f"{folder_name}/output_{i}.txt"
        with open(file_name, "w") as file:
            file.write(f"Round {i}\n")

            bit = (num_flag >> i) & 1
            r = verifier.get_r()

            # give the prover the pair and r
            w = verifier.gen_w(bit, r)
            pair = verifier.gen_pairs()

            file.write(f"w = {w}\n")

            file.write("Pair = \n")
            for p in pair:
                file.write(f"({p[0]}, {p[1]})\n")

            list_i = prover.gen_list_i()
            file.write(f"list_i = {list_i}\n")

            v = verifier.respond(bit, list_i, r)

            v_str = convert_rp_to_string(v)

            file.write("list_of_respond = \n")
            for line in v_str:
                file.write(f"{line}\n")

if __name__ == "__main__":
    main()