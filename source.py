def add(*numbers: float) -> None:
    print(f"{' + '.join(map(str, numbers))} = {sum(numbers)}")


add(1, 2, 3)
add(4, 5, "6")  # Argument 3 has incorrect type
