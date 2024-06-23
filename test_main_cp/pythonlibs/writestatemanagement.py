class WriteStateManagement:
    """
    書き状態をファイルに読み書きするためのクラス
    """
    def __init__(self):
        self.filename = 'write_state.csv'
        with open(self.filename, 'w'):
            pass
    
    def write_state(self, data):
        with open(self.filename, 'a') as file:
            file.write('C' + data + '0\n')

    def get_state(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()   
            if lines:         
                latest_line = lines[-1].strip()
                return latest_line
            else:
                return -1