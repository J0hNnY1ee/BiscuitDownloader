"""
Author: J0hNnY1ee joh1eenny@gmail.com
Date: 2025-01-07 15:25:26
LastEditors: J0hNnY1ee joh1eenny@gmail.com
LastEditTime: 2025-01-10 15:30:48
FilePath: /BiscuitDownloader/util.py
Description: 

Copyright (c) 2025 by J0hNnY1ee joh1eenny@gmail.com, All Rights Reserved. 
"""

import requests, re, json, os, html, sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def decode_html_entities(s):
    # 如果字符串为空或者不是字符串类型，则直接返回
    if not isinstance(s, str) or not s:
        return s

    # 重复解码直到没有变化
    prev_s = None
    while s != prev_s:
        prev_s = s
        s = html.unescape(s)
    return s


def get_html(url, cookie=""):
    try:
        response = requests.get(url, cookies={"cookie": cookie})
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        return response.text
    except requests.RequestException as e:
        print(e, file=sys.stderr)
        return False


def download(filename, url):
    filename = decode_html_entities(filename)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"文件已成功下载并保存到 {filename}")
    except requests.exceptions.RequestException as e:
        print(f"文件下载失败: {e}", file=sys.stderr)


def extract_data_from_html(content):
    # 使用正则表达式查找window.__DATA__中的内容
    match = match = re.search(r"window.__DATA__\s*=\s*({.*?});", content, re.DOTALL)
    if not match:
        print("未能找到window.__DATA__对象", file=sys.stderr)
        return None

    data_str = match.group(1)
    try:
        # 将字符串解析为JSON对象
        data = json.loads(data_str)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None

    try:
        nick_value = data.get("detail", {}).get("nick", "Nick not found")
        song_name = data.get("detail", {}).get("song_name", "Song name not found")
        play_url = data.get("detail", {}).get("playurl", "Play url not found")

        print(f"The nick value in detail is: {nick_value}", file=sys.stderr)
        print(f"The song name in detail is: {song_name}", file=sys.stderr)
        print(f"The play url in detail is: {play_url}", file=sys.stderr)
    except AttributeError:
        print(
            "The structure of the data does not match or data is None.", file=sys.stderr
        )
    return nick_value, song_name, play_url


def getSongs(uid, cookie=""):
    header = {
        # 定义手机的UA，因为触屏版本才可以获取所有音乐
        # 空的Referer不能使用
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Referer": "https://static-play.kg.qq.com/",
    }
    totalCount = 0  # 可以获取到的歌曲总数
    songList = []  # 全部歌曲列表
    user_information = {}  # 用户基本信息
    res = requests.get(
        f"https://kg.qq.com/node/personal?uid={uid}", cookies={"cookie": cookie}
    )

    if res.ok:
        for script in BeautifulSoup(res.text, "lxml").find_all("script"):
            if "window.__DATA__" in script.text:
                user_information = json.loads(
                    script.text[script.text.find("{") : script.text.rfind("};") + 1]
                )["data"]
                totalCount = user_information["ugc_total_count"]
                print(f"当前用户总歌曲数：{totalCount}")

                num = 15
                n = 1
                while n:
                    url = f"https://node.kg.qq.com/fcgi-bin/kg_ugc_get_homepage?"
                    params = {
                        "outCharset": "utf-8",
                        "from": "1",
                        "nocache": "",
                        "format": "json",
                        "type": "get_uinfo",
                        "start": n,
                        "num": num,
                        "share_uid": uid,
                        "g_tk": "",
                        "g_tk_openkey": "",
                    }
                    res = requests.get(url, params=params, headers=header)
                    if res.ok:
                        try:
                            start_brace_index = res.text.find("{")
                            end_brace_index = res.text.rfind("}")
                            if start_brace_index != -1 and end_brace_index != -1:
                                song_information = json.loads(
                                    res.text[start_brace_index : end_brace_index + 1]
                                )["data"]
                                if not song_information["ugclist"]:
                                    break
                                songList += song_information["ugclist"]
                                n += 1
                            else:
                                print(
                                    "响应文本中找不到有效的 JSON 格式", file=sys.stderr
                                )
                        except json.JSONDecodeError as e:
                            print(f"JSON 解析错误: {e}", file=sys.stderr)
                break
        else:
            print("未发现歌曲！", file=sys.stderr)
        # open(
        #     f'{user_information["kgnick"]}/{user_information["kgnick"]}_{uid}.json',
        #     "w",
        #     encoding="utf-8",
        # ).write(json.dumps(songList, indent=4, ensure_ascii=False))
    return songList


def downloadList(songList, cookie=""):
    for _, song in enumerate(songList):
        content = get_html(
            f"https://node.kg.qq.com/play?s={song['shareid']}", cookie=cookie
        )
        nick_name, song_name, play_url = "", "", ""
        if content:
            nick_name, song_name, play_url = extract_data_from_html(content)
        else:
            print("未能成功获取HTML内容", file=sys.stderr)
        download(f"downloads/{nick_name}/{nick_name}-{song_name}.m4a", play_url)


def downloadSong(url):
    html_content = get_html(url)
    nick_name, song_name, play_url = "", "", ""
    if html_content:
        nick_name, song_name, play_url = extract_data_from_html(html_content)
    else:
        print("未能成功获取HTML内容")
    download(f"{nick_name}-{song_name}.m4a", play_url)


def downloadPeople(url):
    uid = getuid(url)
    downloadList(getSongs(uid))


def getuid(url):
    parsed_url = urlparse(url)

    # 提取查询参数
    query_params = parse_qs(parsed_url.query)

    # 获取uid参数值
    uid = query_params.get("uid", [None])[0]

    return uid


if __name__ == "__main__":
    url = "https://static-play.kg.qq.com/node/personal_v2?uid=6a9a9c84272e348d&shareUid=6799998d2c2b368f&pageId=homepage_guest"
    print(getuid(url))
