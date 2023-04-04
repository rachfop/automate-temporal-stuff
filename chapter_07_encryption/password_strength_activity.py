from temporalio import activity
import re
from data_objects import PasswordClipBoard


@activity.defn
async def pass_strength_checker(clipboard: PasswordClipBoard) -> str:
    pass_length_regex = re.compile(r".{8,}")  # >= 8 characters
    pass_upper_regex = re.compile(r"[A-Z]")  # Contains an upper case letter
    pass_lower_regex = re.compile(r"[a-z]")  # Contains a lower case letter
    pass_digit_regex = re.compile(r"[0-9]")  # Contains a digit
    """Check if a password is strong."""
    if pass_length_regex.search(clipboard.password) is None:
        return "Needs to be at least 8 characters long"
    if pass_upper_regex.search(clipboard.password) is None:
        return "Needs an upper case letter"
    if pass_lower_regex.search(clipboard.password) is None:
        return "Needs a lower case letter"
    if pass_digit_regex.search(clipboard.password) is None:
        return "Needs a digit"
    else:
        return "Strong password"
