from math import e
from datetime import datetime
from django.shortcuts import redirect, render, HttpResponse
from django.views import generic
from django.views.generic import View
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import seed
from random import random
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.action_chains import ActionChains
from django.contrib import messages
import sqlite3
from articleapp.models import OrderHistoryModel

global ok, not_ok

# ----------------------------------------------REPLACE PRODUCT IN ORDER--------------------------------------------------
history = []



def replace_product_inorder(driver, product1, product2, el):
    changeComment = product1 + " changé par " + product2 + " "
    for i, e in enumerate(el):
        if str(e.text) == str(product1):
            print("Test => ", e.text)
            a = 'link_{}'.format(i)
            print('try to find: ' + a)
            id = "//a[@id='" + a + "']"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//a[@id='" + a + "']"))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Remplacer')]"))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="ref_article_remplacement_nom_c"]'))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="lib_article_cata_m"]'))).send_keys(product2)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="lib_article_cata_m"]'))).send_keys(Keys.ENTER)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@class="lib_categorie"]'))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="form_remplacement"]/table/tbody/tr[3]/td[5]/label'))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="form_remplacement"]/table/tbody/tr[5]/td[5]/label'))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="form_remplacement"]/table/tbody/tr[6]/td[5]/label'))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Valider les changements')]"))).click()
            WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='new_pop_up_options']")))
            commentFailed = False
            while commentFailed == False:
                try:
                    # Ici faut mettre un temps d'attente mais pas trop long, sinon ça ralentis trop mais pas trop court sinon des fois ça ne va pas charger
                    WebDriverWait(driver, 1.5).until(EC.presence_of_element_located(
                                (By.XPATH, "//h4[@class='modal-title'][text()[contains(.,'Alerte encours')]]")))
                    WebDriverWait(driver, 0.5).until(EC.presence_of_element_located(
                                                (By.XPATH, "//a[@class='close']"))).click()
                    print("PopUp Closed")
                except:
                    print("There is no popup")
                    pass
                #popup_to_close.click()
                print('Popup closed')
                try:
                    #WebDriverWait(driver, 1.5).until(EC.presence_of_element_located(
                     #   (By.XPATH, "//h4[@class='modal-title'][text()[contains(.,'Alerte encours')]]")))
                    #WebDriverWait(driver, 0.5).until(EC.presence_of_element_located(
                    #    (By.XPATH, "//a[@class='close']"))).click()
                    #print("PopUp Closed")

                    print("TRY")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "//li[@id='menu_5']/span"))).click()
                    commentFailed = True
                except:
                    #print("There is no popup")
                    print("FAIL COMMENT")
                    pass
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='tinyeditor']/div[3]/iframe"))).send_keys(changeComment)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='doc_description']"))).click()
            print("Uploaded!!")
    # ---------------------------------------------- PRINT WHICH ORDER HAS BEEN MODIFIED --------------------------------------------------


def isOrderInList(id, list):
    for order in list:
        if order.id == id:
            return True
    return False


def product_replace(driver, product1, product2, buttons_edit, request, orders):
    hasReplaceProduct = False
    popup_to_close =WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                                (By.XPATH, "//*[@class='close']")))
    for i in range(len(orders)):
        if product1 in orders[i].products and product2 in orders[i].products:
            print("Les deux produits sont dans la commande")
            orders[i].date = datetime.now()
        else:
            hasReplaceProduct = True
            print("Ouverture de la page produit")
            driver.execute_script(
                "arguments[0].click();", orders[i].button_edit)
            driver.switch_to.window(driver.window_handles[1])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//*[@class='ov_hidden']")))

            #if popup to close
            try:
                # Ici faut mettre un temps d'attente mais pas trop long, sinon ça ralentis trop mais pas trop court sinon des fois ça ne va pas charger
                WebDriverWait(driver, 1.5).until(EC.presence_of_element_located(
                            (By.XPATH, "//h4[@class='modal-title'][text()[contains(.,'Alerte encours')]]")))
                WebDriverWait(driver, 0.5).until(EC.presence_of_element_located(
                                            (By.XPATH, "//a[@class='close']"))).click()
                print("PopUp Closed")
            except:
                print("There is no popup")
                pass
            #popup_to_close.click()
            print('Popup closed')
            # get all the name of product which are in order
            el = driver.find_elements_by_class_name('ov_hidden')
            print("All Elements => ", el)
            try:
                replace_product_inorder(driver, product1, product2, el)
            except:
                print("PRODUCT CRASHED")
                pass
            orders[i].hasBeenUpdated = True
            orders[i].date = datetime.now()
            print("driver.close")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print("driver.switch_to.window done")
        if isOrderInList(orders[i].id, history) == False:
            history.append(orders[i])
    return hasReplaceProduct
    # ----------------------------------------------POP UP SEARCH LMB--------------------------------------------------


class Order:
    id = 0
    productToUpdate = ''
    productToInsert = ''
    status = ''
    hasBeenUpdated = False
    products = []
    date = datetime.now()
    button_edit = None

    def __init__(self, id, productToUpdate, productToInsert):
        self.id = id
        self.productToUpdate = productToUpdate
        self.productToInsert = productToInsert


def displayOrder(o):
    print(o.id + ':' + o.status + ":" +
          str(len(o.products)) + ":" + str(o.hasBeenUpdated))
    print(o.date)
    for p in o.products:
        print(p, end='')
    print(o.button_edit)
    print('')


