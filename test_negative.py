import subprocess

out = "/home/user/out"
folder1 = "/home/user/folder1"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def test_step1():
    result1 = checkout("cd {}; 7z e bad_arx.7z -o{} -y".format(out, folder1), "ERRORS")
    assert result1, "test1 FAIL"


def test_step2():
    result1 = checkout("cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "test2 FAIL"
