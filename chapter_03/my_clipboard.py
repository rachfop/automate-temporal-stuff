import os
import pyperclip

folder_path = "."  # Replace with the path to your folder
file_contents = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(".py") and file_name != "my_clipboard.py":
        with open(os.path.join(folder_path, file_name), "r") as f:
            file_contents.append("```python\n")
            file_contents.append(f"#{file_name}\n")
            file_contents.append(f.read())
            file_contents.append("\n```\n")
clipboard_text = "".join(file_contents)
password = str(pyperclip.copy(clipboard_text))
print(clipboard_text)
