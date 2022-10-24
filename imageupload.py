from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import os
def id() :
    #認証
    gauth = GoogleAuth()

    #ローカルWebサーバとautoを作成
    #Googleドライブの認証処理
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    #アップロードするフォルダパス指定
    path = r"D:/work/unsupervised/app/stablediffusion_original/images/"

    #for文によるループ処理（繰り返し処理）
    for x in os.listdir(path):
        #GoogleDriveFileオブジェクト作成
        f = drive.CreateFile({'title' : x,  
                            'parents': [{'kind': 'drive#fileLink', 'id':"15tyvSMYuWOwctLOcgmd-vY29K4f_Hwhg"}]})
        #ローカルのファイルをセットしてアップロード
        f.SetContentFile(os.path.join(path,x))
        #Googleドライブにアップロード
        f.Upload()
    return f['id']