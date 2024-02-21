# import
import numpy as np


def makePreset(array: np.ndarray, indices: list) -> np.ndarray:
    """ Creates draggable object array

    This function creates an array of zeros and twos
    based on the empty input array and list of indices.

    :param array: empty input array
    :param indices: list of indices to change to two
    :return: modified array
    """
    for index in indices:
        array[index[0], index[1]] = 2
    return np.transpose(array)


# creates the glider preset
glider = makePreset(np.zeros((3,3)), [[0,1],[1,2],[2,0],[2,1],[2,2]])


# creates the period-three pulsar preset
pulsar_p3 = makePreset(np.zeros((15,15)), [[0,4],[1,4],[2,4],[2,5],[2,9],
                                           [2,10],[1,10],[0,10],[4,6],[4,8],
                                           [5,8],[4,9],[4,5],[5,6],[5,10],
                                           [6,10],[6,9],[5,4],[6,4],[6,5],
                                           [5,12],[4,12],[4,13],[4,14],[5,2],
                                           [4,2],[4,1],[4,0],[8,4],[8,5],
                                           [9,4],[10,5],[10,6],[9,6],[9,8],
                                           [10,8],[10,9],[8,9],[8,10],[9,10],
                                           [9,12],[10,12],[10,13],[10,14],[9,2],
                                           [10,2],[10,1],[10,0],[12,5],[12,4],
                                           [13,4],[14,4],[12,9],[12,10],[13,10],[14, 10]])


# creates the spaceship preset
spaceship = makePreset(np.zeros((5,7)), [[0,1],[0,2],[0,3],[0,4],[0,5],
                                         [0,6],[1,0],[3,0],[4,2],[4,3],
                                         [3,5],[2,6],[1,6]])


# creates the glider machine preset
glider_machine = makePreset(np.zeros((9,36)), [[4,0],[4,1],[5,1],[5,0],[4,10],
                                               [5,10],[6,10],[3,11],[7,11],[2,12],
                                               [2,13],[8,12],[8,13],[5,14],[3,15],
                                               [7,15],[6,16],[5,16],[4,16],[5,17],
                                               [4,20],[3,20],[2,20],[2,21],[3,21],
                                               [4,21],[1,22],[5,22],[1,24],[0,24],
                                               [5,24],[6,24],[2,34],[2,35],[3,35],
                                               [3,34]])


# creates the period-fifteen pulsar preset
pulsar_p15 = makePreset(np.zeros((12,3)), [[0,0],[0,1],[0,2],[1,1],[2,1], 
                                           [3,0],[3,1],[3,2],[5,0],[5,1], 
                                           [5,2],[6,0],[6,1],[6,2],[8,0], 
                                           [8,1],[8,2],[9,1],[10,1],[11,0], 
                                           [11,1],[11,2]])