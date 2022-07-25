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
            movie_url = 'https://imdb.com' + url
            credits = movie_url + 'fullcredits'

            yield scrapy.Request(credits, callback=self.parse_cast)
        
        next_page = response.xpath('//a[contains(@class, "next-page")]/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_cast(self, response):
        actors = [ x.strip() for x in response.xpath('//tr[@class="odd" or @class="even"]/td[not(@class="character")]//a/text()').getall() ]
        movie = response.xpath('//a[@itemprop="url"]/text()').get().strip()
        year = response.xpath('//h3/span[@class="nobr"]/text()').get().strip()

        yield {
            'movie': movie + ' ' + year,
            'actors': actors
        }
