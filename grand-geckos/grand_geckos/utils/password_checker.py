from dataclasses import dataclass
from typing import List

from password_strength import PasswordPolicy, tests, tests_base

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1,
    nonletters=1,
    strength=0.44,
)


@dataclass
class PasswordResult:
    test: tests_base.ATest
    info: str

    def __str__(self):
        return self.info


def check_password(password: str) -> List[PasswordResult]:
    result = policy.test(password)

    output = []

    for issue in result:
        if isinstance(issue, tests.Strength):
            output.append(PasswordResult(issue, "Password too weak. Try to add more complexity."))
        if isinstance(issue, tests.Length):
            output.append(PasswordResult(issue, f"Too short, needs to be {issue.length} or more letters."))
        elif isinstance(issue, tests.Numbers):
            output.append(PasswordResult(issue, f"Too few numbers, need at least {issue.count} or more."))
        elif isinstance(issue, tests.Special):
            output.append(PasswordResult(issue, f"Not enough special letters. Needs to be {issue.count} or more."))
        elif isinstance(issue, tests.NonLetters):
            output.append(
                PasswordResult(issue, f"Not enough non-letter characters. Needs to be {issue.count} or more.")
            )
        elif isinstance(issue, tests.Uppercase):
            output.append(PasswordResult(issue, f"Not enough uppercase letters. Needs to be {issue.count} or more."))

    return output
