# didn't quite understand the requirements. 
# found an elaboration of the requierments in 
# https://dev.to/jbristow/advent-of-code-2019-solution-megathread-day-4-secure-container-255c

from collections import defaultdict

def is_valid(number):
    number = str(number)
    prev_digit = None
   
    repeat_audit = defaultdict(lambda: 1)
    for each_digit in number:
        if prev_digit:
            if each_digit == prev_digit:
                repeat_audit[each_digit] += 1

            if each_digit < prev_digit:
                return False
            else:
                prev_digit = each_digit

        else:
            prev_digit = each_digit

    for each_digit, repeat_count in repeat_audit.items():
        if repeat_count == 2:
            return True

    return False


if __name__ == "__main__":
    assert(is_valid(112233))
    assert(not is_valid(123444))
    assert(is_valid(111122))

    count = 0
    for n_ in range(272091,815432):
        if is_valid(n_):
            count += 1

    print(count)


