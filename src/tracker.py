from dataclasses import dataclass
from typing import List, Optional
from statistics import mean


@dataclass
class Attempt:
    question: str
    correct_answer: int
    user_answer: Optional[int]
    correct: bool
    time_taken: float
    difficulty: str


class PerformanceTracker:
    """
    Tracks learner performance across the session:
    correctness, time taken, and difficulty.
    """

    def __init__(self) -> None:
        self.attempts: List[Attempt] = []

    def log_attempt(
        self,
        question: str,
        correct_answer: int,
        user_answer: Optional[int],
        correct: bool,
        time_taken: float,
        difficulty: str,
    ) -> None:
        self.attempts.append(
            Attempt(
                question=question,
                correct_answer=correct_answer,
                user_answer=user_answer,
                correct=correct,
                time_taken=time_taken,
                difficulty=difficulty,
            )
        )

    # ---------- Summary Properties ----------

    @property
    def total_attempts(self) -> int:
        return len(self.attempts)

    @property
    def num_correct(self) -> int:
        return sum(1 for a in self.attempts if a.correct)

    @property
    def num_incorrect(self) -> int:
        return sum(1 for a in self.attempts if not a.correct)

    @property
    def accuracy(self) -> float:
        if not self.attempts:
            return 0.0
        return self.num_correct / self.total_attempts

    @property
    def average_time(self) -> float:
        if not self.attempts:
            return 0.0
        return mean(a.time_taken for a in self.attempts)

    def recent_correctness(self, n: int = 5) -> List[bool]:
        """
        Returns a list of correctness values (True/False)
        for the last `n` attempts.
        """
        return [a.correct for a in self.attempts[-n:]]
