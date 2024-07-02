#include <Arduino.h>

char state[] = "00000000";
int is_button0_pushed = 0;
int is_button1_pushed = 0;
int is_button2_pushed = 0;
int is_button3_pushed = 0;
int is_button4_pushed = 0;

unsigned long previous_time;

void setup()
{
    Serial.begin(9600);

    // 出力ピンの設定
    pinMode(2, OUTPUT); // LED上（Automatic）
    pinMode(3, OUTPUT); // LED中（Macual(Record)）
    pinMode(4, OUTPUT); // LED下（Manual(Train)）
    pinMode(6, OUTPUT); // LED（左上ボタン）
    pinMode(7, OUTPUT); // LED（右上ボタン）
    pinMode(8, OUTPUT); // LED（左下ボタン）
    pinMode(9, OUTPUT); // LED（右下ボタン）

    // 入力ピンの設定
    pinMode(A0, INPUT_PULLUP); // 左上ボタン   state: 0
    pinMode(A1, INPUT_PULLUP); // 右上ボタン   state: 1
    pinMode(A2, INPUT_PULLUP); // 左下ボタン   state: 2
    pinMode(A3, INPUT_PULLUP); // 右下ボタン   state: 3
    pinMode(5, INPUT_PULLUP);  // Forgetボタン state: 4
    pinMode(A4, INPUT_PULLUP); // 左トグルスイッチ（Auto/Manual）  state:5
    pinMode(A5, INPUT_PULLUP); // 右トグルスイッチ（Collect/Train）state:6

    previous_time = millis();
}

void loop()
{
    // イベント通知
    if (state[5] == '0')
    {
        if (digitalRead(A0) == LOW)
            is_button0_pushed = 1;
        else if (is_button0_pushed == 1)
        {
            changeButtonState(0);
            is_button0_pushed = 0;
        }
        if (digitalRead(A1) == LOW)
            is_button1_pushed = 1;
        else if (is_button1_pushed == 1)
        {
            changeButtonState(1);
            is_button1_pushed = 0;
        }
        if (digitalRead(A2) == LOW)
            is_button2_pushed = 1;
        else if (is_button2_pushed == 1)
        {
            changeButtonState(2);
            is_button2_pushed = 0;
        }
        if (digitalRead(A3) == LOW)
            is_button3_pushed = 1;
        else if (is_button3_pushed == 1)
        {
            changeButtonState(3);
            is_button3_pushed = 0;
        }
        if (digitalRead(5) == LOW)
            is_button4_pushed = 1;
        else if (is_button4_pushed == 1)
        {
            changeButtonState(4);
            is_button4_pushed = 0;
        }
    }

    // 状態連絡
    state[5] = '0' + digitalRead(A4);
    state[6] = '0' + digitalRead(A5);
    unsigned long current_time = millis();
    if (current_time - previous_time > 1000 || current_time - previous_time < 0)
    {
        SendStateNotification();
        previous_time = current_time;
    }

    // PCからの制御出力取得
    if (state[5] == '1')
    {
        if (Serial.available() > 0)
        {
            // シリアル通信から文字列を読み取る
            String receivedString = Serial.readStringUntil('\n');

            // 受信した文字列を1文字ずつ処理する
            if (receivedString[0] == 'C' && receivedString.length() == 7)
            {
                for (int i = 0; i < 4; i++)
                {
                    if (receivedString[i + 1] == '0' || receivedString[i + 1] == '1')
                        state[i] = receivedString[i + 1];
                }
                if (receivedString[5] == '0' || receivedString[5] == '1' || receivedString[5] == '2' || receivedString[5] == '3')
                    state[7] = receivedString[5];
            }
        }
    }

    // リレー操作
    if (state[0] == '1')
        digitalWrite(6, HIGH);
    else
        digitalWrite(6, LOW);
    if (state[1] == '1')
        digitalWrite(7, HIGH);
    else
        digitalWrite(7, LOW);
    if (state[2] == '1')
        digitalWrite(8, HIGH);
    else
        digitalWrite(8, LOW);
    if (state[3] == '1')
        digitalWrite(9, HIGH);
    else
        digitalWrite(9, LOW);

    // LED表示
    if (state[5] == '1')
    {
        digitalWrite(2, HIGH);
        digitalWrite(3, LOW);
        digitalWrite(4, LOW);
        // 状態2の場合は点滅
        if (state[7] == '2')
        {
            delay(100);
            digitalWrite(2, LOW);
            digitalWrite(4, HIGH);
        }
    }
    else
    {
        if (state[6] == '1')
        {
            digitalWrite(2, LOW);
            digitalWrite(3, HIGH);
            digitalWrite(4, LOW);
        }
        else
        {
            digitalWrite(2, LOW);
            digitalWrite(3, LOW);
            digitalWrite(4, HIGH);
            // 状態2の場合は点滅
            if (state[7] == '2')
            {
                delay(100);
                digitalWrite(4, !digitalRead(4));
            }
        }
    }

    delay(100);
}

void changeButtonState(int switchNum)
{
    if (state[switchNum] == '1')
    {
        state[switchNum] = '0';
    }
    else
    {
        state[switchNum] = '1';
    }
    SendEventNotification();
    delay(100); // チャタリング対策
}

void SendEventNotification()
{
    Serial.print("E");
    Serial.print(state[0]);
    Serial.print(state[1]);
    Serial.print(state[2]);
    Serial.print(state[3]);
    Serial.print(state[4]);
    Serial.println("");
}

void SendStateNotification()
{
    Serial.print("S");
    Serial.print(state[0]);
    Serial.print(state[1]);
    Serial.print(state[2]);
    Serial.print(state[3]);
    Serial.print(state[5]);
    Serial.print(state[6]);
    Serial.print(state[7]);
    Serial.println("");
}