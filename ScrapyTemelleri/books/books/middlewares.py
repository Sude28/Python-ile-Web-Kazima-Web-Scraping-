# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


#✔ Her isteğe rastgele User-Agent ve Proxy atar.
#✔ Başarısız yanıtları (200 değilse) yeni User-Agent ve Proxy ile tekrar gönderir.
#✔ Bağlantı hatalarında (timeout, yasaklama vb.) isteği yeniden dener.


class RotateUserAgentAndProxyMiddleWare:
    def __init__(self,user_agents,proxies):
        self.user_agents = user_agents
        self.proxies = proxies


    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.getlist('USER_AGENT_LIST')
        proxies = crawler.settings.getlist('PROXY_LIST')
        return cls(user_agents, proxies) #Middleware'i User-Agent listesiyle başlatır.

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents) #self.user_agents içindeki rastgele bir User-Agent seçilir.
        proxy = random.choice(self.proxies)
        request.headers['User-Agent'] = user_agent #HTTP isteğinin User-Agent başlığı, rastgele seçilen User-Agent ile değiştirilir.
        request.meta['proxy'] = proxy
        spider.logger.info(f'Kullanılan user agent: {user_agent}, proxy: {proxy}')

    def process_response(self, request, response, spider):
        # 200 değilse request başarısız
        if response.status != 200:
            user_agent = random.choice(self.user_agents)  # self.user_agents içindeki rastgele bir User-Agent seçilir.
            proxy = random.choice(self.proxies)
            spider.logger.info(f'Request başarısız. Yeni user agent: {user_agent}, proxy: {proxy}')
            new_request = request.copy()
            new_request.headers['User-Agent'] = user_agent
            new_request.meta['proxy'] = proxy
            new_request.dont_filter = True
            return new_request
        return response

    def process_exception(self, request, exception, spider):
        user_agent = random.choice(self.user_agents)  # self.user_agents içindeki rastgele bir User-Agent seçilir.
        proxy = random.choice(self.proxies)
        spider.logger.info(f'Exception: {exception}.  Yeni user agent: {user_agent}, proxy: {proxy}')
        new_request = request.copy()
        new_request.headers['User-Agent'] = user_agent
        new_request.meta['proxy'] = proxy
        new_request.dont_filter = True
        return new_request

#Hata alınca değiştiriyoruz


#her HTTP isteğinde farklı bir User-Agent kullanarak bot algılanmasını önlemeye yardımcı oluyoruz
class RotateUserAgentMiddleware:
    def __init__(self,user_agents):
        self.user_agents = user_agents


    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.getlist('USER_AGENT_LIST')
        return cls(user_agents) #Middleware'i User-Agent listesiyle başlatır.

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents) #self.user_agents içindeki rastgele bir User-Agent seçilir.
        request.headers['User-Agent'] = user_agent #HTTP isteğinin User-Agent başlığı, rastgele seçilen User-Agent ile değiştirilir.
        spider.logger.info(f'Kullanılan user agent: {user_agent}')




class BooksSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BooksDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
