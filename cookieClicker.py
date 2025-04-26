from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from states import UpgradeSingleton
from estrategia import define_best_buy
import threading
import time

class CookieClicker:
    _instance = None
    _site = 'https://orteil.dashnet.org/cookieclicker/'

    def __new__(cls, nome_padaria):
        if not cls._instance:
            cls._instance = super(CookieClicker, cls).__new__(cls)
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            cls._instance._driver = webdriver.Chrome(options=options)
            cls._instance._driver.get(cls._site)
            cls.start_time = time.time()
            cls._instance.__initial_config(nome_padaria)
        return cls._instance

    def __getattr__(self, name):
        return getattr(self._driver, name)

    def __initial_config(self, nome_padaria) -> None:
        WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, 'langSelect-EN')))
        self.find_element(By.ID, 'langSelect-EN').click()
        WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "bigCookie")))
        self.__set_nome_padaria(nome_padaria)
        self._cookie = self.find_element(By.ID, "bigCookie")
        self._products = [self.find_element(By.ID, f"product{i}") for i in range(0, 20)]
        self._upgrade_list = self.find_element(By.ID, 'upgrades')
        self._product_unlocked_count = 0
        self._products_enabled = []
        self._enabled_upgrades = []
        self.__config_threads()

    def __config_threads(self) -> None:
        self._thread_look4unlocked = threading.Thread(target=self.look4unlocked)
        self._thread_look4enabled = threading.Thread(target=self.look4enabled)
        #self._thread_buy = threading.Thread(target=self.maxBuy)
        self._thread_buy = threading.Thread(target=self.bestBuy)
        self._thread_upgrades = threading.Thread(target=self.look4upgrade)
        self._thread_goldenCookie = threading.Thread(target=self.look4goldenCookie)
        
        self._threads = [
            self._thread_look4unlocked,
            self._thread_look4enabled,
            self._thread_buy,
            self._thread_upgrades,
            self._thread_goldenCookie
        ]
        for t in self._threads:
            t.daemon = True

    def start_threads(self) -> None:
        for t in self._threads:
            t.start()

    def __set_nome_padaria(self, nome_padaria) -> None:
        WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "bakeryName")))
        self.find_element(By.ID, "bakeryName").click()
        WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "bakeryNameInput")))
        self.find_element(By.ID, "bakeryNameInput").send_keys(nome_padaria)
        self.find_element(By.ID, "promptOption0").click()

    def look4unlocked(self) -> None:
        while self._product_unlocked_count <= 20:
            if 'unlocked' in self._products[self._product_unlocked_count].get_attribute('class'):
                self._product_unlocked_count+=1

    def look4enabled(self) -> None:
        while True:
            time.sleep(0.1)
            for i in range(self._product_unlocked_count):
                if 'enabled' in self._products[i].get_attribute('class'):
                    if i not in self._products_enabled:
                        self._products_enabled.append(i)
                else:
                    try:
                        self._products_enabled.remove(i)
                    except:
                        pass

    def get_upgrades(self) -> list:
        return self._upgrade_list.find_elements(By.XPATH, './/div[contains(@class, "upgrade")]')

    def look4upgrade(self) -> None:
        while True:
            try:
                self._enabled_upgrades = [eu for eu in self.get_upgrades() if 'enabled' in eu.get_attribute('class')]
            except StaleElementReferenceException:
                self._enabled_upgrades = []

    def look4goldenCookie(self) -> None:
        while True:
            try:
                WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "shimmer")))
                self.find_element(By.CLASS_NAME, "shimmer").click()
            except TimeoutException:
                pass

    def maxBuy(self) -> None:
        while True:
            try:
                if len(self._products_enabled) > 0:
                    i = max(self._products_enabled)
                    p = self._products[i]
                    p.click()
                    UpgradeSingleton().buy(f'product{i}')
                    time.sleep(0.5) # importante para nao contar errado!!
                if len(self._enabled_upgrades) > 0:
                    self._enabled_upgrades[-1].click()
                    UpgradeSingleton().upgrade_next()
            except:
                pass
    
    def bestBuyCrazy(self) -> None:
        while True:
            try:
                if len(self._products_enabled) > 0:
                    i = define_best_buy(self._products_enabled)
                    p = self._products[i]
                    p.click()
                    UpgradeSingleton().count_product('product{i}') # isso é mais eficiente que p.get_attribute('id')
                    time.sleep(0.5)
                if len(self._enabled_upgrades) > 0:
                    self._enabled_upgrades[-1].click()
                    UpgradeSingleton().upgrade_next()
            except:
                pass

    def bestBuy(self) -> None:
        while True:
            try:
                unlocked = range(0, self._product_unlocked_count)
                i = define_best_buy(unlocked, UpgradeSingleton())
                if i in self._products_enabled:
                    self._products[i].click()
                    UpgradeSingleton().buy(f'product{i}')
                    time.sleep(0.5)
                if len(self._enabled_upgrades) > 0:
                    self._enabled_upgrades[-1].click()
                    UpgradeSingleton().upgrade_next()
            except:
                pass

    def run(self) -> None:
        self.start_threads()
        while True:
            self._cookie.click()

if __name__ == '__main__':
    nome_padaria = input('Digite o nome da sua padaria: ')
    cc = CookieClicker(nome_padaria)
    cc.run()