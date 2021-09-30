
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_my_pets(test):
    # add email
    test.find_element_by_id('email').send_keys('su')
    # add password
    test.find_element_by_id('pass').send_keys('123')
    # click submit button
    test.find_element_by_css_selector('button[type="submit"]').click()

    WebDriverWait(test, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"),
                                                                     'PetFriends'))  

    
    WebDriverWait(test, 10).until(EC.element_to_be_clickable((By.XPATH, '//li/a[@href="/my_pets"]')))
    test.find_element_by_xpath('//li/a[@href="/my_pets"]').click()
    
    assert test.title == "PetFriends: My Pets"  
    

    
    WebDriverWait(test, 10).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "table.table-hover tbody > tr")))  
    pet_number = len(test.find_elements_by_css_selector("table.table-hover tbody > tr"))
    images = test.find_elements_by_css_selector("tbody tr th img")
    names = test.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[1]")
    breeds = test.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[2]")
    ages = test.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[3]")

    images_counter = 0
    names_set = set()
    pets_list = set()
    for i in range(pet_number):

        names_set.add(names[i].text)
        pet = (names[i].text, breeds[i].text, ages[i].text)
        pets_list.add(pet)

        if images[i].get_attribute('src') != '':
            images_counter += 1
        expect(images[i].get_attribute('src') != '', 'Pet has no picture')
        expect(names[i].text != '', 'Empty name field')
        expect(breeds[i].text != '', 'Empty name field')
        expect(ages[i].text != '', 'Empty age field')

   
    pet_number_stat = test.find_elements_by_xpath("/html/body/div[1]//div[@class='.col-sm-4 left']")
    expect((int(pet_number_stat[0].text.split("\n")[1].split(" ")[1])) == pet_number, 'Not all pets are displayed on '
                                                                                      'the page')

  
    expect(images_counter >= pet_number / 2, 'Less then a half of pets has photo number')

    
    expect(len(names) == len(names_set), 'Match of pet names')

    
    expect(pet_number == len(pets_list), 'Not all of pets has different set of name, breed and age')

    assert_expectations()
