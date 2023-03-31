import numpy as np
import heapq

def test_sort_matrix1():
    states_sequence = np.array([[0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                                [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
                                [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
                                [0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
                                [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]])
    print(sort_matrix(states_sequence))

def test_sort_matrix2():
    states_sequence = np.array([[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                                [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                                [0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
                                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
                                [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
                                [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
                                [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
                                [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
                                [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
                                [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
                                [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]])
    print(sort_matrix(states_sequence))

def sort_matrix(states_sequence):
    """

    """
    min_heap = []

    for j in range(states_sequence.shape[1]):
        was_stated = False
        was_finished = False
        # maior valor que pode ser colocado
        start_line = states_sequence.shape[0] - 1
        finish_line = states_sequence.shape[0] - 1
        for i in range(states_sequence.shape[0]):
            if (was_stated and states_sequence[i, j] == 0):
                finish_line = i-1
                was_finished = True
                break
            elif ((not was_stated) and states_sequence[i, j] == 1):
                start_line = i
                was_stated = True

        heapq.heappush(min_heap, (start_line, finish_line, j))

    new_states_sequence = np.zeros(states_sequence.shape)

    for i in range(states_sequence.shape[1]):
        tuple = heapq.heappop(min_heap)
        col = tuple[2]
        new_states_sequence[:, i] = states_sequence[:, col]

    return new_states_sequence

test_sort_matrix1()
test_sort_matrix2()