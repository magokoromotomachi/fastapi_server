import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "http://127.0.0.1:8000/maps/chiyoda_tokyo_publisher"
URL = 'https://magokoromotomachi.github.io/nishi_saitama_city_kyotaku.html'
URL = 'https://ubukawa.github.io/plib-mlb01/gsi-vector.html'
URL = 'http://127.0.0.1:8000/maps/maplibre.html'
# URL = "https://www.amazon.co.jp/"
# URL = "https://www.google.com/"
# google mapのURLを作成
query = "富士山"
url = f"https://www.google.co.jp/maps/?q={query}"
url += "&t=k"  # 航空写真
url += "&z=15"  # ズームレベル
url += "&hl=ja"  # 日本語
url += "&output=embed"  # 埋め込み用
URL = url

# ------ ChromeDriver のオプション ------
options = Options()
# options.add_argument('--blink-settings=imagesEnabled=false')                    # 画像の非表示
options.add_argument('--disable-blink-features=AutomationControlled')  # navigator.webdriver=false とする設定
options.add_argument('--disable-browser-side-navigation')  # Timed out receiving message from renderer: の修正
options.add_argument('--disable-dev-shm-usage')  # ディスクのメモリスペースを使う
options.add_argument('--disable-extensions')  # すべての拡張機能を無効
options.add_argument('--disable-gpu')                                           # GPUハードウェアアクセラレーションを無効
# options.add_argument('--headless')                                            # ヘッドレスモードで起動
options.add_argument('--ignore-certificate-errors')  # SSL認証(この接続ではプライバシーが保護されません)を無効
options.add_argument('--incognito')  # シークレットモードで起動
options.add_argument('--no-sandbox')  # Chromeの保護機能を無効
# options.add_argument('--start-maximized')                                     # 初期のウィンドウサイズを最大化
options.add_argument('--window-size=1920,1080')  # 初期のウィンドウサイズを指定
options.add_experimental_option("excludeSwitches", ['enable-automation'])  # Chromeは自動テスト ソフトウェア~~ を非表示
options.add_experimental_option("excludeSwitches", ['enable-logging'])  # ERROR:device_event_log_impl.cc~~ などのログ出力を無効化
options.add_experimental_option('useAutomationExtension', False)  # 拡張機能の自動更新を停止
# options.add_argument("--disable-3d-apis")                                       # WebGLのレンダリングを無効化
options.add_argument('--hide-scrollbars')  # スクロールバーを非表示
options.add_argument('--incognito')  # シークレットモードで起動

prefs = {
    'profile.default_content_setting_values.notifications': 2,  # 通知ポップアップを無効
    'credentials_enable_service': False,  # パスワード保存のポップアップを無効
    'profile.password_manager_enabled': False,  # パスワード保存のポップアップを無効
    # 'download.default_directory' : download_dir                               # ダウンロード先のディレクトリを指定
}
options.add_experimental_option('prefs', prefs)

# ブラウザ起動
driver = webdriver.Chrome(options=options)

# 保存する画像ファイル名
file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

# テスト用URLに接続
driver.get(URL)
# 暗黙的に指定時間待つ（秒）
driver.implicitly_wait(300)

# ウインドウサイズをWebサイトに合わせて変更　※全画面用
width = driver.get_window_size().get("width")
height = driver.get_window_size().get("height")
driver.set_window_size(width, height)
print(width, height)

# スクショをPNG形式で保存
driver.save_screenshot(f'./screenshot/{file_name}.png')

driver.quit()
