import random
import sys
from collections import Counter
from collections.abc import Mapping, MutableMapping, Sequence
from typing import cast


def roll_dice(number_of_dice: int = 5) -> list[int]:
    """Roll n dice with values between 1-6.

    Args:
        number_of_dice (int, optional): Number of dice to be rolled. Defaults to 5.

    Raises:
        ValueError: Raised if n is outside of the defined 1 to 5 boundary .

    Returns:
        list[int]: List containing the rolls of the dice.
    """
    try:
        if not (1 <= number_of_dice <= 5):
            raise ValueError("Number of dice out of range")

        return [random.randint(1, 6) for _ in range(number_of_dice)]

    except ValueError as e:
        print(f"{type(e).__name__}: {e}")
        sys.exit(1)


def create_empty_scorecard() -> dict[str, int | None]:
    """Helper function to create an empty Yahtzee scorecard.

    Returns:
        dict[str, int | None]: Dictionary with keys for each score category, initialized to None.
    """
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


def select_keep(dice: Sequence[int]) -> list[int]:
    """Prompt user to select which dice to keep.

    Args:
        dice (list[int]): Current dice values.

    Returns:
        list[int]: List of dice values that the user wants to keep.
    """
    print(dice)
    dice_counts: Counter[int] = Counter(dice)

    while True:
        dice_to_keep_string: str = input(
            "Select which dice to keep. This should be a string with the value of the dice you want to keep: "
        ).strip()

        if dice_to_keep_string == "":
            return []

        if not dice_to_keep_string.isdigit():
            print("Invalid string.")
            continue

        if not len(dice_to_keep_string) <= 5:
            print("Invalid string.")
            continue

        kept_dice: list[int] = [int(i) for i in dice_to_keep_string]

        kept_dice_counts: Counter[int] = Counter(kept_dice)

        for face, count in kept_dice_counts.items():
            if count > dice_counts[int(face)]:
                print("Invalid string")
                break
        else:
            return kept_dice


def reroll(kept_dice: list[int]) -> list[int]:
    """Reroll dice that weren't kept.

    Args:
        kept_dice (list[int]): Dice values that the user chose to keep.

    Returns:
        list[int]: New list of dice values after rerolling the non-kept dice.
    """
    """Reroll dice that weren't kept."""
    return kept_dice + roll_dice(5 - len(kept_dice))


def has_straight(dice: Sequence[int], length: int) -> bool:
    """Check for straights (sequences) in dice.

    Args:
        dice (list[int]): Current dice values.
        length (int): Length of the straight to check for (4 or 5).

    Returns:
        bool: True if a straight of the specified length exists, False otherwise.
    """
    sorted_dice: list[int] = sorted(dice)
    if length == 5:
        if sorted_dice == [1, 2, 3, 4, 5] or sorted_dice == [2, 3, 4, 5, 6]:
            return True
        return False
    if (
        all(e in sorted_dice for e in [1, 2, 3, 4])
        or all(e in sorted_dice for e in [2, 3, 4, 5])
        or all(e in sorted_dice for e in [3, 4, 5, 6])
    ):
        return True
    return False


def evaluate(dice: Sequence[int]) -> dict[str, int]:
    """Calculate scores for all possible categories based on current dice.

    Args:
        dice (list[int]): Current dice values.

    Returns:
        dict[str, int]: Dictionary with scores for each category based on the current dice.
    """
    counts: Counter[int] = Counter(dice)
    total: int = sum(dice)
    two_most_common_dice_faces: list[tuple[int, int]] = counts.most_common(2)
    count_most_common: int = two_most_common_dice_faces[0][1]
    has_lg_straight: bool = has_straight(dice, 5)

    scores: dict[str, int] = {
        "ones": counts[1],
        "twos": counts[2] * 2,
        "threes": counts[3] * 3,
        "fours": counts[4] * 4,
        "fives": counts[5] * 5,
        "sixes": counts[6] * 6,
        "three_of_a_kind": total if count_most_common == 3 else 0,
        "four_of_a_kind": total if count_most_common == 4 else 0,
        "full_house": 25
        if two_most_common_dice_faces[0][1] == 3
        and two_most_common_dice_faces[1][1] == 2
        else 0,
        "four_straight": 30 if has_lg_straight or has_straight(dice, 4) else 0,
        "five_straight": 40 if has_lg_straight else 0,
        "yahtzee": 50 if count_most_common == 5 else 0,
        "chance": total,
    }

    return scores


def choose(scores: Mapping[str, int], used: Sequence[str]) -> tuple[str, int]:
    """Present available scoring options to player and get their selection.

    Returns:
        tuple[str, int]: Chosen score category and its value.
    """
    available_scores: dict[str, int] = {
        k: v for k, v in scores.items() if k not in used
    }

    while True:
        print("Available Scores")
        for i, (k, v) in enumerate(available_scores.items()):
            print(f"{i + 1}. {k}: {v}")

        chosen_category = input("Select an available scoring option: ")

        if not chosen_category.isdigit():
            print("Invalid input.")
            continue

        if int(chosen_category) not in range(1, len(available_scores) + 1):
            print("Invalid input.")
            continue

        chosen_score: tuple[str, int] = tuple(available_scores.items())[
            int(chosen_category) - 1
        ]

        return chosen_score


def display_scorecard(
    card: Mapping[str, int | None],
) -> None:
    """Display current scorecard with all categories and their scores.

    Args:
        card (Mapping[str, int | None]): Current scorecard.
    """
    print("Current Scorecard")
    for k, v in card.items():
        print(f"{k}: {v if v is not None else '-'}")


def play_round(card: MutableMapping[str, int | None]) -> dict[str, int | None]:
    """Play one round of Yahtzee with 3 rolls.

    Args:
        card (Mapping[str, int | None]): Current scorecard.
    """
    """Play one round of Yahtzee with 3 rolls."""
    dice: list[int] = roll_dice()

    for _ in range(2):
        kept_dice: list[int] = select_keep(dice)

        if len(kept_dice) == 5:
            break

        dice = reroll(kept_dice)

    print(f"Final dice: {dice}")
    new_score: tuple[str, int] = choose(
        evaluate(dice), [k for k, v in card.items() if v is not None]
    )

    card[new_score[0]] = new_score[1]

    return cast(dict[str, int | None], card)
