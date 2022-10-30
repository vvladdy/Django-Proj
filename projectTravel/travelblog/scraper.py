import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
import re

from travelblog.models import Category, Blog, Image

TIME_OUT = 10
logger = logging.getLogger('logit')



def download_image_to_local_media(img_url, image_name: str, blog: Blog):
    with requests.Session() as session:
        img_responce = session.get(img_url, timeout=TIME_OUT)
    logger.debug(img_url) # логгинг вместо print для записи инф.в файл
    # print(image_name)

    # к этой папке обращается из БД для того, чтобы достать фото
    with open(f'media/images/{image_name}', 'wb') as file:
        file.write(img_responce.content)

    Image.objects.get_or_create(
        image=f'images/{image_name}',
        base_url=img_url,
        blog=blog
    )


def process(html_string: str, url:str):
    soup = BeautifulSoup(html_string, 'html.parser')
    try:
        title = soup.select('.column_attr h1')
        if title == []:
            title = soup.select('h1')
        title = title[0].text.strip()
        print(title)

        images = soup.select('.vc_single_image-wrapper img')
        imag = [img.get('src') for img in images]

        imag_name = [name.split('/')[-1] for name in imag]
        # for im, name in zip(imag, imag_name):
        #     print(name)
        #     download_image_to_local_media(im, name, blog)


        categ_country = soup.select('.title')[0].text.replace(
            'Больше о ', '').replace('От ', '').replace('до ', '')
        cat_name = [nm for nm in categ_country.split(' ') if nm.istitle()]
        # print(f"O{' '.join(cat_name)}")


        textdesc = soup.select('.wpb_wrapper p')
        textdesc = textdesc[0].text.replace('(', '').replace(')', '').strip()\
                   + textdesc[1].text.strip()
        # print(textdesc)

        blog, _ = Blog.objects.get_or_create(
            slug=slugify(soup.select('.title')),
            defaults={
                'base_url': url,
                'title': title,
                'text': textdesc,
               'image': imag[2]
            }
        )

        for im, name in zip(imag, imag_name):
            print(name)
            download_image_to_local_media(im, name, blog)

        # for tit in title:
        #     tit, _ = Category.objects.get_or_create(title=tit)
        #     blog.categories.add(tit)

        country, _ = Category.objects.get_or_create(
            title=f"O {' '.join(cat_name)}",
            slug=slugify(soup.select('.title')),
            country=blog
        )

        # info = {
        #     'title': title1[0].text.strip(),
        #     'textdesc': text1[0].text.strip() + text1[1].text.strip(),
        #     'images': [img.get('src') for img in images]
        # }
        # print(info)

    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Parsing error: ', error, exc_tb.tb_lineno)


def worker(queue: Queue):
    while queue.qsize() > 0:
        url = queue.get()
        print('WORKING ON: ', url)
        # try:
        with requests.Session() as session:
            responce = session.get(
                url,
                allow_redirects=True,
                timeout=TIME_OUT
            )
            print(responce.status_code)
            status_code = [508, 404, 500, 503, 507]
            for code in status_code:
                if responce.status_code == code:
                    print('page not found: ', url)
                    break
            assert responce.status_code in (200, 301, 302), 'Bad responce'
        process(responce.text, url)
        # except (
        #     requests.Timeout,
        #     requests.ConnectionError,
        #     AssertionError
        # ) as error:
        #     print('Error: ', error)
        #     queue.put(url)
        print(queue.qsize())


def main():
    category_urls = ['https://loveyouplanet.com/blog']

    with requests.Session() as links_session:
        response = links_session.get(category_urls[0])

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('.post-title a')
    links = [link.get('href') for link in links]

    #print(links)

    queue = Queue()


    for url in links[:15]:
        queue.put(url)

    work_num = 1

    with ThreadPoolExecutor(max_workers=work_num) as executor:
        for i in range(work_num):
            executor.submit(worker, queue)

if __name__ == '__main__':
    main()
