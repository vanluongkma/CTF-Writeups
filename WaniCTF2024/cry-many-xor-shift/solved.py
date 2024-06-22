import struct

N = 7
M = 17005450388330379
WORD_SIZE = 32
WORD_MASK = (1 << WORD_SIZE) - 1

lst = [1927245640, 871031439, 789877080, 4042398809, 3950816575, 2366948739, 935819524]

def _reverse(state):
    for _ in range(M):

        t = state[-1]
        t = t ^ (t >> 19)
        t = t ^ (t >> 19)  
        t = t ^ (t >> 8)
        t = t ^ (t >> 8)  
        t = state[-1] ^ t
        for i in range(N-1, 0, -1):
            state[i] = state[i-1]
        
        state[0] = t ^ ((t << 11) & WORD_MASK)
        state[0] = state[0] ^ ((state[0] << 11) & WORD_MASK) 

    return state

_state = _reverse(lst.copy())

def state_to_bytes(state):
    return b''.join(struct.pack('<I', x) for x in state)
print(state_to_bytes(_state))
