import subprocess
import yaml
from checkers import ssh_checkout
from conftest import make_files

with open("config.yaml") as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_files, make_stat, start_time):
        result1 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; 7z  a {} {}/arx2".format(data["folder_in"], data["key_t"], data["folder_out"]),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "11", "cd {}; ls".format(data["folder_out"]), "arx2.zip")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, make_files, make_stat, start_time):
        result1 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; 7z e arx2.zip -o{} -y".format(data["folder_out"], data["folder_ext"]),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "11", "cd {}; ls".format(data["folder_ext"]), make_files[0])
        assert result1 and result2, "test2 FAIL"

    def test_step3(self, make_stat, start_time):
        assert ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z t arx2.zip".format(data["folder_out"]),
                            "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        assert ssh_checkout("0.0.0.0", "user2", "11",
                            "cd {}; 7z u {}/arx2.zip".format(data["folder_in"], data["folder_out"]),
                            "Everything is Ok"), "test4 FAIL"

    # def test_step5(self, make_stat, start_time): result1 = ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z d
    # arx2.zip".format(data["folder_out"]), "Everything is Ok"), "test5 FAIL"

    def test_step6(self, make_files, make_stat, start_time):
        result1 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; 7z l arx2.zip".format(data["folder_out"], data["folder_extract"]), make_files[0])
        result2 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; 7z l arx2.zip".format(data["folder_out"], data["folder_extract"]), make_files[0])
        assert result1 and result2, "test6 FAIL"

    def test_step7(self, make_files, make_stat, start_time):
        result1 = ssh_checkout("0.0.0.0", "user2", "11",
                               "cd {}; 7z x arx2.zip -o{} -y".format(data["folder_out"], data["folder_ext2"]),
                               "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "11", "cd {}; ls".format(data["folder_ext2"]), make_files[0])
        result3 = ssh_checkout("0.0.0.0", "user2", "11", "cd {}; ls".format(data["folder_ext2"]), make_files[0])
        assert result1 and result2 and result3, "test7 FAIL"

    # crc32 установил в директории user2 (sudo apt install libarchive-zip-perl)
    def test_8(self, make_stat):
        folder_out = "/home/user2/out"
        result = subprocess.run("crc32 /home/user2/out/arx2.zip", shell=True, stdout=subprocess.PIPE, encoding="utf-8")
        datas = result.stdout.rstrip().upper()
        assert ssh_checkout("0.0.0.0", "user2", "11", f"cd {folder_out}; 7z h arx2.zip", datas), "test8 FAIL"
