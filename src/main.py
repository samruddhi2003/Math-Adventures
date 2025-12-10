import time
from typing import Optional

from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine


def ask_for_difficulty() -> str:
    """
    Ask the user for an initial difficulty level.
    """
    choices = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        print("\nChoose starting difficulty:")
        print("  1) Easy")
        print("  2) Medium")
        print("  3) Hard")
        choice = input("Enter 1, 2, or 3: ").strip()

        if choice in choices:
            return choices[choice]

        print("Invalid choice. Please try again.")


def parse_answer(raw: str) -> Optional[int]:
    """
    Try to parse the user's answer as an int.
    Returns None if parsing fails.
    """
    raw = raw.strip()
    if not raw:
        return None

    try:
        return int(raw)
    except ValueError:
        return None


def run_session(num_questions: int = 10) -> None:
    print("Welcome to Math Adventures — Adaptive Learning Prototype!")
    name = input("What is your name? ").strip() or "Learner"

    initial_level = ask_for_difficulty()

    generator = PuzzleGenerator()
    tracker = PerformanceTracker()
    engine = AdaptiveEngine(initial_level=initial_level)

    print(f"\nHi {name}! Let's get started 🚀")
    print("Type 'q' at any time to quit.\n")

    for i in range(1, num_questions + 1):
        current_level = engine.current_level
        puzzle = generator.generate(current_level)

        print(f"Question {i} (Difficulty: {current_level.capitalize()}):")
        print(f"  {puzzle.question}")

        start_time = time.perf_counter()
        raw_answer = input("Your answer (or 'q' to quit): ").strip()
        end_time = time.perf_counter()
        time_taken = end_time - start_time

        if raw_answer.lower() == "q":
            print("\nYou chose to end the session early.")
            break

        user_answer = parse_answer(raw_answer)
        correct = (user_answer == puzzle.answer)

        if user_answer is None:
            print(f"  That wasn't a valid number. The correct answer was {puzzle.answer}.")
        elif correct:
            print("  ✅ Correct! Well done!")
        else:
            print(f"  ❌ Not quite. The correct answer was {puzzle.answer}.")

        tracker.log_attempt(
            question=puzzle.question,
            correct_answer=puzzle.answer,
            user_answer=user_answer,
            correct=correct,
            time_taken=time_taken,
            difficulty=puzzle.difficulty,
        )

        # Update difficulty based on recent performance
        recent_results = tracker.recent_correctness(n=engine.window_size)
        new_level = engine.update_level(recent_results)

        print(f"  Time taken: {time_taken:.2f} seconds")
        print(f"  Next difficulty will be: {new_level.capitalize()}")
        print("-" * 40)

    print_session_summary(name, tracker, engine)


def print_session_summary(name: str, tracker: PerformanceTracker, engine: AdaptiveEngine) -> None:
    print("\n=== Session Summary ===")
    if tracker.total_attempts == 0:
        print("No questions were answered. See you next time!")
        return

    accuracy_percent = tracker.accuracy * 100

    print(f"Learner: {name}")
    print(f"Total Questions Answered: {tracker.total_attempts}")
    print(f"Correct: {tracker.num_correct}")
    print(f"Incorrect: {tracker.num_incorrect}")
    print(f"Accuracy: {accuracy_percent:.1f}%")
    print(f"Average Time per Question: {tracker.average_time:.2f} seconds")
    print(f"Recommended Next Level: {engine.current_level.capitalize()}")

    print("\nThanks for playing Math Adventures! 🎉")


if __name__ == "__main__":
    run_session()
