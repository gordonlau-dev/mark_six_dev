import random


def generate_random_numbers(n):
    return random.sample(range(0, n), 1)[0]


def generate_initital_mark_six_list():
    list = []
    for i in range(49):
        list.append(i + 1)
    # print(*list, sep = ", ")
    # print("list: ", list)
    return list


def generate_17_units():
    list1 = generate_initital_mark_six_list()
    # print("list1: ", list1)
    # first round: generate 8 units
    unit1 = get_first_8_units(list1)
    # print("list1: ", list1)
    # print(" ")
    extra1 = list1[0]

    list2 = generate_initital_mark_six_list()
    # second round: generate 8 units
    unit2 = get_second_8_units(list1, list2)
    # print("list2: ", list2)
    # print(" ")
    extra2 = list2[0]
    extra3 = list2[1]

    list3 = generate_initital_mark_six_list()
    # third round: generate 1 units
    unit3 = get_last_1_unit(list2, list3)
    # print("list3: ", list3)
    # print(" ")

    # validate
    validate_dict = validate_count(unit1 + unit2 + unit3)

    units = unit1 + unit2 + unit3
    # print("units: ", units)
    return units, extra1, extra2, extra3


def generate_unit(list, pre_list=None):
    selected_items = []

    i = 0
    while i < 6:
        if pre_list:
            s = 0
            selected_items.append(pre_list.pop(s))
            selected_items.sort()
            i += 1
        else:
            s = generate_random_numbers(len(list))
            # print("selected s: ", s)
            if list[s] not in selected_items:
                selected_items.append(list.pop(s))
                selected_items.sort()
                i += 1
            else:
                # print("item exist in list: ", list[s])
                pass

        # print("selected_items: ", selected_items)

    return selected_items


def get_first_8_units(list):
    units = []
    for i in range(8):
        selected_items = generate_unit(list)
        units.append(selected_items)
    # print("list: ", list)
    return units


# list1 is the remaining one number from the first round
# list2 is the list of 49 numbers
def get_second_8_units(list1, list2):
    units = []
    for i in range(8):
        selected_items = generate_unit(list2, list1)
        units.append(selected_items)
    # print("list: ", list2)
    return units


# list1 is the remaining two number from the second round
# list2 is the list of 49 numbers
def get_last_1_unit(list1, list2):
    selected_items = generate_unit(list2, list1)
    return [selected_items]


def validate_count(units):
    # initial count = 0
    dict = {}
    for i in range(49):
        dict[i + 1] = 0

    for unit in units:
        for i in unit:
            dict[i] += 1

    # print("dict: ", dict)
    return dict


def generate_n1_to_n7():
    list = generate_initital_mark_six_list()
    selected_items = generate_unit(list)
    valid_extra_number = False
    while not valid_extra_number:
        _e = generate_random_numbers(49)
        if _e not in selected_items:
            selected_items.append(_e)
            valid_extra_number = True
    return (
        selected_items[0],
        selected_items[1],
        selected_items[2],
        selected_items[3],
        selected_items[4],
        selected_items[5],
        selected_items[6],
    )


def recursive_generate(match_dict, try_count, n1, n2, n3, n4, n5, n6, n7):
    if try_count > 0 or try_count < -3:
        if try_count < -3:
            try_count = 1
        for i in range(try_count):
            results, e1, e2, e3 = generate_17_units()

            for unit in results:
                match_count = 0
                for number in unit:
                    if str(number) == str(n1):
                        match_count += 1
                        continue
                    if str(number) == str(n2):
                        match_count += 1
                        continue
                    if str(number) == str(n3):
                        match_count += 1
                        continue
                    if str(number) == str(n4):
                        match_count += 1
                        continue
                    if str(number) == str(n5):
                        match_count += 1
                        continue
                    if str(number) == str(n6):
                        match_count += 1
                        continue
                    if str(number) == str(n7):
                        match_count += 0.5
                        continue
                match_dict[str(match_count)] += 1
        return try_count
    elif try_count < 0:
        # _type: -1 = first prize, -2 = second prize, -3 = third prize
        _type = try_count
        try_count = 0
        found = False

        while not found:
            results, e1, e2, e3 = generate_17_units()

            for unit in results:
                match_count = 0
                for number in unit:
                    if str(number) == str(n1):
                        match_count += 1
                    if str(number) == str(n2):
                        match_count += 1
                    if str(number) == str(n3):
                        match_count += 1
                    if str(number) == str(n4):
                        match_count += 1
                    if str(number) == str(n5):
                        match_count += 1
                    if str(number) == str(n6):
                        match_count += 1
                    if str(number) == str(n7):
                        match_count += 0.5
                match_dict[str(match_count)] += 1

            try_count += 1
            if _type == -1 and match_dict["6"] == 1:
                found = True
            if _type == -2 and match_dict["5.5"] == 1:
                found = True
            if _type == -3 and match_dict["5"] == 1:
                found = True

        return try_count
