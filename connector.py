import creds
from fyers_api import accessToken
import time
import re
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

log_path = creds.log_path
client_id = creds.client_id
secret_key = creds.secret_key
redirect_url = creds.redirect_url
response_type = creds.response_type
grant_type = creds.grant_type
username = creds.username
pin1 = creds.pin1
pin2 = creds.pin2
pin3 = creds.pin3
pin4 = creds.pin4

def generate_auth_code():
    url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state=state&scope=&nonce="
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    time.sleep(5)

    driver.execute_script(f"document.querySelector('[id=fy_client_id]').value = '{username}'")
    driver.execute_script("document.querySelector('[id=clientIdSubmit]').click()")
    time.sleep(30)

    driver.find_element("id", "verify-pin-page").find_element("id","first").send_keys(pin1)
    driver.find_element("id","verify-pin-page").find_element("id","second").send_keys(pin2)
    driver.find_element("id","verify-pin-page").find_element("id","third").send_keys(pin3)
    driver.find_element("id","verify-pin-page").find_element("id","fourth").send_keys(pin4)
    driver.execute_script("document.querySelector('[id=verifyPinSubmit]').click()")
    time.sleep(8)

    newurl = driver.current_url
    pattern = re.compile(r'(?<=auth_code=).*(?=&state)')
    auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
    auth_code = re.search(pattern,newurl).group()
    driver.quit()
    return auth_code


def generate_access_token():
	appSession = accessToken.SessionModel(client_id=client_id, secret_key=secret_key,grant_type=grant_type)
	appSession.set_token(generate_auth_code())
	response = appSession.generate_token()["access_token"]
	return response