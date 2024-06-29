import csv
import numpy as np


class List_of_Str(list[str]):
    def index_startswith(self, value: str) -> int:
        return [v.startswith(value) for v in self].index(True)


class ModeFrontier_SS7:
    source: List_of_Str
    members: dict[str, list[dict[str, str | list[str]]]] = {}

    def __init__(self, source: str, members_config: list[str]) -> None:
        with open(source, "r", encoding="cp932") as fp:
            self.source = List_of_Str(fp.readlines())
        for member in members_config:
            with open(member, "r", encoding="cp932") as fp:
                self.members[member] = csv.DictReader(fp)
            with open(member, "r", encoding="cp932") as fp:
                table: list[list[str]] = csv.reader(fp)
            idx: int = table[0].index("") - 1
            for i, line in enumerate(table[1:]):
                self.members[member][i][table[0][idx]] = line[i:]

    def section_stt(self, name: str) -> None:
        return self.source.index_startswith(f"name={name}")

    def section_end(self, name: str) -> None:
        return List_of_Str(self.source[self.section_stt(name) + 1:]).index_startswith("name=") + self.section_stt(name) + 1

    def new_value(self, name: str, idx: int, choice: int) -> None:
        return self.members[name][idx]["choices"][choice]

    def replace(self, name: str, choices: list[int]) -> None:
        if len(choices) != len(self.members[name]):
            raise Exception("len(choices) != len(self.members[name])")
        else:
            pass

    def input(self, name: str) -> None:
        with open(f"{name}.csv", "w", encoding="cp932") as fp:
            csv.writer(fp).writerows([
                "Name",
                "Label",
                "Type",
                "Default value",
                "Unit of measure",
                "Expression",
                "Lower bound",
                "Upper bound",
                "Central value",
                "Delta value",
                "Base",
                "Step",
                "Format",
                "Tolerance",
                "Description",
            ] + [
                np.array([
                    f"{name}[{i}]",
                    "",
                    "Var - Discrete ordered",
                    v["choices"].index(v["default"]),
                    "",
                    "",
                    0,
                    len(v["choices"]) - 1,
                    "",
                    "",
                    len(v["choices"]),
                    1,
                    0,
                    0,
                    "",
                ], dtype=str).tolist() for i, v in enumerate(self.members[name])
            ])

    def print(self) -> None:
        with open("input.csv", "w", encoding="cp932") as fp:
            fp.readlines(self.source)
