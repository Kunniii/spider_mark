from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

from os import path, makedirs

class Spider:

  url = 'https://fap.fpt.edu.vn/Phuhuynh/Login.aspx'
  USERNAME = None
  PASSWORD = '12345678'
  browser = None
  state_index = 1

  def __init__(self, username) -> None:
    if not username:
      raise('Null Username')
    self.USERNAME = username

    if not path.isdir(path.abspath('./states')):
      makedirs(path.abspath('./states'))

    opts = Options()
    opts.add_argument("--headless")

    self.browser = Firefox(options=opts)
    self.browser.get(self.url)

  def _logState(self):
    self.browser.get_full_page_screenshot_as_png()
    self.browser.save_full_page_screenshot('./states/'+str(self.state_index)+'.png')
    self.state_index += 1

  def run(self):
    try:
      select = Select(self.browser.find_element('id', 'ctl00_mainContent_dllCampus'))
      # select.select_by_visible_text('FU-Cần Thơ')
      select.select_by_value('6')

      inp_username = self.browser.find_element('id', 'ctl00_mainContent_txtUser')
      inp_password = self.browser.find_element('id', 'ctl00_mainContent_txtPass')
      inp_username.send_keys(self.USERNAME)
      inp_password.send_keys(self.PASSWORD)

      btn_login = self.browser.find_element('id', 'ctl00_mainContent_btLogin')
      btn_login.click()

      link = self.browser.find_element('xpath', '/html/body/form/div[4]/table/tbody/tr[1]/td[1]/ul/li[5]/a')
      link.click()

      btn_export = self.browser.find_element('id', 'ctl00_mainContent_btnExport')
      btn_export.click()

      self.browser.close()
      print(f"[+] Done: {self.USERNAME}")
      with open('./done.txt', 'a+') as f:
        f.write(f'{self.USERNAME}\n')
      return
    except:
      self.browser.close()
      return