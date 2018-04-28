# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from pyvirtualdisplay import Display
import unittest, time, re, datetime, os, fcntl

class PomPurchaseTest(unittest.TestCase):
    def setUp(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        # firefoxのときはこちら
        #self.driver = webdriver.Firefox()
        # PhantomJSを用いてスクレイピング
        self.driver = webdriver.PhantomJS(os.environ.get("PHANTOM_PATH"))
        self.driver.implicitly_wait(30)
        self.repeat_munites = 4
        self.start_url = os.environ.get("START_URL")
        self.verificationErrors = []
        self.accept_next_alert = True
        self.email = os.environ.get("EMAIL")
        self.password = os.environ.get("PASSWORD")
        self.pic_dir = os.environ.get("PIC_DIR")
        self.tmp_dir = os.environ.get("TMP_DIR")
        self.lock_file = os.path.join(self.tmp_dir, os.environ.get("LOCK_FILE"))
        self.end_file = os.path.join(self.tmp_dir, os.environ.get("END_FILE"))
        self.purchase_flg = os.environ.get("PURCHASE_FLG")
        self.date = os.environ.get("DATE")
    
    def test_pom_purchase(self):
        try:
            sttime = datetime.datetime.now()
            print "[START] time of {0}".format(sttime.strftime("%Y-%m-%d %H:%M:%S"))
            driver = self.driver
            ontime = datetime.datetime.now()
            ontime = datetime.datetime.now()
            print "[MOVE] time of {0}".format(ontime.strftime("%Y-%m-%d %H:%M:%S"))
            driver.get(self.start_url)
            print "=>現在のページ:{0}".format(driver.title.encode('utf-8'))
            driver.find_element_by_xpath("//button[@type='submit']").click()
            # 購入完了画面までの中間ページでのの処理
            ontime = datetime.datetime.now()
            print "[MOVE] time of {0}".format(ontime.strftime("%Y-%m-%d %H:%M:%S"))
            # 購入時ログイン確認画面の対応
            if driver.title == u'購入前ログイン':
                print "=>現在のページ:{0}".format(driver.title.encode('utf-8'))
                print "<<ログイン処理中>>"
                driver.find_element_by_name("mainEmail").clear()
                driver.find_element_by_name("mainEmail").send_keys(self.email)
                driver.find_element_by_name("passwd").clear()
                driver.find_element_by_name("passwd").send_keys(self.password)
                driver.find_element_by_css_selector("input.btn.btnPrimary").click()
            ontime = datetime.datetime.now()
            print "[MOVE] time of {0}".format(ontime.strftime("%Y-%m-%d %H:%M:%S"))
            print "=>現在のページ:{0}".format(driver.title.encode('utf-8'))
            print "<<購入確認画面>>"
            
            driver.get(self.start_url)
            print "=>現在のページ:{0}".format(driver.title.encode('utf-8'))
            driver.find_element_by_xpath("//button[@type='submit']").click()
            # 購入完了画面までの中間ページでのの処理
            ontime = datetime.datetime.now()
            print "[MOVE] time of {0}".format(ontime.strftime("%Y-%m-%d %H:%M:%S"))
            # 購入時ログイン確認画面の対応
            if driver.title == u'購入前ログイン':
                print "=>現在のページ:{0}".format(driver.title.encode('utf-8'))
                print "<<ログイン処理中>>"
                driver.find_element_by_name("mainEmail").clear()
                driver.find_element_by_name("mainEmail").send_keys(self.email)
                driver.find_element_by_name("passwd").clear()
                driver.find_element_by_name("passwd").send_keys(self.password)
                driver.find_element_by_css_selector("input.btn.btnPrimary").click()
                ontime = datetime.datetime.now()
                print "[MOVE] time of {0}".format(ontime.strftime("%Y-%m-%d %H:%M:%S"))
            print "=>現在のページ:{0}".format(driver.title.encode('utf-8'))
            print "<<購入確認画面>>"
        
            # email会員解除
            try:
                driver.find_element_by_name("applyShopMail").click()
            except:
                pass
            # ガチで買う時だけ
            if self.purchase_flg == '1':
                # 同時並行で購入しないための制御
                with open(self.lock_file) as oLockFile:
                    # ファイルがすでにロックされていたら待つ
                    fcntl.flock(oLockFile.fileno(), fcntl.LOCK_EX)
                    if not os.path.exists(self.end_file): # 並列時に重ね買いをしないための対処
                        try:
                            driver.find_element_by_css_selector("button.btn.btnPrimary").click()
                            print "=>現在のページ:{0}".format(driver.title.encode('utf-8'))
                            print "<<購入完了>>"
                            # endfileの作成
                            open(self.end_file, "w").close()
                        finally:
                            # ファイルロック解除
                            fcntl.flock(oLockFile.fileno(), fcntl.LOCK_UN)
        finally:
            driver.save_screenshot(self.pic_dir+"/finish_page_"+self.date+".png")
            entime = datetime.datetime.now()
            print "[END] time of {0}".format(entime.strftime("%Y-%m-%d %H:%M:%S"))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        #self.display.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
