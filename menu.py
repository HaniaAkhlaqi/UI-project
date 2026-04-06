"""
Gasthaus Peking Duck - Restaurant Menu Application
====================================================
A Python/Tkinter MVC restaurant menu system for ordering food and beverages.

Architecture: Model-View-Controller (MVC)
- Model: MenuModel — holds menu data, orders, language, filters
- View: MenuView — all Tkinter UI rendering
- Controller: MenuController — handles user actions, updates model & view

Features:
- Full menu with categories (starters, soups, mains, desserts, beverages)
- Set meals (2-course, 3-course) and Today's Special
- Dietary filters: vegan, vegetarian, gluten-free, lactose-free, non-alcoholic
- Allergen info and country of origin
- Single & group ordering with table management
- Drag & drop to add items to order (with button alternative)
- 3 dynamically changeable languages (English, German, Chinese)
- Call for service button
- Order cost display with optional tipping
- Responsive design for tablet (9") and phone screens

Author: Generated for UI Programming Course Project- Baseline lovable Hi-Fi prototype
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import json
import copy

# =============================================================================
# MODEL — Data layer holding menu items, orders, state
# =============================================================================

class MenuModel:
    """
    The Model in MVC. Stores all menu data, current orders, language preference,
    active filters, and session state. No UI logic here.
    
    Attributes:
        menu_items (list): All menu items with multilingual info
        orders (dict): Table orders keyed by table/person name
        current_language (str): Active language code ('en', 'de', 'zh')
        active_filters (set): Currently active dietary filters
        current_table (str): Active table/person for ordering
        service_called (bool): Whether service has been requested
    """

    def __init__(self):
        """Initialize model with full menu data and default state."""
        self.current_language = 'en'  # Default language
        self.active_filters = set()   # No filters active initially
        self.orders = {"Seat 1": []}   # Default single-seat order
        self.current_table = "Seat 1"
        self.service_called = False
        self.tip_percent = 0
        self._build_menu()
        self._build_translations()
        self._build_set_meals()
        self._build_todays_special()

    def _build_menu(self):
        """
        Build the complete menu with all items across categories.
        Each item is a dict with:
            - id: unique identifier
            - category: menu category key
            - name: dict with 'en', 'de', 'zh' translations
            - description: dict with translations
            - price: float in EUR
            - tags: list of dietary/property tags
            - allergens: list of allergen strings
            - origin: country of origin string
            - contains_alcohol: bool
        """
        self.menu_items = [
            # === STARTERS ===
            {
                "id": "s1", "category": "starters",
                "name": {"en": "Spring Rolls", "de": "Frühlingsrollen", "zh": "春卷"},
                "description": {
                    "en": "Crispy vegetable spring rolls with sweet chili dip",
                    "de": "Knusprige Gemüse-Frühlingsrollen mit süßem Chili-Dip",
                    "zh": "脆皮蔬菜春卷配甜辣酱"
                },
                "price": 7.50, "tags": ["vegan", "vegetarian"],
                "allergens": ["gluten"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "s2", "category": "starters",
                "name": {"en": "Peking Duck Pancakes", "de": "Peking-Ente Pfannkuchen", "zh": "北京烤鸭薄饼"},
                "description": {
                    "en": "Thin pancakes with sliced duck, hoisin sauce, cucumber and scallion",
                    "de": "Dünne Pfannkuchen mit Entenscheiben, Hoisin-Sauce, Gurke und Frühlingszwiebeln",
                    "zh": "薄饼配烤鸭片、海鲜酱、黄瓜和葱"
                },
                "price": 12.90, "tags": [],
                "allergens": ["gluten"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "s3", "category": "starters",
                "name": {"en": "Edamame", "de": "Edamame", "zh": "毛豆"},
                "description": {
                    "en": "Steamed soybeans with sea salt and sesame",
                    "de": "Gedämpfte Sojabohnen mit Meersalz und Sesam",
                    "zh": "蒸毛豆配海盐和芝麻"
                },
                "price": 5.50, "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free"],
                "allergens": [], "origin": "Japan", "contains_alcohol": False
            },
            {
                "id": "s4", "category": "starters",
                "name": {"en": "Wonton Dumplings", "de": "Wonton-Teigtaschen", "zh": "馄饨"},
                "description": {
                    "en": "Handmade pork and shrimp wontons in ginger broth",
                    "de": "Handgemachte Schweine- und Garnelen-Wontons in Ingwerbrühe",
                    "zh": "手工猪肉虾仁馄饨配姜汤"
                },
                "price": 8.90, "tags": [],
                "allergens": ["gluten", "shellfish"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "s5", "category": "starters",
                "name": {"en": "Bavarian Pretzel Bites", "de": "Bayerische Brezel-Happen", "zh": "巴伐利亚椒盐脆饼"},
                "description": {
                    "en": "Warm pretzel bites with obatzda cheese dip",
                    "de": "Warme Brezel-Happen mit Obatzda-Käsedip",
                    "zh": "温热椒盐脆饼配奶酪蘸酱"
                },
                "price": 6.90, "tags": ["vegetarian"],
                "allergens": ["gluten", "lactose"], "origin": "Germany", "contains_alcohol": False
            },
            # === SOUPS / LIGHT COURSES ===
            {
                "id": "l1", "category": "soups",
                "name": {"en": "Hot & Sour Soup", "de": "Scharf-Saure Suppe", "zh": "酸辣汤"},
                "description": {
                    "en": "Classic Sichuan soup with tofu, mushrooms and bamboo shoots",
                    "de": "Klassische Sichuan-Suppe mit Tofu, Pilzen und Bambussprossen",
                    "zh": "经典四川酸辣汤配豆腐、蘑菇和竹笋"
                },
                "price": 6.90, "tags": ["vegan", "vegetarian", "lactose-free"],
                "allergens": ["soy"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "l2", "category": "soups",
                "name": {"en": "Wonton Soup", "de": "Wonton-Suppe", "zh": "馄饨汤"},
                "description": {
                    "en": "Light chicken broth with handmade pork wontons",
                    "de": "Leichte Hühnerbrühe mit handgemachten Schweine-Wontons",
                    "zh": "清汤手工猪肉馄饨"
                },
                "price": 7.50, "tags": ["lactose-free"],
                "allergens": ["gluten"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "l3", "category": "soups",
                "name": {"en": "Kartoffelsuppe", "de": "Kartoffelsuppe", "zh": "德式土豆汤"},
                "description": {
                    "en": "Creamy German potato soup with croutons and chives",
                    "de": "Cremige deutsche Kartoffelsuppe mit Croutons und Schnittlauch",
                    "zh": "奶油德式土豆汤配面包丁和细香葱"
                },
                "price": 6.50, "tags": ["vegetarian", "gluten-free"],
                "allergens": ["lactose"], "origin": "Germany", "contains_alcohol": False
            },
            {
                "id": "l4", "category": "soups",
                "name": {"en": "Miso Soup", "de": "Miso-Suppe", "zh": "味噌汤"},
                "description": {
                    "en": "Traditional miso with wakame seaweed and silken tofu",
                    "de": "Traditionelle Miso-Suppe mit Wakame-Algen und Seidentofu",
                    "zh": "传统味噌汤配裙带菜和嫩豆腐"
                },
                "price": 5.90, "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free"],
                "allergens": ["soy"], "origin": "Japan", "contains_alcohol": False
            },
            # === MAIN COURSES ===
            {
                "id": "m1", "category": "mains",
                "name": {"en": "Peking Duck (Half)", "de": "Peking-Ente (Halbe)", "zh": "北京烤鸭（半只）"},
                "description": {
                    "en": "Our signature — crispy-skinned roast duck served with pancakes, hoisin, cucumber and scallion",
                    "de": "Unser Signature-Gericht — knusprige Ente mit Pfannkuchen, Hoisin, Gurke und Frühlingszwiebeln",
                    "zh": "招牌菜 — 脆皮烤鸭配薄饼、海鲜酱、黄瓜和葱"
                },
                "price": 28.90, "tags": [],
                "allergens": ["gluten"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "m2", "category": "mains",
                "name": {"en": "Kung Pao Chicken", "de": "Kung-Pao-Hühnchen", "zh": "宫保鸡丁"},
                "description": {
                    "en": "Spicy diced chicken with peanuts, chili and Sichuan pepper",
                    "de": "Scharfes Hühnchen mit Erdnüssen, Chili und Sichuan-Pfeffer",
                    "zh": "辣味鸡丁配花生、辣椒和花椒"
                },
                "price": 16.90, "tags": ["gluten-free", "lactose-free"],
                "allergens": ["peanuts"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "m3", "category": "mains",
                "name": {"en": "Mapo Tofu", "de": "Mapo Tofu", "zh": "麻婆豆腐"},
                "description": {
                    "en": "Silken tofu in spicy fermented bean sauce with minced pork",
                    "de": "Seidentofu in scharfer fermentierter Bohnensauce mit Schweinehack",
                    "zh": "麻辣豆腐配猪肉末"
                },
                "price": 14.90, "tags": ["gluten-free", "lactose-free"],
                "allergens": ["soy"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "m4", "category": "mains",
                "name": {"en": "Mapo Tofu (Vegan)", "de": "Mapo Tofu (Vegan)", "zh": "麻婆豆腐（素食）"},
                "description": {
                    "en": "Silken tofu in spicy fermented bean sauce — plant-based version",
                    "de": "Seidentofu in scharfer fermentierter Bohnensauce — pflanzliche Version",
                    "zh": "麻辣豆腐 — 纯素版"
                },
                "price": 13.90, "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free"],
                "allergens": ["soy"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "m5", "category": "mains",
                "name": {"en": "Schweinshaxe", "de": "Schweinshaxe", "zh": "德式烤猪肘"},
                "description": {
                    "en": "Crispy Bavarian pork knuckle with sauerkraut and potato dumpling",
                    "de": "Knusprige bayerische Schweinshaxe mit Sauerkraut und Kartoffelknödel",
                    "zh": "脆皮巴伐利亚烤猪肘配酸菜和土豆丸子"
                },
                "price": 22.90, "tags": ["lactose-free"],
                "allergens": ["gluten"], "origin": "Germany", "contains_alcohol": False
            },
            {
                "id": "m6", "category": "mains",
                "name": {"en": "Coq au Vin", "de": "Coq au Vin", "zh": "红酒炖鸡"},
                "description": {
                    "en": "Braised chicken in red wine sauce with mushrooms and pearl onions (contains alcohol)",
                    "de": "Geschmortes Hühnchen in Rotweinsauce mit Pilzen und Perlzwiebeln (enthält Alkohol)",
                    "zh": "红酒炖鸡配蘑菇和珍珠洋葱（含酒精）"
                },
                "price": 19.90, "tags": ["gluten-free", "lactose-free"],
                "allergens": ["onion"], "origin": "France", "contains_alcohol": True
            },
            {
                "id": "m7", "category": "mains",
                "name": {"en": "Char Siu Pork", "de": "Char Siu Schwein", "zh": "叉烧"},
                "description": {
                    "en": "Cantonese BBQ pork with honey glaze, served with steamed rice",
                    "de": "Kantonesisches BBQ-Schwein mit Honigglasur, serviert mit Dampfreis",
                    "zh": "蜜汁叉烧配蒸米饭"
                },
                "price": 17.50, "tags": ["lactose-free"],
                "allergens": ["soy"], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "m8", "category": "mains",
                "name": {"en": "Veggie Stir-Fry", "de": "Gemüsepfanne", "zh": "素炒时蔬"},
                "description": {
                    "en": "Seasonal vegetables wok-fried with garlic and ginger, served with jasmine rice",
                    "de": "Saisonales Gemüse im Wok mit Knoblauch und Ingwer, serviert mit Jasminreis",
                    "zh": "时令蔬菜配蒜姜炒制，配茉莉香米"
                },
                "price": 13.50, "tags": ["vegan", "vegetarian", "lactose-free"],
                "allergens": ["soy"], "origin": "China", "contains_alcohol": False
            },
            # === DESSERTS ===
            {
                "id": "d1", "category": "desserts",
                "name": {"en": "Kladdkaka", "de": "Schwedischer Schokoladenkuchen", "zh": "瑞典黏巧克力蛋糕"},
                "description": {
                    "en": "Sticky Swedish chocolate cake served with green tea ice cream",
                    "de": "Klebriger schwedischer Schokoladenkuchen mit Grüntee-Eis",
                    "zh": "瑞典黏巧克力蛋糕配抹茶冰淇淋"
                },
                "price": 7.50, "tags": ["vegetarian"],
                "allergens": ["gluten", "lactose", "egg"], "origin": "Sweden", "contains_alcohol": False
            },
            {
                "id": "d2", "category": "desserts",
                "name": {"en": "Äppelkaka (Vegan)", "de": "Veganer Apfelkuchen", "zh": "纯素苹果蛋糕"},
                "description": {
                    "en": "Vegan apple cake with cinnamon and light ginger sauce",
                    "de": "Veganer Apfelkuchen mit Zimt und Ingwersauce",
                    "zh": "纯素苹果蛋糕配肉桂和姜汁"
                },
                "price": 6.90, "tags": ["vegan", "lactose-free"],
                "allergens": ["gluten"], "origin": "Sweden", "contains_alcohol": False
            },
            {
                "id": "d3", "category": "desserts",
                "name": {"en": "Kanelbullar (Gluten-Free)", "de": "Glutenfreie Zimtschnecken", "zh": "无麸质肉桂卷"},
                "description": {
                    "en": "Gluten-free cinnamon bun with black sesame filling",
                    "de": "Glutenfreie Zimtschnecke mit schwarzer Sesamfüllung",
                    "zh": "无麸质肉桂卷配黑芝麻馅"
                },
                "price": 5.90, "tags": ["vegetarian", "gluten-free"],
                "allergens": ["lactose"], "origin": "Sweden", "contains_alcohol": False
            },
            {
                "id": "d4", "category": "desserts",
                "name": {"en": "Prinsesstårta", "de": "Prinzessinnentorte", "zh": "公主蛋糕"},
                "description": {
                    "en": "Layered sponge cake with mango cream and marzipan",
                    "de": "Schichtkuchen mit Mangocreme und Marzipan",
                    "zh": "夹层蛋糕配芒果奶油和杏仁糖皮"
                },
                "price": 8.90, "tags": ["vegetarian"],
                "allergens": ["gluten", "lactose", "egg", "nuts"], "origin": "Sweden", "contains_alcohol": False
            },
            {
                "id": "d5", "category": "desserts",
                "name": {"en": "Havreflarn (Vegan)", "de": "Vegane Haferkekse", "zh": "纯素燕麦薄脆饼"},
                "description": {
                    "en": "Vegan oat crisps dipped in dark chocolate with chili",
                    "de": "Vegane Haferkekse mit dunkler Schokolade und Chili",
                    "zh": "纯素燕麦脆饼配黑巧克力和微辣味"
                },
                "price": 4.90, "tags": ["vegan", "lactose-free"],
                "allergens": ["gluten"], "origin": "Sweden", "contains_alcohol": False
            },
            {
                "id": "d6", "category": "desserts",
                "name": {"en": "Swedish Pancakes (Lactose-Free)", "de": "Laktosefreie Pfannkuchen", "zh": "无乳糖瑞典薄煎饼"},
                "description": {
                    "en": "Thin pancakes with red bean paste and lactose-free cream",
                    "de": "Pfannkuchen mit roter Bohnenpaste und laktosefreier Creme",
                    "zh": "薄煎饼配红豆沙和无乳糖奶油"
                },
                "price": 6.50, "tags": ["vegetarian", "lactose-free"],
                "allergens": ["gluten", "egg"], "origin": "Sweden", "contains_alcohol": False
            },
            {
                "id": "d7", "category": "desserts",
                "name": {"en": "Berry Sorbet", "de": "Beerensorbet", "zh": "浆果雪葩"},
                "description": {
                    "en": "Refreshing berry sorbet with lychee and mint",
                    "de": "Erfrischendes Beerensorbet mit Litschi und Minze",
                    "zh": "清爽浆果雪葩配荔枝和薄荷"
                },
                "price": 5.50, "tags": ["vegan", "gluten-free", "lactose-free"],
                "allergens": [], "origin": "Sweden", "contains_alcohol": False
            },
            # === BEVERAGES ===
            {
                "id": "b1", "category": "beverages",
                "name": {"en": "Jasmine Tea", "de": "Jasmintee", "zh": "茉莉花茶"},
                "description": {
                    "en": "Fragrant Chinese jasmine green tea (pot)",
                    "de": "Duftender chinesischer Jasmin-Grüntee (Kanne)",
                    "zh": "芬芳茉莉花绿茶（壶）"
                },
                "price": 4.50, "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free", "non-alcoholic"],
                "allergens": [], "origin": "China", "contains_alcohol": False
            },
            {
                "id": "b2", "category": "beverages",
                "name": {"en": "Tsingtao Beer", "de": "Tsingtao Bier", "zh": "青岛啤酒"},
                "description": {
                    "en": "Classic Chinese lager (330ml)",
                    "de": "Klassisches chinesisches Lagerbier (330ml)",
                    "zh": "经典中国拉格啤酒（330毫升）"
                },
                "price": 5.50, "tags": ["vegan", "vegetarian", "lactose-free"],
                "allergens": ["gluten"], "origin": "China", "contains_alcohol": True
            },
            {
                "id": "b3", "category": "beverages",
                "name": {"en": "Weißbier", "de": "Weißbier", "zh": "小麦啤酒"},
                "description": {
                    "en": "Bavarian wheat beer (500ml)",
                    "de": "Bayerisches Weißbier (500ml)",
                    "zh": "巴伐利亚小麦啤酒（500毫升）"
                },
                "price": 6.50, "tags": ["vegetarian", "lactose-free"],
                "allergens": ["gluten"], "origin": "Germany", "contains_alcohol": True
            },
            {
                "id": "b4", "category": "beverages",
                "name": {"en": "Sparkling Water", "de": "Sprudel", "zh": "气泡水"},
                "description": {
                    "en": "Chilled sparkling mineral water (500ml)",
                    "de": "Gekühltes Sprudelwasser (500ml)",
                    "zh": "冰镇气泡矿泉水（500毫升）"
                },
                "price": 3.50, "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free", "non-alcoholic"],
                "allergens": [], "origin": "Germany", "contains_alcohol": False
            },
            {
                "id": "b5", "category": "beverages",
                "name": {"en": "Lychee Lemonade", "de": "Litschi-Limonade", "zh": "荔枝柠檬水"},
                "description": {
                    "en": "House-made lychee and lime lemonade",
                    "de": "Hausgemachte Litschi-Limetten-Limonade",
                    "zh": "自制荔枝青柠柠檬水"
                },
                "price": 5.90, "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free", "non-alcoholic"],
                "allergens": [], "origin": "House", "contains_alcohol": False
            },
            {
                "id": "b6", "category": "beverages",
                "name": {"en": "Riesling (Glass)", "de": "Riesling (Glas)", "zh": "雷司令（杯）"},
                "description": {
                    "en": "Dry German Riesling white wine (150ml)",
                    "de": "Trockener deutscher Riesling Weißwein (150ml)",
                    "zh": "干型德国雷司令白葡萄酒（150毫升）"
                },
                "price": 7.90, "tags": ["vegetarian", "gluten-free", "lactose-free"],
                "allergens": [], "origin": "Germany", "contains_alcohol": True
            },
            {
                "id": "b7", "category": "beverages",
                "name": {"en": "Plum Wine", "de": "Pflaumenwein", "zh": "梅酒"},
                "description": {
                    "en": "Sweet Japanese plum wine (100ml)",
                    "de": "Süßer japanischer Pflaumenwein (100ml)",
                    "zh": "甜日本梅酒（100毫升）"
                },
                "price": 6.90, "tags": ["vegetarian", "gluten-free", "lactose-free"],
                "allergens": [], "origin": "Japan", "contains_alcohol": True
            },
            {
                "id": "b8", "category": "beverages",
                "name": {"en": "Coca-Cola", "de": "Coca-Cola", "zh": "可口可乐"},
                "description": {
                    "en": "Coca-Cola (330ml)",
                    "de": "Coca-Cola (330ml)",
                    "zh": "可口可乐（330毫升）"
                },
                "price": 3.90, "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free", "non-alcoholic"],
                "allergens": [], "origin": "USA", "contains_alcohol": False
            },
        ]

    def _build_set_meals(self):
        """
        Build pre-configured set meal options.
        Each set meal has a name (translated), included courses, and a discounted price.
        """
        self.set_meals = [
            {
                "id": "set2a", "category": "set_meals",
                "name": {"en": "Lotus Set", "de": "Lotus-Menü", "zh": "莲花套餐"},
                "description": {
                    "en": "Spring Rolls + Veggie Stir-Fry + Berry Sorbet + Jasmine Tea",
                    "de": "Frühlingsrollen + Gemüsepfanne + Beerensorbet + Jasmintee",
                    "zh": "春卷 + 素菜炒时蔬 + 浆果雪葩 + 茉莉花茶"
                },
                "price": 23.90,
                "tags": ["vegan", "vegetarian", "lactose-free", "non-alcoholic"],
                "allergens": ["gluten", "soy"],
                "origin": "Fusion",
                "contains_alcohol": False
            },
            {
                "id": "set2b", "category": "set_meals",
                "name": {"en": "Bamboo Set", "de": "Bambus-Menü", "zh": "竹套餐"},
                "description": {
                    "en": "Edamame + Kung Pao Chicken + Berry Sorbet + Sparkling Water",
                    "de": "Edamame + Kung-Pao-Hühnchen + Beerensorbet + Sprudel",
                    "zh": "毛豆 + 宫保鸡丁 + 浆果雪葩 + 气泡水"
                },
                "price": 25.90,
                "tags": ["gluten-free", "lactose-free", "non-alcoholic"],
                "allergens": ["peanuts"],
                "origin": "Fusion",
                "contains_alcohol": False
            },
            {
                "id": "set2c", "category": "set_meals",
                "name": {"en": "Golden Duck Set", "de": "Goldenes-Enten-Menü", "zh": "金鸭套餐"},
                "description": {
                    "en": "Peking Duck Pancakes + Peking Duck (Half) + Kladdkaka + Jasmine Tea",
                    "de": "Peking-Ente Pfannkuchen + Peking-Ente (Halbe) + Schwedischer Schokoladenkuchen + Jasmintee",
                    "zh": "北京烤鸭薄饼 + 半只北京烤鸭 + 瑞典黏巧克力蛋糕 + 茉莉花茶"
                },
                "price": 39.90,
                "tags": ["non-alcoholic"],
                "allergens": ["gluten", "lactose", "egg"],
                "origin": "Fusion",
                "contains_alcohol": False
            },
            {
                "id": "set3b", "category": "set_meals",
                "name": {"en": "Jade Vegan Set", "de": "Jade Veganes Menü", "zh": "翡翠纯素套餐"},
                "description": {
                    "en": "Edamame + Miso Soup + Mapo Tofu (Vegan) + Berry Sorbet + Lychee Lemonade",
                    "de": "Edamame + Miso-Suppe + Mapo Tofu (Vegan) + Beerensorbet + Litschi-Limonade",
                    "zh": "毛豆 + 味噌汤 + 素麻婆豆腐 + 浆果雪葩 + 荔枝柠檬水"
                },
                "price": 28.90,
                "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free", "non-alcoholic"],
                "allergens": ["soy"],
                "origin": "Fusion",
                "contains_alcohol": False
            },
            {
                "id": "set3c", "category": "set_meals",
                "name": {"en": "Spicy Sichuan Set", "de": "Scharfes Sichuan-Menü", "zh": "川味香辣套餐"},
                "description": {
                    "en": "Hot & Sour Soup + Kung Pao Chicken + Berry Sorbet + Jasmine Tea",
                    "de": "Scharf-Saure Suppe + Kung-Pao-Hühnchen + Beerensorbet + Jasmintee",
                    "zh": "酸辣汤 + 宫保鸡丁 + 浆果雪葩 + 茉莉花茶"
                },
                "price": 26.90,
                "tags": ["lactose-free"],
                "allergens": ["soy", "peanuts"],
                "origin": "China",
                "contains_alcohol": False
            },
            {
                "id": "set3d", "category": "set_meals",
                "name": {"en": "Imperial Duck Set", "de": "Imperiales Enten-Menü", "zh": "御品烤鸭套餐"},
                "description": {
                    "en": "Peking Duck Pancakes + Peking Duck (Half) + Kladdkaka + Jasmine Tea",
                    "de": "Peking-Ente Pfannkuchen + Peking-Ente (Halbe) + Schwedischer Schokoladenkuchen + Jasmintee",
                    "zh": "北京烤鸭薄饼 + 半只北京烤鸭 + 瑞典黏巧克力蛋糕 + 茉莉花茶"
                },
                "price": 39.90,
                "tags": ["vegan", "vegetarian", "gluten-free", "lactose-free", "non-alcoholic"],
                "allergens": ["gluten", "lactose", "egg"],
                "origin": "Fusion",
                "contains_alcohol": False
            },
            {
                "id": "set3e", "category": "set_meals",
                "name": {"en": "Bavarian Fusion Set", "de": "Bayerisches Fusions-Menü", "zh": "巴伐利亚融合套餐"},
                "description": {
                    "en": "Bavarian Pretzel Bites + Schweinshaxe + Swedish Pancakes (Lactose-Free) + Sparkling Water",
                    "de": "Bayerische Brezel-Happen + Schweinshaxe + Laktosefreie Pfannkuchen + Sprudel",
                    "zh": "巴伐利亚椒盐脆饼 + 德式烤猪肘 + 无乳糖瑞典薄煎饼 + 气泡水"
                },
                "price": 31.90,
                "tags": ["vegetarian", "lactose-free", "vegan", "non-alcoholic"],
                "allergens": ["gluten", "lactose", "egg"],
                "origin": "Germany",
                "contains_alcohol": False
            },
        ]

    def _build_todays_special(self):
        """Build today's special offer — a highlighted item with extra discount."""
        self.todays_special = {
            "id": "ts1", "category": "todays_special",
            "name": {
                "en": "🌟 Peking Duck Feast for Two",
                "de": "🌟 Peking-Enten-Festmahl für Zwei",
                "zh": "🌟 双人北京烤鸭盛宴"
            },
            "description": {
                "en": "Whole Peking Duck with pancakes, 2 soups of choice, 2 desserts of choice, and a pot of jasmine tea. Perfect for sharing!",
                "de": "Ganze Peking-Ente mit Pfannkuchen, 2 Suppen nach Wahl, 2 Desserts nach Wahl und einer Kanne Jasmintee. Perfekt zum Teilen!",
                "zh": "整只北京烤鸭配薄饼、2份自选汤、2份自选甜点和一壶茉莉花茶。完美分享！"
            },
            "price": 58.90, "tags": [],
            "allergens": ["gluten"], "origin": "China", "contains_alcohol": False
        }

    def _build_translations(self):
        """
        UI string translations for all three supported languages.
        Keys are used throughout the View for labels, buttons, messages.
        """
        self.translations = {
            "en": {
                "app_title": "Gasthaus Peking Duck",
                "app_subtitle": "German-Chinese Fusion Cuisine",
                "starters": "Starters", "soups": "Soups & Light Courses",
                "mains": "Main Courses", "desserts": "Desserts",
                "beverages": "Beverages", "set_meals": "Set Meals",
                "todays_special": "Today's Special",
                "your_order": "Your Order", "total": "Total",
                "add_to_order": "Add to Order", "remove": "Remove",
                "call_service": "🔔 Call Service", "service_called": "✅ Service Called!",
                "cancel_service": "Cancel Service Call",
                "place_order": "Place Order", "clear_order": "Clear Order",
                "filter": "Filter", "vegan": "Vegan", "vegetarian": "Vegetarian",
                "gluten-free": "Gluten-Free", "lactose-free": "Lactose-Free",
                "non-alcoholic": "Non-Alcoholic",
                "allergens": "Allergens", "origin": "Origin",
                "no_items": "No items match your filters",
                "tip": "Tip", "no_tip": "No Tip",
                "subtotal": "Subtotal", "with_tip": "With Tip",
                "order_placed": "Order Placed!",
                "order_placed_msg": "Your order has been sent to the kitchen. Thank you!",
                "order_empty": "Your order is empty",
                "group_order": "Group Order", "single_order": "Single Order",
                "people": "People", "pay_all": "Pay All", "split_bill": "Split Bill",
                "payment_successful": "Payment Successful",
                "each_paid": "Each of the {count} people paid {amount} {currency}.",
                "paid_total": "Total paid {amount} {currency}.",
                "each_pays_their_own": "Each pays their own total:\n{details}",
                "table": "Table", "contains_alcohol": "⚠️ Contains Alcohol",
                "qty": "Qty", "price": "Price", "item": "Item",
                "drag_hint": "Drag items to your order, or use the + button",
                "language": "Language", "menu": "Menu",
                "clear_confirm": "Clear entire order?",
                "clear_confirm_msg": "This will remove all items from the order.",
                "person_exists": "This person already exists in the order.",
                "enter_name": "Please enter a name.",
            },
            "de": {
                "app_title": "Gasthaus Peking Duck",
                "app_subtitle": "Deutsch-Chinesische Fusionsküche",
                "starters": "Vorspeisen", "soups": "Suppen & Leichte Gerichte",
                "mains": "Hauptgerichte", "desserts": "Nachspeisen",
                "beverages": "Getränke", "set_meals": "Menüs",
                "todays_special": "Tagesangebot",
                "your_order": "Ihre Bestellung", "total": "Gesamt",
                "add_to_order": "Bestellen", "remove": "Entfernen",
                "call_service": "🔔 Bedienung rufen", "service_called": "✅ Bedienung gerufen!",
                "cancel_service": "Ruf abbrechen",
                "place_order": "Bestellung aufgeben", "clear_order": "Bestellung löschen",
                "filter": "Filter", "vegan": "Vegan", "vegetarian": "Vegetarisch",
                "gluten-free": "Glutenfrei", "lactose-free": "Laktosefrei",
                "non-alcoholic": "Alkoholfrei",
                "allergens": "Allergene", "origin": "Herkunft",
                "no_items": "Keine Artikel entsprechen Ihren Filtern",
                "tip": "Trinkgeld", "no_tip": "Kein Trinkgeld",
                "subtotal": "Zwischensumme", "with_tip": "Mit Trinkgeld",
                "order_placed": "Bestellung aufgegeben!",
                "order_placed_msg": "Ihre Bestellung wurde an die Küche gesendet. Vielen Dank!",
                "order_empty": "Ihre Bestellung ist leer",
                "group_order": "Gruppenbestellung", "single_order": "Einzelbestellung",
                "people": "Personen", "pay_all": "Alles bezahlen", "split_bill": "Rechnung teilen",
                "payment_successful": "Zahlung erfolgreich",
                "each_paid": "Jeder der {count} Personen zahlte {amount} {currency}.",
                "paid_total": "Insgesamt bezahlt {amount} {currency}.",
                "each_pays_their_own": "Jeder zahlt seinen eigenen Betrag:\n{details}",
                "table": "Tisch", "contains_alcohol": "⚠️ Enthält Alkohol",
                "qty": "Anz.", "price": "Preis", "item": "Artikel",
                "drag_hint": "Ziehen Sie Artikel in Ihre Bestellung oder verwenden Sie den + Button",
                "language": "Sprache", "menu": "Menü",
                "clear_confirm": "Gesamte Bestellung löschen?",
                "clear_confirm_msg": "Dies entfernt alle Artikel aus der Bestellung.",
                "person_exists": "Diese Person existiert bereits in der Bestellung.",
                "enter_name": "Bitte geben Sie einen Namen ein.",
            },
            "zh": {
                "app_title": "北京烤鸭餐馆",
                "app_subtitle": "德中融合料理",
                "starters": "前菜", "soups": "汤品与轻食",
                "mains": "主菜", "desserts": "甜点",
                "beverages": "饮品", "set_meals": "套餐",
                "todays_special": "今日特惠",
                "your_order": "您的订单", "total": "合计",
                "add_to_order": "加入订单", "remove": "删除",
                "call_service": "🔔 呼叫服务", "service_called": "✅ 已呼叫服务！",
                "cancel_service": "取消呼叫",
                "place_order": "提交订单", "clear_order": "清空订单",
                "filter": "筛选", "vegan": "纯素", "vegetarian": "素食",
                "gluten-free": "无麸质", "lactose-free": "无乳糖",
                "non-alcoholic": "无酒精",
                "allergens": "过敏原", "origin": "产地",
                "no_items": "没有符合筛选条件的菜品",
                "tip": "小费", "no_tip": "不加小费",
                "subtotal": "小计", "with_tip": "含小费",
                "order_placed": "订单已提交！",
                "order_placed_msg": "您的订单已发送至厨房。谢谢！",
                "order_empty": "您的订单为空",
                "group_order": "团体点单", "single_order": "单人点单",
                "people": "人数", "pay_all": "全部支付", "split_bill": "分摊账单",
                "payment_successful": "支付成功",
                "each_paid": "每位{count}人支付了{amount}{currency}。",
                "paid_total": "总计支付{amount}{currency}。",
                "each_pays_their_own": "每人支付自己的账单：\n{details}",
                "table": "餐桌", "contains_alcohol": "⚠️ 含酒精",
                "qty": "数量", "price": "价格", "item": "菜品",
                "drag_hint": "拖拽菜品至订单，或使用 + 按钮",
                "language": "语言", "menu": "菜单",
                "clear_confirm": "清空全部订单？",
                "clear_confirm_msg": "这将删除订单中的所有菜品。",
                "person_exists": "此成员已存在于订单中。",
                "enter_name": "请输入姓名。",
            },
        }

    def t(self, key):
        """
        Translate a UI string key to the current language.
        
        Args:
            key (str): Translation key from self.translations
            
        Returns:
            str: Translated string, or the key itself if not found
        """
        return self.translations.get(self.current_language, {}).get(key, key)

    def get_filtered_items(self, category):
        """
        Get menu items for a category, filtered by active dietary filters.
        
        Args:
            category (str): Category key (e.g., 'starters', 'mains')
            
        Returns:
            list: Filtered menu items matching all active filters
        """
        items = [i for i in self.menu_items if i["category"] == category]
        if self.active_filters:
            items = [i for i in items if self.active_filters.issubset(set(i["tags"]))]
        return items

    def add_to_order(self, item, person=None):
        """
        Add a menu item to the current order.
        If the item already exists for this person/table, increment quantity.
        
        Args:
            item (dict): Menu item dict to add
            person (str, optional): Person name for group orders. Uses current_table if None.
        """
        target = person or self.current_table
        if target not in self.orders:
            self.orders[target] = []
        # Check if item already in order — increment qty
        for order_item in self.orders[target]:
            if order_item["id"] == item["id"]:
                order_item["qty"] += 1
                return
        # New item
        entry = copy.deepcopy(item)
        entry["qty"] = 1
        self.orders[target].append(entry)

    def remove_from_order(self, item_id, person=None):
        """
        Remove one quantity of an item from the order. Removes entirely if qty reaches 0.
        
        Args:
            item_id (str): The item's unique ID
            person (str, optional): Person name. Uses current_table if None.
        """
        target = person or self.current_table
        if target not in self.orders:
            return
        for i, order_item in enumerate(self.orders[target]):
            if order_item["id"] == item_id:
                order_item["qty"] -= 1
                if order_item["qty"] <= 0:
                    self.orders[target].pop(i)
                return

    def get_order_total(self, person=None):
        """
        Calculate total cost for a person or the whole table.
        
        Args:
            person (str, optional): Specific person. If None, totals all persons.
            
        Returns:
            float: Total order cost
        """
        if person:
            return sum(i["price"] * i["qty"] for i in self.orders.get(person, []))
        return sum(
            sum(i["price"] * i["qty"] for i in items)
            for items in self.orders.values()
        )

    def get_order_total_with_tip(self):
        """
        Calculate total with tip applied.
        
        Returns:
            float: Total including tip percentage
        """
        total = self.get_order_total()
        return total * (1 + self.tip_percent / 100)

    def clear_order(self, person=None):
        """
        Clear order items for a person or the whole table.
        
        Args:
            person (str, optional): Specific person to clear. If None, clears all.
        """
        if person:
            self.orders[person] = []
        else:
            for key in self.orders:
                self.orders[key] = []

    def add_person(self, name):
        """
        Add a new person to the group order.
        
        Args:
            name (str): Person's name
            
        Returns:
            bool: True if added, False if name already exists
        """
        if name in self.orders:
            return False
        self.orders[name] = []
        return True

    def remove_person(self, name):
        """
        Remove a person from the group order.
        
        Args:
            name (str): Person's name to remove
        """
        if name in self.orders and name != "Seat 1":
            del self.orders[name]
            if self.current_table == name:
                self.current_table = list(self.orders.keys())[0]

    def get_people_count(self):
        """
        Return the current number of seats/people in the order.
        """
        return len(self.orders)

    def get_next_seat_name(self):
        """
        Generate the next available seat name.
        """
        idx = 1
        while f"Seat {idx}" in self.orders:
            idx += 1
        return f"Seat {idx}"

    def add_seat(self):
        """
        Add a new seat to the group order and switch to it.
        """
        name = self.get_next_seat_name()
        self.orders[name] = []
        self.current_table = name

    def remove_last_seat(self):
        """
        Remove the last seat from the group order if more than one exists.
        """
        if len(self.orders) <= 1:
            return
        seat_names = sorted(
            self.orders.keys(),
            key=lambda name: int(name.split()[-1]) if name.split()[-1].isdigit() else float('inf')
        )
        last = seat_names[-1]
        del self.orders[last]
        if self.current_table == last:
            self.current_table = seat_names[0]


