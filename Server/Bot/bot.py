from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import path
from bidi.algorithm import get_display
import chromedriver_autoinstaller



""" Bot to find the book details,
    From --> 'https://simania.co.il'. """

# Path to chrome driver.
PATH = path.abspath('chromedriver')

""" Check if the current version of chromedriver exists
and if it doesn't exist, download it automatically,
then add chromedriver to path """
chromedriver_autoinstaller.install()


# Add \n to summary for new lines.
def new_lines(text):
    letter_list = text.split(' ')
    count = len(letter_list)
    new_text = str()
    while count >= 0:
        line = ' '.join(letter_list[:12] + ['\n'])
        new_text += line
        letter_list = letter_list[12:]
        count -= 12
    return new_text


def find_book(book, driver_path=PATH):

    driver = webdriver.Chrome()  # Get the update driver.
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
        # Save text as RTL (right to left).
        book_name_text = get_display(book_name.text)
        author_text = get_display(author.text)
        summary_text = get_display(summary.text)

        # Limit the letters in one line.
        summary_text = new_lines(summary_text)

        book_details = [book_name_text, author_text, summary_text, image.get_attribute('src')]

        driver.quit()
        return book_details

    except NameError or AttributeError:
        driver.quit()
        return None


if __name__ == "__main__":
    pass
