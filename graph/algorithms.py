import numpy as np

def get_TA(A, T, depth):
    if depth < 0:
        raise Exception('Depth cannot be negative.')
    elif depth == 1:
        return T
    elif depth > 1:
        T = T @ (A + np.identity(A.shape[0])) # identity preserves history
        depth -= 1
        return get_TA(A, T, depth)
    
def get_reachable_nodes(A, starting_node, depth):
    T = A[starting_node]
    return np.where(get_TA(A, T, depth) > 0)[0]