# =============================================================================
# CONTROLLER — Mediates between Model and View
# =============================================================================

class MenuController:
    """
    The Controller in MVC. Handles user actions, updates the Model,
    and triggers View refreshes. All business logic passes through here.
    
    Attributes:
        model (MenuModel): The data model
        view (MenuView): The view (set after view initialization)
    """

    def __init__(self, model):
        """
        Initialize controller with a model reference.
        
        Args:
            model (MenuModel): The data model instance
        """
        self.model = model
        self.view = None  # Set by view after construction

    def set_view(self, view):
        """
        Connect the view to this controller.
        
        Args:
            view (MenuView): The view instance
        """
        self.view = view

    def change_language(self, lang):
        """
        Switch the interface language and refresh the entire view.
        
        Args:
            lang (str): Language code ('en', 'de', 'zh')
        """
        self.model.current_language = lang
        self.view.refresh_all()

    def toggle_filter(self, filter_tag):
        """
        Toggle a dietary filter on/off and refresh the menu display.
        
        Args:
            filter_tag (str): Filter tag to toggle (e.g., 'vegan', 'gluten-free')
        """
        if filter_tag in self.model.active_filters:
            self.model.active_filters.remove(filter_tag)
        else:
            self.model.active_filters.add(filter_tag)
        self.view.refresh_menu()

    def add_item(self, item):
        """
        Add a menu item to the current person's order and refresh order display.
        
        Args:
            item (dict): Menu item to add
        """
        self.model.add_to_order(item, self.model.current_table)
        self.view.refresh_order()

    def remove_item(self, item_id):
        """
        Remove one quantity of an item from the order and refresh.
        
        Args:
            item_id (str): Item ID to remove
        """
        self.model.remove_from_order(item_id, self.model.current_table)
        self.view.refresh_order()

    def call_service(self):
        """Toggle service call status and refresh the service button."""
        self.model.service_called = not self.model.service_called
        self.view.refresh_service_button()

    def set_tip(self, percent):
        """
        Set the tip percentage and refresh the order total display.
        
        Args:
            percent (int): Tip percentage (0, 5, 10, 15, 20)
        """
        self.model.tip_percent = percent
        self.view.refresh_order()

    def pay_all(self):
        """
        Pay the full order amount for all seats.
        """
        total = self.model.get_order_total_with_tip()
        if total == 0:
            messagebox.showwarning(
                self.model.t("your_order"),
                self.model.t("order_empty")
            )
            return
        messagebox.showinfo(
            self.model.t("payment_successful"),
            self.model.t("paid_total").format(
                amount=f"{total:.2f}", currency="SEK"
            )
        )
        self.model.clear_order()
        self.view.refresh_order()

    def split_bill(self):
        """
        Split the bill so each person pays for their own order.
        """
        total = self.model.get_order_total()
        person_count = self.model.get_people_count()
        if total == 0:
            messagebox.showwarning(
                self.model.t("your_order"),
                self.model.t("order_empty")
            )
            return
        if person_count <= 1:
            messagebox.showinfo(
                self.model.t("payment_successful"),
                self.model.t("paid_total").format(
                    amount=f"{self.model.get_order_total_with_tip():.2f}", currency="SEK"
                )
            )
        else:
            details = []
            for person in self.model.orders:
                person_total = self.model.get_order_total(person)
                person_total_with_tip = person_total * (1 + self.model.tip_percent / 100)
                details.append(f"{person}: €{person_total_with_tip:.2f}")

            messagebox.showinfo(
                self.model.t("payment_successful"),
                self.model.t("each_pays_their_own").format(
                    details="\n".join(details)
                )
            )
        self.model.clear_order()
        self.view.refresh_order()

    def clear_order(self):
        """Clear the entire order after user confirmation."""
        if messagebox.askyesno(
            self.model.t("clear_confirm"),
            self.model.t("clear_confirm_msg")
        ):
            self.model.clear_order()
            self.view.refresh_order()

    def increment_people(self):
        """Add a new seat/person to the group order."""
        self.model.add_seat()
        self.view.refresh_order()

    def decrement_people(self):
        """Remove the last seat/person from the group order."""
        self.model.remove_last_seat()
        self.view.refresh_order()

    def switch_person(self, person):
        """
        Switch the active person tab in group ordering.
        
        Args:
            person (str): Person name to switch to
        """
        self.model.current_table = person
        self.view.refresh_order()

    def add_person(self, name):
        """
        Add a person to the group order.
        
        Args:
            name (str): Person's name
        """
        if not name.strip():
            messagebox.showwarning("", self.model.t("enter_name"))
            return
        if not self.model.add_person(name.strip()):
            messagebox.showwarning("", self.model.t("person_exists"))
            return
        self.model.current_table = name.strip()
        self.view.refresh_order()

    def remove_person(self, name):
        """
        Remove a person from the group order.
        
        Args:
            name (str): Person name to remove
        """
        self.model.remove_person(name)
        self.view.refresh_order()

    def switch_category(self, category):
        """
        Switch the displayed menu category.
        
        Args:
            category (str): Category key to display
        """
        self.view.show_category(category)


