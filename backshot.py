import requests
from bs4 import BeautifulSoup

## Issues:
# * perf: Make the data retrieval async to make it faster
# * feat: Make the data retrieval possible with url and number ignoring the chapter
# * feat: Change the code to javascript


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
}

def get_html(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')


def get_page_content(url):
    soup = get_html(url)
    return '\n'.join(
            [
                item.text
                for item in soup.select('p')
                if item.text.strip() and 'translator' not in item.text.lower() and 'copyright' not in item.text.lower()
            ]
        )


def get_urls(number, chapter, keyword):
    number = int(number)
    chapter = int(chapter)

    url = f"https://novelfull.com/search?keyword={keyword}"

    soup = get_html(url)

    novel_title = soup.select_one('.truyen-title a').text
    page = chapter // 50 + 1


    state = False
    for page_num in range(page-1, page + 2):
        url_part1 = f'https://novelfull.com/infinite-mana-in-the-apocalypse.html?page='
        url = f"{url_part1}{page_num}"
        soup1 = get_html(url)
        titles = [item.text.split('-')[0] for item in soup1.select('#list-chapter .row li a')]
        links = [item['href'] for item in soup1.select('.list-chapter li a')]
        # print(titles)
        for index, (title, link) in enumerate(zip(titles, links)):
            if str(chapter) in title:
                last_page = (index + number)//50 + page_num
                last_index = (index + number)%50 +(last_page - page_num)*50
                for page in range(page_num+1, last_page + 1):
                    url = f"{url_part1}{page}"
                    soup1 = get_html(url)
                    links += [item['href'] for item in soup1.select('.list-chapter li a')]
                
                links = [f"https://novelfull.com{link}" for link in links[index:last_index]]
                state = True
                novel_image = "https://novelfull.com"+soup1.select_one('.book img')['src']
                break
        if state:
            break
    
    return links, novel_title, novel_image


def preprocess(text):
    text = text.replace('.a.p.e', 'ape').replace('l.a.p', 'lap').replace('+', ' plus')
    text = text.replace('.a.r.e', 'are').replace('.o.a.n', 'oan').replace('.a.t.u.r.e', 'ature')
    text = text.replace('.r.e.a.s.t', 'reast')
    text = text.replace('.b.s.c.e.n.e', 'bscene')
    text = text.replace('.u.c.k.i.n.g', 'ucking').replace('.u.c.k.e.d', 'ucked').replace('.i.e.d', 'ed')
    text = text.replace('.U.C.K', 'uck').replace('.u.c.k', 'uck')
    text = text.replace('.h.e.s.t', 'hest').replace('.o.c.k', 'ock').replace('.e.m.e.n', 'emen')
    text = text.replace('.i.p.s', 'ips')
    text = text.replace('.u.m', 'um').replace('.u.s.t', 'ust').replace('.e.x', 'ex')
    text = text.replace('.d.u.l.t', 'dult')
    text = text.replace('.i.c.k', 'ick').replace('.r.o.s.t.i.t.u.t.e', 'rostitute')
    return text


def get_text(keyword, chapter, number):
    
    urls, novel_title, novel_image = get_urls(number, chapter, keyword)

    texts = []
    for url in urls:
        texts.append(get_page_content(url))

    text = '\n'.join(texts)
    text = preprocess(text)

    text_array = [par.strip() for par in text.split("\n")]
    text_formatted = "".join([f'<p id="par{i}">{par}</p>' for i,par in enumerate(text_array)])

    return {
        'text': text,
        "title":novel_title,
        "image":novel_image,
        "formatted":text_formatted,
        "array":text_array
        }


