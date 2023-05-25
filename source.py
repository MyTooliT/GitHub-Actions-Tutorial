from pathlib import Path

example_path = Path("some") / "directory" / "something.txt"
example_path_changed_stem = example_path.with_stem("something else")

print(f"Original:     {example_path}")
print(f"Changed stem: {example_path_changed_stem}")
