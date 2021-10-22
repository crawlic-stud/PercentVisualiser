def all_divs(number):
    """Finding all dividers of the number."""
    dividers = []
    for i in range(1, number + 1):
        if number % i == 0:
            dividers.append(i)
    return dividers


def closest_divs(number):
    """Finding two closest dividers of the number."""
    dividers = all_divs(number)
    center = dividers[len(dividers)//2]
    return center, int(number / center)
