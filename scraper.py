# -*- coding: utf-8 -*-
# filename          : sraper.py
# description       : Deals.gg Scraper
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 07-16-2023
# version           : v1.0
# usage             : python main.py
# notes             : This script should not be run directly
# license           : MIT
# py version        : 3.11.1 (must run on 3.6 or higher)
#==============================================================================
import os
import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from file import *
from settings import *
from wait_until_element import Wait_Until_Element
from find_element import Find_Element

class Scraper(Find_Element, Wait_Until_Element):
	def __init__(self):
		init_timestamp = time.time()
		options = Options()
		user_data_dir = os.path.abspath("selenium_data")
		options.add_argument("--autoplay-policy=no-user-gesture-required")
		options.add_argument("log-level=3")
		options.add_argument("--ignore-certificate-errors-spki-list")
		options.add_argument(f"user-data-dir={user_data_dir}")
		if HEADLESS:
			options.add_argument("--headless")
			options.add_argument("--window-size=1920,1080")
			options.add_argument("--mute-audio")
			options.add_argument("--disable-gpu")
		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		super().__init__(self.driver)
		self.driver.set_window_position(0, 0)
		self.driver.set_window_size(1920, 1080)
		print(f"Completed init in {round(time.time()-init_timestamp,2)}s.")

	def open_link(self, url):
		self.driver.get(url)

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def refresh(self):
		self.driver.refresh()

	def scroll_down(self):
		SCROLL_PAUSE_TIME = 0.5

		# Get scroll height
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		while True:
			# Scroll down to bottom
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# Wait to load page
			time.sleep(SCROLL_PAUSE_TIME)

			# Calculate new scroll height and compare with last scroll height
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height

	def find_elements_by_attribute(self, attribute, value=None):
		if value is None:
			elements = self.find_elements_by_xpath(f"//*[@{attribute}]")
		else:
			elements = self.find_elements_by_xpath(f"//*[@{attribute}='{value}']")

		for element in elements:
			attribute_value = element.get_attribute(attribute)
			print(f"Element: {element.tag_name}, Attribute: {attribute}, Value: {attribute_value}")

		return elements

	def run(self, url):
		# wait_for_input()
		self.open_link(url)
		results = self.find_elements_by_attribute("data-container-game-id")
		print(f"Found {len(results)} results.")

		for result in results:
			game_id = result.get_attribute("data-container-game-id")
			url = result.find_element(
				By.XPATH, ".//a").get_attribute("href")
			try: official_price = result.find_element(
				By.XPATH, "div[3]/div[2]/div[1]/div[1]/div/span/span").text
			except NoSuchElementException: official_price = None
			try: keyshop_price = result.find_element(
				By.XPATH, "div[3]/div[2]/div[1]/div[2]/div/span/span").text
			except NoSuchElementException: keyshop_price = None
			title = result.find_element(
				By.XPATH, "div[3]/div[1]/div/a").text
			print(f"\nGame ID: {game_id}")
			print(f"URL: {url}")
			print(f"Title: {title}")
			print(f"Official Price: {official_price}")
			print(f"Keyshop Price: {keyshop_price}")

def main():
	# url = "https://gg.deals/games/?title="+ input("Enter game title: ").replace(" ", "+")
	url = "https://gg.deals/games/?platform=1,2&type=1&title="+ "jedi"
	scraper = Scraper()
	scraper.run(url)
	scraper.close()
	quit()
