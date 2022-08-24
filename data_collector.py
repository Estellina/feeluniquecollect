import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
import glob
from selenium.common.exceptions import TimeoutException
import time
import os
import random
from init_dict import (
    init_product_dict, init_reviews_dict
)

OPTIONS = Options()
PATH_PRODUCT = os.path.join(os.curdir, 'products')
PATH_REVIEWS_TEST = os.path.join(os.curdir, 'reviews_test')
PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')
PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')
driver = webdriver.Chrome(PATH_DRIVER, options=OPTIONS)

products_urls = []
for url_dict in glob.glob(os.path.join(PATH_URLS_NEW, '*.json')):
    try:
        for products_url in json.load(open(url_dict, 'r', encoding='utf8')):
            products_urls.append(products_url)
    except Exception as e:
        print(e)
        pass


def collect_product_data():
    product_dict = init_product_dict()
    product_data = []
    try:
        driver.get('https://us.feelunique.com/p/BIODERMA-Atoderm-Hand-and-Nail-Cream-50ml')
        print("----Loading the page----")
        cookie_btn = WebDriverWait(driver, 10).until(ec.presence_of_element_located((
            By.ID, 'notice-ok')))
        cookie_btn.click()
        print("[LOG] Click on the cookies button.")
        time.sleep(random.uniform(1, 5))
    except:
        pass

    try:
        product_dict['product_name'] = driver.find_element(By.CSS_SELECTOR, 'h1[class="fn"]').text
        print(product_dict['product_name'])
    except:
        print("error")

    try:
        product_dict['product_information'] = driver.find_element(By.CSS_SELECTOR,
                                                                  'div[class="Layout-golden-main"]').text

        print(product_dict['product_information'])
    except:
        print('did not work')
    try:
        product_dict['product_price'] = driver.find_element(By.CSS_SELECTOR, 'span[class="Price"]').text
        print(product_dict['product_price'])
    except:
        print("l")
    try:
        product_dict['product_availability'] = driver.find_element(By.CSS_SELECTOR,
                                                                   'div[class="stock-level h-display-ib u-nudge-top '
                                                                   'h-third-l"]').text
        print(product_dict['product_availability'])
    except:
        print('l')

    product_data.append(product_dict)
    driver.delete_all_cookies()
    driver.quit()
    print('----saving the product data ----')
    with open(os.path.join(
            PATH_PRODUCT, 'product.json' + str(
                time.strftime('%Y_%m_%d_%H_%M_%S'))), 'w', encoding='utf-8') as file_to_dump:
        json.dump(product_data, file_to_dump, indent=4, ensure_ascii=False)


def collect_reviews_data():
    reviews_data = []

    try:
        driver.get('https://us.feelunique.com/p/BIODERMA-Atoderm-Hand-and-Nail-Cream-50ml')
        print("----Loading the page----")
        cookie_btn = WebDriverWait(driver, 10).until(ec.presence_of_element_located((
            By.ID, 'notice-ok')))
        cookie_btn.click()
        print("[LOG] Click on the cookies button.")
        time.sleep(random.uniform(1, 5))
    except:
        pass

    while True:

        try:
            reviews = WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located((
                By.CSS_SELECTOR, 'li[itemprop = review]')))

        except KeyboardInterrupt:
            exit("[LOG] The collect has been interrupted by the user.")

        except TimeoutException:
            print("[LOG] There aren't any reviews on the current page.")
            pass

        except Exception as e:
            print(e)
            pass

        for i, review in enumerate(reviews):
            review_dict = init_reviews_dict()
            try:
                review_dict['review_rating'] = review.find_element(By.CSS_SELECTOR,
                                                                   'meta[itemprop="ratingValue"]').get_attribute(
                    'content')
                print(review_dict['review_rating'])
            except:
                print("review rating not collected")
                pass
            try:
                review_dict['review_title'] = review.find_element(By.CSS_SELECTOR, 'h3[class="bv-content-title"]').text
                print(review_dict['review_title'])
            except:
                print('review title not collected')
                pass
            try:
                review_dict['review_author'] = review.find_element(By.CSS_SELECTOR, 'span[class="bv-author"]').text
                print(review_dict['review_author'])

            except:
                print('review author not collected')
                pass
            try:
                review_dict['review_text'] = review.find_element(By.CSS_SELECTOR,
                                                                 'div[class="bv-content-summary-body-text"]').text
                print(review_dict['review_text'])

            except:
                print('review text not collected')
                pass
            try:
                review_dict['review_date'] = review.find_element(By.CSS_SELECTOR,
                                                                 'span[class="bv-content-datetime-stamp"]').text
                print(review_dict['review_date'])

            except:
                print('review date not collected')
                pass

            reviews_data.append(review_dict)
        print('----saving all the reviews data-----')
        with open(os.path.join(
                PATH_REVIEWS_TEST, 'reviews_test.json' + str(
                    time.strftime('%Y_%m_%d_%H_%M_%S'))), 'w', encoding='utf-8') as file_to_dump:
            json.dump(reviews_data, file_to_dump, indent=4, ensure_ascii=False)
            print("all the reviews on this page were collected")

        try:
            more_reviews_btn = WebDriverWait(driver, 10).until(ec.presence_of_element_located((
                By.CSS_SELECTOR, 'li[class*="buttons-item-next"] > a[class*="bv-content-btn-pages-active"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", more_reviews_btn)
            driver.execute_script("arguments[0].click();", more_reviews_btn)
            print("[LOG] Click on show more reviews button.")
            time.sleep(random.uniform(1, 5))

        except TimeoutException:
            print("[LOG] There isn't any more reviews to show.")
            break

        except KeyboardInterrupt:
            print("[LOG] The collect has been interrupted by the user.")
            break

        except:
            break


def main():
    collect_product_data()
    collect_reviews_data()

    driver.quit()


if __name__ == "__main__":
    main()
