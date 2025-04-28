import aiohttp
from bs4 import BeautifulSoup
import asyncio
import re
import aiosqlite
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
}

async def init_db():
    async with aiosqlite.connect("novels.db") as conn:
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS chapters (
            url VARCHAR PRIMARY KEY NOT NULL,
            text TEXT NOT NULL
        )
        ''')
        await conn.commit()

asyncio.run(init_db())

async def fetch_html(session, url):
    async with session.get(url) as response:
        html = await response.text()
        return BeautifulSoup(html, 'html.parser')

async def get_page_content(session, url):
    async with aiosqlite.connect("novels.db") as conn:
        async with conn.execute('SELECT text FROM chapters WHERE url = ?', (url,)) as cursor:
            data_fetched = await cursor.fetchone()
            if data_fetched:
                return data_fetched[0]

        soup = await fetch_html(session, url)
        text = '\n'.join(
            [
                item.text
                for item in soup.select('p')
                if item.text.strip() and 'translator' not in item.text.lower() and 'copyright' not in item.text.lower()
            ]
        )

        await conn.execute('INSERT INTO chapters (url, text) VALUES (?, ?)', (url, text))
        await conn.commit()

        return text

async def get_urls(session, number, chapter, keyword):
    number = int(number)
    chapter = int(chapter)
    

    search_url = f"https://novelfull.com/search?keyword={keyword}"
    search_soup = await fetch_html(session, search_url)

    novel_title = search_soup.select_one('.truyen-title a').text
    page = chapter // 50 + 1

    state = False
    links = []
    novel_image = None

    url_part1 = f'https://novelfull.com{search_soup.select_one('.truyen-title a')["href"]}?page='

    tasks = [
        fetch_html(session, f"{url_part1}{page_num}")
        for page_num in range(page, page + 2)
    ]
    page_soups = await asyncio.gather(*tasks)

    for page_num, soup1 in zip(range(page, page + 2), page_soups):
        titles = [item.text.split('-')[0] for item in soup1.select('#list-chapter .row li a')]
        page_links = [item['href'] for item in soup1.select('.list-chapter li a')]

        for index, (title, link) in enumerate(zip(titles, page_links)):
            if str(chapter) in title:
                last_page = (index + number) // 50 + page_num
                for sub_page_num in range(page_num + 1, last_page + 1):
                    sub_page_url = f"{url_part1}{sub_page_num}"
                    soup = await fetch_html(session, sub_page_url)
                    page_links += [item['href'] for item in soup.select('.list-chapter li a')]

                links = [f"https://novelfull.com{link}" for link in page_links[index:][:number]]
                state = True
                novel_image = "https://novelfull.com" + soup1.select_one('.book img')['src']
                break
        if state:
            break

    return links, novel_title, novel_image

def preprocess(text):
    # Regex patterns
    replacements = [
        (r'(?<!\w)\.(\w)\.', r'\1'),  # Replace ".letter." with "letter" only if not part of a longer word
        (r'(?<=\w)\.(\w)', r'\1'),    # Replace ".letter" when preceded by a word character
        (r'(\w)\.(?=\w)', r'\1'),     # Replace "letter." when followed by a word character
        (r'\+', ' plus'),             # Replace "+" with "plus"
    ]
    
    # Apply each regex replacement
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    
    return text

async def get_text(keyword, chapter, number):
    async with aiohttp.ClientSession(headers=headers) as session:
        urls, novel_title, novel_image = await get_urls(session, number, chapter, keyword)

        tasks = [get_page_content(session, url) for url in urls]
        texts = await asyncio.gather(*tasks)

        text = '\n'.join(texts)
        text = preprocess(text)

        text_array = [par.strip() for par in text.split("\n")]
        text_formatted = "".join([f'<p id="par{i}">{par}</p>' for i, par in enumerate(text_array)])

        return {
            'text': text,
            "title": novel_title,
            "image": novel_image,
            "formatted": text_formatted,
            "array": text_array
        }

# Example usage (Run inside an event loop):

# startTime = datetime.now()
# asyncio.run(get_text("alchemy emperor of the divine dao", 1, 100))
# print(f"Time taken: {datetime.now() - startTime}")
