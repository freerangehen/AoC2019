import numpy as np
from math import gcd



SLICE_MAP = {0: [1, 2, 3],
             1: [0, 2, 3],
             2: [0, 1, 3],
             3: [0, 1, 2]}
            

def apply_gravity(moon_pos, moon_vel):

    for moon_idx in range(4):
        other_moons = moon_pos[SLICE_MAP[moon_idx]]
        moon_vel[moon_idx] += \
            np.sign(-moon_pos[moon_idx] + other_moons).sum(axis=0)

    return moon_vel


def apply_velocity(moon_pos, moon_vel):
    moon_pos += moon_vel
    return moon_pos


def calc_total_energy(moon_pos, moon_vel):

    potential_energy = np.abs(moon_pos).sum(axis=1)
    kinetic_energy = np.abs(moon_vel).sum(axis=1)
    return np.dot(potential_energy, kinetic_energy)


def part_I():

    moon_pos = np.array([[-1, 7, 3],
                         [12, 2, -13],
                         [14, 18, -8],
                         [17, 4, -4]])

    moon_vel = np.array([[0, 0, 0] for _ in range(4)])


    for step in range(1, 1001):
        moon_vel = apply_gravity(moon_pos, moon_vel)
        moon_pos = apply_velocity(moon_pos, moon_vel)

    print(calc_total_energy(moon_pos, moon_vel))


def part_II():

    moon_pos = np.array([[-1, 7, 3],
                         [12, 2, -13],
                         [14, 18, -8],
                         [17, 4, -4]])

    moon_vel = np.array([[0, 0, 0] for _ in range(4)])

    step = 1
    # have to get this from Reddit - LCM of independent periods
    pos_periods = {}
    vel_periods = {}
    while True:
        moon_vel = apply_gravity(moon_pos, moon_vel)
        vel_n, vel_m = np.where(moon_vel == 0)
        for n_, m_ in zip(vel_n, vel_m):
            if (n_, m_) not in vel_periods:
                vel_periods.update({(n_, m_): step})
            vel_periods.update({(n_, m_): step})
        
        moon_pos = apply_velocity(moon_pos, moon_vel)
        pos_n, pos_m = np.where(moon_pos == 0)
        for n_, m_ in zip(pos_n, pos_m):
            if (n_, m_) not in pos_periods:
                pos_periods.update({(n_, m_): step})

        if len(pos_periods) == 12 and len(vel_periods) == 12:
            break
        step += 1

    all_periods = [val for _, val in pos_periods.items()] + [val for _, val in vel_periods.items()]
    print(all_periods)
    print(lcm(all_periods))


def lcm(input):
    lcm_ = input[0]
    for n_ in input[1:]:
      lcm_ = int(lcm_*n_/gcd(lcm_, n_))
    return lcm_


if __name__ == "__main__":
    test_moon_pos = np.array([[-1, 0, 2],
                              [2, -10, -7],
                              [4, -8, 8],
                              [3, 5, -1]])

    test_moon_vel = np.array([[0, 0, 0] for _ in range(4)])
    for step in range(1, 11):
        test_moon_vel = apply_gravity(test_moon_pos, test_moon_vel)
        test_moon_pos = apply_velocity(test_moon_pos, test_moon_vel)

    assert((test_moon_pos == np.array([[2, 1, -3], [1, -8, 0], [3, -6, 1], [2, 0, 4]])).all())
    assert((test_moon_vel == np.array([[-3, -2, 1], [-1, 1, 3], [3, 2, -3], [1, -1, -1]])).all())
    assert(calc_total_energy(test_moon_pos, test_moon_vel) == 179)

    part_I()

    part_II()
