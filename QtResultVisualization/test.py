def printOut(a: int) -> None:
    a -= 1
    print(a)

    if a <= 8:
        a += 4
        printOut(a)

    print(a*2)

printOut(1)