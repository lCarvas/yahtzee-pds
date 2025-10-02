import random
import sys
from collections import Counter


def roll_dice(number_of_dice: int = 5) -> list[int]:
    try:
        if not (1 <= number_of_dice <= 5):
            raise ValueError("Number of dice out of range")

        return [random.randint(1, 6) for _ in range(number_of_dice)]

    except ValueError as e:
        print(f"{type(e).__name__}: {e}")
        sys.exit(1)


def create_empty_scorecard() -> dict[str, None]:
    return {
        "ones": None,
        "twos": None,
        "threes": None,
        "fours": None,
        "fives": None,
        "sixes": None,
        "three_of_a_kind": None,
        "four_of_a_kind": None,
        "full_house": None,
        "four_straight": None,
        "five_straight": None,
        "yahtzee": None,
        "chance": None,
    }


def select_keep(dice: list[int]) -> list[int]:
    print(dice)
    dice_counts: Counter[int] = Counter(dice)
    while not (
        (
            dice_to_keep_string := input(
                "Select which dice to keep. This should be a string with the value of the dice you want to keep: "
            )
        )
        and dice_to_keep_string.isdigit()
        and len(dice_to_keep_string) <= 5
        and (
            (str_counts := (Counter([i for i in dice_to_keep_string])))["1"]
            <= dice_counts[1]
            and str_counts["2"] <= dice_counts[2]
            and str_counts["3"] <= dice_counts[3]
            and str_counts["4"] <= dice_counts[4]
            and str_counts["5"] <= dice_counts[5]
            and str_counts["6"] <= dice_counts[6]
        )
    ):
        print("Invalid string.")
        print(dice)

    kept_dice: list[int] = [int(i) for i in dice_to_keep_string]

    return kept_dice


def reroll(kept_dice: list[int]) -> list[int]:
    """Reroll dice that weren't kept."""
    return kept_dice + roll_dice(5 - len(kept_dice))


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


def evaluate(dice: list[int]) -> dict[str, int]:
    counts: Counter[int] = Counter(dice)
    total: int = sum(dice)
    len_most_common: int = counts.most_common(1)[0][1]
    full_house_check: list[tuple[int, int]] = counts.most_common(2)

    scores: dict[str, int] = {
        "ones": counts[1],
        "twos": counts[2] * 2,
        "threes": counts[3] * 3,
        "fours": counts[4] * 4,
        "fives": counts[5] * 5,
        "sixes": counts[6] * 6,
        "three_of_a_kind": total if len_most_common == 3 else 0,
        "four_of_a_kind": total if len_most_common == 4 else 0,
        "full_house": 25
        if full_house_check[0][1] == 3 and full_house_check[1][1] == 2
        else 0,
        "four_straight": 30 if has_straight(dice, 4) else 0,
        "five_straight": 40 if has_straight(dice, 5) else 0,
        "yahtzee": 50 if len_most_common == 5 else 0,
        "chance": total,
    }

    return scores


def choose(scores: dict[str, None] | dict[str, int | None], used: list[str]):
    """Present available scoring options to player and get their selection."""

    available_scores: list[str] = [k for k, v in scores.items() if v is None]

    print("Available Scores")
    for i, option in enumerate(available_scores):
        print(f"{i + 1}. {option}")

    while not (
        (chosen_score := input("Select an available scoring option: "))
        and chosen_score.isdigit()
        and int(chosen_score) <= len(available_scores)
    ):
        print("Invalid string.")
        print("Available Scores")
        for i, option in enumerate(available_scores):
            print(f"{i + 1}. {option}")

    # chosen_score = int(input("Select the index of an available scoring option"))
    # if 0 < chosen_score <= len(scores):
    #     return scores.keys()[chosen_score]
    # if chosen_score == 0:
    #     return False


choose(create_empty_scorecard(), [])
