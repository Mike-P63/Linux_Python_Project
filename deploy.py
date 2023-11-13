from sshcheckers import ssh_checkout, upload_files

def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "11", "tests/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -i /home/p7zip-full.deb", ""))
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' |  sudo -S dpkg -s p7zip-full", "Status: install  ok installed"))
    return all(res)


if deploy():
    print("OK")
else:
    print("Bad")




