def is_palindrome(string):
    filter_string = list(string.lower().replace(' ', ''))
    print(filter_string)

    l, r = 0, len(filter_string) - 1
    while l < r:
        if filter_string[l] != filter_string[r]:
            return False
        l += 1
        r -= 1

    return True


# Должно быть напечатано True:
print(is_palindrome('А роза упала на лапу Азора'))
# Должно быть напечатано False:
print(is_palindrome('Не палиндром'))