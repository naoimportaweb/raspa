import os, sys, time; 

from selenium import webdriver
from selenium.webdriver.common.by import By

# A IDEIA É TRABALHAR COMO SE FOSSE UM HELPER
class ChromeEngine():
    def __init__(self):
        options = webdriver.ChromeOptions( );
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
    
    def navegate(self, url):
        self.driver.get( url );

    def __del__(self):
        self.driver.quit()

    def elements(self, xpath, element_=None):
        if element_ == None:
            element_ = self.driver;
        return element_.find_elements(by=By.XPATH, value=xpath);

    def element(self, xpath, element_=None):
        retorno = self.elements(xpath, element_);
        if len(retorno) == 0:
            return None;
        else:
            return retorno[0];

    def element_value(self, xpath, attribute):
        retorno = self.element(xpath);
        if retorno == None:
            return "";
        else:
            return retorno.get_attribute( attribute );

if __name__ == "__main__":
    c = ChromeEngine() ;
    c.navegate("https://www.camara.leg.br/deputados/quem-sao");
    cornos = c.elements('//*[@id="parametro-nome"]/option');
    for corno in cornos:
        if corno.get_attribute("value") == None or corno.get_attribute("value") == "":
            continue;
        c.navegate("https://www.camara.leg.br/deputados/" + corno.get_attribute("value"));
        time.sleep(30);
        break;
        #print(corno.get_attribute("value"), corno.get_attribute("textContent"));
