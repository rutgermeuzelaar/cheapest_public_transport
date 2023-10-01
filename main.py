import class_subscription
import sqlite3

connection = sqlite3.connect("public_transport.db")
cursor = connection.cursor()
result = cursor.execute("""
                SELECT record_id FROM general_info
                        """)
result_list = result.fetchall()
max_record = len(result_list)

# Supply travel week as a dictionary
week_1 = {'mo': 'spits', 'tu': 'spits', 'we': 'spits', 'th': 'spits', 'fr': None, 'sa': None, 'su': None}
week_2 = {'mo': None, 'tu': 'spits', 'we': 'spits', 'th': 'spits', 'fr': 'spits', 'sa': None, 'su': None}
week_3 = {'mo': 'spits', 'tu': 'spits', 'we': 'spits', 'th': 'spits', 'fr': None, 'sa': None, 'su': None}
week_4 = {'mo': 'spits', 'tu': 'spits', 'we': 'spits', 'th': 'spits', 'fr': 'spits', 'sa': None, 'su': None}
month_list = [week_1, week_2, week_3, week_4]
month_cost_dict = {}
cheapest_ns_list = []
cheapest_qbuzz_list = []
for record_id in range(1, max_record + 1):
    month_cost_dict.setdefault(record_id)
    month_total_with_subscription = 0
    subscription = class_subscription.Subscription(record_id)
    for week in month_list:
        month_total_with_subscription += subscription.calc_week_total(week)
    month_cost_dict[record_id] = round(month_total_with_subscription + subscription.monthly_cost, 2)

for test in sorted(month_cost_dict, key=month_cost_dict.get):
    if test in range(1, 8):
        cheapest_qbuzz_list.append(test)
    else:
        cheapest_ns_list.append(test)

# Calculate month_total without a subscription
month_total_no_subscription_ns = 0
month_total_no_subscription_qbuzz = 0
no_subscription_ns = class_subscription.NoSubscription('NS')
no_subscription_qbuzz = class_subscription.NoSubscription('Qbuzz')

for week in month_list:
    month_total_no_subscription_ns += no_subscription_ns.calculate_week_cost(week)
    month_total_no_subscription_qbuzz += no_subscription_qbuzz.calculate_week_cost(week)
print(f"The cost of this configuration with no Qbuzz subscription is {round(month_total_no_subscription_qbuzz, 2)}.")
print(f"The cost of this configuration with no NS subscription is {round(month_total_no_subscription_ns, 2)}.\n")

# Cheapest subscriptions
cheapest_qbuzz_subscription_record_id = cheapest_qbuzz_list[0]
cheapest_qbuzz_subscription = class_subscription.Subscription(cheapest_qbuzz_subscription_record_id)
cheapest_ns_subscription_record_id = cheapest_ns_list[0]
cheapest_ns_subscription = class_subscription.Subscription(cheapest_ns_subscription_record_id)

# Is there a subscription cheaper, if so, which?
if month_total_no_subscription_qbuzz > month_cost_dict.get(cheapest_qbuzz_subscription_record_id):
    print(f"The cheapest Qbuzz subscription for this configuration is: "
          f"{cheapest_qbuzz_subscription.subscription_name}, whichs costs: {month_cost_dict.get(cheapest_qbuzz_subscription_record_id)}.")
    print(f"You save {round(month_total_no_subscription_qbuzz - month_cost_dict.get(cheapest_qbuzz_subscription_record_id), 2)} this month by using this subscription.")
if month_total_no_subscription_ns > month_cost_dict.get(cheapest_ns_subscription_record_id):
    print(f"The cheapest NS subscription for this configuration is: "
          f"{cheapest_ns_subscription.subscription_name}, whichs costs: {month_cost_dict.get(cheapest_ns_subscription_record_id)}.")
    print(f"You save {round(month_total_no_subscription_ns - month_cost_dict.get(cheapest_ns_subscription_record_id), 2)} this month by using this subscription.")
print(month_cost_dict)