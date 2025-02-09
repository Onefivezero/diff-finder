from collections.abc import Sequence, Mapping
from pprint import pformat
from typing import Any

class DiffReason:
    description: str
    path: str

    def __init__(self, description: str, path: str):
        self.description = description
        self.path = path
    
    def __str__(self) -> str:
        return f"desc: {self.description}, path: {self.path}"

    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, DiffReason):
            return False
        return self.description == other.description and self.path == other.path
    

class _Differ:
    separator_char: str
    diffs: list[DiffReason]

    def __init__(self):
        self.diffs = []
        self.separator_char = "."
    
    def _add_reason(self, description: str, path: str):
        self.diffs.append(DiffReason(description, path))

    def _find_diffs(self, a: Any, b: Any, path: str):
        if not set(type(a).__mro__).intersection(type(b).__mro__).difference({object}):
            self._add_reason(description=f"{a=} != {b=}", path=path)
            return
        
        if isinstance(a, Sequence) and isinstance(b, Sequence) and not isinstance(a, str) and not isinstance(b, str):
            if len(a) != len(b):
                self._add_reason(description=f"{a=} != {b=}", path=path)
                return
    
            for i, (a_i, b_i) in enumerate(zip(a, b)):
                self._find_diffs(a_i, b_i, path=f"{path}[{i}]")
            return
        
        if isinstance(a, Mapping) and isinstance(b, Mapping):
            common_keys = set(a.keys()).intersection(b.keys())
            a_unique_keys = set(a.keys()).difference(common_keys)
            b_unique_keys = set(b.keys()).difference(common_keys)

            if a_unique_keys:
                self._add_reason(f"a has keys: {a_unique_keys} that b does not.", path)
            if b_unique_keys:
                self._add_reason(f"b has keys: {b_unique_keys} that a does not.", path)
            
            for key in common_keys:
                self._find_diffs(a[key], b[key], f"{path}{self.separator_char}{key}")
            return
    
        if a != b:
            self._add_reason(f"{a=} != {b=}", path)
    
    def find_diffs(self, a: Any, b: Any) -> list[DiffReason]:
        self._find_diffs(a, b, "")
        return self.diffs


class DiffFinder:
    @classmethod
    def find_diffs(cls, a: Any, b: Any) -> list[DiffReason]:
        diffs = _Differ().find_diffs(a, b)
        for diff in diffs:
            print(diff)
        return diffs

    @classmethod
    def assert_diffs(cls, a: Any, b: Any) -> None:
        diffs = cls.find_diffs(a, b)
        assert not diffs, pformat(diffs)
