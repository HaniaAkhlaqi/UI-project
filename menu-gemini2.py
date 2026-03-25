import tkinter as tk
from tkinter import messagebox, ttk

# --- MODEL ---
class RestaurantModel:
    def __init__(self):
        self.current_lang = "EN"
        self.active_filters = set()
        self.current_order = []
        self.active_seat = 1
        self.num_people = 1 
        self.view_category = "all"
        
        # Set Meal Builder State
        self.building_set = False
        self.set_slots = {"cat_start": None, "cat_main": None, "cat_dessert": None}

        self.languages = {
            "EN": {"all": "Show All Menu", "start": "Starters", "soup": "Soups", "main": "Main Courses", 
                   "dessert": "Desserts", "bev": "Beverages", "set": "Set Meals", "order": "Order", 
                   "total": "Total", "origin": "Origin", "add": "Add", "seat": "Seat", 
                   "pay_all": "Pay All (Inc. 10% Tip)", "pay_split": "Split Bill (Inc. 10% Tip)", 
                   "group_size": "People:", "filter_title": "Dietary Filters", 
                   "set_instr": "Build Set: 1 Starter + 1 Main + 1 Dessert", "tags": "Tags"},
            "SE": {"all": "Visa Hela Menyn", "start": "Förrätter", "soup": "Soppor", "main": "Varmrätter", 
                   "dessert": "Efterrätter", "bev": "Drycker", "set": "Menypaket", "order": "Beställning", 
                   "total": "Totalt", "origin": "Ursprung", "add": "Lägg till", "seat": "Sittplats", 
                   "pay_all": "Betala Allt (Inkl. 10% Dricks)", "pay_split": "Dela Nota (Inkl. 10% Dricks)", 
                   "group_size": "Personer:", "filter_title": "Kostfilter", 
                   "set_instr": "Bygg: 1 Förrätt + 1 Varmrätt + 1 Efterrätt", "tags": "Info"},
            "CN": {"all": "显示全部", "start": "前菜", "soup": "汤类", "main": "主菜", 
                   "dessert": "甜点", "bev": "饮料", "set": "套餐", "order": "您的订单", 
                   "total": "总计", "origin": "产地", "add": "添加", "seat": "座位", 
                   "pay_all": "全部结账 (含10%小费)", "pay_split": "分摊结账 (含10%小费)", 
                   "group_size": "人数:", "filter_title": "饮食筛选", 
                   "set_instr": "套餐：1前菜 + 1主菜 + 1甜点", "tags": "标签"}
        }
        
        self.trans = {
            "cat_start": {"EN": "Starters", "SE": "Förrätter", "CN": "前菜"},
            "cat_soup": {"EN": "Soups", "SE": "Soppor", "CN": "汤类"},
            "cat_main": {"EN": "Main Courses", "SE": "Varmrätter", "CN": "主菜"},
            "cat_dessert": {"EN": "Desserts", "SE": "Efterrätter", "CN": "甜点"},
            "cat_bev": {"EN": "Beverages", "SE": "Drycker", "CN": "饮料"},
            "cat_set": {"EN": "Set Meals", "SE": "Menypaket", "CN": "套餐"},
            # Items
            "i_sr": {"EN": "Spring Rolls", "SE": "Vårrullar", "CN": "春卷"},
            "i_dum": {"EN": "Veggie Dumplings", "SE": "Veg-Dumplings", "CN": "素饺子"},
            "i_squid": {"EN": "Salt & Pepper Squid", "SE": "Friterad Bläckfisk", "CN": "椒盐鱿鱼"},
            "i_hs": {"EN": "Hot & Sour Soup", "SE": "Surstark Soppa", "CN": "酸辣汤"},
            "i_won": {"EN": "Wonton Soup", "SE": "Wonton Soppa", "CN": "云吞汤"},
            "i_corn": {"EN": "Sweetcorn Soup", "SE": "Majssoppa", "CN": "玉米汤"},
            "i_duck": {"EN": "Peking Duck", "SE": "Pekinganka", "CN": "北京烤鸭"},
            "i_tofu": {"EN": "Mapo Tofu", "SE": "Mapo Tofu", "CN": "麻婆豆腐"},
            "i_beef": {"EN": "Crispy Beef", "SE": "Krispigt Biff", "CN": "干炒牛丝"},
            "i_curry": {"EN": "Yellow Curry Veg", "SE": "Gul Curry Veg", "CN": "黄咖喱蔬菜"},
            "i_ban": {"EN": "Fried Bananas", "SE": "Friterad Banan", "CN": "油炸香蕉"},
            "i_ice": {"EN": "Lychee Ice Cream", "SE": "Litchi Glass", "CN": "荔枝冰淇淋"},
            "i_mochi": {"EN": "Mochi Mix", "SE": "Mochi Mix", "CN": "麻糬"},
            "i_beer": {"EN": "Tsingtao Beer", "SE": "Tsingtao Öl", "CN": "青岛啤酒"},
            "i_tea": {"EN": "Oolong Tea", "SE": "Oolong Te", "CN": "乌龙茶"},
            "i_soda": {"EN": "Plum Soda", "SE": "Plommonläsk", "CN": "酸梅汤"},
            "i_set_3": {"EN": "3-Course Imperial", "SE": "3-Rätters Imperial", "CN": "三道菜套餐"},
            # Tags
            "tag_gf": {"EN": "Gluten-free", "SE": "Glutenfri", "CN": "无麸质"},
            "tag_v": {"EN": "Vegan", "SE": "Vegan", "CN": "纯素食"},
            "tag_veg": {"EN": "Vegetarian", "SE": "Vegetarisk", "CN": "素食"},
            "tag_no_alc": {"EN": "Non-alcoholic", "SE": "Alkoholfri", "CN": "无酒精"},
            "country_cn": {"EN": "China", "SE": "Kina", "CN": "中国"},
            "country_se": {"EN": "Sweden", "SE": "Sverige", "CN": "瑞典"}
        }

        self.menu_items = [
            {"id": "i_sr", "price": 85, "cat": "cat_start", "origin": "country_se", "tags": ["tag_veg"]},
            {"id": "i_dum", "price": 90, "cat": "cat_start", "origin": "country_cn", "tags": ["tag_v", "tag_veg"]},
            {"id": "i_squid", "price": 110, "cat": "cat_start", "origin": "country_se", "tags": ["tag_gf"]},
            {"id": "i_hs", "price": 75, "cat": "cat_soup", "origin": "country_cn", "tags": ["tag_gf", "tag_v"]},
            {"id": "i_won", "price": 80, "cat": "cat_soup", "origin": "country_cn", "tags": []},
            {"id": "i_corn", "price": 70, "cat": "cat_soup", "origin": "country_se", "tags": ["tag_veg", "tag_gf"]},
            {"id": "i_duck", "price": 250, "cat": "cat_main", "origin": "country_cn", "tags": ["tag_gf"]},
            {"id": "i_tofu", "price": 180, "cat": "cat_main", "origin": "country_cn", "tags": ["tag_v", "tag_gf", "tag_veg"]},
            {"id": "i_beef", "price": 210, "cat": "cat_main", "origin": "country_se", "tags": []},
            {"id": "i_curry", "price": 175, "cat": "cat_main", "origin": "country_cn", "tags": ["tag_v", "tag_gf"]},
            {"id": "i_ban", "price": 65, "cat": "cat_dessert", "origin": "country_se", "tags": ["tag_veg"]},
            {"id": "i_ice", "price": 55, "cat": "cat_dessert", "origin": "country_cn", "tags": ["tag_gf", "tag_veg"]},
            {"id": "i_mochi", "price": 70, "cat": "cat_dessert", "origin": "country_cn", "tags": ["tag_gf", "tag_v"]},
            {"id": "i_beer", "price": 60, "cat": "cat_bev", "origin": "country_cn", "tags": []},
            {"id": "i_tea", "price": 40, "cat": "cat_bev", "origin": "country_cn", "tags": ["tag_no_alc", "tag_v", "tag_gf"]},
            {"id": "i_soda", "price": 45, "cat": "cat_bev", "origin": "country_se", "tags": ["tag_no_alc", "tag_v", "tag_gf"]},
            {"id": "i_set_3", "price": 380, "cat": "cat_set", "origin": "country_cn", "tags": []}
        ]

    def add_to_order(self, item_id):
        item = next((i for i in self.menu_items if i["id"] == item_id), None)
        if item:
            self.current_order.append({"id": item_id, "price": item['price'], "seat": self.active_seat})

