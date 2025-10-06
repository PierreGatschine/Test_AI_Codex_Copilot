import unittest

from brew_diagnose import Suggestion, analyze_brew_doctor_output, format_suggestions


SAMPLE_REPORT = """brew doctor
Warning: A newer Command Line Tools release is available.
Update them from Software Update in System Settings.

If that doesn't show you any updates, run:
  sudo rm -rf /Library/Developer/CommandLineTools
  sudo xcode-select --install

Alternatively, manually download them from:
  https://developer.apple.com/download/all/.
You should download the Command Line Tools for Xcode 15.2.



This is a Tier 2 configuration:
  https://docs.brew.sh/Support-Tiers#tier-2
You can report Tier 2 unrelated issues to Homebrew/* repositories!
Read the above document instead before opening any issues or PRs.


Warning: You are using macOS 13.
We (and Apple) do not provide support for this old version.

This is a Tier 3 configuration:
  https://docs.brew.sh/Support-Tiers#tier-3
You can report Tier 3 unrelated issues to Homebrew/* repositories!
Read the above document instead before opening any issues or PRs.
"""


class BrewDiagnoseTests(unittest.TestCase):
    def test_analyze_brew_doctor_output_detects_command_line_tools(self):
        suggestions = analyze_brew_doctor_output(SAMPLE_REPORT)
        self.assertTrue(
            any(
                s.title == "Update the Xcode Command Line Tools" and "Command Line Tools"
                in s.details
                for s in suggestions
            )
        )

    def test_analyze_brew_doctor_output_detects_mac_os_warning(self):
        suggestions = analyze_brew_doctor_output(SAMPLE_REPORT)
        self.assertTrue(
            any(
                s.title == "Unsupported macOS release" and "older macOS versions"
                in s.details
                for s in suggestions
            )
        )

    def test_format_suggestions_handles_empty(self):
        message = format_suggestions([])
        self.assertEqual(message, "No actionable Homebrew doctor warnings detected.")

    def test_format_suggestions_contains_list_items(self):
        suggestions = [
            Suggestion(title="Example", details="Do a thing."),
            Suggestion(title="Second", details="Do another thing."),
        ]
        message = format_suggestions(suggestions)
        self.assertIn("- Example", message)
        self.assertIn("  Do a thing.", message)


if __name__ == "__main__":
    unittest.main()
