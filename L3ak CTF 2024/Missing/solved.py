import hashlib
from typing import List

class FlagProof:
    def __init__(self, root: bytes):
        self.root = root

    def keccak256(self, data: bytes) -> bytes:
        return hashlib.sha3_256(data).digest()

    def commutative_keccak256(self, a: bytes, b: bytes) -> bytes:
        return self.keccak256(a + b) if a < b else self.keccak256(b + a)

    def multi_proof_verify(self, proof: List[bytes], proof_flags: List[bool], leaves: List[bytes]) -> bool:
        return self.process_multi_proof(proof, proof_flags, leaves) == self.root

    def process_multi_proof(self, proof: List[bytes], proof_flags: List[bool], leaves: List[bytes]) -> bytes:
        leaves_len = len(leaves)
        proof_len = len(proof)
        total_hashes = len(proof_flags)

        if leaves_len + proof_len != total_hashes + 1:
            raise ValueError("MerkleProofInvalidMultiproof")

        hashes = [b''] * total_hashes
        leaf_pos = 0
        hash_pos = 0
        proof_pos = 0

        for i in range(total_hashes):
            a = leaves[leaf_pos] if leaf_pos < leaves_len else hashes[hash_pos]
            leaf_pos += 1 if leaf_pos < leaves_len else 0
            hash_pos += 1 if leaf_pos >= leaves_len else 0

            if proof_flags[i]:
                b = leaves[leaf_pos] if leaf_pos < leaves_len else hashes[hash_pos]
                leaf_pos += 1 if leaf_pos < leaves_len else 0
                hash_pos += 1 if leaf_pos >= leaves_len else 0
            else:
                b = proof[proof_pos]
                proof_pos += 1

            hashes[i] = self.commutative_keccak256(a, b)

        if total_hashes > 0:
            if proof_pos != proof_len:
                raise ValueError("MerkleProofInvalidMultiproof")
            return hashes[total_hashes - 1]
        elif leaves_len > 0:
            return leaves[0]
        else:
            return proof[0]

# Ví dụ sử dụng
root = bytes.fromhex('a3c3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2')  # Thay thế bằng giá trị gốc Merkle Tree
flag_proof = FlagProof(root)

proof = [
    bytes.fromhex('b4c3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2'),
    bytes.fromhex('c4c3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2')
]  # Thay thế bằng danh sách các proof

proof_flags = [True, False]  # Thay thế bằng các cờ proof

leaves = [
    bytes.fromhex('d4c3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2'),
    bytes.fromhex('e4c3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2d5a3e2a5d4c2f9b2')
]  # Thay thế bằng danh sách các leaves

result = flag_proof.multi_proof_verify(proof, proof_flags, leaves)
print("Result:", result)