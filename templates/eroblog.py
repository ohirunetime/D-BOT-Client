import requests
import time

from domain.pornhub import pornhub_crawl
from domain.tube8 import tube8_crawl
from domain.extremetube import extremetube_crawl
from domain.javynow import javynow_crawl
from domain.redtube import redtube_crawl
from domain.youporn import youporn_crawl
from domain.spankbang import spankbang_crawl
from domain.sharevideos import sharevideos_crawl
from domain.xvideos import xvideos_crawl


from process1_postgres import InsertDatabase

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}


def domain_judge(eroblog_list, actress, LocalDatabaseURI, driver):

    for box in eroblog_list:
        link = box[0]
        domain = box[1]

        print("domain=", domain)

        if domain == 'PornHub':

            copy_content = pornhub_crawl(link)

        elif domain == 'Tube8':

            copy_content = tube8_crawl(link)

        elif domain == 'ExtremeTube':

            copy_content = extremetube_crawl(link)

        elif domain == 'YouPorn':

            copy_content = youporn_crawl(link)

        elif domain == 'RedTube':

            copy_content = redtube_crawl(link)

        elif domain == 'JavyNow':

            copy_content = javynow_crawl(link)

        elif domain == 'spankbang':

            copy_content = spankbang_crawl(link)

        elif domain == 'ShareVideos':

            copy_content = sharevideos_crawl(link, driver)

        elif domain == 'xvideos':
            copy_content = xvideos_crawl(link)

        else:
            copy_content = None

        if copy_content is not None:
            for i in copy_content:
                link = i[0]
                embedlink = i[1]
                domain = i[2]

                InsertDatabase(link, embedlink, domain,
                               actress, LocalDatabaseURI)
