from intcomputer import IntcodeComputer
from collections import deque

from matplotlib import pyplot as plt


code=[3,8,1005,8,320,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,29,2,1005,1,10,1006,0,11,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,57,1,8,15,10,1006,0,79,1,6,3,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,90,2,103,18,10,1006,0,3,2,105,14,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,123,2,9,2,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1001,8,0,150,1,2,2,10,2,1009,6,10,1,1006,12,10,1006,0,81,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,187,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,209,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,231,1,1008,11,10,1,1001,4,10,2,1104,18,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,264,1,8,14,10,1006,0,36,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,293,1006,0,80,1006,0,68,101,1,9,9,1007,9,960,10,1005,10,15,99,109,642,104,0,104,1,21102,1,846914232732,1,21102,1,337,0,1105,1,441,21102,1,387512115980,1,21101,348,0,0,1106,0,441,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,209533824219,1,1,21102,1,395,0,1106,0,441,21101,0,21477985303,1,21102,406,1,0,1106,0,441,3,10,104,0,104,0,3,10,104,0,104,0,21101,868494234468,0,1,21101,429,0,0,1106,0,441,21102,838429471080,1,1,21102,1,440,0,1106,0,441,99,109,2,21201,-1,0,1,21101,0,40,2,21102,472,1,3,21101,0,462,0,1106,0,505,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,467,468,483,4,0,1001,467,1,467,108,4,467,10,1006,10,499,1102,1,0,467,109,-2,2106,0,0,0,109,4,2101,0,-1,504,1207,-3,0,10,1006,10,522,21101,0,0,-3,21202,-3,1,1,22101,0,-2,2,21102,1,1,3,21102,541,1,0,1106,0,546,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,569,2207,-4,-2,10,1006,10,569,22102,1,-4,-4,1105,1,637,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,588,1,0,1105,1,546,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,607,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,629,21201,-1,0,1,21102,629,1,0,105,1,504,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0
]


BLACK = 0
WHITE = 1

def turn(x, y, facing, indicator):
    """
    Parameters
    ---------
    x, y: current coordinates
    facing: direction encoded as:
        (0, 1): V
        (1, 0): >
        (-1, 0): <
        (0, -1): ^
    indicator: 0 - left 90 degs, 1 - right 90 degs

    Returns
    -------
    new coordinates x_ ,y_ and new direction
    """
    if indicator == 1:
        new_dir_x = - facing[1]
        new_dir_y = facing[0]
    else:
        new_dir_x = facing[1]
        new_dir_y = - facing[0]

    return (x + new_dir_x, y + new_dir_y), (new_dir_x, new_dir_y)

# some tests
for original_direction, expected_xy, expected_dir in \
    zip([(0, 1), (1, 0), (-1, 0), (0, -1)],
        [(6, 5), (5, 4), (5, 6), (4, 5)],
        [(1, 0), (0, -1), (0, 1), (-1, 0)]):
    assert(turn(5, 5, original_direction, 0)[0] == expected_xy)
    assert(turn(5, 5, original_direction, 0)[1] == expected_dir)

for original_direction, expected_xy, expected_dir in \
    zip([(0, 1), (1, 0), (-1, 0), (0, -1)],
        [(4, 5), (5, 6), (5, 4), (6, 5)],
        [(-1, 0), (0, 1), (0, -1), (1, 0)]):
    assert(turn(5, 5, original_direction, 1)[1] == expected_dir)
    assert(turn(5, 5, original_direction, 1)[0] == expected_xy)


if __name__ == "__main__":

    painted_pixels = {}  # {(x, y): color}
    x_ = 0
    y_ = 0
    dir_ = (0, -1)
    start = True
    int_computer = IntcodeComputer(deque(), deque(), code=code)
    while int_computer.op != '99':
        if start:
            color = WHITE
            start = False
        else:
            color = painted_pixels.get((x_, y_), BLACK)
        int_computer.in_que = deque([color])
        while len(int_computer.out_que) != 2:
            int_computer.run_prog(break_on_in=True, break_on_out=True)
            if int_computer.op == '99':
                break
            elif int_computer.op == '03' and len(int_computer.in_que) ==0:
                int_computer.in_que.append(color)

        if int_computer.op != '99':
            painted_pixels.update({(x_, y_): int_computer.out_que.pop()})
            (x_, y_), dir_ = turn(x_, y_, dir_, int_computer.out_que.pop())

    canvas = [[WHITE for _ in range(50)] for __ in range(7)]
    for pixel, color in painted_pixels.items():
        canvas[pixel[1]][pixel[0]] = color
    
    plt.imshow(canvas)
    plt.show()
