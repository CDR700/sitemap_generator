# CDR700
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

class SitemapSpider(scrapy.Spider):
    name = "sitemap_spider"
    
    def __init__(self, *args, **kwargs):
        super(SitemapSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.allowed_domains = [urlparse(self.start_urls[0]).netloc]
        self.visited_urls = set()

    def parse(self, response):
        link_extractor = LinkExtractor(allow_domains=self.allowed_domains)
        links = link_extractor.extract_links(response)

        self.visited_urls.add(response.url)
        for link in links:
            if link.url not in self.visited_urls:
                yield response.follow(link, self.parse)

    def closed(self, reason):
        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for url in self.visited_urls:
            url_tag = ET.SubElement(urlset, "url")
            loc_tag = ET.SubElement(url_tag, "loc")
            loc_tag.text = url
        parsed_url = urlparse(self.start_urls[0])
        domain = parsed_url.netloc.replace('.', '_')
        filename = f"sitemap_{domain}.xml"

        tree = ET.ElementTree(urlset)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Sitemap saved as: {filename}")

if __name__ == "__main__":
    start_url = input("What is the url ? : ")
    process = CrawlerProcess()
    process.crawl(SitemapSpider, start_url=start_url)
    process.start() 
