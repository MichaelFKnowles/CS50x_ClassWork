def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


def main():
    height = get_int("Height: ")
    if height < 1 or height > 8:
        main()

    whitespace = " "
    i = 1
    while i < height + 1:
        print(whitespace * (height - i) + "#" * i + "  " + "#" * i)
        i += 1


main()
