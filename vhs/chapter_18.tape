Output ../chapter_18/demo.gif

Require echo

Set Shell "bash"
Set FontSize 32
Set Width 1200
Set Height 600

Hide
Type "cd ../chapter_18/" Enter
Type "clear" Enter
Show

Type "poetry run python look_busy.py" Sleep 500ms Enter
Sleep 20s