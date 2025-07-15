import pandas as pd
from linkedin_scraper import scrape_linkedin
from x_scraper import scrape_x
from config import OUTPUT_FILE
from config import TXT_OUTPUT_FILE
from selenium.webdriver.chrome.options import Options

def main():
    linkedin_posts = scrape_linkedin()
    x_posts = scrape_x()
    all_posts = linkedin_posts + x_posts

    # Optionally deduplicate posts by link
    for post in all_posts:
        if 'links' not in post:
            post['links'] = extract_links(post.get('text', ''))

    df = pd.DataFrame(all_posts)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(all_posts)} posts to {OUTPUT_FILE}")

    write_tools_to_txt(all_posts)

def write_tools_to_txt(posts, filename=TXT_OUTPUT_FILE):
    seen_links = set()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Top New Automated/Agentic Coding Tools and Platforms\n")
        f.write("===============================================\n\n")
        count = 0
        for post in posts:
            links = post.get('links', [])
            for link in links:
                # Only add unique, likely product/company links (not generic social links)
                if link not in seen_links and not any(domain in link for domain in ["linkedin.com", "twitter.com", "x.com"]):
                    seen_links.add(link)
                    count += 1
                    f.write(f"{count}. {post.get('platform', '')} | {post.get('keyword', '')}\n")
                    f.write(f"Link: {link}\n")
                    if 'text' in post:
                        snippet = post['text'].replace('\n', ' ')[:200]
                        f.write(f"Context: {snippet}...\n")
                    f.write("\n")
    print(f"Saved {count} unique tool links to {filename}")


if __name__ == "__main__":
    main()
