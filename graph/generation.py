import numpy as np

def generate_adjacency(n_nodes: int, n_edges: int, self_loops: bool=True, symmetric=False, no_islands=False):
    """
    Randomly generates an adjacency matrix given number of nodes and edges.

    Parameters
    ----------
    n_nodes : int
        The number of nodes in the generated adjacency.
    n_edges : int
        The number of edges in the generated adjacency.
    self_loops : bool, optional
        Whether or not to allow self-loops when adding edges.
    symmetric : bool, optional
        Whether or not to generate a symmetric adjacency.

    Returns
    -------
    A : numpy.ndarray
        A NxN adjacency matrix.

    Examples
    --------
    >>> generate_adjacency(4, 8)
    array([[0., 1., 0., 0.],
           [1., 0., 1., 0.],
           [0., 0., 1., 1.],
           [1., 1., 1., 0.]])
    >>> generate_adjacency(4, 5, symmetric=True, self_loops=False)
    array([[0., 1., 0., 1.],
           [1., 0., 1., 1.],
           [0., 1., 0., 1.],
           [1., 1., 1., 0.]])
    """
    area_total = n_nodes**2
    area_diagonal = n_nodes
    area_triangle = n_nodes*(n_nodes-1)/2
    if symmetric:
        if self_loops:
            assert n_edges <= area_diagonal + area_triangle
        else:
            assert n_edges <= area_triangle
    else:
        if self_loops:
            assert n_edges <= area_total
        else:
            assert n_edges <= area_total - area_diagonal

    A = np.zeros((n_nodes, n_nodes))
    coords = []
    for i in range(n_nodes):
        for j in range(n_nodes):
            if not self_loops and i == j:
                continue
            if symmetric and i > j:
                coords.append((i, j))
            else:
                coords.append((i, j))
    coords = np.array(coords)
    idx = np.random.choice(len(coords), n_edges, replace=False)
    for i, j in coords[idx]:
        A[i, j] = 1
        if symmetric:
            A[j, i] = 1

    if no_islands:
    	try:
            assert(all([sum(r) > 0 for r in A]))
    	except:
            A = generate_adjacency(n_nodes, n_edges, self_loops, symmetric)

    return A
