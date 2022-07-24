#! /usr/bin/env python3

# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 itachi <itachi@ASUS-G14>
#
# Distributed under terms of the MIT license.

"""
"""
import scrapy

class MoviesSpider(scrapy.Spider):
    name = 'movies'

    start_urls = [
        #'https://www.imdb.com/india/top-rated-indian-movies/'
        'https://www.imdb.com/list/ls004221468/',
    ]

    def parse(self, response):
        urls = response.xpath('//h3[@class="lister-item-header"]/a/@href').getall()

        for url in urls:
            yield {
                'movie_link' : 'https://imdb.com' + url
            }
        
        next_page = response.xpath('//a[contains(@class, "next-page")]/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
