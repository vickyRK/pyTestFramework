import time
import pyautogui
import pytest
from selenium.webdriver.common.by import By
from testdata.testdata import TestData
from utilities.BaseClass import BaseClass


class TestModules(BaseClass):

    def test_TC001(self):
        log = self.getLogger()
        log.info("Add test steps")

    def test_TC002(self):
        log = self.getLogger()
        log.info("Add test steps")
