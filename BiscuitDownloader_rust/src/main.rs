use html_escape::decode_html_entities;
use regex::Regex;
use reqwest::blocking::Client;
use scraper::{Html, Selector};
use serde_json::Value;
use std::collections::HashMap;
use std::error::Error;
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
/// Fetch HTML content from a given URL with optional cookie
pub fn get_html(url: &str, cookie: Option<&str>) -> Result<String, String> {
    // Create an HTTP client
    let client = Client::new();

    // Start building the request
    let mut request = client.get(url)
        .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        .header("Accept", "*/*")
        .header("Connection", "keep-alive");

    // Add the Cookie header if provided
    if let Some(cookie_value) = cookie {
        request = request.header("Cookie", cookie_value);
    }

    // Send the request and handle the response
    match request.send() {
        Ok(response) => {
            if response.status().is_success() {
                match response.text() {
                    Ok(text) => Ok(text),
                    Err(_) => Err("Failed to read response text".to_string()),
                }
            } else {
                Err(format!("HTTP error: {}", response.status()))
            }
        }
        Err(e) => Err(format!("Request failed: {}", e)),
    }
}

fn download(filename: &str, url: &str) -> Result<(), String> {
    let decoded_filename = decode_html_entities(filename).into_owned();
    // Create HTTP client
    let client = Client::new();
    // Send the GET request with streaming enabled
    let response = client
        .get(url)
        .send()
        .map_err(|e| format!("Request failed: {}", e))?;
    // Check if the status code indicates success
    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }
    // Ensure parent directory exists
    let path = Path::new(&decoded_filename);
    if let Some(parent_dir) = path.parent() {
        fs::create_dir_all(parent_dir)
            .map_err(|e| format!("Failed to create directories: {}", e))?;
    }
    // Open the file for writing
    let mut file = File::create(&path)
        .map_err(|e| format!("Failed to create file '{}': {}", decoded_filename, e))?;
    // Write the response body to the file in chunks
    let content = response
        .bytes()
        .map_err(|e| format!("Failed to read content: {}", e))?;
    file.write_all(&content)
        .map_err(|e| format!("Failed to write to file '{}': {}", decoded_filename, e))?;
    println!(
        "File successfully downloaded and saved to: {}",
        decoded_filename
    );
    Ok(())
}

fn extract_data_from_html(content: &str) -> Result<(String, String, String), Box<dyn Error>> {
    // Define the regular expression to match `window.__DATA__`
    let re = Regex::new(r"window\.__DATA__\s*=\s*(\{[^;]*\});")?;
    let caps = re
        .captures(content)
        .ok_or("Failed to find `window.__DATA__` object in the HTML content")?;

    // Extract the JSON string
    let data_str = caps
        .get(1)
        .ok_or("Failed to capture JSON content")?
        .as_str();

    // Parse the JSON string
    let data: Value = serde_json::from_str(data_str)?;

    // Extract the required fields
    let nick_value = data
        .get("detail")
        .and_then(|detail| detail.get("nick"))
        .and_then(|nick| nick.as_str())
        .unwrap_or("Nick not found")
        .to_string();

    let song_name = data
        .get("detail")
        .and_then(|detail| detail.get("song_name"))
        .and_then(|song_name| song_name.as_str())
        .unwrap_or("Song name not found")
        .to_string();

    let play_url = data
        .get("detail")
        .and_then(|detail| detail.get("playurl"))
        .and_then(|play_url| play_url.as_str())
        .unwrap_or("Play URL not found")
        .to_string();
    Ok((nick_value, song_name, play_url))
}

fn download_song(url: &str, cookie: Option<&str>) -> Result<(), Box<dyn Error>> {
    // Get HTML content
    let html_content = get_html(url, cookie)?;

    // Extract data from HTML content
    let (nick_name, song_name, play_url) = extract_data_from_html(&html_content)?;

    // Ensure the play URL is valid
    if play_url.is_empty() {
        return Err("Failed to extract a valid play URL.".into());
    }

    // Construct the file name
    let filename = format!("{}-{}.m4a", nick_name, song_name);

    // Download the song
    download(&filename, &play_url)?;

    Ok(())
}

fn extract_json(script_text: &str, key: &str) -> Result<String, String> {
    // 找到 `window.__FETCH_RES__` 的位置
    if let Some(start_pos) = script_text.find(key) {
        // 从 `window.__FETCH_RES__` 之后开始查找 JSON 的起始位置
        if let Some(json_start) = script_text[start_pos..].find('{') {
            let json_start_absolute = start_pos + json_start;

            // 从 JSON 开始位置查找 JSON 的结束位置 `};`
            if let Some(json_end) = script_text[json_start_absolute..].find("};") {
                let json_end_absolute = json_start_absolute + json_end; // 包括 `}`

                // 提取 JSON 数据
                let json_data = &script_text[json_start_absolute..=json_end_absolute];
                return Ok(json_data.to_string());
            } else {
                return Err("Failed to find the end of the JSON object".to_string());
            }
        } else {
            return Err("Failed to find the start of the JSON object".to_string());
        }
    }

    Err(format!("Key '{}' not found in the script", key))
}

