import random
import string
import pytest
import yaml
from datetime import datetime
from checkers import checkout, getout

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return checkout(
        "mkdir -p {} {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_ext2"],
                                         data["folder_extract"]), "")


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                             data["folder_ext2"], data["folder_extract"]), "")


@pytest.fixture(autouse=True, scope="module")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(
                "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]),
                ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choise(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choise(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mmkdir {}".format(data["folder_out"], subfoldername), ""):
        return None, None
    if checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_out"], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")

@pytest.fixture()
def make_stat():
    yield
    processor_work = getout("cat /proc/loadavg")
    tests_stat = f"{datetime.now()} - Config files qty: {data['count']}, files size:  {data['bs']}, Processor statistics: {processor_work}"
    getout(f"echo '{tests_stat}' >> {data['stat_file']}")