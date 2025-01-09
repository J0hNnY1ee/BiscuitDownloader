'''
Author: J0hNnY1ee joh1eenny@gmail.com
Date: 2025-01-07 15:25:26
LastEditors: J0hNnY1ee joh1eenny@gmail.com
LastEditTime: 2025-01-09 17:00:24
FilePath: /BiscuitDownloader/util.py
Description: 

Copyright (c) 2025 by J0hNnY1ee joh1eenny@gmail.com, All Rights Reserved. 
'''
import requests , re , json


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        return response.text
    except requests.RequestException as e:
        print(e)
        return False
    
    
    
    
def download(filename,url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"文件已成功下载并保存到 {filename}")
    except requests.exceptions.RequestException as e:
        print(f"文件下载失败: {e}")
    
    

def extract_data_from_html(content):
    # 使用正则表达式查找window.__DATA__中的内容
    match = match = re.search(r'window.__DATA__\s*=\s*({.*?});', content, re.DOTALL)
    if not match:
        print("未能找到window.__DATA__对象")
        return None
    
    data_str = match.group(1)
    try:
        # 将字符串解析为JSON对象
        data = json.loads(data_str)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    
    try:
        nick_value = data.get('detail', {}).get('nick', 'Nick not found')
        song_name = data.get('detail', {}).get('song_name', 'Song name not found')
        play_url = data.get('detail', {}).get('playurl', 'Play url not found')
        print(f"The nick value in detail is: {nick_value}")
        print(f"The song name in detail is: {song_name}")
        print(f"The play url in detail is: {play_url}")
    except AttributeError:
        print("The structure of the data does not match or data is None.")
    return nick_value, song_name, play_url
    
    
    
    
if __name__ == '__main__':
    url = 'https://static-play.kg.qq.com/node/LjdYJwfYwz/play_v2?s=y4W6QvyXzvUtYyn-&shareuid=6a9a9c84272e348d&abtype=13&shareDescABType=1&topsource=a0_pn201001006_z11_u1160167006_l0_t1736182334__&pageId=homepage_guest'
    html_content = get_html(url)
    if html_content:
        extract_data_from_html(html_content)
    else:
        print("未能成功获取HTML内容")
    