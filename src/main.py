from typing import cast

from .yahtzee import create_empty_scorecard, display_scorecard, play_round


def main() -> None:
    """Main game loop for Yahtzee."""
    print("Welcome to Yahtzee!")

    scorecard: dict[str, int | None] = create_empty_scorecard()

    for _ in range(13):
        scorecard = play_round(scorecard)
        display_scorecard(scorecard)

    assert all(value is not None for value in scorecard.values())

    scorecard_no_nones: dict[str, int] = cast(dict[str, int], scorecard)

    scores: tuple[int, ...] = tuple(scorecard_no_nones.values())

    if sum(scores[:6]) >= 63:
        print(f"\nGame over! Final score: {sum(scores) + 35}")
        return

    print(f"\nGame over! Final score: {sum(scores)}")


if __name__ == "__main__":
    main()
