import numpy as np

def get_TA(A, T, depth, perserve_history=True):
    if depth < 0:
        raise Exception('Depth cannot be negative.')
    elif depth == 1:
        return T
    elif depth > 1:
        if perserve_history:
            T = T @ (A + np.identity(A.shape[0]))
        else:
            T = T @ A
        depth -= 1
        return get_TA(A, T, depth, perserve_history=perserve_history)
    
def get_reachable_nodes(A, starting_node, depth, include_starting_node=False):
    T = A[starting_node]
    TA = get_TA(A, T, depth, perserve_history=True)
    if include_starting_node:
        TA[starting_node] = 1
    return np.where(TA > 0)[0]