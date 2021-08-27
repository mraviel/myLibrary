from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import path

""" Bot to find the book details,
    From --> 'https://simania.co.il'. """


def find_book(book):

    l = []
    book_name, author, summary, image = "", "", "", ""

    # Path to chrome driver that I download
    PATH = path.abspath('chromedriver')
    driver = webdriver.Chrome(PATH)

    driver.get("https://simania.co.il")

    search = driver.find_element_by_id("query")
    search.send_keys(book)
    search.send_keys(Keys.RETURN)

    try:
        # If the program get the main book page.
        summary = driver.find_element_by_class_name("description")
        book_name = driver.find_element_by_xpath("//h2")
        author = driver.find_element_by_xpath("//h3")
        image = driver.find_element_by_class_name("bookImage")

    except:
        try:
            # If the program get multiple books options
            book_info = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "person"))
            )
            book_info.click()

            summary = driver.find_element_by_class_name("description")
            book_name = driver.find_element_by_xpath("//h2")
            author = driver.find_element_by_xpath("//h3")
            image = driver.find_element_by_class_name("bookImage")

        except:
            # If books does not appear
            print("The book does not exists")
            return None

    try:
        l.append(book_name.text)
        l.append(author.text)
        l.append(summary.text)
        l.append(image.get_attribute('src'))

        return l  # [book_name, author, summary, image]
    except NameError or AttributeError:
        return None

    # driver.quit()


if __name__ == "__main__":
    l = find_book("השנאה שנתתם")
    for i in l:
        print(i)
