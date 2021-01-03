from OCW import AutoOCW
from GUI import GUIWindow


if __name__ == '__main__':
    # gui = GUIWindow()
    path = 'chromedriver.exe'
    email = 'tiffanybellanagari_9@student.uns.ac.id'
    password = 'Bellaa98'
    headless = False

    ocw = AutoOCW(path, email, password, headless=headless)
    ocw.login()
    ocw.buka_matkul()
    ocw.buka_dosen()
    ocw.run(refresh=5, check=2, delay=3)