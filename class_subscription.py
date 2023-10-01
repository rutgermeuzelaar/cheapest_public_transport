import sqlite3

PRICE_SINGLE_QBUZZ = 8.81
PRICE_SINGLE_NS = 8.8
transporter_dict = {'NS': PRICE_SINGLE_NS, 'Qbuzz': PRICE_SINGLE_QBUZZ}
time_options = ['spits', 'weekend', 'dal'] 

def get_data(table: str, record_id: int) -> list:
    connection = sqlite3.connect("public_transport.db")
    cursor = connection.cursor()
    params = (record_id,)
    result = cursor.execute("""SELECT * FROM """ + table + """ WHERE record_id=?""", params)
    return result.fetchall()

class Subscription:
    def __init__(self, record_id: int) -> None: 
        self.record_id = record_id
        self.general_data = get_data('general_info', record_id)
        self.cond_one_data = get_data('discount_1_conditions', record_id)
        self.cond_two_data = get_data('discount_2_conditions', record_id)
        self.transporter = self.general_data[0][2]
        self.subscription_name = self.general_data[0][1]
        self.monthly_cost = self.general_data[0][3]
        self.disc_percentage_dict = self.make_disc_percentage_dict()
        self.disc_condition_dict = self.make_disc_condition_dict()

    def make_disc_percentage_dict(self) -> dict:
        disc_percentage_dict = {'discount_1': None, 'discount_2': None}
        disc_percentage_dict['discount_1'] = self.general_data[0][4]
        disc_percentage_dict['discount_2'] = self.general_data[0][5]
        return disc_percentage_dict

    def is_time_period(self, data_row: list) -> list:
        return_list = []
        if data_row[0][1] == 1:
            return_list.append('weekend')
        if data_row[0][2] == 1:
            return_list.append('dal')
        if data_row[0][3] == 1:
            return_list.append('spits')
        return return_list
    
    def make_disc_condition_dict(self) -> dict:
        disc_condition_dict = {'discount_1': None, 'discount_2': None}
        disc_condition_dict['discount_1'] = self.is_time_period(self.cond_one_data)
        disc_condition_dict['discount_2'] = self.is_time_period(self.cond_two_data)
        return disc_condition_dict

    def apply_disc(self, time_period: str) -> float:
        ticket_price = 0
        ticket_price = transporter_dict.get(self.transporter)
        if time_period == None:
            return 0
        for key, value in self.disc_condition_dict.items():
            if time_period in value:
                ticket_price *= 1 - self.disc_percentage_dict.get(key)
        return ticket_price

    def calc_week_total(self, week_dict: dict) -> float:
        week_total = 0
        for value in week_dict.values():
            week_total += self.apply_disc(value)
        return week_total * 2

class NoSubscription:
    def __init__(self, transporter: str) -> None:
        self.transporter = transporter
        self.ticket_price = transporter_dict.get(self.transporter)
        self.week_total = 0
        
    def calculate_week_cost(self, week_dict: dict):
        self.week_total = 0
        for value in week_dict.values():
            if value != None:
                self.week_total += self.ticket_price
        return self.week_total * 2

# method to go from database to dictionaries
# if time period is not None but also not in disc_dict -> use regular ticket price
week_1 = {'mo': None, 'tu': None, 'we': 'dal', 'th': None, 'fr': None, 'sa': None, 'su': None}
test_1 = Subscription(1)
print(test_1.calc_week_total(week_1))
