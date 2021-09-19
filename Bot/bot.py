from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import path

""" Bot to find the book details,
    From --> 'https://simania.co.il'. """

# Path to chrome driver.
PATH = path.abspath('chromedriver')


def find_book(book, driver_path=PATH):

    driver = webdriver.Chrome(driver_path)  # driver.
    driver.get("https://simania.co.il")  # Enter the website.

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
            driver.quit()
            print("The book does not exists")
            return None

    try:
        book_details = [book_name.text, author.text, summary.text, image.get_attribute('src')]

        driver.quit()
        return book_details

    except NameError or AttributeError:
        driver.quit()
        return None


if __name__ == "__main__":
    pass
