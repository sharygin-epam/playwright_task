#Common imports
import re

import pytest
from playwright.sync_api import Locator, Page, expect


# Fixtures
@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    # Navigate to the appointment planner page
    page.goto("https://ej2.syncfusion.com/showcase/angular/appointmentplanner/#/calendar")
    # Check page title 
    expect(page).to_have_title(re.compile("Appointment Planner"))
    yield

# Define the UI element classes
class UIElement:
    def __init__(self, page: Page, location: Locator = None):
        self.page = page
        self.location: Locator = location if location else page

class SideBar(UIElement):
    def __init__(self, page: Page):
        super().__init__(page, location=page.locator("xpath=//*[@id='plannerSiderBar']"))

class MainBody(UIElement):
    def __init__(self, page: Page):
        super().__init__(page, location = page.locator("xpath=//*[@id='app-*']"))

class Header(UIElement):
    def __init__(self, page: Page):
        super().__init__(page, location=page.locator("xpath=//*[@id='planner-header']"))

class Button(UIElement):
    def __init__(self, page: Page, button_text: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.name = button_text
        self.button = self.location.get_by_role("button", name=button_text)
        
class InputField(UIElement): 
    def __init__(self, page: Page, placeholder_text: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.placeholder_text = placeholder_text
        self.input_field = self.location.get_by_placeholder(placeholder_text)
    
class SideBarElement(UIElement):
    def __init__(self, page: Page, element_text: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.element_text = element_text
        self.sidebar_element = self.location.get_by_text(element_text)


# Test cases


