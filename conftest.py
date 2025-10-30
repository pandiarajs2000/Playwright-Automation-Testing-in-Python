import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser


@pytest.fixture
def page(browser):
    context = browser.new_context()
    print("Context", context)
    page = context.new_page()
    page.set_default_timeout(30000)  # 30s timeout for stability
    yield page
    context.close()


@pytest.fixture
def excel_sheet():
    excel_path = "D:\\Playwright\\test_data_sheet.xlsx"
    return excel_path
