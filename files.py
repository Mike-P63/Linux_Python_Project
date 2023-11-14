import paramiko
import yaml


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"Loading file {local_path} to catalog {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def download_files(host, user, passwd, remote_path, local_path, port=22):
    print(f"Loading file {remote_path} to catalog {local_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


# Загружаем файлы из stat.txt user2
if __name__ == "__main__":
    with open('config.yaml') as fy:
        data = yaml.safe_load(fy)
        download_files("0.0.0.0", "user2", "11", "/home/user2/stat.txt", "/home/user/stat.txt")
