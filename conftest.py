import random
import string
import pytest
import yaml
from datetime import datetime
from checkers import getout, ssh_checkout, ssh_get
from files import upload_files

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "11",
                        "mkdir -p {} {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                         data["folder_ext2"],
                                                         data["folder_extract"]), "")


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "11",
                        "rm -rf {}/* {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"],
                                                                 data["folder_ext"],
                                                                 data["folder_ext2"], data["folder_extract"]), "")


@pytest.fixture(autouse=True, scope="module")
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "11",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename,
                                                                                               data["bs"]),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choise(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choise(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout("0.0.0.0", "user2", "11", "cd {}; mmkdir {}".format(data["folder_out"], subfoldername),
                        ""):
        return None, None
    if ssh_checkout("0.0.0.0", "user2", "11",
                    "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_out"],
                                                                                              subfoldername,
                                                                                              testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]),
                 "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "11", "truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]),
                 "")


@pytest.fixture()
def make_stat():
    yield
    processor_work = getout("cat /proc/loadavg")
    tests_stat = (f"{datetime.now()} - Config files qty: {data['count']}, files size:  {data['bs']}, Processor "
                  f"statistics: {processor_work}")
    getout(f"echo '{tests_stat}' >> {data['stat_file']}")


#  File stat.txt :

# 2023-11-11 20:25:47.094729 - Config files qty: 5, files size:  1M, Processor statistics: 3.04 3.31 2.74 5/541 7633
#
# 2023-11-11 20:25:47.286194 - Config files qty: 5, files size:  1M, Processor statistics: 3.04 3.31 2.74 6/542 7641
#
# 2023-11-11 20:25:47.495237 - Config files qty: 5, files size:  1M, Processor statistics: 3.04 3.31 2.74 11/544 7648
#
# 2023-11-11 20:25:47.987628 - Config files qty: 5, files size:  1M, Processor statistics: 3.04 3.31 2.74 5/549 7662
#
# 2023-11-11 20:25:48.603462 - Config files qty: 5, files size:  1M, Processor statistics: 3.04 3.31 2.74 6/550 7673
#
# 2023-11-11 20:25:49.104461 - Config files qty: 5, files size:  1M, Processor statistics: 3.04 3.31 2.74 2/550 7680

@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "11", "/home/user/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' |  sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)


@pytest.fixture(scope="module")
def save_log(start_time):
    with open("stat.txt", 'w') as f:
        f.write(ssh_get("0.0.0.0", "user2", "11",
                        "journalctl --since {}".format(start_time)))


@pytest.fixture(autouse=True, scope="module")
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
