#imports
import re

import pytest
from playwright.sync_api import Page, expect
from POM import *


# Fixtures
@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    # Navigate to the appointment planner page
    page.goto("https://ej2.syncfusion.com/showcase/angular/appointmentplanner/")
    yield

@pytest.fixture
def ui_elements(page: Page):
    return {
        #sidebar 
        "sidebar_doctors": SideBarElement(page, "Doctors", parent=SideBar(page)),
        "sidebar_schedule": SideBarElement(page, "Schedule", parent=SideBar(page)),
        #buttons
        "add_doctor_button": Button(page, "Add New Doctor", parent=MainBody(page)),
        "save_button": Button(page, "Save", parent=Dialog(page)),
        "edit_button": Button(page, "Edit"),
        "delete_button": Button(page, "Delete"),
        #inputs
        "name_input": InputField(page, "Name"),
        "phone_input": InputField(page, "Mobile Number"),
        "email_input": InputField(page, "Email"),
        "education_input": InputField(page, "Education"),
        "designation_input": InputField(page, "Designation"),
        "department_dropdown": DropDown(page, "Department"),
        "experience_dropdown": DropDown(page, "Experience"),
        "duty_dropdown": DropDown(page, "Duty Timing"),        
    }
    
#Util
format_phone = lambda p: f"({p[:3]}) {p[4:7]}-{p[8:]}"

# Test data
test_doctor_data = {
    "name": "Pepper",
    "phone": "123-456-7890",
    "email": "example_email@gmail.com",
    "department": "Cardiology",
    "experience": "5+ years",
    "duty": "12:00 AM - 09:00 PM",
    "designation": "Cardiologist",
    "education": "MD"
}
# Test cases

def test_add_doctor(page: Page, ui_elements: dict):    
    #navigate to doctors page and click add doctor button
    ui_elements["sidebar_doctors"].sidebar_element.click()
    ui_elements["add_doctor_button"].button.click()
    # New doctor popup should be visible
    expect(page.locator("ejs-dialog")).to_be_visible() 
    #Fill in details
    ui_elements["name_input"].input_field.fill(test_doctor_data["name"])
    ui_elements["phone_input"].input_field.fill(test_doctor_data["phone"])
    page.locator("//*[@id='new-doctor-form']/div[2]/div[1]/div[2]/label[2]").click() #temp, select female gender
    ui_elements["email_input"].input_field.fill(test_doctor_data["email"])
    ui_elements["education_input"].input_field.fill(test_doctor_data["education"])
    ui_elements["designation_input"].input_field.fill(test_doctor_data["designation"])
    ui_elements["department_dropdown"].select_option(test_doctor_data["department"])
    ui_elements["experience_dropdown"].select_option(test_doctor_data["experience"], exact=True)
    ui_elements["duty_dropdown"].select_option(test_doctor_data["duty"])
    #save
    ui_elements["save_button"].button.click()
    #verify that the new doctor is added to the list
    expect(page.locator(f'xpath=//div[@class="specialist-detail"]/div[@class="name" and text()="Dr. {test_doctor_data["name"]}"]')).to_be_visible()
    #verify doctor profile details
    page.locator(f'xpath=//div[@class="specialist-detail"]/div[@class="name" and text()="Dr. {test_doctor_data["name"]}"]').click()
    expect(page.get_by_text("DOCTOR DETAILS", exact=True)).to_be_visible()
    details_locator = page.locator("app-doctor-details")
    expect(details_locator).to_contain_text(f"Dr. {test_doctor_data["name"]}")
    expect(details_locator).to_contain_text(format_phone(test_doctor_data["phone"]))
    # expect(details_locator).to_contain_text(test_doctor_data["email"])
    expect(details_locator).to_contain_text(test_doctor_data["department"])
    expect(details_locator).to_contain_text(test_doctor_data["experience"])
    expect(details_locator).to_contain_text(test_doctor_data["designation"])
    expect(details_locator).to_contain_text(test_doctor_data["education"])

def test_delete_appointment(page: Page, ui_elements: dict):
    ui_elements["sidebar_schedule"].sidebar_element.click()
    expect(page.locator("app-calendar")).to_be_visible()
    patient_app = re.compile(r"Laura.*Tuesday", re.IGNORECASE) # name and day match
    patient_appointment = Button(page, patient_app)
    expect(patient_appointment.button).to_be_visible()
    patient_appointment.button.click()
    page.wait_for_timeout(500) #wait for dialog to open
    ui_elements["edit_button"].button.click()
    page.wait_for_timeout(500) #wait for dialog to open
    ui_elements["delete_button"].button.click()
    page.wait_for_timeout(500) #wait for dialog to open
    ui_elements["delete_button"].button.click()
    expect(patient_appointment.button).not_to_be_visible()

