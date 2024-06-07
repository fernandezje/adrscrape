from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime, timedelta

def get_total_base_price(listing_id, start_date, end_date, guest_count):
    # Setup the webdriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    
    base_url = f'https://www.airbnb.com/rooms/{listing_id}'
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    
    date_range = (end_date_obj - start_date_obj).days + 1
    price_matrix = pd.DataFrame(index=range(date_range), columns=range(date_range))

    for i in range(date_range):
        for j in range(i + 1, date_range):
            check_in = start_date_obj + timedelta(days=i)
            check_out = start_date_obj + timedelta(days=j)
            check_in_str = check_in.strftime('%Y-%m-%d')
            check_out_str = check_out.strftime('%Y-%m-%d')

            url = f'{base_url}?check_in={check_in_str}&check_out={check_out_str}&adults={guest_count}'
            driver.get(url)
            
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, 'span._tyxjp1')
                price = float(price_element.text.replace('$', '').replace(',', ''))
                price_matrix.iloc[i, j] = price
            except Exception as e:
                price_matrix.iloc[i, j] = None
                print(f"Error retrieving price for {check_in} to {check_out}: {e}")

    driver.quit()
    return price_matrix

if __name__ == "__main__":
    listing_id = 'your_listing_id'
    start_date = 'your_start_date'
    end_date = 'your_end_date'
    guest_count = 2  # your_guest_count

    price_matrix = get_total_base_price(listing_id, start_date, end_date, guest_count)
    print(price_matrix)
