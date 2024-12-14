import aiohttp
from bs4 import BeautifulSoup
import asyncio

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
}

async def fetch_html(session, url):
    async with session.get(url) as response:
        html = await response.text()
        return BeautifulSoup(html, 'html.parser')

async def get_page_content(session, url):
    soup = await fetch_html(session, url)
    return '\n'.join(
        [
            item.text
            for item in soup.select('p')
            if item.text.strip() and 'translator' not in item.text.lower() and 'copyright' not in item.text.lower()
        ]
    )

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

    tasks = []
    for page_num in range(page, page + 2):
        url_part1 = f'https://novelfull.com/infinite-mana-in-the-apocalypse.html?page='
        page_url = f"{url_part1}{page_num}"
        tasks.append(fetch_html(session, page_url))

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
    replacements = {
        '.a.p.e': 'ape', 'l.a.p': 'lap', '+': ' plus',
        '.a.r.e': 'are', '.o.a.n': 'oan', '.a.t.u.r.e': 'ature',
        '.r.e.a.s.t': 'reast', '.b.s.c.e.n.e': 'bscene',
        '.u.c.k.i.n.g': 'ucking', '.u.c.k.e.d': 'ucked', '.i.e.d': 'ed',
        '.U.C.K': 'uck', '.u.c.k': 'uck',
        '.h.e.s.t': 'hest', '.o.c.k': 'ock', '.e.m.e.n': 'emen',
        '.i.p.s': 'ips', '.u.m': 'um', '.u.s.t': 'ust', '.e.x': 'ex',
        '.d.u.l.t': 'dult', '.i.c.k': 'ick', '.r.o.s.t.i.t.u.t.e': 'rostitute'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
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
# print(asyncio.run(get_text("alchemy emperor of the divine dao", 1, 1)))


