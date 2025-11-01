from playwright.sync_api import Page, expect
from utils.logger import logger
import time
import logging
import traceback
import os

class LoginClass:
    def __init__(self, page: Page):
        self.page = page
        self.email_field_xpath =  "//form/descendant::input[@id='login_email']"
        self.password_field_xpath =  "//form/descendant::input[@id='login_password']"
        self.password_show_xpath =  "//form[contains(@class, 'form-signin') and contains(@class, 'form-login')]/descendant::div[@class='password-field']//span"
        self.login_btn_xpath =  "//button[normalize-space()='Login']"
        self.popup_input =  "//div[@class='form-group']/descendant::input[contains(@data-fieldname, 'password')]"
        self.popup_password_show =  "//div[@class='form-group']/descendant::div[@class='toggle-password']"
        self.popup_submit_btn =  "//div[@class='form-group']/descendant::button[contains(@data-fieldname, 'submit')]"
        self.popup_label =  "//div[@class='form-group']/child::div[@class='clearfix']//label[@class='control-label reqd']"
        self.invalid_login_text =  "//button[normalize-space()='Invalid Login. Try again.']"
        self.popup_close_xpath =  "//div[@class='modal-actions']/descendant::button[@data-dismiss='modal']"
        self.search_box_xpath =  "//form[contains(@role, 'search')]/descendant::input[@id='navbar-search']"
        self.apps_popup_xpath = "//a[@href='/app/home']"
        self.login_fail_text = "//button[normalize-space()='Invalid Login. Try again.']"

    # login function
    def login_page_load(self):
        try:
            url = "http://127.0.0.1:8000/#login"
            logger.info(f"Navigating to login page: {url}")
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"D:\\Playwright\\reports\\screenshots\\login_form{timestamp}.png"
            self.page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot saved at {screenshot_path}")
            site_url = self.page.url
            return site_url
        except Exception as e:
            logger.error(f"Error while loading login page: {str(e)}")
            traceback.print_exc()
            return f"Exception: {str(e)}"
    
    # login form field access
    def login_screen_validate(self, user_email, password, expected_result="Success"):
        try:
            logger.info(f"Attempting login with Email: {user_email} | Password: {password}")
            user_email = str(user_email or "").strip()
            password = str(password or "").strip()
            # Fill credentials
            email_field = self.page.locator(self.email_field_xpath)
            password_field = self.page.locator(self.password_field_xpath)

            email_field.clear()
            password_field.clear()

            email_field.fill(user_email)
            password_field.fill(password)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"D:\\Playwright\\reports\\screenshots\\login_form_{timestamp}.png"
            self.page.screenshot(path=screenshot_path)
            self.page.wait_for_timeout(2000)

            email_valid = email_field.evaluate("el => el.validity.valid")
            print("Email Valid Check", email_valid)
            password_valid = password_field.evaluate("el => el.validity.valid")
            print("Password Valid Check", password_valid)

            # email field validation
            if not email_valid:
                validation_msg = email_field.evaluate("el => el.validationMessage")
                print("Email Valid Required Check", validation_msg)
                logger.info(f"Email validation message: {validation_msg}")
                return validation_msg
            
            # password field validation 
            if not password_valid:
                validation_msg = password_field.evaluate("el => el.validationMessage")
                print("Password Valid Required Check", validation_msg)
                logger.info(f"Password validation message: {validation_msg}")
                return validation_msg
            
            login_btn = self.page.locator(self.login_btn_xpath)
            login_btn.click()
            logger.info("Clicked login button.")

            error_button_check = self.page.locator(self.login_fail_text)
            apps_popup = self.page.locator(self.apps_popup_xpath)

            self.page.wait_for_timeout(2000)

            if error_button_check.is_visible(timeout=5000):
                error_button_check.is_visible()
                print("Error Button")
                actual_text = error_button_check.text_content().strip()
                print("Login Fail Actual Text",actual_text)
                logger.info(f"Login Fail Actual Text {actual_text}")
                return actual_text
            
            if apps_popup.is_visible():
                print("Apps Popup")
                apps_popup.click()
            self.page.wait_for_timeout(3000)
            page_title = self.page.title()
            print("Page Title", page_title)
            self.page.reload()

            if "Home" in page_title:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"D:\\Playwright\\reports\\screenshots\\home_page_{timestamp}.png"
                self.page.screenshot(path=screenshot_path)
                self.page.wait_for_timeout(3000)
                return "Login Successful"
        except Exception as e:
            traceback.print_exc()
            self.page.wait_for_timeout(3000)
            return f"Exception: {str(e)}"