Certainly! Here is your README in Markdown (`.md`) format for GitHub:

# Instagram Account Duplicator

**Code Originally Created By Perplexity AI**

Automate the process of duplicating a public Instagram account by scraping posts, downloading media, and uploading to a target account.

## Features

- **Scraping**
  - Uses Instagram's GraphQL API to fetch posts
  - Handles pagination for multiple posts
  - Retrieves both images and videos
  - Captures captions and media URLs

- **Download**
  - Saves media to a local directory
  - Preserves original file formats
  - Handles both images and videos

- **Upload**
  - Uses Instabot for Instagram automation
  - Maintains original captions
  - Includes 30-second delays between uploads to avoid detection

## Requirements

- **Install dependencies:**
  ```bash
  pip install httpx requests instabot
  ```
- **Create a directory for temporary files:**
  ```bash
  mkdir instagram_media
  ```

## Limitations

- **Account Requirements**
  - Source account must be public
  - Target account must have no 2FA enabled

- **Technical Constraints**
  - Instagram API changes may break scraping
  - Upload limits (~10 posts/hour recommended)
  - Carousel posts not supported

- **Risks**
  - Violates Instagram's Terms of Service
  - May trigger account verification
  - Potential for temporary blocks

## Usage

1. **Replace credentials in the script:**
   - `SOURCE_USERNAME`
   - `TARGET_USERNAME`
   - `TARGET_PASSWORD`

2. **Run the script:**
   ```bash
   python instagram_duplicator.py
   ```

## Optimization Notes

- **Add proxy rotation for large-scale operations**
- **Implement error retry logic**
- **Use S3/cloud storage instead of local files**
- **Add video duration checks (max 60s for IG)**
- **Include user-agent rotation in headers**

**This script automates the entire duplication process while handling media types and captions. Monitor your accounts for verification requests during/after execution.**
