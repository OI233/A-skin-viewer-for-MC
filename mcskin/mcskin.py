# 作者：AQ114514 (Minecraft Java)
# 版本：v1.0.2
# 日期：2025-08-29
# 编码： UTF-8

import requests
import json
from io import BytesIO
import PIL
import os
from PIL import Image

#几种显示皮肤的模式: [ FACE：头像 ] [ HEAD：头部 (立体) ] [ BODY：全身 (立体) ] [ SKIN：皮肤 ] [ CAPE：披风 ] (实质是调用Crafatar API)
FACE = "https://crafatar.com/avatars/" 
HEAD = "https://crafatar.com/renders/head/"
BODY = "https://crafatar.com/renders/body/"
SKIN = "https://crafatar.com/skins/"
CAPE = "https://crafatar.com/capes/"

#前面的id就是去匹配mode的
m_list = {
        "FACE" : FACE,
        "HEAD" : HEAD,
        "BODY" : BODY,
        "SKIN" : SKIN,
        "CAPE" : CAPE
    }


def get_uuid(name : str) -> str:   #通过玩家名称获取UUID
    try:
        url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
        name_json = requests.get(url).text
        uuid = json.loads(name_json)["id"]
        return str(uuid)
    except KeyError:
        return f"错误：玩家[{name}]不存在"
    except requests.exceptions.RequestException as e:
        return f"错误：网络请求失败"
    except json.JSONDecodeError:
        return f"错误：玩家[{name}]可能不存在"
    except Exception as e:
        return ""


def is_uuid(uuid: str) -> bool:
    return len(uuid) == 32 and all(c in "0123456789abcdefABCDEF" for c in uuid)


def get_skin_2(uuid : str,mode : str = "SKIN"):   #获取皮肤为二进制形式
    try:
        if mode in m_list.keys():
            mode = m_list[mode]
        else:
            mode = SKIN
        skin = requests.get(f"{mode}{uuid}").content
        return skin
    except Exception as e:
        return e


def get_skin_text(uuid : str,mode : str = "SKIN") -> str:    #获取皮肤为文本形式
    try:
        if mode in m_list.keys():
            mode = m_list[mode]
        else:
            mode = SKIN
        skin = requests.get(f"{mode}{uuid}").text
        return skin
    except Exception as e:
        return e


def show_skin(skin : bytes):  #显示皮肤
    try:
        img = Image.open(BytesIO(skin))
        img.show()
    except PIL.UnidentifiedImageError:
        print("无法显示皮肤，可能是玩家不存在或没有该皮肤")
        return False
    return True


def save_skin(skin : bytes,filename : str,path : str = os.path.dirname(os.path.abspath(__file__))): #保存皮肤
    try:
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        img = Image.open(BytesIO(skin))
        save_path = os.path.join(path, filename)
        img.save(save_path)
        print(f"皮肤已保存至{save_path}")
    except PIL.UnidentifiedImageError:
        print("无法保存皮肤，可能是玩家不存在或没有该皮肤")


def show_skin_one_click(name : str,mode : str = ""):  #一键显示皮肤
    uuid = get_uuid(name)
    if not is_uuid(uuid):
        print(uuid)
        return
    return show_skin(get_skin_2(uuid,mode))


def test():
    playername = input("请输入玩家名称: ")
    mode = input("请输入获取模式(FACE,HEAD,BODY,SKIN,CAPE): ").upper()
    if mode not in m_list.keys():
        print("输入模式错误，已自动切换为默认模式SKIN")
        mode = "SKIN"
    print(f"正在获取玩家[{playername}]的皮肤...")
    show_result = show_skin_one_click(playername, mode)
    if not show_result:
        input("按回车键退出...")
        return
    fpath = input("请输入保存路径(不输入则退出): ")
    if fpath:
        uuid = get_uuid(playername)
        skin_bytes = get_skin_2(uuid, mode)
        filename = f"{playername}_{mode}.png"
        save_skin(skin_bytes, filename, fpath)
    input("按回车键退出...")


if __name__ == "__main__":
    test()
