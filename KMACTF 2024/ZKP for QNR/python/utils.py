import random
from typing import List, Union
from dataclasses import dataclass

# Define Rp class equivalent
@dataclass
class Rp:
    pass

@dataclass
class RpTuple(Rp):
    a: int
    b: int

@dataclass
class RpNumber(Rp):
    n: int

def rand_below(n: int) -> int:
    """Generate a random integer less than n."""
    bit_length = n.bit_length()
    
    while True:
        y = random.getrandbits(bit_length)
        if y < n:
            return y

def bytes_to_bigint(bytes_data: bytes) -> int:
    """Convert a byte array to an integer."""
    return int.from_bytes(bytes_data, byteorder='big')

def convert_rp_to_string(v: List[Rp]) -> List[str]:
    """Convert a list of Rp objects to a list of strings."""
    normal_numbers = []
    for item in v:
        if isinstance(item, RpTuple):
            normal_numbers.append(f"({item.a}, {item.b})")
        elif isinstance(item, RpNumber):
            normal_numbers.append(f"{item.n}")
    return normal_numbers