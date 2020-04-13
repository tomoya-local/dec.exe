# coding: cp932
import base64
import pyminizip
import os
import urllib.parse
import zipfile
import time,sys
import warnings
import getpass
import hashlib
import configparser
os.chdir(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
chk=os.path.isfile('config.ini')
if chk==True:
    config.read('config.ini')
else:
    print('')
    print(' 設定ファイルが見つかりません')
    key=input(' 展開キーワード　>> ')
warnings.simplefilter('ignore')

# 主キーここを変えると互換性が失われる変える際は注意すること
print('')
# また主キーはパスワードより長くしなければならない
#key=input(' 起動パスワード　>> ')
key=config.get('config', 'key')
hkey=len(key)
if hkey<6:
    print('')
    print(' 警告：起動パスワードは脆弱です。')
    print('')
    print(' 起動パスワードは最低でも17文字以上である必要があります。')
    print('')
    print(' 起動許可...')
    time.sleep(5)
# 疑似暗号生成関数

def xor_encrypt(plaintext, key):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(plaintext, key)])
def xor_decrypt(ciphertext, key):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(ciphertext, key)])

# zipファイルの圧縮

def pyzip(key):
    while True:
        plaintext=getpass.getpass(prompt=' パスワード (17文字までの英数字)>> ')
        print('')
        plaintext2=getpass.getpass(prompt=' もう一度パスワードを入力 (17文字までの英数字)>> ')
        if plaintext!=plaintext2:
            print('')
            print(' パスワードが一致しません')
            print('')
            print(' もう一度やり直してください')
            time.sleep(5)
            continue
        elif plaintext==plaintext2:
            break
    
    ciphertext=xor_encrypt(plaintext, key)
    s = urllib.parse.quote(ciphertext)
    pass2=base64.b64encode(s.encode('utf-8'))
    pass2=str(pass2)
    pass2=hashlib.sha224(pass2.encode()).hexdigest()
    print(' 警告　現在このソフトウェアの展開モードは英数字以外のファイル名に対応していません')
    print('')
    filename=input(' 圧縮対象ファイル名 >> ')
    filename = filename.replace("\"","")
    name,ext = os.path.splitext(filename)
    if ext==".lnk":
        print(' 対応していないファイル形式です。')
        print('')
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    elif ext==".zip":
        print(' ZIP形式のファイルは圧縮することはできません。')
        print('')
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    d=os.path.isfile(filename)
    if d!=True:
        print('ファイルが存在しません...')
        print('')
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    sf=os.path.dirname(filename)
    basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    basename_without_ext=basename_without_ext+".zip"
    basefiles=os.path.basename(filename) 
    os.chdir(sf)
    try :
        # 圧縮関係(英数字以外のファイル名もちゃんと圧縮できる)
        pyminizip.compress(basefiles.encode('cp932'),"\\".encode('cp932'),basename_without_ext.encode('cp932'),pass2,int(9))
        print(' 警告 :このソフトで圧縮したファイルはWindows標準機能でパスワードを入力して展開することはできません。')
        print('')
        print(' 圧縮中　しばらくお待ちください。(ファイルサイズによっては時間がかかる場合があります)')
    except OSError:
        print(' エラー: 現在日本語のファイル名に対応していません。')
        print('')
        print(' 対策:日本語のファイル名を英語に変更する')
        print('')
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    except PermissionError:
        print(' エラー :アクセスが拒否されたため圧縮ファイルを作成できませんでした。')
        print('')
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    else:
        print(' 圧縮が完了しました。')
    time.sleep(5)

# ファイルの展開

# 英数字以外のファイル名は文字化けする

def openzip(key):
    pass3=getpass.getpass(prompt=' パスワード (17文字までの英数字)>> ')
    ciphertext =xor_encrypt(pass3, key)
    s = urllib.parse.quote(ciphertext)
    pass2=base64.b64encode(s.encode('utf-8'))
    pass2=str(pass2)
    pass2=hashlib.sha224(pass2.encode()).hexdigest()
    pass2=bytes(pass2,encoding = "utf-8")
    filename=input(' 展開ファイル名 >> ')
    filename = filename.replace("\"","")
    sf=os.path.dirname(filename)
    name,ext = os.path.splitext(filename)
    ext=str(ext)
    name=name+".zip"
    if ext!=".zip":
        print(' 対応していないファイル形式です。')
        print('')
        print(ext)
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    try:
        print('')
        print(' 注意! ファイル名が英数字以外の圧縮ファイルはファイル名だけ文字化けします。')
        print('')
        print(' (ファイル自体のデータは問題ありません)')
        print('')
        print(' (対策　圧縮時にファイル名を英数字に変更する)')
        print('')
        k=input(' 続行しますか? ( Y or N )')
        if k=="Y" or k=="YES" or k=="y":
            print(' 展開中　しばらくお待ちください。(ファイルサイズによっては時間がかかる場合があります)')
            zipfilepointer=zipfile.ZipFile(filename,"r")# ここから展開関係
            zipfilepointer.extractall(sf,pwd=bytes(pass2))
            zipfilepointer.close() # 展開関係ここで終わり
        if k=="N" or k=="n" or k=="NO" or k=="no" or k=="":
            print('')
            print(' 展開をキャンセルしました。')
            print('')
            time.sleep(5)
            return
    except RuntimeError:
        print(' パスワードエラー: パスワードが間違っています。')
        print('')
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    except PermissionError:
        print(' エラー :アクセスが拒否されたため圧縮ファイルを展開できませんでした。')
        print('')
        input(' メニュー画面に戻るにはエンターキーを押してください')
        return
    else:
        print(' 展開が完了しました')
        print('')
        print(' 出力先フォルダ: '+sf)
        time.sleep(5)

# メニュー表示
c=-1
zipfilepointer=0
while True:
    os.system('cls')
    print('')
    print('')
    print(' ******パスワードZIP圧縮ツール　Ver 4.0******')
    print('')
    print(' 0:ファイルのパスワードZIP圧縮')
    print('')
    print(' 1:パスワードZIPファイルの展開')
    print('')  
    print(' 終了するには[N]を入力してください')
    print('')
    print('')
    print(' 警告 :このソフトで圧縮したファイルはWindows標準機能で\n パスワードを入力して展開することはできません。')
    print('')
    print('')
    print(' ************')
    print('')
    c= input(' 操作ID (0 or 1) >> ')
    if c!="N" and c!="n":
        try:
            c=int(c)
        except ValueError:
            pass
    if c==0:
        pyzip(key)
        continue
    if c==1:
        openzip(key)
        continue  
    if c=="N" or c=="n":
        print(' プログラムを終了しています。')
        time.sleep(5)
        sys.exit()
