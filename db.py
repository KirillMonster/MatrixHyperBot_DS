import sqlite3
from humanize import intcomma
  
db = sqlite3.connect("server.db")
sql = db.cursor()

# embed color
embed_color = 0x00eeff
# new user
start_cash = 20000
start_bank = 10000
start_lvl = 1
start_rep = 1
start_rtx3060 = 1
start_rtx3070 = 0
start_rtx3080 = 0
start_rtx3090 = 0
start_hypercoin = 0
# emoji
emoji_cash = ':leaves:'
emoji_lvl = ':high_brightness:'
emoji_rep = ':fist:'
# shop
price_rtx_3060 = 100000
price_rtx_3070 = 200000
price_rtx_3080 = 400000
price_rtx_3090 = 550000
sell_rtx_3060 = 50000
sell_rtx_3070 = 100000
sell_rtx_3080 = 200000
sell_rtx_3090 = 275000
items_price = [{'rtx3060': price_rtx_3060, 'rtx3070': price_rtx_3070, 'rtx3080': price_rtx_3080, 'rtx3090': price_rtx_3090}]
items_sell = [{'rtx3060': sell_rtx_3060, 'rtx3070': sell_rtx_3070, 'rtx3080': sell_rtx_3080, 'rtx3090': sell_rtx_3090}]
# bank 
percent = 0.05
# clan
clan_cost = 50000
# other
def not_money(ctx, price, cash):
    return f'**{ctx.author}**, недостаточно средств, нехватает - **{adv_num(price-cash)}**{emoji_cash}'

# Tables  
def create_users():
    sql.execute('''CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id_bot INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id INT,
        clan_id INT,
        cash BIGINT,
        bank BIGINT,
        rep INT,
        lvl INT,
        rtx3060 INT,
        rtx3070 INT,
        rtx3080 INT,
        rtx3090 INT,
        hypercoin INT
    )''')
    db.commit()

def create_auc():
    sql.execute('''CREATE TABLE IF NOT EXISTS auction (
            name TEXT,
            id_bot INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            id INT,
            cost BIGINT,
            item TEXT
        )''')
    db.commit()

def create_pay():
    sql.execute('''CREATE TABLE IF NOT EXISTS donate (
            name TEXT,
            id_bot INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            id INT,
            amount INT,
            bild_id VARCHAR,
            status TEXT
        )''')
    db.commit()
    
def create_clans():
    sql.execute('''CREATE TABLE IF NOT EXISTS clans (
            name TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            id_owner INT,
            money BIGINT
        )''')
    db.commit()

def create_crypto():
    sql.execute('''CREATE TABLE IF NOT EXISTS crypto (
            name TEXT,
            cost BIGINT
        )''')
    db.commit()    

# log
def log(system, log, user):
    return f'[LOG]\nSystem: **{system}**\nUser: **{user}**\nContent:\n**{log}**'

# Клан
def check_clan(clan_id):
    if sql.execute('SELECT `clan_id` FROM `users` WHERE `clan_id` = ?',(clan_id,)).fetchone() is None:return False
    else:return True

def clan_users(clan_id):
    return sql.execute('SELECT name FROM `users` WHERE `clan_id` = ?',(clan_id,)).fetchall()[0]

def get_clan(item, value, name):
    return sql.execute(f'SELECT `{item}` FROM `clans` WHERE `{value}` = ?',(name,)).fetchone()[0]

def check_clan_name(name):
    if sql.execute('SELECT `id` FROM `clans` WHERE `name` = ?',(name,)).fetchone() is None:return True
    else:return False

def check_clan_count(user_id):
    if sql.execute('SELECT `clan_id` FROM `users` WHERE `id` = ?',(user_id,)).fetchone()[0] is None:return True
    else:return False

def new_clan(name, user):
    sql.execute("INSERT INTO clans VALUES (?, ?, ?, ?)", (name, None, user.id, 0,))
    db.commit()

def del_clan(clan_id):
    sql.execute('DELETE FROM `clans` WHERE `id` = ?',(clan_id,))
    db.commit()    

