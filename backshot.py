import requests
from bs4 import BeautifulSoup


def get_text(keyword, chapter, number):
    """
    Get the text of a specified chapter of a novel given its keyword.
    """

    number = int(number)
    chapter = int(chapter)

    url = f"https://novelfull.com/search?keyword={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    page = chapter // 50 + 1
    state = False
    for page_num in range(page-1, page + 2):
        url = f"https://novelfull.com{soup.select('div.list-truyen a')[0]['href']}?page={page_num}"

        response = requests.get(url, headers=headers)
        soup1 = BeautifulSoup(response.text, 'html.parser')


        for title, link in zip(
            [item.text for item in soup1.select('#list-chapter .row li a')],
            [item['href'] for item in soup1.select('#list-chapter li a')]
        ):
            if str(chapter) in title.split('-')[0]:
                url = f"https://novelfull.com{link}"
                state = True
                break
        if state:
            break

    texts = []
    for _ in range(number):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = '\n'.join(
            [
                item.text
                for item in soup.select('p')
                if item.text.strip() and 'translator' not in item.text.lower() and 'copyright' not in item.text.lower()
            ]
        )
        url = f"https://novelfull.com{soup.select('a.btn.btn-success')[1]['href']}"
        texts.append(text)

    text = '\n'.join(texts)
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
    text = text.replace('+', 'plus')

    return {'url': url, 'text': text}



print(get_text("alchemy emperor of the divine dao", "1", "3"))