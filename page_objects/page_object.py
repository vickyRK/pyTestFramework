from selenium.webdriver.common.by import By


class PageObject:

    def __init__(self, driver):
        self.driver = driver

    ele = (By.ID, "ID value")

    def ele_fun(self):
        return self.driver.find_element(*PageObject.ele)
