from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyquery import PyQuery as PQ
import time
from selenium.webdriver.common.proxy import ProxyType

def pagedown():
    for i in range (1,3):
        time.sleep(2)
        wait.until(expected.presence_of_element_located(
            (By.XPATH, '//*[@id="resultList"]/div[1]/table/tbody/tr[1]/td/div/a[2]')))
        #输出文书列表结果
        print("html=====" + driver.page_source)
        docids = driver.find_element_by_class_name("dataItem")

        print("docid number====" + driver.page_source.count("DocIds").__str__())
        # print(html)
        print("html=====end")


        next = driver.find_element_by_class_name('next')
        #next = driver.find_element_by_css_selector('#pageNumber > a.next')
        print("翻页对象的文本为：")
        print(next.location)
        print(next.get_attribute("innerText"))
        print(PQ(next).html())

        page = driver.find_element_by_class_name('pageNumber')


        print("页数对象的文本为：")
        print(page.location)
        print(page.get_attribute("innerText"))
        print(PQ(page).html())
        #以下模拟点击


        pageNumber = driver.find_element_by_class_name("pageNumber")#找到并设置页数
        print("page_source===="+driver.page_source)
        print("pagesize====="+pageNumber.get_attribute("pagesize"))
        #pageNumber.__setattr__("pagesize", "20")
        print("pagesize set =====" + pageNumber.get_attribute("pagesize"))
        driver.execute_script("$(arguments[0]).click()", next)

        time.sleep(2)
        # pageNumber > a.next
        #next.click()
        wait.until(expected.presence_of_element_located(
            (By.XPATH, '//*[@id="resultList"]/div[1]/table/tbody/tr[1]/td/div/a[2]')))
        #html = PQ(driver.page_source)


if __name__ == '__main__':

    #driver = webdriver.PhantomJS()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    )
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = '139.224.80.139:3128'
    #proxy.add_to_capabilities(dcap)

    service_args = []
    service_args.append('--load-images=no')  ##关闭图片加载
    service_args.append('--disk-cache=yes')  ##开启缓存
    #service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    print(driver.capabilities)


    driver.get("http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+%E5%8C%97%E4%BA%AC%E5%B8%82%E9%AB%98%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2+++%E9%AB%98%E7%BA%A7%E6%B3%95%E9%99%A2:%E5%8C%97%E4%BA%AC%E5%B8%82%E9%AB%98%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2")


    data = driver.title
    #time.sleep(2)
    print((data))
    #print(driver.find_element_by_class_name("contentStyle").text)
    wait = WebDriverWait(driver, timeout=150)
    wait.until(expected.presence_of_element_located(
        (By.XPATH, '//*[@id="resultList"]/div[1]/table/tbody/tr[1]/td/div/a[2]')))

    data = driver.title
    wait.until(expected.presence_of_element_located(
        (By.XPATH, '//*[@id="pageNumber"]/a[5]')))
    #next = driver.find_element_by_xpath('//*[@id="pageNumber"]/a[5]')

    #docids = driver.find_element_by_class_name("dataItem")
    #print(docids.text)
    print("docid number====" + driver.page_source.count("DocIds").__str__())
    #切换为每页20条
    selected = driver.find_element_by_id("12_input_20")
    driver.execute_script("$(arguments[0]).click()", selected)
    pagedown()
