# Refactoring Existing Code

Restructuring code that already works, often with weak or no tests. For the smell catalogue and post-green cleanup inside a TDD cycle, see `planning/references/refactoring.md`.

## 1. Before Touching Code
- **Goal and stop condition first.** State them so they can be checked: "`ingest` no longer imports `db`", "adding a sensor type touches one file", "`run()` under 10 branches". "Make it cleaner" is not a goal.
- **Chesterton's Fence:** follow `operational.md` before removing anything.
- **Pick targets by churn x complexity.** Code nobody changes is not worth refactoring.
  ```bash
  git log --since=1.year --format= --name-only | sort | uniq -c | sort -rn | head -20
  ruff check --select C901 src/   # McCabe complexity
  ```
- **Map the public surface:** everything imported outside the module, plus CLI flags, HTTP routes, serialized formats, DB schema, config keys, entry points in `pyproject.toml`. Changing the inside is cheap; changing these needs a migration (section 3).

## 2. Characterization Tests
Pin current behaviour, bugs included, before changing structure.
- **Test at the highest seam** that covers the code (CLI, public function, HTTP route). Tests bound to internals will break during the refactor and prove nothing.
- **Golden files:** run representative inputs once, save outputs, assert equality afterwards. Use real (scrubbed) production samples plus edge cases from the bug history.
- **Normalize nondeterminism:** timestamps, dict/set ordering, random seeds, float tolerance (`pytest.approx`, `np.testing.assert_allclose`).
- **Prove the net works:** break the code on purpose (or run `mutmut` on the module) and confirm a test fails.
- **Bugs found:** record them, keep the buggy behaviour pinned, fix in a separate commit after the refactor.

```python
GOLDEN_DIR = Path(__file__).parent / "golden"
CASES = sorted(GOLDEN_DIR.glob("*.input.json"))


@pytest.mark.parametrize("input_path", CASES, ids=lambda p: p.stem)
def test_process_matches_golden(input_path: Path) -> None:
    payload = json.loads(input_path.read_text())
    expected_path = input_path.with_name(input_path.name.replace(".input", ".expected"))
    expected = json.loads(expected_path.read_text())

    result = process(payload=payload)

    assert normalize(result) == normalize(expected)
```

Snapshot libraries (`syrupy`) work too. Never run `--snapshot-update` without reading the diff.

## 3. Safe-Step Techniques
Every step leaves the main branch green and deployable. No long-lived refactor branches.

| Situation                                               | Technique                                                                                                                                                                            |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Rename or reshape a public function, schema, config key | **Parallel change:** add new alongside old, migrate callers, delete old. One commit per phase.                                                                                       |
| Swap an implementation used in many places              | **Branch by abstraction:** route callers through one function, swap the implementation behind it, delete the old one. Inline the seam afterwards if only one implementation remains. |
| Replace a whole subsystem or service                    | **Strangler fig:** move one route or entry point at a time to the new code; the old code shrinks until it can be deleted.                                                            |
| Logic tangled with I/O, no tests possible               | **Extract a seam:** pull the pure logic into a function taking plain data; leave I/O in a thin shell.                                                                                |
| High-risk numeric or geospatial output                  | **Dual run:** run old and new on the same inputs, diff outputs with an explicit tolerance before switching.                                                                          |

```python
# Before: needs a database to test anything
def monthly_report(month: str) -> Report:
    rows = db.fetch_sales(month=month)
    ...  # 80 lines of aggregation


# After: pure core is testable with plain lists
def monthly_report(month: str) -> Report:
    rows = db.fetch_sales(month=month)
    report = build_report(rows=rows)
    return report


def build_report(rows: list[SaleRow]) -> Report:
    ...
```

For external users of a moved symbol, keep a re-export at the old path that emits a `DeprecationWarning`, and remove it on a stated version.

## 4. Mechanics
- **Moves and edits in separate commits.** Git only detects renames when content stays mostly similar; a move with edits shows as delete plus add.
- **Use tooling for renames** (IDE refactor, `rope`), then grep for what it misses: strings in `getattr`, `patch("pkg.mod.name")`, config files, docs, pickled objects, entry points.
- **After every step:** tests and type checker (`mypy`/`pyright` catch most breakage from moves).
- **Dead code:** `vulture`, then confirm with grep; dynamic use gives false positives.
- **Lock in new boundaries** with `import-linter` contracts in CI so the structure does not regress.

## 5. Stop Conditions
Stop when any holds:
- The goal from section 1 is met.
- The next change would not make the motivating feature or fix easier.
- Remaining smells are in code with low churn.

Rewrite from scratch only when the module is small, fully characterized, and incremental steps cost more than the rewrite. State that reasoning before starting.

## 6. Anti-patterns
- ❌ Refactor and behaviour change in the same commit.
- ❌ Silently fixing bugs found during the refactor (callers may depend on them).
- ❌ Adding abstractions "for later" while restructuring; refactoring should usually remove layers.
- ❌ Updating golden files or snapshots without reviewing the diff.
- ❌ A refactor branch that lives for weeks.
