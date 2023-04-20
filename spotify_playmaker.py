import os
import argparse
from random import uniform
from time import sleep
from selenium.webdriver import ActionChains
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from seleniumwire import webdriver


def setup_driver(headless):
    """Setup the Chrome driver with the required options."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver


def login(driver, email, password):
    """Login to Spotify using the given email and password."""
    driver.get('https://www.spotify.com')
    driver.get(
        'https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F%3F'
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-username'))
    ).send_keys(email)
    sleep(uniform(1, 2))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-password'))
    ).send_keys(password)
    sleep(uniform(1, 2))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-button'))
    ).click()
    sleep(uniform(1, 2))
    print(f'Logged in successfully')


def create_playlist(driver):
    """Create a new playlist in Spotify."""
    print(f'Creating new playlist...')
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@data-testid='create-playlist-button']")
        )
    ).click()


def search_artist(driver, artist):
    """Search for the given artist and click on the top result."""
    print(f'Searching for {artist}')
    sleep(uniform(4, 5))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/search"]'))
    ).click()
    sleep(uniform(3, 4))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'form[role="search"] input[data-testid="search-input"]')
        )
    ).send_keys(artist)
    sleep(uniform(3, 6))
    # click top result
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="herocard-click-handler"]'))
    ).click()
    sleep(uniform(4, 6))

    # select albums checkbox
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Albums']/ancestor::button"))
    ).click()
    sleep(uniform(4, 6))

    # click albums checkbox
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Show all']/parent::a"))
    ).click()
    sleep(uniform(4, 5))


def view_albums(driver):
    """Switch to the grid view for the albums."""
    button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='grid']"))
    )
    if button.get_attribute("aria-checked") == "false":
        button.click()
    sleep(uniform(4, 5))


def add_to_playlist(driver):
    # add to playlist option
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[@data-encore-id='type' and text()='Add to playlist']")
        )
    ).click()
    sleep(uniform(1, 1.5))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//ul[@data-depth='1']//li[@role='presentation'][3]")
        )
    ).click()
    sleep(uniform(0.6, 0.9))


def save_albums(driver):
    """Save all albums on the current page to the playlist."""
    parent_div = driver.find_element(By.XPATH, '//div[@data-testid="grid-container"]')
    child_divs = parent_div.find_elements(By.XPATH, './/div[@draggable="true"]')
    for child_div in child_divs:
        action = ActionChains(driver)
        action.context_click(child_div).perform()
        add_to_playlist(driver)


def rename_playlist(driver, playlist_name):
    """Rename the created playlist to the given playlist_name."""
    sleep(5)
    parent_div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//li[@role="listitem"]'))
    )
    first_child_div = WebDriverWait(parent_div, 10).until(
        EC.visibility_of_element_located((By.XPATH, './div[1]'))
    )
    action = ActionChains(driver)
    action.context_click(first_child_div).perform()

    button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//span[contains(text(),"Rename")]'))
    )
    button.click()

    # Add a wait after clicking the "Rename" button
    input_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//li[@role="listitem"]//input[@data-testid="rename-input"]')
        )
    )
    input_element.send_keys(playlist_name)
    input_element.send_keys(Keys.ENTER)
    sleep(3)
    driver.refresh()
    sleep(4)
    print(f'Renamed to {playlist_name} succesfully')


def main(playlist_name, artists, headless):
    """Main function to create a Spotify playlist with the given artists."""
    load_dotenv()
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    driver = setup_driver(headless)
    login(driver, email, password)
    create_playlist(driver)
    for artist in artists:
        search_artist(driver, artist)
        view_albums(driver)
        save_albums(driver)
    rename_playlist(driver, playlist_name)
    print(f'Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create a Spotify playlist with the given artists."
    )
    parser.add_argument("-playlistname", type=str, help="The name of the playlist.")
    parser.add_argument("-artists", type=str, help="A comma-separated list of artists.")
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Run the script in headless mode (default: headful).",
    )
    args = parser.parse_args()
    playlist_name = args.playlistname
    artists = args.artists.split(", ")
    headless = args.headless
    main(playlist_name, artists, headless)
