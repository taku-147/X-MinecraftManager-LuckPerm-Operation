# X-MinecraftManager-LuckPerm-Operation
MinecraftのLuckPermのグループ別ユーザー管理をやりやすくするためのものです。
<br>基本[XServer VPS for Game](https://vps.xserver.ne.jp/game-server/)向けに作成されていますが、統一すれば他の環境でも使用可能です。

## 必要条件
### XServer VPS for Game / 個人サーバー共通
- MinecraftにLuckPermsが導入されていること
- SSHポートが開放されていること
- minecraftが実行されているユーザー(XServerの場合は`minecraft`)に対して公開鍵認証が利用可能なこと(パスワード認証でも一応できるように作っていますが、確認はしていません。)

### 個人サーバー
- screenが利用可能であること
- screenのminecraftという名前でターミナルを立てていること
  - 例: `screen -S minecraft`
  - このターミナルからサーバーを起動していること
- /opt/minecraft/にminecraftがインストールされていること
- sudo権限があること

## 使い方
config.jsonを編集してください。多分見れば何を書けばわかります。

## LICENSE

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

### Permissions
- **Commercial use**: You can use this project for commercial purposes.
- **Modification**: You can modify the code as you wish.
- **Distribution**: You can share this project freely.
- **Private use**: You can use this project in private.

### Limitations
- **Liability**: The author is not responsible for any damages caused by using this project.
- **Warranty**: This project is provided "as-is," without any warranty of any kind.