import random
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Puzzle:
    question: str
    answer: int
    difficulty: str
    operation: str


class PuzzleGenerator:
    """
    Generates simple math puzzles for different difficulty levels.
    Designed for children aged 5–10.
    """

    def __init__(self) -> None:
        # You can tune these ranges and operations.
        self.difficulty_settings = {
            "easy": {
                "range": (0, 10),
                "operations": ["+", "-"],
            },
            "medium": {
                "range": (0, 20),
                "operations": ["+", "-", "*"],
            },
            "hard": {
                "range": (1, 50),  # start from 1 for safer division
                "operations": ["+", "-", "*", "/"],
            },
        }

    def _get_range(self, difficulty: str) -> Tuple[int, int]:
        return self.difficulty_settings[difficulty]["range"]

    def _get_operations(self, difficulty: str) -> List[str]:
        return self.difficulty_settings[difficulty]["operations"]

    def generate(self, difficulty: str) -> Puzzle:
        """
        Generate a single puzzle at the given difficulty level.
        """
        difficulty = difficulty.lower()
        if difficulty not in self.difficulty_settings:
            raise ValueError(f"Unknown difficulty: {difficulty}")

        num_range = self._get_range(difficulty)
        operations = self._get_operations(difficulty)
        op = random.choice(operations)

        a = random.randint(*num_range)
        b = random.randint(*num_range)

        # Make division safe & clean (integer results only)
        if op == "/":
            b = random.randint(1, num_range[1])  # no zero
            result = random.randint(1, num_range[1])
            a = b * result
            question = f"{a} ÷ {b}"
            answer = result
        elif op == "+":
            question = f"{a} + {b}"
            answer = a + b
        elif op == "-":
            question = f"{a} - {b}"
            answer = a - b
        elif op == "*":
            question = f"{a} × {b}"
            answer = a * b
        else:
            raise ValueError(f"Unsupported operation: {op}")

        return Puzzle(
            question=question,
            answer=answer,
            difficulty=difficulty,
            operation=op,
        )
