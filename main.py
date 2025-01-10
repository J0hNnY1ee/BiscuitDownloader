"""
Author: J0hNnY1ee joh1eenny@gmail.com
Date: 2025-01-07 15:16:06
LastEditors: J0hNnY1ee joh1eenny@gmail.com
LastEditTime: 2025-01-10 17:27:20
FilePath: /BiscuitDownloader/main.py
Description: 

Copyright (c) 2025 by J0hNnY1ee joh1eenny@gmail.com, All Rights Reserved. 
"""

from util import *



if __name__ == "__main__":
    selected = input("请选择要下载的内容(1. 歌曲 2. 用户): ")
    if selected == "1":
        url = input("请输入要下载的歌曲的URL: ")
        downloadSong(url)
    elif selected == "2":
        url = input("请输入要下载的用户的URL: ")
        downloadPeople(url)
    else:
        print("无效的选项")