# =============================================================================
# VIEW — All Tkinter UI rendering and layout
# =============================================================================

class MenuView:
    """
    The View in MVC. Handles all Tkinter widget creation, layout,
    styling, and user interaction bindings. Delegates all actions to Controller.
    
    The layout is a two-panel design:
    - Left panel: Menu browsing with category tabs, filters, and item cards
    - Right panel: Order summary with person tabs, item list, totals, and actions
    
    Attributes:
        root (tk.Tk): The main Tkinter window
        model (MenuModel): Data model reference (read-only from view)
        controller (MenuController): Controller for handling actions
        current_category (str): Currently displayed menu category
    """

    # Color scheme — Chinese red + dark tones for restaurant atmosphere
    COLORS = {
        "bg_dark": "#1a1a2e",       # Deep navy background
        "bg_card": "#16213e",       # Card background
        "bg_panel": "#0f3460",      # Panel background
        "accent_red": "#c0392b",    # Chinese red accent
        "accent_gold": "#d4a017",   # Gold accent
        "text_light": "#ecf0f1",    # Light text
        "text_muted": "#95a5a6",    # Muted text
        "text_gold": "#f0c040",     # Gold text
        "highlight": "#e74c3c",     # Highlight red
        "success": "#27ae60",       # Green for success
        "btn_bg": "#2c3e50",        # Button background
        "tag_vegan": "#27ae60",     # Vegan tag
        "tag_veg": "#2ecc71",       # Vegetarian tag
        "tag_gf": "#e67e22",        # Gluten-free tag
        "tag_lf": "#3498db",        # Lactose-free tag
        "tag_na": "#9b59b6",        # Non-alcoholic tag
        "tag_alcohol": "#e74c3c",   # Alcohol warning
        "white": "#ffffff",
        "order_bg": "#1e2740",
    }

    # Tag color mapping for dietary badges
    TAG_COLORS = {
        "vegan": "#27ae60",
        "vegetarian": "#2ecc71",
        "gluten-free": "#e67e22",
        "lactose-free": "#3498db",
        "non-alcoholic": "#9b59b6",
    }

    def __init__(self, root, model, controller):
        """
        Initialize the view, create all widgets, and bind events.
        
        Args:
            root (tk.Tk): Main Tkinter window
            model (MenuModel): Data model
            controller (MenuController): Action controller
        """
        self.root = root
        self.model = model
        self.controller = controller
        self.controller.set_view(self)
        self.current_category = "todays_special"
        
        # Drag-and-drop state
        self._drag_data = {"item": None, "widget": None}
        
        self._setup_window()
        self._setup_styles()
        self._build_ui()
        self.refresh_all()

    def _setup_window(self):
        """Configure the main window properties."""
        self.root.title("Gasthaus Peking Duck")
        self.root.geometry("1024x768")
        self.root.minsize(360, 600)
        self.root.configure(bg=self.COLORS["bg_dark"])
        
        # Make responsive
        self.root.grid_rowconfigure(0, weight=0)  # Header
        self.root.grid_rowconfigure(1, weight=1)  # Main content
        self.root.grid_columnconfigure(0, weight=1)
        # Bind the resize event to handle responsive layout switching
        self.root.bind("<Configure>", self._handle_responsiveness)
    def _setup_styles(self):
        """Configure ttk styles for consistent theming."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure Notebook (tabs) style
        self.style.configure("Category.TNotebook", background=self.COLORS["bg_dark"])
        self.style.configure("Category.TNotebook.Tab",
                             background=self.COLORS["btn_bg"],
                             foreground=self.COLORS["text_light"],
                             padding=[12, 6])
        self.style.map("Category.TNotebook.Tab",
                       background=[("selected", self.COLORS["accent_red"])],
                       foreground=[("selected", self.COLORS["white"])])

    def _build_ui(self):
        """Build the complete UI layout: header + main content area."""
        self._build_header()
        self._build_main_content()

    def _build_header(self):
        """
        Build the top header bar with:
        - Restaurant name and subtitle
        - Language selector buttons
        - Call service button
        """
        header = tk.Frame(self.root, bg=self.COLORS["accent_red"], padx=10, pady=8)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        # Restaurant name
        self.title_label = tk.Label(
            header, text="🦆 Gasthaus Peking Duck",
            font=("Georgia", 18, "bold"),
            bg=self.COLORS["accent_red"], fg=self.COLORS["text_gold"]
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = tk.Label(
            header, text="",
            font=("Georgia", 10, "italic"),
            bg=self.COLORS["accent_red"], fg=self.COLORS["text_light"]
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w")

        # Right side: language + service
        right_frame = tk.Frame(header, bg=self.COLORS["accent_red"])
        right_frame.grid(row=0, column=2, rowspan=2, sticky="e", padx=(10, 0))

        # Language buttons
        lang_frame = tk.Frame(right_frame, bg=self.COLORS["accent_red"])
        lang_frame.pack(side=tk.TOP, anchor="e")
        
        self.lang_buttons = {}
        for code, label in [("en", "EN"), ("de", "DE"), ("zh", "中文")]:
            btn = tk.Button(
                lang_frame, text=label, width=4,
                font=("Arial", 9, "bold"),
                bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"],
                activebackground=self.COLORS["accent_gold"],
                relief=tk.FLAT, cursor="hand2",
                command=lambda c=code: self.controller.change_language(c)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.lang_buttons[code] = btn

        # Service button
        self.service_btn = tk.Button(
            right_frame, text="🔔 Call Service",
            font=("Arial", 10, "bold"),
            bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"],
            activebackground=self.COLORS["success"],
            relief=tk.FLAT, cursor="hand2", padx=10, pady=4,
            command=self.controller.call_service
        )
        self.service_btn.pack(side=tk.TOP, anchor="e", pady=(4, 0))

    def _build_main_content(self):
        """
        Build the main two-panel layout:
        - Left: menu browsing (categories, filters, items)
        - Right: order panel (tabs, items, totals)
        Uses PanedWindow for resizable split.
        """
        self.main_pane = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL,
            bg=self.COLORS["bg_dark"], sashwidth=4,
            sashrelief=tk.FLAT
        )
        self.main_pane.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Left panel — Menu
        self.menu_frame = tk.Frame(self.main_pane, bg=self.COLORS["bg_dark"])
        self.main_pane.add(self.menu_frame, minsize=300, stretch="always")

        # Right panel — Order
        self.order_frame = tk.Frame(self.main_pane, bg=self.COLORS["order_bg"])
        self.main_pane.add(self.order_frame, minsize=250, stretch="never")

        self._build_menu_panel()
        self._build_order_panel()

    # ---- MENU PANEL ----

    def _build_menu_panel(self):
        """
        Build the left menu panel with:
        - Filter bar (Horizontally scrollable with visible scrollbar)
        - Category buttons (Horizontally scrollable with visible scrollbar)
        - Scrollable item card area
        """
        self.menu_frame.grid_rowconfigure(2, weight=1)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        # --- 1. Filter Bar (Visible Scrollbar Setup) ---
        self.filter_wrapper = tk.Frame(self.menu_frame, bg=self.COLORS["bg_panel"])
        self.filter_wrapper.grid(row=0, column=0, sticky="ew")
        self.filter_wrapper.grid_columnconfigure(0, weight=1)

        self.filter_canvas = tk.Canvas(self.filter_wrapper, bg=self.COLORS["bg_panel"], highlightthickness=0, height=40)
        self.filter_scrollbar = ttk.Scrollbar(self.filter_wrapper, orient=tk.HORIZONTAL, command=self.filter_canvas.xview)
        self.filter_canvas.configure(xscrollcommand=self.filter_scrollbar.set)
        
        self.filter_frame = tk.Frame(self.filter_canvas, bg=self.COLORS["bg_panel"], pady=6, padx=8)
        self.filter_canvas.create_window((0, 0), window=self.filter_frame, anchor="nw")
        
        self.filter_canvas.grid(row=0, column=0, sticky="ew")
        self.filter_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.filter_frame.bind("<Configure>", lambda e: self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all")))

        self._build_filters()

        # --- 2. Category Buttons Row (Visible Scrollbar Setup) ---
        self.cat_wrapper = tk.Frame(self.menu_frame, bg=self.COLORS["bg_dark"])
        self.cat_wrapper.grid(row=1, column=0, sticky="ew")
        self.cat_wrapper.grid_columnconfigure(0, weight=1)

        self.cat_canvas = tk.Canvas(self.cat_wrapper, bg=self.COLORS["bg_dark"], highlightthickness=0, height=40)
        self.cat_scrollbar = ttk.Scrollbar(self.cat_wrapper, orient=tk.HORIZONTAL, command=self.cat_canvas.xview)
        self.cat_canvas.configure(xscrollcommand=self.cat_scrollbar.set)
        
        self.cat_frame = tk.Frame(self.cat_canvas, bg=self.COLORS["bg_dark"], pady=4, padx=4)
        self.cat_canvas.create_window((0, 0), window=self.cat_frame, anchor="nw")
        
        self.cat_canvas.grid(row=0, column=0, sticky="ew")
        self.cat_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.cat_frame.bind("<Configure>", lambda e: self.cat_canvas.configure(scrollregion=self.cat_canvas.bbox("all")))

        self._build_category_buttons()

        # --- 3. Menu Items Scroll Area (Existing Vertical Code) ---
        self.menu_canvas_frame = tk.Frame(self.menu_frame, bg=self.COLORS["bg_dark"])
        self.menu_canvas_frame.grid(row=2, column=0, sticky="nsew")
        self.menu_canvas_frame.grid_rowconfigure(0, weight=1)
        self.menu_canvas_frame.grid_columnconfigure(0, weight=1)

        self.menu_canvas = tk.Canvas(
            self.menu_canvas_frame, bg=self.COLORS["bg_dark"],
            highlightthickness=0
        )
        self.menu_scrollbar = ttk.Scrollbar(
            self.menu_canvas_frame, orient=tk.VERTICAL,
            command=self.menu_canvas.yview
        )
        self.menu_inner = tk.Frame(self.menu_canvas, bg=self.COLORS["bg_dark"])
        
        self.menu_inner.bind("<Configure>",
            lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))
        )
        self.menu_canvas_window = self.menu_canvas.create_window(
            (0, 0), window=self.menu_inner, anchor="nw"
        )
        self.menu_canvas.configure(yscrollcommand=self.menu_scrollbar.set)

        self.menu_canvas.grid(row=0, column=0, sticky="nsew")
        self.menu_scrollbar.grid(row=0, column=1, sticky="ns")

        self.menu_canvas.bind("<Configure>", self._on_menu_canvas_configure)
        
        # Vertical mouse wheel scrolling for main menu items
        self.menu_canvas.bind_all("<MouseWheel>", lambda e: self.menu_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def _on_menu_canvas_configure(self, event):
        """Resize the inner frame to match canvas width for proper layout."""
        self.menu_canvas.itemconfig(self.menu_canvas_window, width=event.width)

    def _build_filters(self):
        """Build the dietary filter toggle buttons."""
        self.filter_label = tk.Label(
            self.filter_frame, text="Filter:",
            font=("Arial", 10, "bold"),
            bg=self.COLORS["bg_panel"], fg=self.COLORS["text_light"]
        )
        self.filter_label.pack(side=tk.LEFT, padx=(0, 8))

        self.filter_buttons = {}
        filter_tags = ["vegan", "vegetarian", "gluten-free", "lactose-free", "non-alcoholic"]
        for tag in filter_tags:
            btn = tk.Button(
                self.filter_frame, text=tag,
                font=("Arial", 9),
                bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"],
                activebackground=self.TAG_COLORS.get(tag, self.COLORS["accent_gold"]),
                relief=tk.FLAT, cursor="hand2", padx=8, pady=2,
                command=lambda t=tag: self.controller.toggle_filter(t)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.filter_buttons[tag] = btn

    def _build_category_buttons(self):
        """Build the menu category navigation buttons."""
        self.cat_buttons = {}
        categories = [
            "todays_special", "starters", "soups", "mains",
            "desserts", "beverages", "set_meals"
        ]
        for cat in categories:
            btn = tk.Button(
                self.cat_frame, text=cat,
                font=("Arial", 10, "bold"),
                bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"],
                activebackground=self.COLORS["accent_red"],
                relief=tk.FLAT, cursor="hand2", padx=10, pady=5,
                command=lambda c=cat: self.controller.switch_category(c)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.cat_buttons[cat] = btn

    # ---- ORDER PANEL ----

    def _build_order_panel(self):
        """
        Build the right order panel with:
        - Order header with group/single toggle
        - Person tabs (for group orders)
        - Order items list (scrollable, drop target)
        - Total/tip section
        - Action buttons (place order, clear)
        """
        self.order_frame.grid_rowconfigure(2, weight=1)
        self.order_frame.grid_columnconfigure(0, weight=1)

        # Order header
        self.order_header = tk.Frame(self.order_frame, bg=self.COLORS["bg_panel"], padx=8, pady=6)
        self.order_header.grid(row=0, column=0, sticky="ew")

        self.order_title = tk.Label(
            self.order_header, text="Your Order",
            font=("Georgia", 14, "bold"),
            bg=self.COLORS["bg_panel"], fg=self.COLORS["text_gold"]
        )
        self.order_title.pack(side=tk.LEFT)

        # Group order controls
        self.group_frame = tk.Frame(self.order_header, bg=self.COLORS["bg_panel"])
        self.group_frame.pack(side=tk.RIGHT)

        self.people_minus_btn = tk.Button(
            self.group_frame, text="−",
            font=("Arial", 10, "bold"),
            bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"],
            relief=tk.FLAT, cursor="hand2", width=3,
            command=self.controller.decrement_people
        )
        self.people_minus_btn.pack(side=tk.RIGHT, padx=2)

        self.people_count_label = tk.Label(
            self.group_frame, text=f"{self.model.t('people')}: {self.model.get_people_count()}",
            font=("Arial", 10, "bold"),
            bg=self.COLORS["bg_panel"], fg=self.COLORS["text_light"]
        )
        self.people_count_label.pack(side=tk.RIGHT, padx=6)

        self.add_person_btn = tk.Button(
            # self.group_frame, text=self.model.t("add_person"), # Fixed: Using dynamic text instead of static "+"
            # font=("Arial", 10, "bold"),
            # bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"],
            # relief=tk.FLAT, cursor="hand2", padx=10, # Fixed: Removed fixed width=3 and added padx=10 for dynamic resizing
            self.group_frame, text="+",
            font=("Arial", 10, "bold"),
            bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"],
            relief=tk.FLAT, cursor="hand2", width=3,
            command=self.controller.increment_people
        )
        self.add_person_btn.pack(side=tk.RIGHT, padx=2)

        # Person tabs
        self.person_tabs_frame = tk.Frame(self.order_frame, bg=self.COLORS["order_bg"], padx=4, pady=4)
        self.person_tabs_frame.grid(row=1, column=0, sticky="ew")

        # Order items area (also drop target)
        self.order_list_frame = tk.Frame(self.order_frame, bg=self.COLORS["order_bg"])
        self.order_list_frame.grid(row=2, column=0, sticky="nsew")
        self.order_list_frame.grid_rowconfigure(0, weight=1)
        self.order_list_frame.grid_columnconfigure(0, weight=1)

        self.order_canvas = tk.Canvas(
            self.order_list_frame, bg=self.COLORS["order_bg"], highlightthickness=0
        )
        self.order_scrollbar = ttk.Scrollbar(
            self.order_list_frame, orient=tk.VERTICAL,
            command=self.order_canvas.yview
        )
        self.order_inner = tk.Frame(self.order_canvas, bg=self.COLORS["order_bg"])
        self.order_inner.bind("<Configure>",
            lambda e: self.order_canvas.configure(scrollregion=self.order_canvas.bbox("all"))
        )
        self.order_canvas_window = self.order_canvas.create_window(
            (0, 0), window=self.order_inner, anchor="nw"
        )
        self.order_canvas.configure(yscrollcommand=self.order_scrollbar.set)
        self.order_canvas.grid(row=0, column=0, sticky="nsew")
        self.order_scrollbar.grid(row=0, column=1, sticky="ns")
        self.order_canvas.bind("<Configure>",
            lambda e: self.order_canvas.itemconfig(self.order_canvas_window, width=e.width))

        # Register as drop target
        self.order_canvas.bind("<Button-1>", self._on_order_drop)

        # Drag hint
        self.drag_hint = tk.Label(
            self.order_inner, text="",
            font=("Arial", 9, "italic"),
            bg=self.COLORS["order_bg"], fg=self.COLORS["text_muted"]
        )
        self.drag_hint.pack(pady=10)

        # Bottom: totals + actions
        self.bottom_frame = tk.Frame(self.order_frame, bg=self.COLORS["bg_panel"], padx=8, pady=8)
        self.bottom_frame.grid(row=3, column=0, sticky="ew")
        self._build_totals()

    def _build_totals(self):
        """Build the order total, tip selector, and action buttons."""
        # Tip selection
        tip_frame = tk.Frame(self.bottom_frame, bg=self.COLORS["bg_panel"])
        tip_frame.pack(fill=tk.X, pady=(0, 4))

        self.tip_label = tk.Label(
            tip_frame, text="Tip:",
            font=("Arial", 10), bg=self.COLORS["bg_panel"], fg=self.COLORS["text_light"]
        )
        self.tip_label.pack(side=tk.LEFT)

        self.tip_buttons = {}
        for pct in [0, 5, 10, 15, 20]:
            label = f"{pct}%" if pct > 0 else "0%"
            btn = tk.Button(
                tip_frame, text=label,
                font=("Arial", 9),
                bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"],
                activebackground=self.COLORS["accent_gold"],
                relief=tk.FLAT, cursor="hand2", padx=6, pady=2,
                command=lambda p=pct: self.controller.set_tip(p)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.tip_buttons[pct] = btn

        # Subtotal / total
        self.subtotal_label = tk.Label(
            self.bottom_frame, text="Subtotal: €0.00",
            font=("Arial", 11), bg=self.COLORS["bg_panel"], fg=self.COLORS["text_light"],
            anchor="e"
        )
        self.subtotal_label.pack(fill=tk.X)

        self.total_label = tk.Label(
            self.bottom_frame, text="Total: €0.00",
            font=("Georgia", 14, "bold"), bg=self.COLORS["bg_panel"], fg=self.COLORS["text_gold"],
            anchor="e"
        )
        self.total_label.pack(fill=tk.X, pady=(2, 6))

        # Action buttons
        btn_frame = tk.Frame(self.bottom_frame, bg=self.COLORS["bg_panel"])
        btn_frame.pack(fill=tk.X)

        self.pay_all_btn = tk.Button(
            btn_frame, text="Pay All",
            font=("Arial", 12, "bold"),
            bg=self.COLORS["success"], fg=self.COLORS["white"],
            activebackground="#219a52",
            relief=tk.FLAT, cursor="hand2", padx=16, pady=8,
            command=self.controller.pay_all
        )
        self.pay_all_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))

        self.split_bill_btn = tk.Button(
            btn_frame, text="Split Bill",
            font=("Arial", 12, "bold"),
            bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"],
            activebackground="#d4a017",
            relief=tk.FLAT, cursor="hand2", padx=16, pady=8,
            command=self.controller.split_bill
        )
        self.split_bill_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 4))

        self.clear_order_btn = tk.Button(
            btn_frame, text="Clear",
            font=("Arial", 12, "bold"),
            bg=self.COLORS["highlight"], fg=self.COLORS["white"],
            activebackground="#c0392b",
            relief=tk.FLAT, cursor="hand2", padx=16, pady=8,
            command=self.controller.clear_order
        )
        self.clear_order_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))

    # ---- REFRESH METHODS ----

    def refresh_all(self):
        """Refresh all UI elements — called on language change."""
        self._update_header_text()
        self._update_filter_text()
        self._update_category_text()
        self._update_lang_highlights()
        self.show_category(self.current_category)
        self.refresh_order()
        self.refresh_service_button()

    def refresh_menu(self):
        """Refresh only the menu items display (e.g., after filter change)."""
        self._update_filter_highlights()
        self.show_category(self.current_category)

    def refresh_order(self):
        self._build_person_tabs()
        self._render_order_items()
        self._update_totals()
        # Synchronize slide-in drawer if it is currently open
        if hasattr(self, 'drawer_open') and self.drawer_open:
            self._refresh_drawer_ui()

    def refresh_service_button(self):
        """Update the service button appearance based on state."""
        if self.model.service_called:
            self.service_btn.configure(
                text=self.model.t("service_called"),
                bg=self.COLORS["success"]
            )
        else:
            self.service_btn.configure(
                text=self.model.t("call_service"),
                bg=self.COLORS["accent_gold"]
            )

    def _update_header_text(self):
        """Update header labels for current language."""
        self.title_label.configure(text="🦆 " + self.model.t("app_title"))
        self.subtitle_label.configure(text=self.model.t("app_subtitle"))

    def _update_filter_text(self):
        """Update filter button labels for current language."""
        self.filter_label.configure(text=self.model.t("filter") + ":")
        for tag, btn in self.filter_buttons.items():
            btn.configure(text=self.model.t(tag))

    def _update_filter_highlights(self):
        """Highlight active filter buttons."""
        for tag, btn in self.filter_buttons.items():
            if tag in self.model.active_filters:
                btn.configure(bg=self.TAG_COLORS.get(tag, self.COLORS["accent_gold"]),
                              fg=self.COLORS["white"])
            else:
                btn.configure(bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"])

    def _update_category_text(self):
        """Update category button labels for current language."""
        for cat, btn in self.cat_buttons.items():
            btn.configure(text=self.model.t(cat))

    def _update_lang_highlights(self):
        """Highlight the active language button."""
        for code, btn in self.lang_buttons.items():
            if code == self.model.current_language:
                btn.configure(bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"])
            else:
                btn.configure(bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"])

    def show_category(self, category):
        """
        Display menu items for the given category.
        Updates category button highlights and renders item cards.
        
        Args:
            category (str): Category key to display
        """
        self.current_category = category
        
        # Highlight active category
        for cat, btn in self.cat_buttons.items():
            if cat == category:
                btn.configure(bg=self.COLORS["accent_red"], fg=self.COLORS["white"])
            else:
                btn.configure(bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"])

        # Clear existing items
        for widget in self.menu_inner.winfo_children():
            widget.destroy()

        # Get items for this category
        if category == "todays_special":
            items = [self.model.todays_special]
        elif category == "set_meals":
            items = self.model.set_meals
        else:
            items = self.model.get_filtered_items(category)

        if not items:
            no_items = tk.Label(
                self.menu_inner, text=self.model.t("no_items"),
                font=("Arial", 12, "italic"),
                bg=self.COLORS["bg_dark"], fg=self.COLORS["text_muted"],
                pady=40
            )
            no_items.pack(fill=tk.X)
            return

        # Render each item as a card
        for item in items:
            self._render_menu_card(item)

        # Reset scroll
        self.menu_canvas.yview_moveto(0)

    def _render_menu_card(self, item):
        """
        Render a single menu item as a styled, fully responsive card.
        Includes dietary tags, allergens, and origin info.
        """
        lang = self.model.current_language
        is_special = item.get("category") == "todays_special"
        
        card = tk.Frame(
            self.menu_inner, bg=self.COLORS["bg_card"],
            padx=12, pady=10, relief=tk.FLAT,
            highlightbackground=self.COLORS["accent_gold"] if is_special else self.COLORS["bg_panel"],
            highlightthickness=2 if is_special else 1
        )
        card.pack(fill=tk.X, padx=8, pady=4)

        # Header Row: Name, Price and Add Button
        top = tk.Frame(card, bg=self.COLORS["bg_card"])
        top.pack(fill=tk.X)

        name_text = item["name"].get(lang, item["name"]["en"])
        name_label = tk.Label(
            top, text=name_text, font=("Georgia", 13, "bold"),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_gold"] if is_special else self.COLORS["text_light"],
            anchor="w", cursor="hand2", justify=tk.LEFT
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        add_btn = tk.Button(
            top, text="+", font=("Arial", 12, "bold"),
            bg=self.COLORS["success"], fg=self.COLORS["white"],
            activebackground="#219a52", relief=tk.FLAT, cursor="hand2", width=3,
            command=lambda i=item: self.controller.add_item(i)
        )
        add_btn.pack(side=tk.RIGHT, padx=(8, 0))

        price_label = tk.Label(
            top, text=f"€{item['price']:.2f}", font=("Georgia", 13, "bold"),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_gold"]
        )
        price_label.pack(side=tk.RIGHT)

        # Description text
        desc_text = item["description"].get(lang, item["description"]["en"])
        desc_label = tk.Label(
            card, text=desc_text, font=("Arial", 10),
            bg=self.COLORS["bg_card"], fg=self.COLORS["text_muted"],
            anchor="w", justify=tk.LEFT
        )
        desc_label.pack(fill=tk.X, pady=(4, 6))
        
        # Drag bindings for the whole card, title, and description
        for widget in (card, name_label, desc_label):
            widget.bind("<ButtonPress-1>", lambda e, i=item: self._on_drag_start(e, i))
            widget.bind("<B1-Motion>", self._on_drag_motion)
            widget.bind("<ButtonRelease-1>", self._on_drag_end)

        # --- TAGS & METADATA SECTION (Fixed/Full implementation) ---
        meta_frame = tk.Frame(card, bg=self.COLORS["bg_card"])
        meta_frame.pack(fill=tk.X)
        
        # Tags (Vegan, Vegetarian, etc. - The "Yellow" parts)
        tags_frame = tk.Frame(meta_frame, bg=self.COLORS["bg_card"])
        tags_frame.pack(side=tk.LEFT)
        
        if item.get("tags"):
            for tag in item["tags"]:
                tk.Label(
                    tags_frame, text=self.model.t(tag),
                    font=("Arial", 8, "bold"),
                    bg=self.TAG_COLORS.get(tag, self.COLORS["accent_gold"]),
                    fg=self.COLORS["white"], padx=6, pady=2
                ).pack(side=tk.LEFT, padx=(0, 4))
                
        # Alcohol Warning (Mandatory requirement)
        if item.get("contains_alcohol"):
            tk.Label(
                tags_frame, text=self.model.t("contains_alcohol"),
                font=("Arial", 8, "bold"), bg=self.COLORS["tag_alcohol"],
                fg=self.COLORS["white"], padx=6, pady=2
            ).pack(side=tk.LEFT, padx=(0, 4))

        # Allergens & Origin info (The "Non-yellow" parts)
        info_str = []
        if item.get("allergens"):
            info_str.append(f"{self.model.t('allergens')}: {', '.join(item['allergens'])}")
        if item.get("origin"):
            info_str.append(f"{self.model.t('origin')}: {item['origin']}")
            
        if info_str:
            tk.Label(
                meta_frame, text=" | ".join(info_str),
                font=("Arial", 8, "italic"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_muted"]
            ).pack(side=tk.RIGHT)

        # Handle responsive wrapping
        def on_card_resize(event, d_lbl=desc_label, n_lbl=name_label):
            target_width = event.width - 30 
            if target_width > 50:
                d_lbl.configure(wraplength=target_width)
                n_lbl.configure(wraplength=max(target_width - 120, 50))

        card.bind("<Configure>", on_card_resize)

    def _handle_responsiveness(self, event):
        """Handles responsive layout and ensures header buttons do not overlap."""
        if event.widget == self.root:
            width = event.width
            
            # Identify the right-side frame in the header (contains languages & service button)
            header = self.root.winfo_children()[0]
            header_right_frame = None
            for widget in header.winfo_children():
                if isinstance(widget, tk.Frame) and len(widget.winfo_children()) >= 2:
                    header_right_frame = widget
                    break

            if width < 850:
                # --- Mobile View Adjustments ---
                if self.order_frame in self.main_pane.panes():
                    self.main_pane.forget(self.order_frame)
                
                self.main_pane.configure(sashwidth=0)
                self.main_pane.paneconfigure(self.menu_frame, width=width, minsize=width)
                
                full_name = "🦆 " + self.model.t("app_title")
                self.title_label.configure(
                    text=full_name, font=("Georgia", 11, "bold"),
                    wraplength=max(width - 240, 120), justify=tk.LEFT
                )
                self.subtitle_label.grid_remove()

                # Safely reposition language and service buttons to make space for the Order button
                if header_right_frame:
                    header_right_frame.grid(row=0, column=1, sticky="e", padx=(0, 95)) 
                    if hasattr(self, 'lang_buttons'):
                        for btn in self.lang_buttons.values():
                            btn.configure(font=("Arial", 8, "bold"), width=3)
                    if hasattr(self, 'service_btn'):
                        self.service_btn.configure(width=10, font=("Arial", 8, "bold"), padx=2)

                # Order Button Logic (Visibility Management)
                is_drawer_open = hasattr(self, 'drawer_open') and self.drawer_open
                if not is_drawer_open:
                    if not hasattr(self, 'mobile_cart_btn'):
                        self._create_mobile_cart_button()
                    else:
                        self.mobile_cart_btn.place(relx=1.0, x=-8, y=10, anchor="ne")
                        self.mobile_cart_btn.lift()
                else:
                    if hasattr(self, 'mobile_cart_btn'):
                        self.mobile_cart_btn.place_forget()
            
            else:
                # --- Desktop View Adjustments ---
                self.main_pane.configure(sashwidth=4)
                self.main_pane.paneconfigure(self.menu_frame, minsize=300, width=0)

                if self.order_frame not in self.main_pane.panes():
                    self.main_pane.add(self.order_frame, minsize=250, stretch="never")
                
                full_name = "🦆 " + self.model.t("app_title")
                self.title_label.configure(text=full_name, font=("Georgia", 18, "bold"), wraplength=0)
                self.subtitle_label.grid()

                # Restore language and service buttons to normal desktop size
                if header_right_frame:
                    header_right_frame.grid(row=0, column=2, sticky="e", padx=(0, 10))
                    if hasattr(self, 'lang_buttons'):
                        for btn in self.lang_buttons.values():
                            btn.configure(font=("Arial", 9, "bold"), width=4)
                    if hasattr(self, 'service_btn'):
                        self.service_btn.configure(width=15, font=("Arial", 9, "bold"), padx=10)

                # Ensure mobile order button is hidden on desktop
                if hasattr(self, 'mobile_cart_btn'):
                    self.mobile_cart_btn.place_forget()

    def _create_mobile_cart_button(self):
        """Creates a  floating action button."""
        premium_gold = "#D4AF37"
        hover_gold = "#F1D570"
        dark_text = "#111111"

        self.mobile_cart_btn = tk.Button(
            self.root, text="🛒 Order",
            font=("Segoe UI", 10, "bold"),
            bg=premium_gold, fg=dark_text,
            activebackground=hover_gold, activeforeground=dark_text,
            relief=tk.FLAT, borderwidth=0, highlightthickness=0,
            cursor="hand2", padx=16, pady=6,
            command=self._show_cart_popup
        )
        
        # Hover Animation
        self.mobile_cart_btn.bind("<Enter>", lambda e: self.mobile_cart_btn.configure(bg=hover_gold))
        self.mobile_cart_btn.bind("<Leave>", lambda e: self.mobile_cart_btn.configure(bg=premium_gold))
        
        # Initial placement
        self.mobile_cart_btn.place(relx=1.0, x=-12, y=38, anchor="ne")
    def _show_cart_popup(self):
        if hasattr(self, 'drawer_open') and self.drawer_open:
            return

        # Hide floating order button to prevent overlapping with drawer exit button
        if hasattr(self, 'mobile_cart_btn'):
            self.mobile_cart_btn.place_forget()

        self.drawer_width = min(self.root.winfo_width(), 420) 
        
        if hasattr(self, 'drawer_frame') and self.drawer_frame.winfo_exists():
            self.drawer_frame.destroy()

        self.drawer_frame = tk.Frame(self.root, bg=self.COLORS["order_bg"], 
                                   highlightbackground=self.COLORS["accent_gold"], 
                                   highlightthickness=1)
        
        # Drawer Header Section
        header = tk.Frame(self.drawer_frame, bg=self.COLORS["bg_panel"], padx=15, pady=12)
        header.pack(fill=tk.X)
        tk.Label(header, text=self.model.t("your_order"), font=("Georgia", 15, "bold"), 
                 bg=self.COLORS["bg_panel"], fg=self.COLORS["text_gold"]).pack(side=tk.LEFT)
        
        # Exit icon (X) replaces the Order button position
        tk.Button(header, text="✕", font=("Arial", 14, "bold"), bg=self.COLORS["bg_panel"], 
                  fg="#ff6b6b", bd=0, cursor="hand2", activebackground=self.COLORS["bg_panel"],
                  command=self._close_drawer).pack(side=tk.RIGHT)
        
        tk.Button(header, text=self.model.t("add_person"), font=("Arial", 9, "bold"), 
                  bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"], 
                  relief=tk.FLAT, cursor="hand2", padx=10, 
                  command=self._show_add_person_dialog).pack(side=tk.RIGHT, padx=15)

        self.drawer_tabs_frame = tk.Frame(self.drawer_frame, bg=self.COLORS["order_bg"], padx=5, pady=5)
        self.drawer_tabs_frame.pack(fill=tk.X)

        # Scrollable content area
        container = tk.Frame(self.drawer_frame, bg=self.COLORS["order_bg"])
        container.pack(fill=tk.BOTH, expand=True)
        self.drawer_canvas = tk.Canvas(container, bg=self.COLORS["order_bg"], highlightthickness=0, yscrollincrement=12)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.drawer_canvas.yview)
        self.drawer_inner = tk.Frame(self.drawer_canvas, bg=self.COLORS["order_bg"])
        self.drawer_inner.bind("<Configure>", lambda e: self.drawer_canvas.configure(scrollregion=self.drawer_canvas.bbox("all")))
        self.drawer_canvas_window = self.drawer_canvas.create_window((0, 0), window=self.drawer_inner, anchor="nw", width=self.drawer_width-20)
        self.drawer_canvas.configure(yscrollcommand=scrollbar.set)
        self.drawer_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.drawer_canvas.bind_all("<MouseWheel>", self._on_drawer_mousewheel)

        # Footer Area (Totals and Actions)
        self.drawer_footer = tk.Frame(self.drawer_frame, bg=self.COLORS["bg_panel"], padx=15, pady=15)
        self.drawer_footer.pack(fill=tk.X, side=tk.BOTTOM)

        self._refresh_drawer_ui()

        # Place drawer off-screen initially then animate in
        
        
        self.drawer_open = True
        self._show_overlay()
        self.drawer_frame.place(relx=1.0, rely=0, relheight=1.0, width=self.drawer_width, x=self.drawer_width)
        self.drawer_frame.lift()
        self._animate_drawer_in(self.drawer_width)

    def _on_drawer_mousewheel(self, event):
        """Enables smooth mouse scrolling within the drawer"""
        if hasattr(self, 'drawer_open') and self.drawer_open:
            self.drawer_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _show_overlay(self):
        if hasattr(self, '_overlay') and self._overlay.winfo_exists():
            self._overlay.destroy()
        self._overlay = tk.Frame(self.root, bg="#000000")
        self._overlay.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        self._overlay.lift()
        self._overlay.bind("<Button-1>", lambda e: self._close_drawer())
        tk.Label(self._overlay, text="🦆", font=("Segoe UI Emoji", 48),
                 bg="#000000", fg="#ffffff").place(relx=0.5, rely=0.5, anchor="center")

    def _fade_overlay_in(self):
        if not hasattr(self, '_overlay') or not self._overlay.winfo_exists(): return
        if not hasattr(self, 'drawer_open') or not self.drawer_open: return
        colors = ["#0a0a1a", "#0d0d20", "#101025", "#121228", "#14142b",
                  "#16162e", "#181831", "#1a1a34", "#1a1a2e"]
        if self._overlay_alpha < len(colors) - 1:
            self._overlay_alpha += 1
            self._overlay.configure(bg=colors[self._overlay_alpha])
            self.root.after(18, self._fade_overlay_in)

    def _fade_overlay_out(self):
        if not hasattr(self, '_overlay') or not self._overlay.winfo_exists(): return
        colors = ["#1a1a2e", "#181831", "#16162e", "#14142b",
                  "#121228", "#101025", "#0d0d20", "#0a0a1a"]
        if self._overlay_alpha < len(colors):
            self._overlay.configure(bg=colors[self._overlay_alpha])
            self._overlay_alpha += 1
            self.root.after(18, self._fade_overlay_out)
        else:
            self._overlay.destroy()

    def _animate_drawer_in(self, current_x):
        if not hasattr(self, 'drawer_frame') or not self.drawer_frame.winfo_exists(): return
        target_x = -self.drawer_width
        step = (target_x - current_x) // 4
        if abs(step) < 1: step = -1 if target_x < current_x else 1
        next_x = current_x + step
        if (step < 0 and next_x <= target_x) or (step > 0 and next_x >= target_x):
            self.drawer_frame.place(x=target_x)
            self.drawer_frame.lift()
        else:
            self.drawer_frame.place(x=next_x)
            self.drawer_frame.lift()
            self.root.after(10, lambda: self._animate_drawer_in(next_x))

    def _close_drawer(self):
        if not hasattr(self, 'drawer_open') or not self.drawer_open: return
        self._animate_drawer_out(-self.drawer_width)

    def _animate_drawer_out(self, current_x):
        if not hasattr(self, 'drawer_open') or not self.drawer_open: return
        if not hasattr(self, 'drawer_frame') or not self.drawer_frame.winfo_exists(): return
        target_x = 0
        step = (target_x - current_x) // 4
        if abs(step) < 1: step = 1
        next_x = current_x + step
        if next_x >= target_x:
            self.drawer_frame.place(x=target_x)
            self.drawer_frame.place_forget()
            self.drawer_open = False
            if hasattr(self, '_overlay') and self._overlay.winfo_exists():
                self._overlay.destroy()
            if hasattr(self, 'mobile_cart_btn'):
                self.mobile_cart_btn.place(relx=1.0, x=-8, y=10, anchor="ne")
                self.mobile_cart_btn.lift()
        else:
            self.drawer_frame.place(x=next_x)
            self.drawer_frame.lift()
            self.root.after(10, lambda: self._animate_drawer_out(next_x))

    def _refresh_drawer_ui(self):
        if not hasattr(self, 'drawer_frame') or not self.drawer_frame.winfo_exists(): return
        self._render_drawer_tabs_content()
        self._render_drawer_items_content()
        self._render_drawer_footer_content()

    def _render_drawer_tabs_content(self):
        for widget in self.drawer_tabs_frame.winfo_children(): widget.destroy()
        for person in self.model.orders:
            bg = self.COLORS["accent_red"] if person == self.model.current_table else self.COLORS["btn_bg"]
            tab = tk.Frame(self.drawer_tabs_frame, bg=bg, padx=2)
            tab.pack(side=tk.LEFT, padx=2, pady=2)
            tk.Button(tab, text=person, font=("Arial", 9, "bold"), bg=bg, fg=self.COLORS["white"], 
                      relief=tk.FLAT, cursor="hand2", command=lambda p=person: self.controller.switch_person(p)).pack(side=tk.LEFT)
            if person != "Table":
                tk.Button(tab, text="×", font=("Arial", 9, "bold"), bg=bg, fg=self.COLORS["text_muted"], 
                          relief=tk.FLAT, width=2, command=lambda p=person: self.controller.remove_person(p)).pack(side=tk.LEFT)

    def _render_drawer_items_content(self):
        for widget in self.drawer_inner.winfo_children(): widget.destroy()
        items = self.model.orders.get(self.model.current_table, [])
        lang = self.model.current_language
        if not items:
            tk.Label(self.drawer_inner, text=self.model.t("order_empty"), font=("Arial", 11, "italic"), 
                     bg=self.COLORS["order_bg"], fg=self.COLORS["text_muted"], pady=60).pack()
            return
        for item in items:
            row = tk.Frame(self.drawer_inner, bg=self.COLORS["bg_card"], padx=12, pady=10)
            row.pack(fill=tk.X, pady=4, padx=8)
            top = tk.Frame(row, bg=self.COLORS["bg_card"])
            top.pack(fill=tk.X)
            tk.Label(top, text=item["name"].get(lang, item["name"]["en"]), font=("Arial", 10, "bold"), 
                     bg=self.COLORS["bg_card"], fg=self.COLORS["text_light"]).pack(side=tk.LEFT)
            tk.Label(top, text=f"€{item['price'] * item['qty']:.2f}", font=("Arial", 11, "bold"), 
                     bg=self.COLORS["bg_card"], fg=self.COLORS["text_gold"]).pack(side=tk.RIGHT)
            ctrls = tk.Frame(row, bg=self.COLORS["bg_card"])
            ctrls.pack(fill=tk.X, pady=(8,0))
            tk.Button(ctrls, text="−", font=("Arial", 10, "bold"), bg=self.COLORS["highlight"], fg=self.COLORS["white"], 
                      relief=tk.FLAT, width=3, cursor="hand2", command=lambda iid=item["id"]: self.controller.remove_item(iid)).pack(side=tk.LEFT)
            tk.Label(ctrls, text=str(item["qty"]), font=("Arial", 11, "bold"), bg=self.COLORS["bg_card"], 
                     fg=self.COLORS["text_light"], width=4).pack(side=tk.LEFT)
            tk.Button(ctrls, text="+", font=("Arial", 10, "bold"), bg=self.COLORS["success"], fg=self.COLORS["white"], 
                      relief=tk.FLAT, width=3, cursor="hand2", command=lambda i=item: self.controller.add_item(i)).pack(side=tk.LEFT)

    def _render_drawer_footer_content(self):
        for widget in self.drawer_footer.winfo_children(): widget.destroy()
        tip_f = tk.Frame(self.drawer_footer, bg=self.COLORS["bg_panel"])
        tip_f.pack(fill=tk.X, pady=(0, 8))
        tk.Label(tip_f, text="Tip:", font=("Arial", 10), bg=self.COLORS["bg_panel"], fg=self.COLORS["text_light"]).pack(side=tk.LEFT)
        for pct in [0, 5, 10, 15, 20]:
            bg_c = self.COLORS["accent_gold"] if pct == self.model.tip_percent else self.COLORS["btn_bg"]
            fg_c = self.COLORS["bg_dark"] if pct == self.model.tip_percent else self.COLORS["text_light"]
            tk.Button(tip_f, text=f"{pct}%", font=("Arial", 9, "bold"), bg=bg_c, fg=fg_c, relief=tk.FLAT, 
                      padx=6, cursor="hand2", command=lambda p=pct: self.controller.set_tip(p)).pack(side=tk.LEFT, padx=2)
        sub = self.model.get_order_total()
        tot = self.model.get_order_total_with_tip()
        tk.Label(self.drawer_footer, text=f"Subtotal: €{sub:.2f}", font=("Arial", 10), 
                 bg=self.COLORS["bg_panel"], fg=self.COLORS["text_light"], anchor="e").pack(fill=tk.X)
        tk.Label(self.drawer_footer, text=f"Total: €{tot:.2f}", font=("Georgia", 18, "bold"), 
                 bg=self.COLORS["bg_panel"], fg=self.COLORS["text_gold"], anchor="e").pack(fill=tk.X, pady=(2, 10))
        btns = tk.Frame(self.drawer_footer, bg=self.COLORS["bg_panel"])
        btns.pack(fill=tk.X)
        tk.Button(btns, text="Place Order", font=("Arial", 12, "bold"), bg=self.COLORS["success"], 
                  fg=self.COLORS["white"], relief=tk.FLAT, pady=10, cursor="hand2",
                  command=self._handle_drawer_order_final).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        tk.Button(btns, text="Clear", font=("Arial", 12, "bold"), bg=self.COLORS["highlight"], 
                  fg=self.COLORS["white"], relief=tk.FLAT, pady=10, cursor="hand2",
                  command=self.controller.clear_order).pack(side=tk.LEFT, expand=True, fill=tk.X)

    def _handle_drawer_order_final(self):
        self._close_drawer()
        self.controller.place_order()
        
    def _is_over_order_drop_target(self, x_root, y_root):
        """
        Return True if the given screen coordinates are over the order drop area.
        Uses the visible order list/canvas as the drop target.
        """
        target = self.order_list_frame

        x1 = target.winfo_rootx()
        y1 = target.winfo_rooty()
        x2 = x1 + target.winfo_width()
        y2 = y1 + target.winfo_height()

        return x1 <= x_root <= x2 and y1 <= y_root <= y2
    
    # ---- DRAG AND DROP ----

    def _on_drag_start(self, event, item):
        """
        Start a drag operation — stores the item being dragged.
        
        Args:
            event: Tkinter event
            item (dict): Menu item being dragged
        """
        self._drag_data["item"] = item
        self._drag_data["x"] = event.x_root
        self._drag_data["y"] = event.y_root
        
        # Create floating label to indicate drag
        self._drag_label = tk.Label(
            self.root,
            text=f"🍽 {item['name'][self.model.current_language]}",
            font=("Arial", 10, "bold"),
            bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"],
            padx=8, pady=4, relief=tk.RAISED
        )

    def _on_drag_motion(self, event):
        """
        Update floating drag label position and highlight drop target.
        """
        if hasattr(self, "_drag_label") and self._drag_label:
            x = event.x_root - self.root.winfo_rootx()
            y = event.y_root - self.root.winfo_rooty()
            self._drag_label.place(x=x + 10, y=y + 10)

        if self._is_over_order_drop_target(event.x_root, event.y_root):
            self.order_list_frame.configure(bg="#243b55")
            self.order_canvas.configure(bg="#243b55")
            self.order_inner.configure(bg="#243b55")
        else:
            self.order_list_frame.configure(bg=self.COLORS["order_bg"])
            self.order_canvas.configure(bg=self.COLORS["order_bg"])
            self.order_inner.configure(bg=self.COLORS["order_bg"])

    def _on_drag_end(self, event):
        """
        End drag — add item if dropped over order area.
        """
        if hasattr(self, "_drag_label") and self._drag_label:
            self._drag_label.destroy()
            self._drag_label = None

        if self._drag_data["item"] is None:
            return

        if self._is_over_order_drop_target(event.x_root, event.y_root):
            self.controller.add_item(self._drag_data["item"])

        self.order_list_frame.configure(bg=self.COLORS["order_bg"])
        self.order_canvas.configure(bg=self.COLORS["order_bg"])
        self.order_inner.configure(bg=self.COLORS["order_bg"])

        self._drag_data["item"] = None
        self._drag_data["x"] = None
        self._drag_data["y"] = None

    def _on_order_drop(self, event):
        """Handle click on order panel (for potential drop target feedback)."""
        pass

    # ---- PERSON TABS (GROUP ORDER) ----

    def _build_person_tabs(self):
        """Build person/table tabs for group ordering."""
        for widget in self.person_tabs_frame.winfo_children():
            widget.destroy()

        for person in self.model.orders:
            is_active = person == self.model.current_table
            bg = self.COLORS["accent_red"] if is_active else self.COLORS["btn_bg"]
            
            tab_frame = tk.Frame(self.person_tabs_frame, bg=bg, padx=2)
            tab_frame.pack(side=tk.LEFT, padx=2, pady=2)

            btn = tk.Button(
                tab_frame, text=person,
                font=("Arial", 9, "bold"),
                bg=bg, fg=self.COLORS["white"],
                relief=tk.FLAT, cursor="hand2",
                command=lambda p=person: self.controller.switch_person(p)
            )
            btn.pack(side=tk.LEFT)

            # Remove button (except for default "Table")
            if person != "Table":
                rm_btn = tk.Button(
                    tab_frame, text="×",
                    font=("Arial", 9, "bold"),
                    bg=bg, fg=self.COLORS["text_muted"],
                    relief=tk.FLAT, cursor="hand2", width=2,
                    command=lambda p=person: self.controller.remove_person(p)
                )
                rm_btn.pack(side=tk.LEFT)

    def _show_add_person_dialog(self):
        """Standard dialog to add person - Centered and Smart Overlay Fix"""
        # Ensure the floating Order button stays hidden immediately
        if hasattr(self, 'mobile_cart_btn'):
            self.mobile_cart_btn.place_forget()

        dialog = tk.Toplevel(self.root)
        dialog.title(self.model.t("add_person"))
        dialog.geometry("320x160")
        dialog.configure(bg=self.COLORS["bg_card"])
        dialog.transient(self.root)
        dialog.grab_set()

        # Logic to center the popup window relative to the main app
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_w = self.root.winfo_width()
        main_h = self.root.winfo_height()
        dialog.geometry(f"+{main_x + (main_w//2) - 160}+{main_y + (main_h//2) - 80}")

        tk.Label(dialog, text=self.model.t("person_name"), font=("Arial", 11, "bold"), 
                 bg=self.COLORS["bg_card"], fg=self.COLORS["text_light"]).pack(pady=(20, 5))

        entry = tk.Entry(dialog, font=("Arial", 12), width=22, bg=self.COLORS["bg_panel"], 
                         fg=self.COLORS["white"], insertbackground="white", relief=tk.FLAT)
        entry.pack(pady=10, padx=20)
        entry.focus_set()

        def submit():
            name = entry.get().strip()
            if name:
                self.controller.add_person(name)
                # Lock the Order button state if the drawer is still open
                if hasattr(self, 'drawer_open') and self.drawer_open:
                    if hasattr(self, 'mobile_cart_btn'):
                        self.mobile_cart_btn.place_forget()
                dialog.destroy()

        entry.bind("<Return>", lambda e: submit())
        
        tk.Button(dialog, text="OK", font=("Arial", 11, "bold"), bg=self.COLORS["accent_gold"], 
                  fg=self.COLORS["bg_dark"], relief=tk.FLAT, cursor="hand2", padx=30, pady=5, 
                  command=submit).pack(pady=10)

        # Handle X button on popup to prevent 'Order' button overlap
        dialog.protocol("WM_DELETE_WINDOW", lambda: [
            self.mobile_cart_btn.place_forget() if hasattr(self, 'drawer_open') and self.drawer_open else None,
            dialog.destroy()
        ])
    # ---- ORDER ITEMS RENDERING ----

    def _render_order_items(self):
        """Render the current person's order items in the order panel."""
        for widget in self.order_inner.winfo_children():
            widget.destroy()

        # Drag hint
        hint = tk.Label(
            self.order_inner, text=self.model.t("drag_hint"),
            font=("Arial", 9, "italic"),
            bg=self.COLORS["order_bg"], fg=self.COLORS["text_muted"]
        )
        hint.pack(pady=(8, 4), padx=8)

        items = self.model.orders.get(self.model.current_table, [])
        if not items:
            empty = tk.Label(
                self.order_inner, text=self.model.t("order_empty"),
                font=("Arial", 11, "italic"),
                bg=self.COLORS["order_bg"], fg=self.COLORS["text_muted"],
                pady=30
            )
            empty.pack()
            return

        lang = self.model.current_language
        for item in items:
            row = tk.Frame(self.order_inner, bg=self.COLORS["bg_card"], padx=8, pady=6)
            row.pack(fill=tk.X, padx=6, pady=2)

            # Item name
            name = item["name"].get(lang, item["name"]["en"])
            tk.Label(
                row, text=name,
                font=("Arial", 10, "bold"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_light"],
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Quantity controls
            qty_frame = tk.Frame(row, bg=self.COLORS["bg_card"])
            qty_frame.pack(side=tk.RIGHT)

            tk.Button(
                qty_frame, text="−",
                font=("Arial", 10, "bold"),
                bg=self.COLORS["highlight"], fg=self.COLORS["white"],
                relief=tk.FLAT, cursor="hand2", width=2,
                command=lambda iid=item["id"]: self.controller.remove_item(iid)
            ).pack(side=tk.LEFT, padx=2)

            tk.Label(
                qty_frame, text=str(item["qty"]),
                font=("Arial", 10, "bold"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_light"],
                width=3
            ).pack(side=tk.LEFT)

            tk.Button(
                qty_frame, text="+",
                font=("Arial", 10, "bold"),
                bg=self.COLORS["success"], fg=self.COLORS["white"],
                relief=tk.FLAT, cursor="hand2", width=2,
                command=lambda i=item: self.controller.add_item(i)
            ).pack(side=tk.LEFT, padx=2)

            tk.Label(
                qty_frame, text=f"€{item['price'] * item['qty']:.2f}",
                font=("Arial", 10, "bold"),
                bg=self.COLORS["bg_card"], fg=self.COLORS["text_gold"],
                width=8, anchor="e"
            ).pack(side=tk.LEFT, padx=(8, 0))

    def _update_totals(self):
        """Update the subtotal, tip, and total labels."""
        subtotal = self.model.get_order_total()
        total = self.model.get_order_total_with_tip()
        tip = self.model.tip_percent

        self.people_count_label.configure(
            text=f"{self.model.t('people')}: {self.model.get_people_count()}"
        )

        self.subtotal_label.configure(
            text=f"{self.model.t('subtotal')}: €{subtotal:.2f}"
        )
        
        if tip > 0:
            self.total_label.configure(
                text=f"{self.model.t('total')} (+{tip}%): €{total:.2f}"
            )
        else:
            self.total_label.configure(
                text=f"{self.model.t('total')}: €{subtotal:.2f}"
            )

        # Highlight active tip button
        for pct, btn in self.tip_buttons.items():
            if pct == tip:
                btn.configure(bg=self.COLORS["accent_gold"], fg=self.COLORS["bg_dark"])
            else:
                btn.configure(bg=self.COLORS["btn_bg"], fg=self.COLORS["text_light"])

        # Update button text
        self.tip_label.configure(text=self.model.t("tip") + ":")
        self.pay_all_btn.configure(text=self.model.t("pay_all"))
        self.split_bill_btn.configure(text=self.model.t("split_bill"))
        self.clear_order_btn.configure(text=self.model.t("clear_order"))
        self.order_title.configure(text=self.model.t("your_order"))
        self.people_count_label.configure(text=f"{self.model.t('people')}: {self.model.get_people_count()}")


# =============================================================================
# MAIN — Application entry point
# =============================================================================

def main():
    """
    Application entry point.
    Creates MVC components and starts the Tkinter main loop.
    """
    root = tk.Tk()
    model = MenuModel()
    controller = MenuController(model)
    view = MenuView(root, model, controller)
    root.mainloop()


if __name__ == "__main__":
    main()