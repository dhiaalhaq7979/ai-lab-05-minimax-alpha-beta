# AI Lab 05 — Adversarial Search: Minimax and Alpha-Beta Pruning

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-success?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

This lab covers search in **two-player games**. One player (MAX) tries to get the highest score and the other (MIN) the lowest. I implemented **Minimax**, then **Alpha-Beta pruning**, counted how many leaves each one evaluates, and tested how the **order of moves** affects pruning.

## Structure

```
ai-lab-05-minimax-alpha-beta/
├── run_lab.py
├── games/
│   ├── minimax_search.py     # manual minimax + leaf counter + backed-up values
│   ├── alphabeta_search.py   # manual alpha-beta + counting version with cut log
│   └── analysis.py           # Task 2 comparison and Task 3 ordering experiment
└── results/
    └── sample_run.txt
```

## Run

```bash
python run_lab.py
```

## Task 1 — Minimax on the manual tree

Leaves `[3, 5, 2, 9, 0, 7]` padded with zeros to 8 leaves (depth 3):

| Level | Player | Values |
|-------|--------|--------|
| 0 | MAX | **5** |
| 1 | MIN | 5, 0 |
| 2 | MAX | 5, 9, 7, 0 |
| 3 | leaves | 3, 5, 2, 9, 0, 7, 0, 0 |

## Task 2 — How many leaves are evaluated?

| Tree | Value | Minimax | Alpha-Beta |
|------|-------|---------|------------|
| Manual 5.2 `[3,5,2,9,3,5,2,9]` | 5 | 8 | **6** |
| Manual 5.1 (padded) | 5 | 8 | 8 |
| My tree `[4,8,1,6,7,2,9,3]` | 7 | 8 | **7** |

Alpha-Beta always returns the **same value** as Minimax — it only skips branches that cannot change the decision.

## Task 3 — Move ordering

| Ordering (my tree) | Value | Alpha-Beta leaves |
|--------------------|-------|-------------------|
| best child first everywhere | 7 | **5** |
| as given | 7 | 7 |
| right MIN children swapped | 7 | 8 |
| worst child first everywhere | 7 | 8 |

Good move ordering lets Alpha-Beta prune much more, and bad ordering removes the benefit completely. The value never changes. (The same pattern appears on the manual 5.2 tree: 5 leaves best-first, 8 worst-first.)

## Note on padding

The zeros added to complete the 5.1 tree act like real moves for MIN. With padding = 99 the result is 7, which is the true value of the original 6-leaf game. Padding is a convenience, but it can change the answer.

## Author

**Dheya Alhag** — BS Software Engineering, Superior University, Lahore
GitHub: [@dhiaalhaq7979](https://github.com/dhiaalhaq7979)

Licensed under the [MIT License](LICENSE).
