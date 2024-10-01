import time

from behave import given, then, when
from selenium.common import TimeoutException
from selenium.webdriver.chrome import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


@given('I will launch a Browser in chrome')
def launch_browser(context):
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.com/")
    context.driver = driver
    context.driver.maximize_window()
    #adding time to add captcha manually
    time.sleep(10)

@when('I will search toys')
def search_bar(context):
    search_box = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
    search_box.send_keys("toys")
    search_box.send_keys(Keys.RETURN)

@then('I will Select any 2 products and add to cart and validate the price')
def select_toy(context):
    # Add the first product to the cart
    first_product = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 's-main-slot')]//span[contains(@class, 'a-price-whole')])[1]")))
    first_search_price = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 's-main-slot')]//span[contains(@class, 'a-price-whole')])[1]"))).text
    first_product.click()
    first_detail_price = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='a-price aok-align-center reinventPricePriceToPayMargin priceToPay']//span[@class='a-price-whole']"))).text
    WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.ID, 'add-to-cart-button'))).click()
    time.sleep(2)
    Cart_button = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.ID, 'nav-cart-count')))
    Cart_button.click()
    time.sleep(5)
    first_cart_price = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-item-index="1"]//span[@class="a-size-medium a-color-base sc-price sc-white-space-nowrap sc-product-price a-text-bold"]'))).text
    whole_price1 = first_cart_price.replace('$', '').split('.')[0]

    print(f"Whole number part of the first product price: {whole_price1}")
    # Validate prices for the first product
    assert first_search_price == first_detail_price, f"Price mismatch1: {first_search_price} != {first_detail_price}"
    assert first_detail_price == whole_price1, f"Price mismatch2: {first_detail_price} != {whole_price1}"

    #ADD 2ND Product into the cart

    # Go back to the search results
    context.driver.back()
    time.sleep(2)
    context.driver.back()
    time.sleep(2)
    context.driver.back()


    # Add the second product to the cart
    second_product = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 's-main-slot')]//span[contains(@class, 'a-price-whole')])[2]"))
    )
    second_search_price = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 's-main-slot')]//span[contains(@class, 'a-price-whole')])[2]"))
    ).text

    second_product.click()

    get_text_of_2nd_Prod = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.ID, "productTitle"))
    ).text

    second_detail_price = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='a-price aok-align-center']//span[@class='a-price-whole']"))).text

    WebDriverWait(context.driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'add-to-cart-button'))
    ).click()

    time.sleep(2)

    # Go to the cart page
    Cart_button = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.ID, 'nav-cart-count'))
    )
    Cart_button.click()

    time.sleep(5)

    product_title_found = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{get_text_of_2nd_Prod}')]"))
    )
    try:
        product_title_found = WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{get_text_of_2nd_Prod}')]"))
        )
        print(f"The product title '{get_text_of_2nd_Prod}' is found on the other page.")

        cart_price = product_title_found.find_element(By.XPATH, "//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap sc-product-price a-text-bold']").text
        whole_price2 = cart_price.replace('$', '').split('.')[0]
        print(f"Whole number part of the first product price: {whole_price2}")
        print(f"The price of the product '{get_text_of_2nd_Prod}' in the cart is: {cart_price}")

    except TimeoutException:
        print(f"The product title '{get_text_of_2nd_Prod}' is not found on the other page.")
        cart_price = None

    assert second_search_price == second_detail_price == whole_price2, (
        f"Price mismatch: search price ({second_search_price}), detail price ({second_detail_price}), cart price ({cart_price})"
    )

    print("All prices match!")

    # Close the browser
    context.driver.quit()
