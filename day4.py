
def is_valid(number):
    number = str(number)
    prev_digit = None
    have_double = False
    for each_digit in number:
        if prev_digit:
            if each_digit == prev_digit:
                have_double = True

            if each_digit < prev_digit:
                return False
            else:
                prev_digit = each_digit

        else:
            prev_digit = each_digit
    return have_double


if __name__ == "__main__":
    assert(is_valid(111111))
    assert(not is_valid(223450))
    assert(not is_valid(123789))

    count = 0
    for n_ in range(272091,815432):
        if is_valid(n_):
            count += 1

    print(count)


