"""Entry point for AI Lab 05. Run with:  python run_lab.py"""
import sys

from games import analysis, minimax_search


if __name__ == "__main__":
    print("AI Lab 05 - Adversarial Search: Minimax and Alpha-Beta Pruning")
    print("Student: Dheya Alhag | BS Software Engineering")
    print(f"Python {sys.version.split()[0]} (standard library only)")
    print()
    minimax_search.run()
    print()
    analysis.run()
