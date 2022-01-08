import time
from selenium import webdriver

class WebScraping:
    def __init__(self, target, reaction, quantity): #python builder
        self.target   = target
        self.reaction = reaction
        self.quantity = quantity
        self.driver   = webdriver.Firefox()
        #self.driver.set_window_position(-10000,0) #hide browser
        self.enterWebSite()
        self.setCrossSectionData()
        self.saveText()  

    def enterWebSite(self):  
        self.driver.get("https://www-nds.iaea.org/exfor/endf.htm")
        time.sleep(2)

    def setCrossSectionData(self):
        elemTarget   = self.driver.find_element_by_name("Target")
        elemReaction = self.driver.find_element_by_name("Reaction")
        elemQuantity = self.driver.find_element_by_name("Quantity")

        elemTarget.clear()
        elemReaction.clear()
        elemQuantity.clear()

        elemTarget.send_keys(self.target)
        elemReaction.send_keys(self.reaction)
        elemQuantity.send_keys(self.quantity)
        time.sleep(2)

        self.driver.find_element_by_name("chkLib0").click()
        self.driver.find_element_by_css_selector("input[type=submit]").click()
        self.driver.find_element_by_css_selector("form > input:nth-child(14)").click() #select ll
        self.driver.find_element_by_css_selector("form > input:nth-child(10)").click() #select retrieve
        self.driver.find_element_by_css_selector("a[title='Show ENDF-6 file...']").click()
        time.sleep(8)

    def saveText(self):
        text = self.driver.find_element_by_css_selector("pre").get_attribute("textContent").encode("utf-8")

        with open('OutputCrossSection.txt', 'wb') as file:
            file.write(text)

        assert "No results found." not in self.driver.page_source
        self.driver.close()

