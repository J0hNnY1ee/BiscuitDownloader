'''
Author: J0hNnY1ee joh1eenny@gmail.com
Date: 2025-01-07 15:16:06
LastEditors: J0hNnY1ee joh1eenny@gmail.com
LastEditTime: 2025-01-09 17:08:07
FilePath: /BiscuitDownloader/main.py
Description: 

Copyright (c) 2025 by J0hNnY1ee joh1eenny@gmail.com, All Rights Reserved. 
'''

from util import *

if __name__ == '__main__':
    url = 'https://node.kg.qq.com/O9itc3EBI8/play_v2/?s=96l4_C9LToI5X9at&g_f=personal&appsource=&pageId=personalH5'
    html_content = get_html(url)
    nick_name, song_name, play_url = "", "", ""
    if html_content:
        nick_name, song_name, play_url = extract_data_from_html(html_content)
    else:
        print("未能成功获取HTML内容")
        
    download(f"{nick_name}-{song_name}.m4a", play_url)