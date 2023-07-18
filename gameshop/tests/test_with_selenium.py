def test_login(helpers, driver_init):
    helpers().auth_user(driver_init)
    assert helpers().wait_of_element_located(xpath="//*[@id='navbarSupportedContent']/ul[2]/li[5]/a",
                                             driver_init=driver_init)


def test_product_detail(helpers, driver_init):
    #  проверка для неавторизованного пользователя:
    helpers().product_detail(driver_init)
    assert helpers().wait_of_element_located(xpath="//*[@id='id_login']", driver_init=driver_init)
    #  проверка для авторизованного пользователя:
    helpers().auth_user(driver_init)
    helpers().product_detail(driver_init)
    assert helpers().wait_of_element_located(xpath="/html/body/div/div/ul/div/div[1]/a/button", driver_init=driver_init)


def test_add_favorite(helpers, driver_init):
    helpers().add_favorite(driver_init)
    helpers().favorite(driver_init)
    assert helpers().wait_of_element_located(xpath="/html/body/div/div/ul/li[3]/a/img", driver_init=driver_init)
    delete_favorite_button = helpers().wait_of_element_located(xpath="/html/body/div/div/ul/li[4]/a/button",
                                                               driver_init=driver_init)
    delete_favorite_button.click()
    assert helpers().wait_of_element_located(xpath="/html/body/div/div/a/button", driver_init=driver_init)
