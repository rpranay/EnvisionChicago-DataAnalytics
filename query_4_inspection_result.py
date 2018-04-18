from utils import jaccard, address_refine, progress
import csv

restaurant_data = {}


def run_food_inspection_result():
    with open('Data/restaurants_60601-60606.csv', newline='', encoding='utf8') as rev:
        r = csv.reader(rev, delimiter=',')
        i = 0
        row_count = len(list(r))
        rev.seek(0)
        for row in r:
            i += 1
            if row[1] == 'name':
                continue
            id = row[0].strip()
            name = row[1].strip()
            address = row[6].strip()
            rating = float(row[4].strip())
            try:
                restaurant_data[id].append(name)
                restaurant_data[id].append(address)
                restaurant_data[id].append(rating)
            except KeyError:
                restaurant_data[id] = []
                restaurant_data[id].append(name)
                restaurant_data[id].append(address)
                restaurant_data[id].append(rating)
                progress(i, row_count, status='Building dictionary from restaurants CSV')

    with open('Data/Food_Inspections.csv', newline='', encoding='utf8') as rev:
        r = csv.reader(rev, delimiter=',')
        i = 0
        end = len(restaurant_data)
        for key, val in restaurant_data.items():
            i += 1
            name1 = val[0]
            address1 = address_refine(val[1])
            if address1 == "":
                continue
            flag = 0
            pass_inspection = 0
            fail_inspection = 0
            conditional_inspection = 0
            rev.seek(0)
            for row in r:
                name2 = row[0].strip()
                address2 = row[1].strip()
                if name1[:1] == name2[:1]:
                    flag = 1
                else:
                    if flag == 1:
                        break
                try:
                    if name1[:4].lower() != name2[:4].lower():
                        continue
                    elif jaccard(name1, name2) < 0.4:
                        continue
                except IndexError:
                    print('Index error')
                if jaccard(address1, address2) >= 0.6:
                    result = row[3].strip().lower()
                    if "pass" in result and "conditions" in result:
                        conditional_inspection += 1
                    elif "pass" in result:
                        pass_inspection += 1
                    elif "fail" in result:
                        fail_inspection += 1
            progress(i, end, status='Integrating Food inspection and Restaurant data')

            restaurant_data[key].append(pass_inspection)
            restaurant_data[key].append(conditional_inspection)
            restaurant_data[key].append(fail_inspection)

    i = 0
    end = len(restaurant_data)
    with open('Results/query_4_result.csv', 'w', newline='', encoding='utf8') as writeFile:
        writer = csv.writer(writeFile, delimiter=',')
        writer.writerow(["Restaurant Name", "Address", "Average Yelp Review", "#Pass", "#Conditional", "#Failed Inspection"])
        for key, val in restaurant_data.items():
            i += 1
            try:
                if val[3] == 0 and val[4] == 0 and val[5] == 0:
                    continue
            except IndexError:
                continue
            writer.writerow(val)
            progress(i, end, status='Writing data to query_4_food_inspection_result.csv')
