from pages.login_page import LoginClass
from utils.excel_utils import read_data, write_data
from utils.logger import logger
import pytest
import time
import allure
import pandas as pd

@allure.title("Test the Valid Email/Password")
@allure.testcase("TC-001")
@allure.description("Test the Valid Email/Password")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login Form Test")
@allure.step("Verify and Load the Site URL")
def test_valid_login(page, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (2, 3) 
    password_cell = (2, 4)
    expected_msg_cell = (2,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load()
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    time.sleep(3)
    try:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=2, column=6, data=res)
    except Exception as e:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=2, column=6, data=res)

@allure.title("Test the Login Screen InValid Email/Password")
@allure.testcase("TC-002")
@allure.description("Test the Login Screen InValid Email/Password")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login Form Test")
@allure.step("Verify and Load the Site URL")
def test_invalid_login_with_email_password(page, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (3, 3) 
    password_cell = (3, 4)
    expected_msg_cell = (3,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load()
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    time.sleep(3)
    try:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=2, column=6, data=res)
    except Exception as e:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=3, column=6, data=res)
    
@allure.title("Test Login Screen without User Email it should not be allowed")
@allure.testcase("TC-003")
@allure.description("Test Login Screen without User Email it should not be allowed")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login Form Test")
@allure.step("Verify and Load the Site URL")
def test_invalid_login_without_email(page, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (4, 3) 
    password_cell = (4, 4)
    expected_msg_cell = (4,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    
    email_empty_value = str(email_read_from_excel or "").strip()
    print("Email Empty Value", email_empty_value)
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load()
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_empty_value, password_read_from_excel)
    time.sleep(3)
    try:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=4, column=6, data=res)
    except Exception as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=4, column=6, data=res)
        allure.attach(
            page.screenshot(full_page=True),
            name="Login_Failure_Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        raise e
    
@allure.title("Test Login Screen Without Password it should not be allowed")
@allure.testcase("TC-004")
@allure.description("Test Login Screen Without Password it should not be allowed")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login Form Test")
@allure.step("Verify and Load the Site URL")
def test_invalid_login_without_password(page, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (5, 3) 
    password_cell = (5, 4)
    expected_msg_cell = (5,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    password_empty_value = str(password_read_from_excel or "").strip()
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load()
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_read_from_excel, password_empty_value)
    time.sleep(3)
    try:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=5, column=6, data=res)
    except Exception as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=5, column=6, data=res)
        allure.attach(
            page.screenshot(full_page=True),
            name="Login_Failure_Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        raise e
    
@allure.title("Test Login Screen with useremail as number should not be allowed")
@allure.testcase("TC-005")
@allure.description("Test Login Screen with useremail as number should not be allowed")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login Form Test")
@allure.step("Verify and Load the Site URL")
def test_invalid_login_with_useremail_as_number(page, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (6, 3) 
    password_cell = (6, 4)
    expected_msg_cell = (6,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    email_empty_value = int(email_read_from_excel or "")
    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load()
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_empty_value, password_read_from_excel)
    time.sleep(3)
    try:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=6, column=6, data=res)
    except Exception as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=6, column=6, data=res)
        allure.attach(
            page.screenshot(full_page=True),
            name="Login_Failure_Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        raise e
    
@allure.title("Test Login Screen with useremail and password should not be empty")
@allure.testcase("TC-006")
@allure.description("Test Login Screen with useremail and password should not be empty")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Login Form Test")
@allure.step("Verify and Load the Site URL")
def test_invalid_login_without_useremail_password(page, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (7, 3) 
    password_cell = (7, 4)
    expected_msg_cell = (7,5)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)
    expectedmsg_read_from_excel = read_data(excel_sheet, sheet_name, *expected_msg_cell)
    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)

    email_empty_value = str(email_read_from_excel or "").strip()
    password_empty_value = str(password_read_from_excel or "").strip()

    login_form = LoginClass(page)
    logger.info("Navigating to login page")
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load()
    with allure.step("Enter credentials and submit login form"):
        res = login_form.login_screen_validate(email_empty_value, password_empty_value)
    time.sleep(3)
    try:
        assert expectedmsg_read_from_excel in res, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{res}'"
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=7, column=6, data=res)
    except Exception as e:
        write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=7, column=6, data=res)
        allure.attach(
            page.screenshot(full_page=True),
            name="Login_Failure_Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        raise e