# Crypto
def check_crypto(item):
    return sql.execute(f'SELECT `cost` FROM `crypto` WHERE `name` = ?',(item,)).fetchone()

def item_crypto(item):
    return sql.execute(f'SELECT `cost` FROM `crypto` WHERE `name` = ?',(item,)).fetchone()[0]

def new_crypto(item, cost):
    sql.execute(f"INSERT INTO crypto VALUES (?, ?)", (item, cost,))
    db.commit()

# Donate
def new_pay(user, amount, bill_id, status):
    sql.execute("INSERT INTO donate VALUES (?, ?, ?, ?, ?, ?)", (str(user), None, user.id, amount, bill_id, status,))
    db.commit()

def get_pay(bill_id):
    return sql.execute('SELECT * FROM `donate` WHERE `bill_id` = ?',(bill_id,)).fetchone()[0]

def all_pays(user_id):
    return sql.execute(f'SELECT `bill_id, status` FROM `users` WHERE `id` = ?',(user_id,)).fetchone()[0]

def status_pay(bill_id):
    pass

def delete_pay(bill_id):
    sql.execute('DELETE FROM `donate` WHERE `bill_id` = ?',(bill_id,))
    db.commit()

# Adv
def adv_num(number):
    return intcomma(number).replace(",", ".")

def adv_item(item):
    return item.replace("rtx3060", "RTX 3060").replace("rtx3070", "RTX 3070").replace("rtx3080", "RTX 3080").replace("rtx3090", "RTX 3090")

# User
def item_user(item, user_id):
    return sql.execute(f'SELECT `{item}` FROM `users` WHERE `id` = ?',(user_id,)).fetchone()[0]

def count_items(user_id):
    return int(adv_num(item_user('rtx3060', user_id)) + adv_num(item_user('rtx3070', user_id)) + adv_num(item_user('rtx3080', user_id)) + adv_num(item_user('rtx3090', user_id)))

def give_user(item, count, user_id):
    sql.execute(f'UPDATE `users` SET `{item}` = {item} + ? WHERE `id` = ?',(count,user_id,))
    db.commit()
    
def take_user(item, count, user_id):
    sql.execute(f'UPDATE `users` SET `{item}` = {item} - ? WHERE `id` = ?',(count,user_id,))
    db.commit()

def new_user(member):
    sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(member), None, member.id, None, start_cash, start_bank, start_rep, start_lvl, start_rtx3060, start_rtx3070, start_rtx3080, start_rtx3090, start_hypercoin,))
    db.commit()

def set_user(item, value, user_id):
    sql.execute(f'UPDATE `users` SET `{item}` = {value} WHERE `id` = ?',(user_id,))
    db.commit()

def check_user(user_id):
    if sql.execute(f'SELECT id FROM users WHERE id = ?',(user_id,)).fetchone() is None:return True
    else:return False

def top_user(item):
    return sql.execute(f'SELECT name, {item} FROM users ORDER BY {item} DESC LIMIT 10')

def top_auc():
    return sql.execute('SELECT name, item, cost, id_bot FROM auction')

def all_count_users(): 
    return sql.execute(f"SELECT COUNT() FROM users WHERE id").fetchone()[0]

def all_users():
    return sql.execute(f"SELECT id FROM users WHERE id")

# Auc 
def new_auc(user, user_id, cost, item):
    sql.execute(f"INSERT INTO auction VALUES (?, ?, ?, ?, ?)", (str(user), None, user_id, cost, item,))
    db.commit()

def del_auc(item_id):
    sql.execute(f'DELETE FROM auction WHERE id_bot = ?',(item_id,))
    db.commit()    
    
def check_auc(item_id):
    if sql.execute(f'SELECT id_bot FROM auction WHERE id_bot = ?',(item_id,)).fetchone() is None:return False
    else:return True
    
def get_auc(item_id):
    auc_data = []
    for i in sql.execute(f'SELECT cost, id FROM auction WHERE id_bot = ?',(item_id,)).fetchone():
        auc_data.append(i)
    return auc_data
