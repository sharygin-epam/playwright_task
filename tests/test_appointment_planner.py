#imports
import pytest
from playwright.sync_api import Page, expect
from POM import *


# Fixtures
@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    # Navigate to the appointment planner page
    page.goto("https://ej2.syncfusion.com/showcase/angular/appointmentplanner/")
    yield

#Util
format_phone = lambda p: f"({p[:3]}) {p[4:7]}-{p[8:]}"
# Test cases

def test_add_doctor(page: Page):
    #UI Elements
    #buttons
    sidebar_doctors = SideBarElement(page, "Doctors", parent=SideBar(page))
    add_doctor_button = Button(page, "Add New Doctor", parent=MainBody(page))
    save_button = Button(page, "Save", parent=Dialog(page))
    #inputs
    name_input = InputField(page, "Name")
    phone_input = InputField(page, "Mobile Number")
    email_input = InputField(page, "Email")
    education_input = InputField(page, "Education")
    designation_input = InputField(page, "Designation")
    #dropdowns
    department_dropdown = DropDown(page, "Department")
    experience_dropdown = DropDown(page, "Experience")
    duty_dropdown = DropDown(page, "Duty Timing")

    #test data
    test_doctor_name = "Pepper"
    test_doctor_phone = "123-456-7890"
    test_doctor_email = "example_email@gmail.com"
    test_doctor_department = "Cardiology"
    test_doctor_experience = "5+ years"
    test_doctor_duty = "12:00 AM - 09:00 PM"
    test_doctor_designation = "Cardiologist"
    test_doctor_education = "MD"
    #navigate to doctors page and click add doctor button
    sidebar_doctors.sidebar_element.click()
    add_doctor_button.button.click()
    # New doctor popup should be visible
    expect(page.locator("ejs-dialog")).to_be_visible() 
    #Fill in details
    name_input.input_field.fill(test_doctor_name)
    phone_input.input_field.fill(test_doctor_phone)
    page.locator("//*[@id='new-doctor-form']/div[2]/div[1]/div[2]/label[2]").click() #select female gender
    email_input.input_field.fill(test_doctor_email)
    education_input.input_field.fill(test_doctor_education)
    designation_input.input_field.fill(test_doctor_designation)
    department_dropdown.select_option(test_doctor_department)
    experience_dropdown.select_option(test_doctor_experience, exact=True)
    duty_dropdown.select_option(test_doctor_duty)
    #save
    save_button.button.click()
    #verify that the new doctor is added to the list
    expect(page.locator(f'xpath=//div[@class="specialist-detail"]/div[@class="name" and text()="Dr. {test_doctor_name}"]')).to_be_visible()
    #verify doctor profile details
    page.locator(f'xpath=//div[@class="specialist-detail"]/div[@class="name" and text()="Dr. {test_doctor_name}"]').click()
    expect(page.get_by_text("DOCTOR DETAILS", exact=True)).to_be_visible()
    details_locator = page.locator("app-doctor-details")
    expect(details_locator).to_contain_text(f"Dr. {test_doctor_name}")
    expect(details_locator).to_contain_text(format_phone(test_doctor_phone))
    # expect(details_locator).to_contain_text(test_doctor_email)
    expect(details_locator).to_contain_text(test_doctor_department)
    expect(details_locator).to_contain_text(test_doctor_experience)
    expect(details_locator).to_contain_text(test_doctor_designation)
    expect(details_locator).to_contain_text(test_doctor_education)

    
