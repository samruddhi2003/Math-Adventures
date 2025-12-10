from typing import List


class AdaptiveEngine:
    """
    Rule-based adaptive engine.

    Uses recent correctness history to adjust difficulty:

    - If recent accuracy ≥ up_threshold → increase difficulty (if possible)
    - If recent accuracy ≤ down_threshold → decrease difficulty (if possible)
    - Otherwise → keep same difficulty
    """

    def __init__(
        self,
        initial_level: str = "easy",
        window_size: int = 5,
        up_threshold: float = 0.8,
        down_threshold: float = 0.5,
    ) -> None:
        self.levels = ["easy", "medium", "hard"]
        self.window_size = window_size
        self.up_threshold = up_threshold
        self.down_threshold = down_threshold

        initial_level = initial_level.lower()
        if initial_level not in self.levels:
            initial_level = "easy"
        self.current_index = self.levels.index(initial_level)

    @property
    def current_level(self) -> str:
        return self.levels[self.current_index]

    def _decide_new_level(self, recent_results: List[bool]) -> str:
        if not recent_results:
            return self.current_level

        accuracy = sum(recent_results) / len(recent_results)

        # Doing well → move up
        if accuracy >= self.up_threshold and self.current_index < len(self.levels) - 1:
            self.current_index += 1

        # Struggling → move down
        elif accuracy <= self.down_threshold and self.current_index > 0:
            self.current_index -= 1

        return self.current_level

    def update_level(self, recent_results: List[bool]) -> str:
        """
        Given recent correctness history, update and return the new difficulty level.
        """
        return self._decide_new_level(recent_results)