# --- VIEW & CONTROLLER ---
class GasthausApp:
    def __init__(self, root):
        self.model = RestaurantModel()
        self.root = root
        self.root.title("Gasthaus Peking Duck")
        self.root.geometry("1300x850")
        self.root.configure(bg="#2c3e50")
        self.setup_ui()
        self.update_view()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#c0392b", height=60)
        header.pack(fill="x")
        for lang in ["EN", "SE", "CN"]:
            tk.Button(header, text=lang, width=4, command=lambda l=lang: self.change_lang(l)).pack(side="right", padx=5, pady=10)

        self.main_container = tk.Frame(self.root, bg="#2c3e50")
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)

        self.left_sidebar = tk.Frame(self.main_container, width=200, bg="#34495e")
        self.left_sidebar.pack(side="left", fill="y", padx=5)
        self.left_sidebar.pack_propagate(False)

        self.menu_canvas = tk.Canvas(self.main_container, bg="#ecf0f1")
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.menu_canvas.yview)
        self.menu_scroll_frame = tk.Frame(self.menu_canvas, bg="#ecf0f1")
        self.menu_canvas.create_window((0, 0), window=self.menu_scroll_frame, anchor="nw")
        self.menu_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.menu_canvas.pack(side="left", expand=True, fill="both", padx=5)
        self.scrollbar.pack(side="left", fill="y")

        self.order_frame = tk.LabelFrame(self.main_container, text="Order Cart", bg="#ecf0f1", width=380)
        self.order_frame.pack(side="right", fill="both", padx=5)
        self.order_frame.pack_propagate(False)

    def update_view(self):
        for w in [self.menu_scroll_frame, self.left_sidebar, self.order_frame]:
            for child in w.winfo_children(): child.destroy()

        lp = self.model.languages[self.model.current_lang]
        categories = ["cat_set", "cat_start", "cat_soup", "cat_main", "cat_dessert", "cat_bev"]

        # 1. Left Sidebar
        tk.Button(self.left_sidebar, text=lp['all'], bg="#c0392b", fg="white", font=("Arial", 10, "bold"),
                  command=lambda: self.set_view("all")).pack(fill="x", pady=5, padx=5)
        for cat in categories:
            name = self.model.trans[cat][self.model.current_lang]
            btn_bg = "#f1c40f" if self.model.view_category == cat else "#2c3e50"
            tk.Button(self.left_sidebar, text=name, bg=btn_bg, fg="white", 
                      command=lambda c=cat: self.set_view(c)).pack(fill="x", pady=1, padx=5)

        ttk.Separator(self.left_sidebar, orient='horizontal').pack(fill='x', pady=15)
        for tag in ["tag_v", "tag_veg", "tag_gf", "tag_no_alc"]:
            is_active = tag in self.model.active_filters
            tk.Button(self.left_sidebar, text=("● " if is_active else "○ ") + self.model.trans[tag][self.model.current_lang], 
                      anchor="w", command=lambda t=tag: self.toggle_filter(t)).pack(fill="x", pady=1, padx=5)

        # 2. Menu Rendering with Details
        for cat in categories:
            if self.model.view_category != "all" and self.model.view_category != cat:
                continue

            items = [i for i in self.model.menu_items if i["cat"] == cat and self.model.active_filters.issubset(set(i["tags"]))]
            if items:
                tk.Label(self.menu_scroll_frame, text=self.model.trans[cat][self.model.current_lang], 
                         font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#c0392b").pack(anchor="w", padx=10, pady=(15, 5))
                for item in items:
                    f = tk.Frame(self.menu_scroll_frame, bd=1, relief="ridge", bg="white")
                    f.pack(fill="x", pady=2, padx=10)
                    
                    name = self.model.trans[item['id']][self.model.current_lang]
                    origin = self.model.trans[item['origin']][self.model.current_lang]
                    tags_list = [self.model.trans[t][self.model.current_lang] for t in item['tags']]
                    
                    details = f"{name} - {item['price']} SEK\n{lp['origin']}: {origin} | {lp['tags']}: {', '.join(tags_list)}"
                    tk.Label(f, text=details, justify="left", bg="white", font=("Arial", 9)).pack(side="left", padx=10, pady=5)
                    tk.Button(f, text=lp['add'], bg="#27ae60", fg="white", command=lambda i=item: self.handle_add(i)).pack(side="right", padx=10)

        # 3. Order Cart
        if self.model.building_set:
            b_f = tk.Frame(self.order_frame, bg="#f39c12", pady=5)
            b_f.pack(fill="x")
            tk.Label(b_f, text=lp['set_instr'], font=("Arial", 8, "bold"), bg="#f39c12").pack()
            for slot, item_id in self.model.set_slots.items():
                txt = self.model.trans[slot][self.model.current_lang] + ": "
                txt += self.model.trans[item_id][self.model.current_lang] if item_id else "---"
                tk.Label(b_f, text=txt, bg="#f39c12", font=("Arial", 8)).pack(anchor="w", padx=10)
            tk.Button(b_f, text="Cancel", command=self.cancel_set).pack()

        # Seat selector
        size_f = tk.Frame(self.order_frame, bg="#ecf0f1")
        size_f.pack(pady=5)
        tk.Label(size_f, text=lp['group_size'], bg="#ecf0f1").pack(side="left")
        tk.Button(size_f, text="-", command=lambda: self.adjust_group(-1)).pack(side="left")
        tk.Label(size_f, text=str(self.model.num_people), width=3).pack(side="left")
        tk.Button(size_f, text="+", command=lambda: self.adjust_group(1)).pack(side="left")

        # Restored grouping by Seat Header (Clean)
        for s in range(1, self.model.num_people + 1):
            seat_items = [i for i in self.model.current_order if i["seat"] == s]
            if seat_items:
                tk.Label(self.order_frame, text=f"{lp['seat']} {s}", font=("Arial", 9, "bold"), bg="#bdc3c7").pack(fill="x", pady=(5,0))
                for idx, item_data in enumerate(self.model.current_order):
                    if item_data['seat'] == s:
                        row = tk.Frame(self.order_frame, bg="white")
                        row.pack(fill="x", pady=1, padx=5)
                        tk.Label(row, text=self.model.trans[item_data['id']][self.model.current_lang], bg="white", font=("Arial", 9)).pack(side="left")
                        tk.Button(row, text="✕", fg="red", bd=0, command=lambda i=idx: self.remove_item(i)).pack(side="right")

        # Payment Section with Tipping
        total = sum(i['price'] for i in self.model.current_order)
        if total > 0:
            total_w_tip = int(total * 1.10)
            tk.Label(self.order_frame, text=f"{lp['total']}: {total} SEK\n(Inc. 10% Tip: {total_w_tip} SEK)", 
                     font=("Arial", 11, "bold"), bg="#ecf0f1", pady=10).pack(side="bottom")
            tk.Button(self.order_frame, text=lp['pay_split'], bg="#2980b9", fg="white", 
                      command=lambda: self.pay(True, total_w_tip)).pack(side="bottom", fill="x", padx=10, pady=2)
            tk.Button(self.order_frame, text=lp['pay_all'], bg="#c0392b", fg="white", 
                      command=lambda: self.pay(False, total_w_tip)).pack(side="bottom", fill="x", padx=10, pady=2)

        self.menu_scroll_frame.update_idletasks()
        self.menu_canvas.config(scrollregion=self.menu_canvas.bbox("all"))

    # --- CONTROLLERS ---
    def pay(self, split, amount):
        msg = f"Paid {amount} SEK."
        if split: msg = f"Each of the {self.model.num_people} people paid {amount // self.model.num_people} SEK."
        messagebox.showinfo("Payment Successful", msg)
        self.model.current_order = []
        self.update_view()

    def set_view(self, cat):
        self.model.view_category = cat
        self.update_view()

    def handle_add(self, item):
        if item['id'] == "i_set_3":
            self.model.building_set = True
            self.model.set_slots = {"cat_start": None, "cat_main": None, "cat_dessert": None}
        elif self.model.building_set:
            if item['cat'] in self.model.set_slots and self.model.set_slots[item['cat']] is None:
                self.model.set_slots[item['cat']] = item['id']
                if all(self.model.set_slots.values()):
                    self.model.add_to_order("i_set_3")
                    self.model.building_set = False
        else:
            self.model.add_to_order(item['id'])
        self.update_view()

    def cancel_set(self):
        self.model.building_set = False
        self.update_view()

    def toggle_filter(self, t):
        if t in self.model.active_filters: self.model.active_filters.remove(t)
        else: self.model.active_filters.add(t)
        self.update_view()

    def adjust_group(self, d):
        v = self.model.num_people + d
        if 1 <= v <= 10: self.model.num_people = v; self.update_view()

    def set_seat(self, s): self.model.active_seat = s; self.update_view()
    def change_lang(self, l): self.model.current_lang = l; self.update_view()
    def remove_item(self, idx): self.model.current_order.pop(idx); self.update_view()

if __name__ == "__main__":
    root = tk.Tk()
    app = GasthausApp(root)
    root.mainloop()