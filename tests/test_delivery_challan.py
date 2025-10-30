from pages.login_page import LoginClass
from pages.delivery_challan_page import DeliveryChallan
from utils.excel_utils import read_data, write_data
import pytest
import time
import allure
import logging
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@allure.description("To open a Delivery Challan Screen")
@allure.title("To open a Delivery Challan Screen and Test the All fields.")
@allure.testcase("TC-0001")
@allure.story("Open a Delivery Challan Screen")
@allure.severity(allure.severity_level.NORMAL)
def test_delivery_note_valid_data(page, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (2, 3) 
    password_cell = (2, 4)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)

    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    login_form = LoginClass(page)
    with allure.step("Verify and Load the Site URL"):
        login_form.login_page_load()
    with allure.step("Validate the Login Datas"):
        res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    with allure.step("Open a Delivery Challan Screen"):
        delivery_challan_page = DeliveryChallan(page)

    sheet_name = "Delivery Challan"

    excel_data = {
        "vendor_id" : (2,3),
        "job_work_type" : (2,4),
        "expected_devliver_date" : (2,5),
        "source_warehouse" : (2,6),
        "target_warehouse" : (2,7),
        "scrap_warehouse" : (2,8),
        "vehcile_no" : (2,9),
        "item_file_url" : (2,10),
        "expected_msg_cell" : (2,14)
    }

    data_from_excel = {}
    for key, cell_value in excel_data.items():
        data_from_excel[key] = read_data(excel_sheet_path, sheet_name, *cell_value)

    expectedmsg_read_from_excel = data_from_excel.get("expected_msg_cell")
    with allure.step("Get the data from the excel and send to the respective fields"):
        status = delivery_challan_page.open_dn_page(data_from_excel)

    print("Current URL:", status)
    logger.info(f"Response => {status}")
    # time.sleep(3)
    assert expectedmsg_read_from_excel in status, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{status}'"

    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=2, column=15, data=status)

@allure.description("To open a Delivery Challan Screen without Item Data System should be throw an error.")
@allure.title("To open a Delivery Challan Screen without Item Data")
@allure.testcase("TC-0002")
@allure.severity(allure.severity_level.CRITICAL)
def test_delivery_note_without_item(driver, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (2, 3) 
    password_cell = (2, 4)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)

    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    login_form = LoginClass(driver)
    login_form.login_page_load()
    res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    delivery_challan_page = DeliveryChallan(driver)

    sheet_name = "Delivery Challan"
    excel_data = {
        "vendor_id" : (3,3),
        "job_work_type" : (3,4),
        "expected_devliver_date" : (3,5),
        "source_warehouse" : (3,6),
        "target_warehouse" : (3,7),
        "scrap_warehouse" : (3,8),
        "vehcile_no" : (3,9),
        # "item_file_url" : (3,10),
        "expected_msg_cell" : (3,14)
    }

    data_from_excel = {}
    for key, cell_value in excel_data.items():
        data_from_excel[key] = read_data(excel_sheet_path, sheet_name, *cell_value)

    expectedmsg_read_from_excel = data_from_excel.get("expected_msg_cell")
    status = delivery_challan_page.open_dn_page(data_from_excel)
    time.sleep(2)
    logger.info(f"Expected Status => {expectedmsg_read_from_excel}")
    logger.info(f"Response => {status}")
    time.sleep(3)
    assert expectedmsg_read_from_excel in status, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{status}'"

    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=3, column=15, data=status)


@allure.description("To open a Delivery Challan Screen with Item Data and Raw Material Data Upload and Bill and Ship Address")
@allure.title("To open a Delivery Challan Screen with Item Data and Raw Material Data Upload and Bill and Ship Address")
@allure.testcase("TC-0003")
@allure.severity(allure.severity_level.NORMAL)
def test_delivery_note_item_data_raw_material(driver, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (2, 3) 
    password_cell = (2, 4)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)

    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    login_form = LoginClass(driver)
    login_form.login_page_load()
    res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    delivery_challan_page = DeliveryChallan(driver)

    sheet_name = "Delivery Challan"

    excel_data = {
        "vendor_id" : (4,3),
        "job_work_type" : (4,4),
        "expected_devliver_date" : (4,5),
        "source_warehouse" : (4,6),
        "target_warehouse" : (4,7),
        "scrap_warehouse" : (4,8),
        "vehcile_no" : (4,9),
        "item_file_url" : (4,10),
        "raw_material_sheet_url":(4,11),
        "shipping_address":(4,12),
        "billing_address":(4,13),
        "expected_msg_cell" : (4,14)
    }

    data_from_excel = {}
    for key, cell_value in excel_data.items():
        data_from_excel[key] = read_data(excel_sheet_path, sheet_name, *cell_value)

    expectedmsg_read_from_excel = data_from_excel.get("expected_msg_cell")
    status = delivery_challan_page.open_dn_page(data_from_excel)
    time.sleep(2)
    print("Current URL:", status)
    logger.info(f"Response => {status}")
    time.sleep(3)
    assert expectedmsg_read_from_excel in status, f"Expected message: '{expectedmsg_read_from_excel}', but got: '{status}'"

    write_data(file_path=excel_sheet_path, sheet_name=sheet_name, row=4, column=15, data=status)


@allure.description("To get the Delivery Challan IDs")
@allure.title("To get the Delivery Challan IDs")
@allure.testcase("TC-0004")
@allure.severity(allure.severity_level.NORMAL)
def test_random_select_and_submit(driver, excel_sheet):
    excel_sheet_path = excel_sheet
    print("Excel Sheet Path", excel_sheet_path)
    sheet_name = "Login"
    email_cell = (2, 3) 
    password_cell = (2, 4)
    email_read_from_excel = read_data(excel_sheet_path, sheet_name, *email_cell)
    password_read_from_excel = read_data(excel_sheet, sheet_name, *password_cell)

    print("Email Read","=", email_read_from_excel)
    print("Password Read","=", password_read_from_excel)
    login_form = LoginClass(driver)
    login_form.login_page_load()
    res = login_form.login_screen_validate(email_read_from_excel, password_read_from_excel)
    delivery_challan_page = DeliveryChallan(driver)

    sheet_name = "Delivery Challan ID"
    excel_data = {
        "delivery_challan_id_cell":(2,3),
        "expected_msg_cell":(2,4)
    }

    data_from_excel = {}
    for key, cell_value in excel_data.items():
        data_from_excel[key] = read_data(excel_sheet_path, sheet_name, *cell_value)

    expectedmsg_read_from_excel = data_from_excel.get("expected_msg_cell")

    delivery_challan_page.open_delivery_challan()
    result = delivery_challan_page.get_delivery_note_ids()
    submit_res = delivery_challan_page.delivery_challan_doc_submit(data_from_excel)
    for i in result:
        print("Delivery Challan ID", i)