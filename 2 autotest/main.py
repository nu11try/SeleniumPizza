import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

url = "https://hermes-dev.devteam.win/123-pizza-roedermark/5/"
basket_id = "basket-component"
address_id = "address-form-component"
pay_class = "paymethod-title"
order_succ_class = "order-success"

order_succ_title = "Ihre Bestellung war erfolgreich!"

menu_item_href = "/123-pizza-roedermark/5/cat/"
product_id_menu = "24"

pref_product_in_menu = '//*[@id="products-view-wrapper"]/div/div[2]/div['
postf_product_in_menu = ']/div/div[2]/div'
postf_product_name_in_menu = ']/div/div[1]/div[1]/div/div/div'

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

        # ДЕЛАЕМ ПАУЗУ НА 3 СЕК ЧТОБЫ ПРОГРУЗИЛАСЬ СТРАНИЦА С ТОВАРОМ
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
        assert self.driver.find_element_by_class_name("order-price").find_element_by_class_name("value").text == self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_in_menu + "/div").text

        # НАЖИМАЕМ КНОПКУ "ЗАКАЗАТЬ СЕЙЧАС"
        self.driver.find_element_by_css_selector(".button-order.positive-action").click()
        time.sleep(1)

        # ОЖИДАЕМ ПОЯВЛЕНИЯ БЛОКА ОПЛАТЫ
        WebDriverWait(self.driver, 500).until(
            lambda driver: driver.find_element_by_id(address_id))

        # НАЖИМАЕМ НА КНОПКУ "К ОПЛАТЕ"
        self.driver.find_element_by_css_selector(".button-order.positive-action").click()
        time.sleep(1)

        # ПРОВЕРЯЕМ НА НАЛИЧИЕ ПРЕДУПРЕЖДЕНИЯ
        assert len(self.driver.find_elements_by_class_name("ant-form-explain")) == 7

        # ЗАПОЛНЯЕМ ВСЕ НЕОБХОДИМЫЕ ПОЛЯ
        self.driver.find_element_by_id("first_name").send_keys("test")
        self.driver.find_element_by_id("last_name").send_keys("test")
        self.driver.find_element_by_id("street").send_keys("test")
        self.driver.find_element_by_id("street_no").send_keys("test")
        self.driver.find_element_by_id("city").send_keys("test")
        self.driver.find_element_by_id("email").send_keys("test@test.test")
        self.driver.find_element_by_id("phone").send_keys("88888888888")
        time.sleep(1)

        # НАЖИМАЕМ НА КНОПКУ "К ОПЛАТЕ"
        self.driver.find_element_by_css_selector(".button-order.positive-action").click()
        time.sleep(1)

        # ОЖИДАЕМ ПОЯВЛЕНИЯ БЛОКА ОПЛАТЫ
        WebDriverWait(self.driver, 500).until(
            lambda driver: driver.find_element_by_class_name(pay_class))

        # ПРОВЕРЯЕМ СООТВЕТСТВИЕ ТОВАРА С ЗАКАЗОМ
        assert self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_name_in_menu).text == \
               self.driver.find_element_by_id("basket-item").find_element_by_class_name("product-name").text + "G"
        assert self.driver.find_element_by_class_name("order-price").find_element_by_class_name("value").text == \
               self.driver.find_element_by_xpath(pref_product_in_menu + "1" + postf_product_in_menu + "/div").text

        # ВЫБИРАЕМ СПОСОБ ОПЛАТЫ "НАЛИЧНЫМИ"
        self.driver.find_elements_by_css_selector("input[name='paymentMethod']")[0].click()
        time.sleep(1)

        # ВЫБИРАЕМ СПОСОБ ОПЛАТЫ "ЗАКАЗАТЬ"
        self.driver.find_element_by_css_selector(".button-order.positive-action").click()
        time.sleep(1)

        # ОЖИДАЕМ ПОЯВЛЕНИЯ БЛОКА УСПЕШНОЙ ОПЛАТЫ
        WebDriverWait(self.driver, 500).until(
            lambda driver: driver.find_element_by_class_name(order_succ_class))

        # ПРОВЕРЯЕМ НАЛИЧИЕ ТЕКСТА ОБ УСПЕШНОЙ ОПЛАТЕ
        assert self.driver.find_element_by_class_name(order_succ_class).find_element_by_class_name("wrapper").find_element_by_class_name("title").text == order_succ_title


if __name__ == '__main__':
    unittest.main()
