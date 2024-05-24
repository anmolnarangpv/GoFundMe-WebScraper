from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import os
import sys
from attribute_scraper import attributes_scraper
import pandas as pd
from uszipcode import SearchEngine


# python scraper.py <link of the category>;python test.py memorial-fundraiser

import pickle

# # Specify the file name
# filename = 'category_campaign_list.pkl'

# # Open the file in read-binary mode and load the list
# with open(filename, 'rb') as file:
#     loaded_donor_list = pickle.load(file)

# # Now, loaded_text_list contains the list of text
# print("campaign links",loaded_donor_list)



def generate_pdfs(donors_list,project_link_url,metadata):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    print("starting generating pdf files!!!!!!!!!")
    # List of names
    # names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]
    proj_url=project_link_url.replace('/','_')
    proj_url=proj_url.replace(':','_')
    proj_url=proj_url.replace('.','_')
    # Create a PDF document
    pdf_filename = f"campaigns/"+str(proj_url)+".pdf"

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Create a list of paragraphs with styles
    story = []
    name_style = getSampleStyleSheet()["Normal"]
    name_style.textColor = colors.black
    name_style.spaceAfter=20
    name_style.alignment = 1

    for i in metadata:
        metadata_para=Paragraph(i,name_style)
        story.append(metadata_para)


    # Define a style for the title
    title_style = getSampleStyleSheet()["Normal"]
    title_style.spaceAfter = 30
    title = Paragraph(str(project_link_url), title_style)
    story.append(title)

    # Define a style for the names
      # Center alignment

    # Add names to the PDF
    for name in donors_list:
        name_paragraph = Paragraph(name, name_style)
        story.append(name_paragraph)

    # Build the PDF document
    doc.build(story)

    print(f"PDF generated: {pdf_filename}")

    return "PDF_GENERATED!!!!!!"



if len(sys.argv)>1:
    
    cat=sys.argv[1]
    print("category",cat)
    cat_file=[f for f in os.listdir() if cat in f]
    print("Cat_file",cat_file)

    
    filename = cat_file[0]

# Open the file in read-binary mode and load the list
    with open(filename, 'rb') as file:
        loaded_donor_list = pickle.load(file)
    

    # # Now, loaded_text_list contains the list of text
    # print("campaign links",loaded_donor_list)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    # loaded_donor_list=['https://www.gofundme.com/f/help-heal-the-rioux-ranch-tragedy-in-september']
    # print(loaded_donor_list)
    for i in loaded_donor_list:
        print(i)
            

        try:
                
            d_link=i.split('?')[0]
            l=d_link.replace('/','_')
            l=l.replace(':','_')
            l=l.replace('.','_')
            filename = f"campaigns/"+str(l)+".pdf"
            if os.path.exists(filename):
                print("FILE ALREADY EXISTS!!! SKIPPING FILE")
                continue
            base_url = d_link+'/donations'

            print("..........................................",base_url)

            metadata=attributes_scraper(d_link)

            print("metadataaaaaa",metadata)

            driver.get(base_url)

            # from selenium import webdriver
            import time

            # Setup WebDriver
            # driver = webdriver.Chrome()

            # Navigate to the Webpage
            # driver.get('http://yourwebpage.com')

            # Locate the Scrollable Div
            scrollable_div = driver.find_element(By.XPATH,"//div[@class='campaign-modal_content__S9Qxt']")
            print(scrollable_div)

            # Scroll within the Div
            len_of_div = 0
            match = False
            while(match == False):
                last_count = len_of_div
                # time.sleep(7)
                print(last_count)
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)

                time.sleep(7)  # wait for names to load
                len_of_div = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                print(len_of_div)
                if last_count == len_of_div:
                    match = True
            

            # driver.save_screenshot()
            donor_names=driver.find_elements(By.XPATH,"//div[@class='hrt-avatar-lockup-content']")

            print(len(donor_names))
            # donor_list=[]
            donor_list=[donor.text for donor in donor_names]
            df=[i.split('\n')[0:2] for i in donor_list]
            temp=[i for i in df if len(i)==2]
            print("tempppppp",temp)
            # print([goal,organizer,category,date_of_creation])
            temp=[i+metadata for i in temp]
            print("tempppppppppp",temp)
            temp_df=pd.DataFrame(temp,columns=['Donor Name','Contribution','Total Amount Raised','Category','Creation Date','Created By','City','State','Zip_Code'])
            temp_df.to_csv("csv/"+str(l)+".csv")


            
            # print(df)

            df1=[i[0]+' - '+i[1] for i in temp]
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",df1)
            # df1.to_csv('df1.csv')
            # for donor in donor_names:
            #     d=donor.text
            #     print("DONORS_NAME ",d)
            #     donor_list.append(d)

            generate_pdfs(df1,d_link,metadata)
        except Exception as error:
            print("An error occurred:", type(error).__name__, "–", error)

