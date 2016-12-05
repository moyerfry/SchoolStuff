test_count = 0


def check_expect(actual, expected, description=''):
    global test_count
    test_count += 1
    print_string = "Test " + str(test_count) + " {0}" + (": " + description if description else "")
    if actual == expected:
        print print_string.format("passed")
    else:
        print print_string.format('failed') + "\n" + str(expected) + "\n" + str(actual)


def check_true(value, description=''):
    global test_count
    test_count += 1
    print_string = "Test " + str(test_count) + " {0}" + (": " + description if description else "")
    if value:
        print print_string.format("passed")
    else:
        print print_string.format("failed")


def check_false(value, description=''):
    check_true(not value, description)
