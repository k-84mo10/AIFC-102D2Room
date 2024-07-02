import re

class ReadStateManagement:
    """
    読み状態をファイルに読み書きするためのクラス
    """
    def __init__(self):
        self.filename = 'read_state.csv'
        with open(self.filename, 'w'):
            pass

    def record_state(self, data):
        if self.is_valid_format(data):
            with open(self.filename, 'a') as file:
                file.write(data + '\n')

    def get_state(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()   
            if lines:         
                latest_line = lines[-1].strip()
                state = latest_line[1:5]
            else:
                state = "0000"
        return state

    def is_manual(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()   
            if lines:         
                latest_line = lines[-1].strip()
                if latest_line[5] == '0':
                    return True
                else:
                    return False
            else:
                return False

    def is_valid_format(self, data):
        pattern = r'^S\d{7}'
        if re.match(pattern, str(data)):
            return True
        else:
            return False