else:


    cat='fundraiser'
    print("category",cat)
    cat_file=[f for f in os.listdir() if cat in f]
    print("Cat_file",cat_file)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)

    for pkl in cat_file:

        filename = pkl

    # Open the file in read-binary mode and load the list
        with open(filename, 'rb') as file:
            loaded_donor_list = pickle.load(file)

        # Now, loaded_text_list contains the list of text
        print("campaign links",loaded_donor_list)

        

        for i in loaded_donor_list:
                

            try:
                    
                d_link=i.split('?')[0]
                l=d_link.replace('/','_')
                l=l.replace(':','_')
                l=l.replace('.','_')
                filename = f"campaigns/"+str(l)+".pdf"
                if os.path.exists(filename):
                    print("FILE ALREADY EXISTS!!! SKIPPING FILE")
                    continue
                base_url = d_link+'/donations'

                print(base_url)
                metadata=attributes_scraper(d_link)

                print("metadataaaaaa",metadata)

                driver.get(base_url)

                # from selenium import webdriver
                import time

                # Setup WebDriver
                # driver = webdriver.Chrome()

                # Navigate to the Webpage
                # driver.get('http://yourwebpage.com')

                # Locate the Scrollable Div
                scrollable_div = driver.find_element(By.XPATH,"//div[@class='campaign-modal_content__S9Qxt']")
                print(scrollable_div)

                # Scroll within the Div
                len_of_div = 0
                match = False
                while(match == False):
                    last_count = len_of_div
                    # time.sleep(7)
                    print(last_count)
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)

                    time.sleep(7)  # wait for names to load
                    len_of_div = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                    print(len_of_div)
                    if last_count == len_of_div:
                        match = True
                

                # driver.save_screenshot()
                donor_names=driver.find_elements(By.XPATH,"//div[@class='hrt-avatar-lockup-content']")

                print(len(donor_names))
                # donor_list=[]
                donor_list=[donor.text for donor in donor_names]
                df=[i.split('\n')[0:2] for i in donor_list]
                temp=[i for i in df if len(i)==2]
                # print("tempppppp",temp)
                # print(df)
                temp=[i+metadata for i in temp]

                print("tempppppppppp",temp)
                temp_df=pd.DataFrame(temp,columns=['Donor Name','Contribution','Total Amount Raised','Category','Creation Date','Created By','City','State','Zip_Code'])
                temp_df.to_csv("csv/"+str(l)+".csv")


                df1=[i[0]+' - '+i[1] for i in temp]
                print(df1)
                # for donor in donor_names:
                #     d=donor.text
                #     print("DONORS_NAME ",d)
                #     donor_list.append(d)

                generate_pdfs(df1,d_link,metadata)
            except:
                continue

# Extract Names from the Div
# names_elements = scrollable_div.find_elements_by_css_selector('.name-selector')
# names = [name.text for name in names_elements]

# Close the WebDriver
# driver.quit()

# Print the Extracted Names
# for name in names:
#     print(name)
