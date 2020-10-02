import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

url = ""
basket_id = "basket-component"

menu_item_href = ""
product_id_menu = "24"

pref_product_in_menu = '//*[@id="products-view-wrapper"]/div/div[2]/div['
postf_product_in_menu = ']/div/div[2]/div'

delivery_types_class = "switch"
delivery_text = "Mindestbestellwert 0,00 €"

class_added_product = "same-item-in-basket"


class AddIdBasket(unittest.TestCase):

    def setUp(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--window-size=1420,1080')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def test_add_product_in_basket(self):
        # ОТКРЫТИЕ БРАУЗЕРА СО СТРАНИЦЕЙ МАГАЗИНА
        self.driver.get(url)

        # ОЖИДАЕМ ПОЯВЛЕНИЯ КОРЗИНЫ
        WebDriverWait(self.driver, 500).until(
            lambda driver: driver.find_element_by_id(basket_id))

        # ПЕРЕХОДИМ В НУЖНЫЙ ПУНКТ МЕНЮ
        self.driver.find_element_by_css_selector("a[href='" + menu_item_href + product_id_menu + "']").click()
        time.sleep(3)

        # МЕНЯЕМ МЕТОД ДОСТАВКИ НА "САМОВЫВОЗ"
        delivery = self.driver.find_element_by_class_name(delivery_types_class)
        delivery.find_elements_by_tag_name("span")[1].click()

        # ПРОВЕРЯЕМ ЧТО ИЗМЕНИЛСЯ ТЕКСТ КОРЗИНЫ
        assert self.driver.find_element_by_class_name("delivery-info-text").text == delivery_text

        # ДОБАВЛЯЕМ В КОРЗИНУ ПРОДУКТ НАЖИМАЯ НА КНОПКУ ДОБАВЛЕНИЯ
        self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_in_menu).click()

        # ПРОВЕРЯЕМ ЧТО ТОВАР ДОБАВИЛСЯ В КОРЗИНУ
        assert len(self.driver.find_elements_by_id("basket-item")) == 1

        # ПРОВЕРЯЕМ ЧТО ИЗМЕНИЛАСЬ СУММА ЗАКАЗА
        time.sleep(1)
        order = self.driver.find_element_by_class_name("order-price")
        time.sleep(3)

        assert order.find_element_by_class_name("value").text == self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_in_menu + "/div").text

        # ДОБАВЛЯЕМ В КОРЗИНУ 2 ПРОДУКТ НАЖИМАЯ НА КНОПКУ ДОБАВЛЕНИЯ
        self.driver.find_element_by_xpath(pref_product_in_menu + "2" + postf_product_in_menu).click()

        # ДОБАВЛЯЕМ В КОРЗИНУ 3 ПРОДУКТ НАЖИМАЯ НА КНОПКУ ДОБАВЛЕНИЯ
        self.driver.find_element_by_xpath(pref_product_in_menu + "3" + postf_product_in_menu).click()

        # ПРОВЕРЯЕМ ЧТО ТОВАР ДОБАВИЛСЯ В КОРЗИНУ
        assert len(self.driver.find_elements_by_id("basket-item")) == 3

        # ПРОВЕРЯЕМ ЧТО ИЗМЕНИЛАСЬ СУММА ЗАКАЗА
        time.sleep(1)
        first_product_price = self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_in_menu + "/div").text.split(" ")[0].replace(',', '.')
        second_product_price = self.driver.find_element_by_xpath(pref_product_in_menu + "2" + postf_product_in_menu + "/div").text.split(" ")[0].replace(',', '.')
        third_product_price = self.driver.find_element_by_xpath(pref_product_in_menu + "3" + postf_product_in_menu + "/div").text.split(" ")[0].replace(',', '.')
        all_products_price = float("{0:.2f}".format(float(first_product_price) + float(second_product_price) + float(third_product_price)))
        order = self.driver.find_element_by_class_name("order-price").find_element_by_class_name("value").text

        assert order == (str(all_products_price) + "0 €").replace('.', ',')

        # ДОБАВЛЯЕМ ПОВТОРНО ПЕРВОЕ БЛЮДО
        self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_in_menu).click()
        time.sleep(1)

        # ПРОВЕРЯЕМ ЧТО ИЗМЕНИЛИСЬ КОЛИЧЕСТВО И МНОЖИТЕЛЬ ТОВАРА
        basket_item = self.driver.find_elements_by_id("basket-item")[0]
        basket_item_count = basket_item.find_element_by_class_name("count-label").text
        product_multiplier = self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_in_menu + "/i").text
        order = self.driver.find_element_by_class_name("order-price").find_element_by_class_name("value").text
        all_products_price += float(first_product_price)

        assert basket_item_count == "2"
        assert product_multiplier == "2x"
        assert order == (str(float("{0:.2f}".format(all_products_price))) + "0 €").replace('.', ',')

        # ДОБАВЛЯЕМ ПОВТОРНО ВТОРОЕ БЛЮДО
        basket_item = self.driver.find_elements_by_id("basket-item")[1]
        basket_item.find_element_by_css_selector(".fas.fa-plus-circle").click()
        time.sleep(1)

        # ПРОВЕРЯЕМ ЧТО ИЗМЕНИЛИСЬ КОЛИЧЕСТВО И МНОЖИТЕЛЬ ТОВАРА
        basket_item_count = basket_item.find_element_by_class_name("count-label").text
        product_multiplier = self.driver.find_element_by_xpath(
            pref_product_in_menu + "2" + postf_product_in_menu + "/i").text
        order = self.driver.find_element_by_class_name("order-price").find_element_by_class_name("value").text
        all_products_price += float(second_product_price)

        assert basket_item_count == "2"
        assert product_multiplier == "2x"
        assert order == (str(float("{0:.2f}".format(all_products_price))) + "0 €").replace(
            '.', ',')

        # УБИРАЕМ ТРЕТЬЕ БЛЮДО
        basket_item = self.driver.find_elements_by_id("basket-item")[2]
        basket_item.find_element_by_css_selector(".fas.fa-minus-circle").click()
        time.sleep(1)
        self.driver.find_element_by_class_name("ant-modal").find_element_by_css_selector(".button-order.positive-action").click()
        time.sleep(1)

        # ПРОВЕРЯЕМ ЧТО ИЗМЕНИЛИСЬ КОЛИЧЕСТВО И МНОЖИТЕЛЬ ТОВАРА
        assert len(self.driver.find_elements_by_class_name("ant-modal")) == 0
        assert len(self.driver.find_elements_by_id("basket-item")) == 2
        assert self.driver.find_element_by_xpath(pref_product_in_menu + "3" + postf_product_in_menu + "/i").text == "+"

        all_products_price -= float(third_product_price)
        order = self.driver.find_element_by_class_name("order-price").find_element_by_class_name("value").text

        assert order == (str(float("{0:.2f}".format(all_products_price))) + "0 €").replace(
            '.', ',')


if __name__ == '__main__':
    unittest.main()
