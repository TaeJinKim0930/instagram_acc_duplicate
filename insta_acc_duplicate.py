import os
import json
import httpx
import requests
from instabot import Bot
from urllib.parse import quote
import time

# Configuration
SOURCE_USERNAME = "your_source_username"  # Public account to duplicate
TARGET_USERNAME = "your_target_username"
TARGET_PASSWORD = "your_target_password"
TEMP_DIR = "instagram_media"
INSTAGRAM_DOCUMENT_ID = "8845758582119845"  # GraphQL query ID (may change over time)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "x-ig-app-id": "936619743392459"
}

def ensure_dir(path):
    """Create directory if not exists"""
    os.makedirs(path, exist_ok=True)

def get_user_id(username):
    """Get Instagram user ID from username"""
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    response = httpx.get(url, headers=HEADERS)
    return response.json()["data"]["user"]["id"]

def scrape_user_posts(user_id, max_posts=12):
    """Scrape user posts via GraphQL"""
    posts = []
    base_url = "https://www.instagram.com/graphql/query/"
    variables = {
        "id": user_id,
        "first": max_posts,
        "after": None
    }
    
    while True:
        encoded_vars = quote(json.dumps(variables, separators=(",", ":")))
        url = f"{base_url}?query_hash={INSTAGRAM_DOCUMENT_ID}&variables={encoded_vars}"
        response = httpx.get(url, headers=HEADERS)
        data = response.json()
        
        # Extract posts
        edges = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        posts.extend([edge["node"] for edge in edges])
        
        # Pagination
        page_info = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]
        if not page_info["has_next_page"]:
            break
        variables["after"] = page_info["end_cursor"]
    
    return posts

def download_media(url, filename):
    """Download image/video to local file"""
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def upload_media(bot, media_path, caption, is_video=False):
    """Upload media to Instagram"""
    if is_video:
        bot.upload_video(media_path, caption=caption)
    else:
        bot.upload_photo(media_path, caption=caption)

def main():
    ensure_dir(TEMP_DIR)
    
    # Step 1: Scrape source account
    print(f"Scraping posts from @{SOURCE_USERNAME}")
    user_id = get_user_id(SOURCE_USERNAME)
    posts = scrape_user_posts(user_id)
    print(f"Found {len(posts)} posts")
    
    # Step 2: Download media
    downloaded_files = []
    for i, post in enumerate(posts):
        try:
            # Determine media type and URL
            is_video = post["is_video"]
            media_url = post["video_url"] if is_video else post["display_url"]
            ext = "mp4" if is_video else "jpg"
            filename = os.path.join(TEMP_DIR, f"post_{i+1}.{ext}")
            
            # Download media
            print(f"Downloading media {i+1}/{len(posts)}")
            download_media(media_url, filename)
            downloaded_files.append((filename, post["edge_media_to_caption"]["edges"][0]["node"]["text"], is_video))
        except Exception as e:
            print(f"Error downloading post {i+1}: {str(e)}")
    
    # Step 3: Upload to target account
    bot = Bot()
    print(f"Logging into @{TARGET_USERNAME}")
    bot.login(username=TARGET_USERNAME, password=TARGET_PASSWORD)
    
    for i, (file_path, caption, is_video) in enumerate(downloaded_files):
        try:
            print(f"Uploading {i+1}/{len(downloaded_files)}")
            upload_media(bot, file_path, caption, is_video)
            print(f"Uploaded: {caption[:30]}...")
            time.sleep(30)  # Avoid rate limits
        except Exception as e:
            print(f"Error uploading post {i+1}: {str(e)}")
    
    bot.logout()
    print("Duplication process completed")

if __name__ == "__main__":
    main()
