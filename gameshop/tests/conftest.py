import pytest
from products.models import Category, Product

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def password():
    return 'qwertyasdfgh1234'


@pytest.fixture
def create_user(db, django_user_model, password):
    def _user(**kwargs):
        kwargs['password'] = password
        if 'username' not in kwargs:
            kwargs['username'] = "test_user"
        # if 'email' not in kwargs:
        # kwargs['email'] = "test_user@email.com"
        return django_user_model.objects.create_user(**kwargs)
    return _user


@pytest.fixture
def auto_login_user(db, client, create_user):
    def _login(user=None):
        if user is None:
            user = create_user()
        login = client.login(username=user.username, password=user.password)
        if not login:
            client.force_login(user)
        return client, user
    return _login


@pytest.fixture
def create_product(db, client):
    category = Category.objects.create(title='Shooter', slug='sh')
    product = Product.objects.create(title='Qwerty', price='1234', image=None, slug='asd',
                                     cat=Category.objects.filter(title='Shooter').first())
    # product = Product.objects.create(title='second', price='1000', image=None, slug='sec',
    #                                  cat=Category.objects.filter(title='Shooter').first())
    return category, product


# Инициализция драйвера
@pytest.fixture
def driver_init():
    options = webdriver.ChromeOptions()
    service = Service(executable_path='/chromedriver.exe')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://127.0.0.1:8000/")
    driver.maximize_window()
    yield driver
    driver.close()


class Helper:
    @staticmethod
    def wait_of_element_located(xpath, driver_init):
        element = WebDriverWait(driver_init, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )
        return element

    def auth_user(self, driver_init):
        login_button = driver_init.find_element(By.XPATH, "//*[@id='navbarSupportedContent']/ul[2]/a")
        login_button.click()
        input_mail = self.wait_of_element_located(xpath="//*[@id='id_login']", driver_init=driver_init)
        input_password = self.wait_of_element_located(xpath="//*[@id='id_password']", driver_init=driver_init)
        authentication_button = self.wait_of_element_located(xpath="/html/body/div/form/button", driver_init=driver_init)

        input_mail.send_keys("qwerty@mail.ru")
        input_password.send_keys("1234")
        authentication_button.send_keys(Keys.RETURN)

    def catalog(self, driver_init):
        catalog_button = self.wait_of_element_located(xpath="//*[@id='navbarSupportedContent']/ul[1]/li[2]/a",
                                                      driver_init=driver_init)
        catalog_button.click()

    def product_detail(self, driver_init):
        self.catalog(driver_init)
        product_button = self.wait_of_element_located(xpath="/html/body/div/div/div[1]/ul/li[3]/a/img",
                                                      driver_init=driver_init)
        product_button.click()

    def favorite(self, driver_init):
        favorite_button = self.wait_of_element_located(xpath="//*[@id='navbarSupportedContent']/ul[2]/li[4]/a",
                                                       driver_init=driver_init)
        favorite_button.click()

    def add_favorite(self, driver_init):
        self.auth_user(driver_init)
        self.product_detail(driver_init)
        add_favorite_button = self.wait_of_element_located(xpath="/html/body/div/div/ul/div/div[1]/a/button",
                                                           driver_init=driver_init)
        add_favorite_button.click()


@pytest.fixture
def helpers():
    return Helper
