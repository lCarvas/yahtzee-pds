import random
import sys
from collections import Counter


def roll_dice(number_of_dice: int, kept_dice: int = 0) -> list[int]:
    try:
        if not (1 <= number_of_dice + kept_dice <= 5):
            raise ValueError("Number of dice out of range")

        # def dice_generator(number_of_dice: int) -> Generator[int]:
        #     for _ in range(number_of_dice):
        #         yield random.randint(1, 6)

        # return dice_generator(number_of_dice)
        return [random.randint(1, 6) for _ in range(number_of_dice)]

    except ValueError as e:
        print(f"{type(e).__name__}: {e}")
        sys.exit(1)


def create_empty_dictionary() -> dict[str, None]:
    return {
        "1": None,
        "2": None,
        "3": None,
        "4": None,
        "5": None,
        "6": None,
        "three_of_a_kind": None,
        "four_of_a_kind": None,
        "full_house": None,
        "four_straight": None,
        "five_straight": None,
        "yahtzee": None,
    }


def select_keep(dice: list[int]) -> list[int]:
    print(dice)
    while not (
        (
            dice_to_keep_string := input(
                "Select which dice to keep. This should be a string with the position of the dice you want to keep. e.g. '123' would keep the first 3 dice"
            )
        )
        and dice_to_keep_string.isdigit()
        and len(dice_to_keep_string) <= 5
    ):
        print("Invalid string.")
        print(dice)

    for i in dice_to_keep_string:
        dice.pop(int(i) - 1)

    return dice


def has_straight(dice: list[int], length: int) -> bool:
    sorted_dice: list[int] = sorted(dice)
    if length == 5:
        if sorted_dice == [1, 2, 3, 4, 5] or sorted_dice == [2, 3, 4, 5, 6]:
            return True
        return False
    if (
        [1, 2, 3, 4] in sorted_dice
        or [2, 3, 4, 5] in sorted_dice
        or [3, 4, 5, 6] in sorted_dice
    ):
        return True
    return False


def evaluate(dice: list[int]):
    # counts: Counter[int] = Counter(dice)
    NotImplemented
