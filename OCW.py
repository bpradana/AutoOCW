from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


class AutoOCW:
    def __init__(self, path, email, password, headless=True):
        self.EMAIL = email
        self.PASSWORD = password

        self.tab_matkul = []
        self.tab_dosen = []
        self.tab_presensi = []

        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.geolocation': 1})
        self.driver = webdriver.Chrome(executable_path=path, options=chrome_options)

    def login(self):
        self.driver.get('https://ocw.uns.ac.id/saml/login')
        self.driver.find_element_by_xpath('//body/div[1]/div[3]/form[1]/div[1]/input[1]').send_keys(self.EMAIL)
        self.driver.find_element_by_xpath('//body/div[1]/div[3]/form[1]/div[2]/input[1]').send_keys(self.PASSWORD)
        self.driver.find_element_by_xpath("//button[contains(text(),'Masuk')]").click()

        if self.driver.current_url == 'https://ocw.uns.ac.id/':
            print('Masuk sebagai ' + self.EMAIL)
        else:
            print('Password atau email salah')

    def buka_matkul(self):
        self.driver.get('https://ocw.uns.ac.id/presensi-online-mahasiswa/index')
        main_tab = self.driver.window_handles[0]
        buttons = self.driver.find_elements_by_class_name('btn')

        for button in buttons:
            button.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.RETURN)
            self.tab_matkul.append(self.driver.current_window_handle)
        self.driver.switch_to.window(main_tab)
        self.driver.close()
        self.tab_matkul = self.driver.window_handles

    def buka_dosen(self):
        for tab in self.tab_matkul:
            self.driver.switch_to.window(tab)
            buttons = self.driver.find_elements_by_class_name('btn')
            for button in buttons:
                button.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.RETURN)
                self.driver.switch_to.window(tab)
            self.driver.close()
        self.tab_dosen = self.driver.window_handles

    def buka_jam(self):
        for tab in self.tab_dosen:
            self.driver.switch_to.window(tab)
            latest_status = self.driver.find_element_by_xpath('//body/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/p[4]')
            if latest_status.text == 'Kehadiran Anda: ALPHA':
                self.driver.find_element_by_xpath('//body/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/a[1]').send_keys(Keys.CONTROL + Keys.SHIFT + Keys.RETURN)
            self.driver.refresh()
        self.tab_presensi = [tab for tab in self.driver.window_handles if tab not in self.tab_dosen]

    # TODO: bikin fungsi buat ngecek tab absen tiap 5 menit sebanyak 12 kali
    #       kalo udah 12 kali hapus semua tab presensi, jalanin fungsi buka_jam lagi
    def check(self, refresh=5, check=12, delay=3):
        for i in range(check):
            for tab in self.tab_presensi:
                self.driver.switch_to.window(tab)
                # TODO: bikin code buat ngecek tombol absen ada ga (if), kalo ada klik geolocation + absen, else refresh
                print('Mengecek tab %s' % tab)
                buttons = self.driver.find_elements_by_class_name('btn')
                if buttons:
                    for button in buttons:
                        print('Melakukan presensi')
                        button.click()
                        sleep(delay)
                else:
                    print('Presensi tidak valid' % tab)
                    self.driver.refresh()
            print('Menunggu selama %d menit' % refresh)
            sleep(60 * refresh)
        for tab in self.tab_presensi:
            self.driver.switch_to.window(tab)
            self.driver.close()
        print('Menutup semua tab')
        self.tab_presensi.clear()

    def run(self, refresh=5, check=12, delay=3):
        while True:
            self.buka_jam()
            self.check(refresh, check, delay)
            print('Membuka tab')

    def test(self, tabs):
        for tab in tabs:
            self.driver.switch_to.window(tab)
            sleep(2)