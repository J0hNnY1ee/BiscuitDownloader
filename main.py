"""
Author: J0hNnY1ee joh1eenny@gmail.com
Date: 2025-01-07 15:16:06
LastEditors: J0hNnY1ee joh1eenny@gmail.com
LastEditTime: 2025-01-07 21:53:13
FilePath: /BiscuitDownloader/main.py
Description: 

Copyright (c) 2025 by J0hNnY1ee joh1eenny@gmail.com, All Rights Reserved. 
"""

from util import *

if __name__ == '__main__':
    url = 'https://static-play.kg.qq.com/node/LjdYJwfYwz/play_v2?s=y4W6QvyXzvUtYyn-&shareuid=6a9a9c84272e348d&abtype=13&shareDescABType=1&topsource=a0_pn201001006_z11_u1160167006_l0_t1736182334__&pageId=homepage_guest'
    html_content = get_html(url)
    nick_name, song_name, play_url = "", "", ""
    if html_content:
        nick_name, song_name, play_url = extract_data_from_html(html_content)
    else:
        print("未能成功获取HTML内容")
        
    download(f"{nick_name}-{song_name}.m4a", play_url)