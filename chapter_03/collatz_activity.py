from temporalio import activity

import matplotlib.pyplot as plt


@activity.defn
async def collatz(number):
    """Collatz the number and print each step and tracks the number of them."""
    number = int(number)
    if number > 1:
        steps = 0
        num_list = []
        while number != 1:
            if number % 2 == 0:
                print(int(number / 2))
                number = number / 2
                num_list.append(int(number))
                steps += 1
            else:
                print(int(number * 3 + 1))
                number = number * 3 + 1
                num_list.append(int(number))
                steps += 1

        return num_list, steps


@activity.defn
async def graph(num_list, filename="collatz_sequence.png"):
    """Plot a graph of the numbers in num_list and save it to a file."""
    if not num_list:
        raise ValueError("num_list is empty")
    plt.plot(num_list)
    plt.ylabel("Numbers")
    plt.xlabel("Steps")
    plt.title("Collatz Sequence Graph")
    with open(filename, "wb") as f:
        plt.savefig(f)
    plt.show()
    return filename
