from playwright.sync_api import sync_playwright
import time
import os

def get_chapter_content(novel_id, page, chapter_num):
    try:
        # Navigate to the chapter URL
        url = f"https://m.xiaoshubao.net/read/456039/{chapter_num}.html"
        page.goto(url)
        
        # Wait for the content to load
        page.wait_for_selector("#nr1")
        
        # Get the chapter content
        content = page.locator("#nr1").inner_text()
        
        # Clean up the content
        # Remove the website notice at beginning and end
        lines = content.split('\n')
        cleaned_lines = [line.strip() for line in lines if not line.strip().startswith('小书包小说网')]
        cleaned_content = '\n'.join(cleaned_lines)
        
        return cleaned_content
    except Exception as e:
        print(f"Error scraping chapter {chapter_num}: {str(e)}")
        return None

def scrape(novel_id, end_chapter, single_chapter=0):
    # Create output directory if it doesn't exist
    os.makedirs(f"{novel_id}", exist_ok=True)

    if single_chapter == 0:
    # Read the last scraped chapter from end_chapter.txt if it exists
        start_chapter = 1
        if os.path.exists(f"{novel_id}/end_chapter.txt"):
            with open(f"{novel_id}/end_chapter.txt", "r") as f:
                last_chapter = int(f.read().strip())
                start_chapter = last_chapter + 1
    else:
        start_chapter = single_chapter

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        if single_chapter != 0:
            end_chapter = single_chapter  # Adjust this number based on total chapters
        else:
            end_chapter = end_chapter

        print(f"Scraping chapters {start_chapter} to {end_chapter}...")
        
        for chapter_num in range(start_chapter, end_chapter + 1):
            print(f"Scraping chapter {chapter_num}...")
            
            content = get_chapter_content(novel_id, page, chapter_num)
            
            if content:
                # Save to file
                with open(f"{novel_id}/chapter_{chapter_num}.txt", "w", encoding="utf-8") as f:
                    f.write(content)
                
                # Add delay to avoid overwhelming the server
                # time.sleep(2)  # 2 second delay between requests
            
            # Optional: Add a checkpoint every 50 chapters
            if chapter_num % 50 == 0:
                print(f"Checkpoint reached at chapter {chapter_num}")
                # time.sleep(5)  # Longer pause at checkpoints")
        with open(f"{novel_id}/end_chapter.txt", "w", encoding="utf-8") as f:
            f.write(str(end_chapter))
        browser.close()
    print("Scraping complete!")

def validate(novel_id, end_chapter):
    # Create a set of expected chapter filenames
    expected_files = {f"chapter_{i}.txt" for i in range(1, end_chapter + 1)}
    
    # Get actual files in directory
    actual_files = set(os.listdir(f"{novel_id}"))
    
    # Find missing chapters by getting difference between expected and actual
    missing_chapters = expected_files - actual_files
    
    if missing_chapters:
        print("Missing chapters:")
        for chapter in sorted(missing_chapters, key=lambda x: int(x.split('_')[1].split('.')[0])):
            print(chapter)
            scrape(novel_id, end_chapter, int(chapter.split('_')[1].split('.')[0]))
            print(f"Chapter {chapter} scraped!")
    else:
        print("No missing chapters found!")

def parse_url(url):
    # Extract novel_id and chapter_num from URL
    parts = url.strip().split('/')
    novel_id = int(parts[-2])
    chapter_num = int(parts[-1].split('.')[0])
    return novel_id, chapter_num

if __name__ == "__main__":
    url = input("Enter the novel URL: ")
    novel_id, end_chapter = parse_url(url)
    print(f"Novel ID: {novel_id}, End Chapter: {end_chapter}")
    # scrape(novel_id, end_chapter)
    validate(novel_id, end_chapter)