from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd



# Creating a webdriver instance
driver = webdriver.Chrome()

# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

time.sleep(5)

#entering username
username = driver.find_element(By.ID, "username")
# Enter Your Email Address
user_name=input("User Name")
username.send_keys(user_name)

# entering password
pword = driver.find_element(By.ID, "password")
# Enter Your Password
password=input("Password")
pword.send_keys(password)

time.sleep(2)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
# In case of an error, try changing the
# XPath used here.

def get_linkedin_profile(first_name, last_name):
    """Opens LinkedIn search results for the given name in a web browser."""
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={first_name}+{last_name}"
    driver.get(search_url)
    time.sleep(10)  # Adjust wait time as needed
    src = driver.page_source

    # Now using beautiful soup
    soup = BeautifulSoup(src, 'lxml')
    divs = soup.find_all("div", {"class": "t-roman t-sans"})
    # initializing variables
    log = []
    lst = []
    count = 0
    data = []

    for i in divs:
        count += 1
        if (i.find("a").find_all("span")[1].text.lower() == f"{first_name} {last_name}"):
            lst.append(i.find("a").get("href"))
        if count >= 10:
            break
    for i in lst:

        try:
            driver.get(i)
            time.sleep(8)  # Adjust wait time as needed
            profile_src = driver.page_source
            soup = BeautifulSoup(profile_src, 'lxml')
        except Exception as e:
            log.append(f'in {i} at soup error: {e} ')


        try:
            name = soup.find("h1").text
        except Exception as e:
            name=''
            log.append(f'in {i} at name error: {e} ')


        try:
            bg_img = soup.find("img", {"id": "profile-background-image-target-image"}).get('src')
        except Exception as e:
            bg_img=''
            log.append(f'in {i} at bg_img error: {e} ')


        try:
            prf_img = soup.find("div", {"class": 'ph5'}).find('img').get('src')
        except Exception as e:
            prf_img=''
            log.append(f'in {i} at prf_img error: {e} ')


        try:
            headline = soup.find("div", {"class": "text-body-medium break-words"}).text.lstrip().rstrip().strip()
        except Exception as e:
            headline=''
            log.append(f'in {i} at headline error: {e} ')


        try:
            current_comapany_school = soup.find('ul', {'class': 'pv-text-details__right-panel'}).text.strip()
            current_comapany_school = current_comapany_school.replace("\n", "")
        except Exception as e:
            current_comapany_school=''
            log.append(f'in {i} at current_company error: {e} ')


        try:
            location = soup.find("span", {
                "class": "text-body-small inline t-black--light break-words"}).text.lstrip().rstrip().strip()
        except Exception as e:
            location=''
            log.append(f'in {i} at location error: {e} ')


        try:
            status = soup.find('h3').text.strip() if soup.find('h3').text else "null"
        except Exception as e:
            status=''
            log.append(f'in {i} at status error: {e} ')


        try:
            about = soup.find('div', {'class': 'display-flex ph5 pv3'}).text.lstrip().rstrip()
        except Exception as e:
            about=''
            log.append(f'in {i} at about error: {e} ')


        experience = ''
        education = ''
        skills = ''
        volunteer = ''
        honors_and_awards = ''

        for h2 in soup.find_all('h2'):
            try:
                if 'Experience' in h2.text:
                    for span in h2.find_next('ul').find_all('span', {'class': ''}):
                        if span.find(class_='visually-hidden'):
                            continue
                        if span.text.strip().lstrip().rstrip() not in experience:
                            experience = experience + " ".join(span.text.split()) + " \n "
                    experience = experience
                    a = 1 / 0
            except Exception as e:
                log.append(f'in {i} at experience error: {e} ')
                continue

            try:
                if 'Education' in h2.text:
                    for span in h2.find_next('ul').find_all('span', {'class': ''}):
                        if span.find_all(class_='visually-hidden'):
                            continue
                        if span.text.strip().lstrip().rstrip() not in education:
                            education = education + " ".join(span.text.split()) + " \n "
                    education = education
            except Exception as e:
                log.append(f'in {i} at education error: {e} ')
                continue

            try:
                if 'Volunteering' in h2.text:
                    for span in h2.find_next('ul').find_all('span', {'class': ''}):
                        if span.find_all(class_='visually-hidden'):
                            continue
                        if span.text.strip().lstrip().rstrip() not in volunteer:
                            volunteer = volunteer + " ".join(span.text.split()) + " \n "
                    volunteer = volunteer
            except Exception as e:
                log.append(f'in {i} at volunteering error: {e} ')
                continue

            try:
                if 'Honors & awards' in h2.text:
                    for span in h2.find_next('ul').find_all('span', {'class': ''}):
                        if span.find_all(class_='visually-hidden'):
                            continue
                        if span.text.strip().lstrip().rstrip() not in honors_and_awards:
                            honors_and_awards = honors_and_awards + " ".join(span.text.split()) + " \n "
                    honors_and_awards = honors_and_awards
            except Exception as e:
                log.append(f'in {i} at honors and awards error: {e} ')
                continue

            try:
                if 'Skills' in h2.text:
                    skills_link=h2.find_next('div',{'class':'pvs-list__footer-wrapper'}).find("a").get('href')
                    if skills_link:
                        driver.get(skills_link)
                        time.sleep(8)  # Adjust wait time as needed
                        skills_src = driver.page_source
                        skills_page = BeautifulSoup(skills_src, 'lxml')
                        for h2 in skills_page.find_all('h2'):
                            if 'Skills' in h2.text:
                                for a in h2.find_next('ul').find_all('a'):
                                    for span in a.find_all('span', {'class': ''}):
                                        if span.find_all(class_='visually-hidden'):
                                            continue
                                        if span.text.strip().lstrip().rstrip() not in skills:
                                            skills = skills + " ".join(span.text.split()) + ","
                    else:
                        for a in h2.find_next('ul').find_all('a'):
                            for span in a.find_all('span', {'class': ''}):
                                if span.find_all(class_='visually-hidden'):
                                    continue
                                if span.text.strip().lstrip().rstrip() not in skills:
                                    skills = skills + " ".join(span.text.split()) + ","
            except Exception as e:
                log.append(f'in {i} at skills error: {e} ')
                continue
        data.append({'name': name, 'headline': headline, 'about': about, 'location': location, 'status': status,
                     'current_comapany_school': current_comapany_school, 'experience': experience,
                     'volunteer': volunteer, 'education': education, 'skills': skills, 'prf_img': prf_img,
                     'bg_img': bg_img, 'Honors & awards': honors_and_awards})
    df = pd.DataFrame(data, columns=['name', 'headline', 'about', 'location', 'status', 'current_comapany_school',
                                     'experience', 'volunteer', 'education', 'skills', 'Honors & awards', 'prf_img',
                                     'bg_img'])
    df.to_csv('linked_in_data.csv', index=False)
    pd.DataFrame(log, columns=['logs']).to_csv('log.csv', index=False)


# Example usage
first_name = input('first_name').lower()
last_name = input('last_name').lower()
get_linkedin_profile(first_name, last_name)