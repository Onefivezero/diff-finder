# Diff Finder

Python project for finding differences between two objects.
Designed for nested structures with sequences and mappings.

## Usage

```
from diff_finder import DiffFinder
from pprint import pp

[desc: a='different-0' != b='different-1', path: .different,
 desc: a=3 != b=10, path: .nested_field.list_of_numbers[2],
 desc: a=4 != b=20, path: .nested_field.list_of_numbers[3],
 desc: a=10 != b=5, path: .nested_field.different_number]
struct_a = {
    "same": "same",
    "different": "different-0",
    "nested_field": {
        "same_number": 1,
        "different_number": 10,
        "list_of_numbers": [1, 2, 3, 4],
    },
}
struct_b = {
    "same": "same",
    "different": "different-1",  # different-0 != different-1
    "nested_field": {
        "same_number": 1,
        "different_number": 5,  # 10 != 5
        "list_of_numbers": [1, 2, 10, 20],  # 3, 4 != 10, 20
    },
}

diffs = DiffFinder.find_diffs(struct_a, struct_b)
pp(diffs)

# [desc: a='different-0' != b='different-1', path: .different,
# desc: a=3 != b=10, path: .nested_field.list_of_numbers[2],
# desc: a=4 != b=20, path: .nested_field.list_of_numbers[3],
# desc: a=10 != b=5, path: .nested_field.different_number]
```
