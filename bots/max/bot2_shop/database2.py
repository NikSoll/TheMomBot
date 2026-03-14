import gspread
import datetime
from google.oauth2.service_account import Credentials
from config2 import SHEET_URL, SHOP_SETTINGS


class ShopDatabase:
    def __init__(self):
        self.sheet = None
        self.connect()

    def connect(self):
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(
                "creds2.json",
                scopes=scopes
            )
            client = gspread.authorize(creds)
            self.sheet = client.open_by_url(SHEET_URL).sheet1
            print("✅ Подключено к Google Sheets")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            self.sheet = None

    def add_order(self, order_data):
        if not self.sheet:
            return False

        try:
            cart_summary = "\n".join([
                f"{item['name']} - {item['price']}₽"
                for item in order_data.get('cart', [])
            ])

            row = [
                order_data.get('created_at', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                order_data.get('user_id', ''),
                order_data.get('username', ''),
                order_data.get('name', ''),
                order_data.get('phone', ''),
                order_data.get('address', ''),
                order_data.get('comment', ''),
                cart_summary,
                order_data.get('total', 0),
                SHOP_SETTINGS.get('currency', '₽'),
                'новый'
            ]
            self.sheet.append_row(row)
            return True
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False

    def get_user_orders(self, user_id):
        if not self.sheet:
            return []
        try:
            records = self.sheet.get_all_records()
            user_orders = []
            for record in records:
                if str(record.get('ID пользователя', '')) == str(user_id):
                    user_orders.append(record)
            return user_orders
        except:
            return []


db = ShopDatabase()