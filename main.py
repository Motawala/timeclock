from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime
import pandas as pd


def read_data(filepath):
    df = pd.read_csv(filepath, dtype='str')
    # Convert the 'Total' column to numeric, forcing errors to NaN if there are non-numeric values
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

    # Group by 'Display Name' and calculate the sum of the 'Total' column for each group
    grouped_df = df.groupby("Display Name")["Total"].sum()

    # Print the results
    for person, total in grouped_df.items():
        print(f"{person}: Total = {total:.2f}")


# Specify the path to the ChromeDriver if not in your PATH
service = Service('/usr/local/bin/chromedriver')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the HTML page
driver.get('http://192.168.1.223')  # Replace with the path to your local HTML file

# Locate the username and password input fields
username_input = driver.find_element(By.NAME, 'username')
password_input = driver.find_element(By.NAME, 'password')

if username_input and password_input:
    # Input the username and password
    username_input.send_keys('PK45193')  # Replace with your actual username
    password_input.send_keys('Karan2992002$')  # Replace with your actual password

    # Store the current URL
    current_url = driver.current_url

    # Submit the form by pressing Enter
    password_input.send_keys(Keys.RETURN)

    try:
        # Wait for the login to complete and ensure you are on the correct page
        WebDriverWait(driver, 15).until(
            EC.url_changes(current_url)  # Wait until the URL changes from the login page
        )
        print("Login successful, URL changed.")

       
        
        # Redirect to the desired page
        driver.get('http://192.168.1.223/report.html?rt=2')  # Replace with the target URL

        # Optional: Verify the new page loaded correctly
        print("Redirecting to the new page...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'pageTitleSC'))  # Replace with an ID or condition from the new page
        )
        start_date = input("Enter Start Date: ")
        end_date = input("Enter End Date: ")


        s = start_date.strip().split('/')
        e = end_date.strip().split('/')
        time_card_url = f"http://192.168.1.223/report.html?rt=2&type=7&customfld_fieldId=0&from={s[0]}%2F{s[1]}%2F{s[2]}&to={e[0]}%2F{e[1]}%2F{e[2]}&eid=0&submitMenu=Submit"
        #print("New page loaded successfully."(time_card_url))
        driver.get(time_card_url)
        export_csv_url = f"http://192.168.1.223/report.html?rt=2&from={s[0]}/{s[1]}/{s[2]}&to={e[0]}/{e[1]}/{e[2]}&eid=ss&stdexport=1"
        driver.get(export_csv_url)
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        now_date, now_time = (now.split(' '))
        now_date = now_date.split('-')
        now_time = now_time.split(':')
        curr_dt = ""
        for dt in now_date:
            curr_dt = curr_dt + dt 
        curr_tm = ""
        now_time.pop()
        for tm in now_time:
            curr_tm = curr_tm + tm 
        newfile_name = f"/Users/karanpatel/Downloads/icon-{curr_dt}-{curr_tm}.csv"
        time.sleep(5)
        read_data(newfile_name)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Note: No driver.quit() so that the browser remains open.
