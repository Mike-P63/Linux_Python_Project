import yaml
from checkers import ssh_checkout_negative


with open("config.yaml") as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_bad_arx):
        result1 = ssh_checkout_negative("0.0.0.0", "user2", "11",
                                        "cd {}; 7z e bad_arx.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                                        "ERRORS")
        assert result1, "test1 FAIL"

    def test_step2(self):
        assert ssh_checkout_negative("0.0.0.0", "user2", "11", "cd {}; 7z t bad_arx.7z".format(data["folder_out"]),
                                     "ERRORS"), "test2 FAIL"
