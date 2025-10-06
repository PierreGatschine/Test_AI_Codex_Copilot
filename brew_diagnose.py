#!/usr/bin/env python3
"""Utilities for interpreting ``brew doctor`` output.

This module provides a small helper that inspects the text produced by
``brew doctor`` and returns actionable suggestions that can be relayed to a
user.  The goal is not to perfectly understand every diagnostic that Homebrew
prints, but to cover a handful of common warnings so they can be presented in a
friendlier format inside support tools such as the Tkinter GUI that ships with
this repository.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class Suggestion:
    """Represents a human friendly suggestion extracted from ``brew doctor``."""

    title: str
    details: str

    def format(self) -> str:
        """Return a formatted, multi-line string representation."""

        return f"- {self.title}\n  {self.details}"


def _contains_any(text: str, needles: Iterable[str]) -> bool:
    """Return ``True`` if ``text`` contains any of the substrings in ``needles``."""

    return any(needle in text for needle in needles)


def analyze_brew_doctor_output(output: str) -> List[Suggestion]:
    """Generate suggestions based on a ``brew doctor`` diagnostic report."""

    normalized = output.strip()
    suggestions: List[Suggestion] = []

    if not normalized:
        return suggestions

    if "A newer Command Line Tools release is available" in normalized:
        suggestions.append(
            Suggestion(
                title="Update the Xcode Command Line Tools",
                details=(
                    "Install the latest Command Line Tools from System Settings or by "
                    "running `sudo rm -rf /Library/Developer/CommandLineTools` and "
                    "`sudo xcode-select --install`. You can also download the "
                    "installer from Apple's developer portal."
                ),
            )
        )

    if "Warning: You are using macOS" in normalized:
        suggestions.append(
            Suggestion(
                title="Unsupported macOS release",
                details=(
                    "Homebrew labels older macOS versions as unsupported. Consider "
                    "upgrading macOS or be prepared for limited assistance from the "
                    "Homebrew maintainers."
                ),
            )
        )

    if _contains_any(normalized, {"Tier 2 configuration", "Tier 3 configuration"}):
        tier_details = (
            "The output mentions Homebrew support tiers. Read the linked support "
            "policy before opening issues, because only Tier 1 configurations "
            "receive full support."
        )
        suggestions.append(
            Suggestion(title="Homebrew support policy reminder", details=tier_details)
        )

    return suggestions


def format_suggestions(suggestions: Iterable[Suggestion]) -> str:
    """Return the suggestions as a single string suitable for display."""

    suggestions = list(suggestions)
    if not suggestions:
        return "No actionable Homebrew doctor warnings detected."
    return "\n".join(suggestion.format() for suggestion in suggestions)


def main() -> None:
    """Read ``brew doctor`` output from stdin and print suggestions."""

    import sys

    report = sys.stdin.read()
    suggestions = analyze_brew_doctor_output(report)
    print(format_suggestions(suggestions))


if __name__ == "__main__":
    main()
