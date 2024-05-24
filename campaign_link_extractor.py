from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# for category in sys.argv:
print(sys.argv)
if len(sys.argv)>1:
    print("Extracting a particular category!!!")

# Set up the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    url = sys.argv[1]
    driver.get(url)
    cat=url.split('/')[-1]

    # Allow some time for the page to load initially
    time.sleep(5)

    try:
        count=1
        while True:
            print(count)
            # Find the "Show More" button and click it
            show_more_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='hrt-secondary-button hrt-secondary-button--inline hrt-secondary-button--large hrt-secondary-button--default hrt-base-button']"))
            )
            print("CLICKING SHOW MORE")
            show_more_button.click()
            count+=1
            
            
            # Allow some time for new content to load
            time.sleep(5)
    except Exception as e:
        print("Show more button not found or not clickable. Proceeding to extract links.")

    # Find all links on the page
    links = driver.find_elements(By.TAG_NAME, "a")

    # Extract href attribute to get the link and print it
    category_links=[]
    for link in links:
        href = link.get_attribute("href")
        print("CAMPAIGN LINK",href)
        if '/f/' in href:
            print("DONATION CAMPAIGN",href)
            category_links.append(href)



    import pickle

    # Suppose text_list is your list of text
    # text_list = ['text1', 'text2', 'text3']

    # Specify the file name
    filename = cat+'-campaign-list.pkl'

    # Open the file in write-binary mode and dump the list
    with open(filename, 'wb') as file:
        pickle.dump(category_links, file)


else:
    print("Extracting all categories!!!")


    categories=['https://www.gofundme.com/discover/medical-fundraiser','https://www.gofundme.com/discover/memorial-fundraiser','https://www.gofundme.com/discover/emergency-fundraiser','https://www.gofundme.com/discover/financial-emergency-fundraiser','https://www.gofundme.com/discover/animal-fundraiser',
# https://www.gofundme.com/discover/animal-fundraiser
'https://www.gofundme.com/discover/environment-fundraiser',
'https://www.gofundme.com/discover/business-fundraiser',
'https://www.gofundme.com/discover/community-fundraiser',
'https://www.gofundme.com/discover/competition-fundraiser',
'https://www.gofundme.com/discover/creative-fundraiser',
'https://www.gofundme.com/discover/event-fundraiser',
'https://www.gofundme.com/discover/faith-fundraiser',
'https://www.gofundme.com/discover/family-fundraiser',
'https://www.gofundme.com/discover/sports-fundraiser',
'https://www.gofundme.com/discover/travel-fundraiser',
'https://www.gofundme.com/discover/volunteer-fundraiser',
'https://www.gofundme.com/discover/wishes-fundraiser',
'https://www.gofundme.com/discover/other-fundraiser']

# Set up the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    # category_links=[]
    for url in categories:
        # url_cat = "https://www.gofundme.com/discover/charity-fundraiser"
        print("URL CATEGORY",url)
        cat=url.split('/')[-1]
        driver.get(url)

        # Allow some time for the page to load initially
        time.sleep(5)

        try:
            count=1
            while True:
                print(count)
                # Find the "Show More" button and click it
                show_more_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='hrt-secondary-button hrt-secondary-button--inline hrt-secondary-button--large hrt-secondary-button--default hrt-base-button']"))
                )
                print("CLICKING SHOW MORE")
                show_more_button.click()
                count+=1
                
                
                # Allow some time for new content to load
                time.sleep(5)
        except Exception as e:
            print("Show more button not found or not clickable. Proceeding to extract links.")

        # Find all links on the page
        links = driver.find_elements(By.TAG_NAME, "a")

        # Extract href attribute to get the link and print it
        category_links=[]
        for link in links:
            href = link.get_attribute("href")
            print("CAMPAIGN LINK",href)
            if '/f/' in href:
                print("DONATION CAMPAIGN",href)
                category_links.append(href)



        import pickle

        # Suppose text_list is your list of text
        # text_list = ['text1', 'text2', 'text3']

        # Specify the file name
        filename = str(cat)+'_category.pkl'

        # Open the file in write-binary mode and dump the list
        with open(filename, 'wb') as file:
            pickle.dump(category_links, file)





        # driver.get(href)
        # link=href.replace('.','_')
        # link=link.replace('/','_')

        # tmp_page_fname='campaigns/'+str(link)+'.html'
        # with open(tmp_page_fname, 'w') as fh:
            
        #     fh.write(driver.page_source)
        

    # see_all_button=WebDriverWait(driver,60).until(
    #     EC.element_to_be_clickable((By.XPATH,"//a[text()='See all']"))
    # )

    # see_all_button.click()


    # if href:
    #     print(href)

# Close the browser window
driver.quit()
