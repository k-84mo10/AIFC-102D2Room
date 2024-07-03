# AIFC

## 概要
このコードは東京大学工学部2号館102D3室（落合研究室）にて、建築AIのショールームを動かすためのコードです。  
回路基板の制御コードと、メインPCの制御コードが含まれています。

## ファイルのディレクトリ構造
```plaintext
/AIFC
├── /ciruit_board
│   └── circuit_board.ino
├── /main_cp_20240702
│   ├── /configs
│   │   └── config.ino
│   ├── /data
│   │   ├── /csv
│   │   └── /image
│   |       ├── /raw
│   |       ├── /train
│   |       └── /result
│   ├── /model
│   ├── /src
│   │   ├── __init__.py
│   │   ├── machine_learning.py
│   │   ├── serial_communication.py
│   │   └── take_image.py
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 回路基板の制御コード
circuit_board内には、回路基板の制御コードが含まれています。  
Arduino IDEを用いて、circuit_board.inoをArduinoに書き込んでください。  
回路基板の制御コードは、以下の機能を持っています。  
ToDo: 気が向いたら書く

## メインPCの制御コード
main_cp_20240702内には、メインPCの制御コードが含まれています。  
### 各ファイルの説明
#### configs/config.ino
config.inoには、各種設定値が含まれています。
ここで、モデルのパスやシリアル通信のポートを設定してください。
#### data
data内には、画像データが含まれています。
- raw : カメラから取得した生の画像データ
- train : 学習用の画像データ
- result : 予測結果の画像データ
#### model
model内には、学習済みモデルを保存しています。
vgg19_bnを使用した学習済みモデルにのみ、現在は対応しています。
#### src
src内には、各種スクリプトが含まれています。
- machine_learning.py : 機械学習を行うスクリプト
- serial_communication.py : シリアル通信を行うスクリプト
- take_image.py : カメラから画像を取得するスクリプト
#### cli.py
main.pyを実行するためのCLIスクリプトです。
### 実行方法
AIFCディレクトリで、以下のコマンドを実行してください。
```bash
python3 -m main_cp_20240702
```
回路基板の左のトグルスイッチ（Automatic/Manual）によって動作が異なります。
#### Automatic
自動モードでは、カメラから画像を取得し、機械学習モデルによって予測を行い、回路基板に制御信号を送ります。  
予測した結果は、resultディレクトリに保存されます。
#### Manual
手動モードでは、カメラから画像を取得し、回路基板からの制御信号を元に、学習用の画像データを保存します。
保存先は、trainディレクトリです。
