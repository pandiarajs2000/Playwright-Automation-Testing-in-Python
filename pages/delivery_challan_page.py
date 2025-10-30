from datetime import datetime
from playwright.sync_api import Page, expect
import traceback
import time
import openpyxl
import pdb
import logging
import os
import sys

# logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeliveryChallan:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_box_xpath = "//input[@id='navbar-search']"
        self.add_delivery_challan = "//button[@data-label='Add Delivery Challan']"

        self.vendor_xpath = "//div[@data-fieldname='vendor']//input[@role='combobox']"
        self.job_work_type = "//div[@data-fieldname='job_work_type']//select[@type='text']"
        self.expected_delivery_date = "//input[@data-fieldname='expected_delivery_date']"
        self.source_warehouse_xpath = "//div[@data-fieldname='source_warehouse']//input[@role='combobox']"
        self.target_warehouse_xpath = "//div[@data-fieldname='target_warehouse']//input[@role='combobox']"
        self.scrap_warehouse_xpath = "//div[@data-fieldname='scrap_warehouse']//input[@role='combobox']"
        self.dn_more_info_tab = "//a[@id='delivery-challan-tab_other_info-tab']"
        self.vehicle_no_xpath = "//div[@data-fieldname='vehicle_no']//input[@type='text']"
        self.dn_save_btn_xpath = "//div[@id='page-Delivery Challan']//button[@data-label='Save']"
        self.status_draft = "//span[@class='indicator-pill no-indicator-dot whitespace-nowrap red']//span[contains(text(),'Draft')]"
        self.empty_for_item_table = "//div[@data-fieldname='items']//div[@class='grid-body']"
        self.item_upload_xpath = "//div[@data-fieldname='items']//button[@type='button'][normalize-space()='Upload']"
        self.click_to_device = "//div[@class='file-upload-area']/descendant::button[@class='btn btn-file-upload'][1]"
        self.final_upload_sheet_item_table = "//button[@class='btn btn-primary btn-sm btn-modal-primary'][normalize-space()='Upload']"
        self.file_upload_msg = "//div[@class='modal-dialog msgprint-dialog']//div[@class='modal-body ui-front']"
        self.popup_msg_close = "(//button[contains(@class,'btn btn-modal-close btn-link')])[1]"
        self.line_item_rows = "//div[@data-fieldname='items']//div[@class='rows']"
        self.document_submit_xpath = "//button[@data-label='Submit']"
        self.submit_confirm_xpath = "//div[@role='dialog']//button[@type='button'][normalize-space()='Yes']"
        self.submission_error_popup_xpath = "//div[@class='modal-dialog msgprint-dialog']//div[@class='modal-body ui-front']"

        self.shipping_address_xpath = "//div[@data-fieldname='shipping_address']//input[@role='combobox']"
        self.billing_address_xpath = "//div[@data-fieldname='billing_address']//input[@role='combobox']"
        self.address_tab = "//a[@id='delivery-challan-tab_addresses-tab']"
        self.raw_materail_upload_xpath = "//div[@data-fieldname='raw_materials']//button[@type='button'][normalize-space()='Upload']"

        self.item_without_save_popup_xpath = "//div[@class='modal-body ui-front']/descendant::div[@class='msgprint']"
        
        self.get_delivery_not_ids_xpath = "//div[@class='list-row-container']/descendant::span[contains(@class,'ellipsis') and starts-with(@title, 'ID')]//a"
        self.id_filter_xpath = "//input[@placeholder='ID']"
    
    def open_delivery_challan(self):
        logger.info("Search Box Open..")
        search_input = self.page.locator(self.search_box_xpath)
        expect(search_input).to_be_visible(timeout=10000)
        search_input.fill('Delivery Challan List')
        logger.info("Search Box Input Send")
        time.sleep(1)
        search_input.press("Enter")
        self.page.wait_for_load_state("networkidle")
        

    def open_dn_page(self,data=None):
        vendor_id = data.get("vendor_id")
        job_work_type = data.get("job_work_type")
        expected_devliver_date = data.get("expected_deliver_date")
        source_warehouse = data.get("source_warehouse")
        target_warehouse = data.get("target_warehouse")
        scrap_warehouse = data.get("scrap_warehouse")
        vehcile_no = data.get("vehicle_no")
        item_file_url = data.get("item_file_url")
        raw_materail_file_url = data.get("raw_material_sheet_url")
        shipping_address = data.get('shipping_address')
        billing_address = data.get('billing_address')


        print("Item File URL",item_file_url)
        print("vehcile_no",vehcile_no)

        # logger.info("Search Box Open..")
        # search_input = WebpageWait(self.page, 10).until(EC.presence_of_element_located(self.search_box_xpath))
        # search_input.send_keys('Delivery Challan List')
        # logger.info("Search Box Input Send")
        # time.sleep(1)
        # search_input.send_keys(Keys.ENTER)
        # self.page.implicitly_wait(3)
        # add_mr = WebpageWait(self.page, 10).until(EC.element_to_be_clickable(self.add_delivery_challan))
        # logger.info("Add Button Click")
        # add_mr.click()
        # logger.info("Open a Material Request Screen.")
    
        # self.page.refresh()
        self.open_delivery_challan()
        # self.page.implicitly_wait(3)
        add_mr = self.page.locator(self.add_delivery_challan)
        logger.info("Add Button Click")
        add_mr.click()
        logger.info("Open a Material Request Screen.")
    
        self.page.reload()
        result = self.get_dn_field_xpaths(
            vendor_id, job_work_type,expected_devliver_date,source_warehouse,target_warehouse,scrap_warehouse,vehcile_no,item_file_url,
            raw_materail_file_url, shipping_address, billing_address
            )
        if result == "Draft":
            logger.info("Delivery Challan Added..")
            return "Delivery Challan Added"
        elif result == "Submitted":
            logger.info("Delivery Challan Added..")
            return "Delivery Challan Added"
        # elif submission_error:
        #     logger.error(f"Error on Delivery Challan Submission: {submission_error}")
        #     print
        else:
            logger.error("Error on Delivery Challan")
            return result
    
    def get_dn_field_xpaths(
            self,vendor_id, job_work_type_value,expected_devliver_date,source_warehouse,target_warehouse,scrap_warehouse,vehcile_no,item_file_url,
            raw_materail_file_url, shipping_address, billing_address
            ):
        try:
            print("Vendor ID",vendor_id)
            # self.page.implicitly_wait(5)
            vendor_input = self.page.locator(self.vendor_xpath)
            vendor_input.clear()
            vendor_input.fill(vendor_id)
            vendor_input.press("Enter")

            job_work_type_input = self.page.locator(self.job_work_type)
            job_work_type_input.select_option(value=job_work_type_value)

            expected_date_input = self.page.locator(self.expected_delivery_date)
            expected_date_input.click()
            expected_date_input.clear()

            if isinstance(expected_devliver_date, datetime):
                date_val = expected_devliver_date.strftime("%d-%m-%Y")
            else:
                date_val = expected_devliver_date or datetime.now().strftime("%d-%m-%Y")

            expected_date_input.fill(date_val)
            # time.sleep(1)

            source_warehouse_input = self.page.locator(self.source_warehouse_xpath)
            source_warehouse_input.clear()
            source_warehouse_input.fill(source_warehouse)
            
            target_warehouse_input = self.page.locator(self.target_warehouse_xpath)
            target_warehouse_input.clear()
            target_warehouse_input.fill(target_warehouse)
            
            scrap_warehouse_input = self.page.locator(self.scrap_warehouse_xpath)
            scrap_warehouse_input.clear()
            scrap_warehouse_input.fill(scrap_warehouse)
            print("Item File URL",item_file_url)
            if item_file_url :
                print("Item File URL",item_file_url)
                try:
                    upload_btn_click = self.page.locator(self.item_upload_xpath)
                    upload_btn_click.click()
                    # time.sleep(3)
                
                    file_input = self.page.locator("input[type='file']")
                    file_path = os.path.abspath(f"{item_file_url}")
                    print("file_path", file_path)
                    file_input.set_input_files(file_path)

                    confirm_btn = self.page.locator(self.final_upload_sheet_item_table)
                    confirm_btn.click()

                    upload_msg = self.page.locator(self.file_upload_msg)
                    message = upload_msg.inner_text()
                    print("Meesgae", message)
                    
                    close_popup = self.page.locator(self.popup_msg_close)
                    close_popup.click()
                    print("Popup Closed")
                    self.page.mouse.wheel(10,50)

                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"D:\\Playwright\\reports\\screenshots\\delivery_challan{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)

                    if raw_materail_file_url:
                        print("Raw Material File URL:", raw_materail_file_url)
                        raw_upload_btn = self.page.locator(self.raw_materail_upload_xpath)
                        raw_upload_btn.click()

                        raw_file_input = self.page.locator("input[type='file']")
                        raw_file_path = os.path.abspath(raw_materail_file_url)
                        raw_file_input.set_input_files(raw_file_path)

                        raw_confirm_btn = self.page.locator(self.final_upload_sheet_item_table)
                        raw_confirm_btn.click()

                        raw_upload_msg = self.page.locator(self.file_upload_msg)
                        print("Raw Material Upload Message:", raw_upload_msg.inner_text())

                        raw_close_popup = self.page.locator(self.popup_msg_close)
                        raw_close_popup.click()
                        print("Raw Material Upload Popup Closed")

                    # ===== CONTINUE WITH OTHER FIELDS =====
                    self.page.mouse.wheel(10,50)
                    # time.sleep(1)
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"D:\\Playwright\\reports\\screenshots\\screenshot_after_upload_{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)
                    self.page.mouse.wheel(0,-50)

                    if shipping_address or billing_address:
                        # address tab
                        address_tab_section = self.page.locator(self.address_tab)
                        address_tab_section.click()
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        screenshot_path = f"D:\\Playwright\\reports\\screenshots\\delivery_challan_address_tab{timestamp}.png"
                        self.page.screenshot(path=screenshot_path)

                        shipping_address_input = self.page.locator(self.shipping_address_xpath)
                        shipping_address_input.clear()
                        shipping_address_input.fill(shipping_address)
                        # time.sleep(1)
                        shipping_address_input.press("Enter")

                        billing_address_input = self.page.locator(self.billing_address_xpath)
                        billing_address_input.clear()
                        billing_address_input.fill(billing_address)
                        # time.sleep(1)
                        billing_address_input.press("Enter")

                    else:
                        logger.info("Shipping Address or Billing Address is not found in the test data sheet")
                    
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"D:\\Playwright\\reports\\screenshots\\delivery_challan{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)

                    more_info_tab = self.page.locator(self.dn_more_info_tab)
                    more_info_tab.click()
                    # time.sleep(1)
                    if vehcile_no:
                        vehcile_no_input = self.page.locator(self.vehicle_no_xpath)
                        print("Vehcile No", str(vehcile_no))
                        vehcile_no_input.fill(vehcile_no)
                    else:
                        vehcile_no_input = self.page.locator(self.vehicle_no_xpath)
                        print("Vehcile No", str(vehcile_no))
                        vehcile_no_input.fill("TN09AZ5647")

                    self.page.mouse.wheel(0,-50)             
                    save_click = self.page.locator(self.dn_save_btn_xpath)
                    save_click.scroll_into_view_if_needed()
                    save_click.wait_for(state="visible")
                    save_click.dblclick(force=True)

                    self.page.wait_for_load_state("networkidle")

                    draft_status = self.page.locator(self.status_draft)
                    draft_status.wait_for(state="visible", timeout=30000)

                    draft_text = draft_status.inner_text()
                    print("Draft Status Text:", draft_text)

                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"D:\\Playwright\\reports\\screenshots\\delivery_challan_submit_popup{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)
                    return draft_text
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(f"\n Exception Type: {exc_type.__name__}")
                    print(f"File: {fname}")
                    print(f"Line: {exc_tb.tb_lineno}")
                    print(f"Message: {str(e)}")
                    traceback.print_exc()
            else:
                item_tabel_empty = self.page.locator(self.empty_for_item_table)
                if len(item_tabel_empty) > 0:
                    # take a screenshot
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"D:\\Playwright\\reports\\screenshots\\delivery_challan{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)
                    self.page.mouse.wheel(0,-50)
                    more_info_tab = self.page.locator(self.dn_more_info_tab)
                    more_info_tab.click()
                    if vehcile_no:
                        vehcile_no_input = self.page.locator(self.vehicle_no_xpath)
                        print("Vehcile No", str(vehcile_no))
                        vehcile_no_input.fill(vehcile_no)
                    else:
                        vehcile_no_input = self.page.locator(self.vehicle_no_xpath)
                        print("Vehcile No", str(vehcile_no))
                        vehcile_no_input.fill("TN09AZ5647")

                    self.page.mouse.wheel(0,-50)                    
                    save_click = self.page.locator(self.dn_save_btn_xpath)
                    save_click.click()

                    mandatory_popup_text = self.page.locator(self.item_without_save_popup_xpath)
                    defect_messgae = mandatory_popup_text.inner_text()
                    print("Bug", defect_messgae)
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"D:\\Playwright\\reports\\screenshots\\delivery_challan{timestamp}.png"
                    self.page.screenshot(path=screenshot_path)
                    return defect_messgae
                else:
                    logger.info("Item Table was filled..")
                    traceback.print_exc()
                time.sleep(2)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"\n Exception Type: {exc_type.__name__}")
            print(f"File: {fname}")
            print(f"Line: {exc_tb.tb_lineno}")
            print(f"Message: {str(e)}")
            traceback.print_exc()


    def get_delivery_note_ids(self):
        # self.page.implicitly_wait(2)
        dn_id_list = []

        # list_view_xpath = WebpageWait(self.page, 10).until(EC.presence_of_element_located(self.get_delivery_not_ids_xpath))
        list_view_xpath = self.page.locator(self.get_delivery_not_ids_xpath)
        for id in list_view_xpath:
            print(id.inner_text())
            dn_id_list.append(id.inner_text())
        
        return dn_id_list
    
    def delivery_challan_doc_submit(self, data):
        dn_id = data.get('delivery_challan_id_cell')
        # delivery_challan_id = dn_id.strip()
        # self.page.implicitly_wait(2)
        id_filter_input = self.page.locator(self.id_filter_xpath)
        id_filter_input.clear()
        id_filter_input.fill(dn_id)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"D:\\Playwright\\reports\\screenshots\\delivery_challan_list_id_filter{timestamp}.png"
        self.page.screenshot(path=screenshot_path)