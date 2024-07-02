import os

class PhotoNameManeger:
    """
    写真の名前を管理するためのクラス
    """
    def __init__(self, photoname):
        self.photoname = photoname
    
    def change_photoname(self, state):
        old_picture_name = 'train/{}.jpg'.format(self.photoname)
        new_picture_name = 'train/{}_{}.jpg'.format(self.photoname, state)
        os.rename(old_picture_name, new_picture_name)
        self.photoname = new_picture_name
        