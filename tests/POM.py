from playwright.sync_api import Locator, Page


# Define the UI element classes
class UIElement:
    def __init__(self, page: Page, location: Locator = None):
        self.page = page
        self.location: Locator = location if location else page

# Page divisions
class SideBar(UIElement):
    def __init__(self, page: Page):
        super().__init__(page, location=page.locator("xpath=//*[@id='plannerSiderBar']"))

class MainBody(UIElement):
    def __init__(self, page: Page):
        super().__init__(page, location = page.locator("xpath=//main/*[starts-with(local-name(), 'app-')]"))

class Dialog(UIElement):
    def __init__(self, page: Page):
        super().__init__(page, location=page.locator("ejs-dialog"))

class Header(UIElement):
    def __init__(self, page: Page):
        super().__init__(page, location=page.locator("xpath=//*[@id='planner-header']"))

class List(UIElement):
    def __init__(self, page: Page, list_name: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.list_name = list_name
        self.list = self.location.get_by_role("ejs-listview", name=list_name)#fix 


# Specific interactive elements
class Button(UIElement):
    def __init__(self, page: Page, button_text: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.name = button_text
        self.button = self.location.get_by_role("button", name=button_text)
    
class SideBarElement(UIElement):
    def __init__(self, page: Page, element_text: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.element_text = element_text
        self.sidebar_element = self.location.get_by_text(element_text)

class SearchBar(UIElement):
    def __init__(self, page: Page, placeholder_text: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.placeholder_text = placeholder_text
        self.search_bar = self.location.get_by_placeholder(placeholder_text)
        self.search_button = self.location.locator("xpath=//*[@id='schedule_searchbutton']")
        self.clear_button = self.location.locator("xpath=//*[@id='searchTemplate']/div/span[1]") #temp, copied from devtools 
    
class DropDown(UIElement):
    def __init__(self, page: Page, name: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.dropdown_name = name
        self.dropdown = self.location.locator(f".e-ddl:has(label:text('{name}'))")

    @property
    def options(self):
        return self.page.get_by_role("option")
    
    def select_option(self, option_text: str, exact: bool = False):
        self.dropdown.click()
        self.page.wait_for_timeout(300) #small wait to render options
        self.page.get_by_role("option", name=option_text, exact=exact).click()

class InputField(UIElement):
    def __init__(self, page: Page, name: str, parent: UIElement = None):
        super().__init__(page, location=parent.location if parent else page)
        self.name = name
        self.input_field = self.location.get_by_role("textbox", name=name)

