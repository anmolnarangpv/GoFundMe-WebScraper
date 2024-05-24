from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from uszipcode import SearchEngine

def zipcode(city,state):
    print(city,state)
    eng = SearchEngine()
    zipcodes = eng.by_city_and_state(city=city, state=state)
    # zipcode=zipcodes[0].zipcode
    print(zipcodes[0].zipcode)
    return zipcodes[0].zipcode

# if len(sys.argv)>1:
def attributes_scraper(d_link):
        
    # category='animal-fundraiser'
    
    # print("category",cat)
    
    # Now, loaded_text_list contains the list of text
    # print("campaign links",loaded_donor_list)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)

    

    print("..........................................",d_link)
    driver.get(d_link)

    goal=driver.find_element(By.XPATH,"//div[@class='progress-meter_progressMeterHeading__A6Slt']").text
    print("goal and funds raised - ",goal)

    organizer=driver.find_element(By.XPATH,"//div[@class='campaign-members-main_organizer__NRaa5']").text
    print('organizer name and location - ',organizer)

    location_and_name=organizer.replace('\nOrganizer\n','!').split('!')
    
    print("location and name of the organizer",location_and_name)
    name=location_and_name[0]
    print(name)
    location=location_and_name[1].split(',')
    print("location",location)
    city=location[0]
    print(city)
    state=location[1].strip()
    print(state)

    category=driver.find_element(By.XPATH,"//a[@class='hrt-disp-flex hrt-align-center hrt-link hrt-link--gray-dark']").text
    print('category',category)

    date_of_creation=driver.find_element(By.XPATH,"//span[@class='m-campaign-byline-created a-created-date']").text
    print('date of creation',date_of_creation)

    zip_code=zipcode(city=city,state=state)
    print("zip_code",zip_code)

    final_attribute_list=[goal,category,date_of_creation,name,city,state,zip_code]

    # driver.close()

    return final_attribute_list


# attributes_scraper()

# zipcode("Jefferson","SD")