fn get_songs(uid: &str, cookie: &str) -> Result<Vec<Value>, Box<dyn Error>> {
    let user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1";
    let referer = "https://static-play.kg.qq.com/";

    // Initialize HTTP client
    let client = Client::new();

    // Prepare headers
    let mut headers = reqwest::header::HeaderMap::new();
    headers.insert("User-Agent", user_agent.parse()?);
    headers.insert("Referer", referer.parse()?);
    headers.insert("Cookie", cookie.parse()?);

    // Fetch user information
    let user_url = format!("https://kg.qq.com/node/personal?uid={}", uid);
    let res = client.get(&user_url).headers(headers.clone()).send()?;

    if !res.status().is_success() {
        return Err(format!("Failed to fetch user information for UID: {}", uid).into());
    }

    let html = res.text()?;
    let document = Html::parse_document(&html);
    let script_selector = Selector::parse("script").unwrap();

    let mut song_list: Vec<Value> = Vec::new();

    for element in document.select(&script_selector) {
        let script_text = element.text().collect::<Vec<_>>().join("");
        if script_text.contains("window.__FETCH_RES__") {
            let json_data = extract_json(&script_text, "window.__FETCH_RES__")?;
            let parsed_old: Value = serde_json::from_str(&json_data)?;

            if let Some(parsed) = parsed_old.get("userInfoRes") {
                if let Some(data) = parsed.get("data") {
                    let total_count = data
                        .get("ugc_total_count")
                        .and_then(|v| v.as_u64())
                        .unwrap_or(0);
                    println!("Total song count: {}", total_count);

                    let num = 15;
                    let mut n = 1;

                    while n <= (total_count as usize + num - 1) / num {
                        let num_string = num.to_string();
                        let n_string = n.to_string();
                        let url = "https://node.kg.qq.com/fcgi-bin/kg_ugc_get_homepage?";
                        let mut params = HashMap::new();
                        params.insert("outCharset", "utf-8");
                        params.insert("from", "1");
                        params.insert("nocache", "");
                        params.insert("format", "json");
                        params.insert("type", "get_uinfo");
                        params.insert("start", &n_string);
                        params.insert("num", &num_string);
                        params.insert("share_uid", uid);
                        params.insert("g_tk", "");
                        params.insert("g_tk_openkey", "");

                        let res = client
                            .get(url)
                            .query(&params)
                            .headers(headers.clone())
                            .send()?;

                        if res.status().is_success() {
                            let json_text = res.text()?;
                            if let Some(start_index) = json_text.find('{') {
                                if let Some(end_index) = json_text.rfind('}') {
                                    let json_data = &json_text[start_index..=end_index];
                                    let parsed: Value = serde_json::from_str(json_data)?;
                                    if let Some(data) = parsed.get("data") {
                                        if let Some(ugclist) =
                                            data.get("ugclist").and_then(|v| v.as_array())
                                        {
                                            if ugclist.is_empty() {
                                                break;
                                            }
                                            song_list.extend(ugclist.clone());
                                        }
                                    }
                                }
                            }
                        } else {
                            eprintln!("Failed to fetch songs for page {}", n);
                            break;
                        }
                        n += 1;
                    }
                }
            }
        }
    }

    if song_list.is_empty() {
        eprintln!("No songs found!");
    }

    Ok(song_list)
}

fn download_list(
    song_list: &[serde_json::Value],
    cookie: Option<&str>,
) -> Result<(), Box<dyn Error>> {
    for song in song_list.iter() {
        let shareid = match song.get("shareid").and_then(|v| v.as_str()) {
            Some(id) => id,
            None => {
                eprintln!("Missing 'shareid' in song: {:?}", song);
                continue;
            }
        };
        let url = format!("https://node.kg.qq.com/play?s={}", shareid);
        let content = get_html(&url, cookie)?;
        let (nick_name, song_name, play_url) = extract_data_from_html(&content)?;

        // 构建文件保存路径
        let file_path = format!("downloads/{}/{}-{}.m4a", nick_name, nick_name, song_name);

        // 下载歌曲
        if let Err(err) = download(&file_path, &play_url) {
            eprintln!("Failed to download song '{}': {}", song_name, err);
        }
    }

    Ok(())
}
fn main() -> Result<(), Box<dyn Error>> {
    let uid = "";
    let cookie = Some("session=abc123");

    let songs = get_songs(uid, "")?;

    download_list(&songs, cookie)?;
    Ok(())
}