def parse_page(driver, product1, product2, request):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@data-lmb-infobulle='Éditer la commande']")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    buttons_edit = driver.find_elements_by_xpath(
        "//a[@data-lmb-infobulle='Éditer la commande']")
    if len(buttons_edit) == 0:
        return False
    data = []
    orders = []
    div = soup.find('table', {'class': 'style-2'})
    tbody = div.find('tbody')
    tr_orders = tbody.find_all('tr')
    order = Order('', product1, product2)
    print("Start parsing")

    print("En attente") #tesssssst
    time.sleep(15)

    for tr in tr_orders:
        td = tr.find_all('td')
        if isinstance(tr.get('class'), list):
            for t in td:
                value = t.text.strip()
                if value == product1 or value == product2:
                    order.products.append(value)
        else:
            if order.id != '' and order.status != '' and isOrderInList(order.id, orders) == False:
                orders.append(order)
            if len(orders) >= len(buttons_edit):
                break
            order = Order('', product1, product2)
            order.products = []
            order.button_edit = buttons_edit[len(orders)]
            for t in td:
                value = t.text.strip()
                if t.get('qa_id') == '480148':
                    order.id = value
                #if value == "En cours" or value == 'En saisie':
                if value != "Traitée" or value != 'Annulée':
                    order.status = value
    return product_replace(driver, product1, product2, buttons_edit, request, orders)


def get_pages(driver, product1, product2, request):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@data-lmb-infobulle='Éditer la commande']")))

    nombrePages = len(driver.find_elements_by_xpath(
        '//*[@qa_id="170278"][string-length(text()) > 0]')) / 2

    idx = 1
    while idx <= int(nombrePages):
        try:
            researchButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@qa_id="480146"]')))
        except:
            continue
        if parse_page(driver, product1, product2, request) == False:
            if (idx == int(nombrePages)):
                break
            idx += 1
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@qa_id="170278"][contains(text(), "' + str(idx) + '") > 0]'))).click()
        else:
            researchButton.click()
            nombrePages = len(driver.find_elements_by_xpath(
                '//*[@qa_id="170278"][string-length(text()) > 0]')) / 2


def search_product(driver, product1, product2, request):

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="lib_article_cata_m"]'))).send_keys(product1)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="lib_article_cata_m"]'))).send_keys(Keys.ENTER)
        #time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="lib_article_cata_m"]').send_keys(Keys.ENTER)
        # click on hyperlink | This close the POP UP
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@class="r_art_lib"]'))).click()
        # ---------------------------------------------- END POP UP SEARCH LMB--------------------------------------------------
        actions = ActionChains(driver)

        for _ in range(3):
            actions.send_keys(Keys.SPACE).perform()

        # ----------------------------------------------POP UP SEARCH LMB--------------------------------------------------
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="form_recherche_c"]/div[2]/button/span'))).click()


        get_pages(driver, product1, product2, request)
        print("NOW ITS HISTORY")
        for order in history:
            displayOrder(order)
            record = OrderHistoryModel(orderId=order.id,
                                       initial=order.productToUpdate,
                                       final=order.productToInsert,
                                       date=order.date,
                                       status="Done" if order.hasBeenUpdated else "Product's already in order")
            record.save()
        print("Done scroll pages")
    except Exception as e:
        print(e)
        driver.close()
        messages.warning(request, e)

        # ----------------------------------------------LOG IN--------------------------------------------------

#  https://masada.lundimatin.biz/profil_collab/#documents_cmde_cli_recherche.php
def login(driver, product1, product2, request, userName, password):
    try:
        driver.get(
            'https://french-retro.lundimatin.biz/profil_collab/#documents_cmde_cli_recherche.php')
        driver.maximize_window()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="login"]'))).send_keys(userName)
        driver.find_element_by_id('code').send_keys(password)
        driver.find_element_by_id('code').send_keys(Keys.ENTER)
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '/²html/body/div/div/div/div/a[1]/div[1]/i'))).click()
        except:
            pass
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="form_recherche_c"]/div[1]/div[1]/table/tbody/tr[3]/td[2]/div[1]/label/div'))).click()

        WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Options avancées']"))).click()
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="form_recherche_c_advanced"]/div[2]/table/tbody/tr[2]/td[2]/div/button[1]/i'))).click()
        search_product(driver, product1, product2, request)
    except Exception as e:
        driver.close()
        print(e)
        messages.warning(request, e)

        # ----------------------------------------------INPUTS PRODUCTS--------------------------------------------------

# JEY-G65-S JEFF-M65-S


def home(request):
    if request.method == "GET":
        return render(request, "articleapp/home.html")
    elif request.method == 'POST':
        product1 = request.POST.get('Product1')
        product2 = request.POST.get('Product2')
        userName = request.POST.get('UserName')
        password = request.POST.get('Password')
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
        #driver = webdriver.Chrome(ChromeDriverManager().install())

        login(driver, product1, product2, request, userName, password)
        return redirect('home')
    else:
        messages.warning(request, "Something went wrong, Please try again!")
        return redirect('home')


class HistoryView(generic.ListView):
    model = OrderHistoryModel
    context_object_name = 'history_list'
    queryset = OrderHistoryModel.objects.all()
    template_name = 'articleapp/history.html'
