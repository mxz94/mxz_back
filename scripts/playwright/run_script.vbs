Set objShell = CreateObject("WScript.Shell")
objShell.Run "python D:\mxz\mxz_back\scripts\playwright\get_reward_list.py", 0, True
WScript.Quit