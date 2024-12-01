import paramiko
import gzip
import io
import json

ver = "1.0.1"
print(f'X-MinecraftManager-LuckPerms-Operation ver.{ver}')
print("--------------------------------------")

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("config.jsonが見つかりません。")
    input("Enterキーを押すと終了します。")
    exit(1)
except json.JSONDecodeError:
    print("config.jsonの形式が不正です。")
    input("Enterキーを押すと終了します。")
    exit(1)

hostname = config['hostname']
username = config['username']
groups = config['groups']
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print(f'{hostname}に接続しています...')
try:
    if config['private_key_path'] != "":
        try:
            private_key_path = config['private_key_path']
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            client.connect(hostname, username=username, pkey=private_key)
        except FileNotFoundError:
            print("秘密鍵が見つかりません。\nconfig.jsonのprivate_key_pathを確認してください。")
            input("Enterキーを押すと終了します。")
            exit(1)
    else:
        password = config['password']
        client.connect(hostname, username=username, password=password)
except paramiko.AuthenticationException:
    print("認証に失敗しました。\nconfig.jsonの設定を確認してください。")
    input("Enterキーを押すと終了します。")
    exit(1)

print('接続しました\n')
try:
    command = 'screen -S minecraft -X stuff "lp export luckperms.json\n"'
    client.exec_command(command)
    detach_command = 'screen -d'
    client.exec_command(detach_command)
    command = 'cat /opt/minecraft/server/plugins/LuckPerms/luckperms.json.json.gz'
    stdin, stdout, stderr = client.exec_command(command)
    compressed_data = stdout.read()
    command = 'rm /opt/minecraft/server/plugins/LuckPerms/luckperms.json.json.gz'
    client.exec_command(command)

    with gzip.GzipFile(fileobj=io.BytesIO(compressed_data)) as f:
        decompressed_data = f.read()
    data = json.loads(decompressed_data)

    print("ユーザー一覧")
    grouped_users = {group: [] for group in groups}

    for user_id, user_info in data["users"].items():
        primary_group = user_info['primaryGroup']
        if primary_group in grouped_users:
            grouped_users[primary_group].append(user_info['username'])

    for group in groups:
        users = grouped_users[group]
        if users:
            print(f"{group.capitalize()}: {', '.join(users)}")

    print("操作を選択してください。")
    print("1: ユーザー追加/変更")
    print("2: ユーザー削除")
    print("-------------")
    print("9: 終了")
    operation = input("操作番号を入力してください: ")

    if operation == '1':
        username = input("ユーザー名を入力してください: ")
        available_groups = ', '.join(groups)
        group = input(f'グループを入力してください({available_groups}): ')
        command = f'screen -S minecraft -X stuff "lp user {username} parent set {group}\n"'
        client.exec_command(command)
        client.exec_command(detach_command)
        print(f'{username}を{group}に追加/変更しました。')
        input("Enterキーを押すと終了します。")
    elif operation == '2':
        username = input("ユーザー名を入力してください: ")
        command = f'screen -S minecraft -X stuff "lp user {username} parent set default\n"'
        client.exec_command(command)
        client.exec_command(detach_command)
        print(f'{username}を削除しました。')
        input("Enterキーを押すと終了します。")
    elif operation == '9':
        print("終了します。")
finally:
    client.close()