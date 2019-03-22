import requests
from bs4 import BeautifulSoup
import datetime
import boto3
import json
from time import strftime, localtime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
IMDB_LOGIN_URL = '''https://www.imdb.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fap-signin-handler&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl91cyIsInJlZGlyZWN0VG8iOiJodHRwczovL3d3dy5pbWRiLmNvbS91c2VyL3VyMjM0NzczNjMvP3JlZl89bGduX25iX3Vzcl9wcm9mXzAifQ&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&tag=imdbtag_reg-20'''


def login_imdb():
	pass
	 


def deal_scrape():
	content=""
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options,service_log_path="/tmp/geckodriver.log")
	driver.get(IMDB_LOGIN_URL)
	driver.find_element_by_id("ap_email").send_keys("<your email>")
	driver.find_element_by_id("ap_password").send_keys("<your password>")
	driver.find_element_by_id("signInSubmit").click()
	if driver.session_id is not None:
		driver.get("https://www.imdb.com/chart/top")
		content= BeautifulSoup(driver.page_source,"html5lib")
		movie_list = content.select(".lister-list tr")
		unseen_movies = [movie.select(".titleColumn a")[0].get_text() for movie in movie_list if len(movie.select(".seen-widget.seen")) == 0]
		return "\n".join(unseen_movies)
	return ["salman"]	

def save_file_to_s3(bucket, file_name, data):
	s3 = boto3.resource('s3')
	obj = s3.Object(bucket, file_name)
	obj.put(Body=data)	

def scrape(event, context):
	data = deal_scrape()
	today = strftime("%d.%m.%Y %H:%M:%S", localtime())
	file_name = f"imdb-{today}"
	save_file_to_s3('imdb-scraper' , file_name , data)
	return "success"




