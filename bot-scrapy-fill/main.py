from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from dateutil.relativedelta import *
import pandas as pd
import locale
import time
import configs

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
previous_month = format((pd.to_datetime('today').floor('D')).replace(day=1) - relativedelta(months=1), '%B')

# Return {Username, Password, Chronos and Url}
cfgs = configs.get()

driver = webdriver.Chrome("C:/Users/Jonas Ramos/Documents/Desenvolvimento/Python/chromedriver")
driver.get(cfgs['Url'])

# Login
driver.find_element_by_id('Email').send_keys(cfgs['Username'])
driver.find_element_by_id('Password').send_keys(cfgs['Password'])
driver.find_element_by_id('btnEntrar').click()

# Wait load the home page
try:
    entries = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, 'Lançamentos')))
except TimeoutException:
    print('Time to wait the element page exceeded!')

# Open entries section and go to the activies
entries.click()
driver.find_element_by_link_text('Horas/Atividades').click()

# Read services data
services = pd.read_csv('data/services.csv', nrows=1)

# Fill the fields with services data
for serv in services.itertuples():
    periodo = driver.find_element_by_id('IdPeriodo')

    for mes in periodo.find_elements_by_tag_name('option'):
        if previous_month in mes.text.lower():
            mes.click()

    projetos = driver.find_element_by_id('IdProjeto')

    for prj in projetos.find_elements_by_tag_name('option'):
        if serv.Cliente.upper() in prj.text.upper():
            prj.click()

    driver.find_element_by_id('DataLancamento').send_keys(serv.Data)
    driver.find_element_by_tag_name('body').click()
    driver.find_element_by_id('DataInicio').send_keys(serv.Início)
    driver.find_element_by_id('DataFim').send_keys(serv.Fim)
    driver.find_element_by_id('Descricao').send_keys(serv.Desc)