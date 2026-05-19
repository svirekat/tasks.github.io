import csv
from datetime import datetime

filename = "5-1.csv"

MONTHS_RU = {
    'январь': 'january', 'февраль': 'february', 'март': 'march', 'апрель': 'april',
    'май': 'may', 'июнь': 'june', 'июль': 'july', 'август': 'august',
    'сентябрь': 'september', 'октябрь': 'october', 'ноябрь': 'november', 'декабрь': 'december'
}

def parse_russian_date(date_str):
    for ru, en in MONTHS_RU.items():
        if ru in date_str.lower():
            date_str = date_str.lower().replace(ru, en)
            break
    return datetime.strptime(date_str, '%d %B %Y %H:%M')

def find_question_columns(header):
    col_q1 = col_q2 = col_q3 = None
    for col in header:
        if 'В. 1' in col:
            col_q1 = col
        elif 'В. 2' in col:
            col_q2 = col
        elif 'В. 3' in col:
            col_q3 = col
    return col_q1, col_q2, col_q3

def main():
    input_date_str = input("введите дату в формате ДД.ММ.ГГГГ: ").strip()
    try:
        spec_date = datetime.strptime(input_date_str, "%d.%m.%Y")
        spec_date = spec_date.replace(hour=0, minute=0, second=0)
    except ValueError:
        print("ошибка: дата должна быть в формате ДД.ММ.ГГГГ")
        return

    col_status = "Состояние"
    col_completed = "Завершено"

    wrong_ans1 = 0
    wrong_ans2 = 0
    wrong_ans3 = 0

    if filename == "5-1.csv":
        maximum = 1.0
    elif filename == "5-2.csv":
        maximum = 10.0
    else:
        return 
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            if filename == "5-1.csv":
                maximum = 1.0
            elif filename == "5-2.csv":
                maximum = 10.0
            else:
                return 

            reader = csv.DictReader(f, delimiter=',')
            col_q1, col_q2, col_q3 = find_question_columns(reader.fieldnames)

            for row in reader:
                if row.get(col_status) != "Завершено":
                    continue
                completed_str = row.get(col_completed, '').strip()
                if not completed_str:
                    continue
                try:
                    completed_date = parse_russian_date(completed_str)
                except:
                    continue

                if completed_date <= spec_date:
                    continue

                try:
                    q1 = float(row.get(col_q1, 0).replace(',', '.'))
                    q2 = float(row.get(col_q2, 0).replace(',', '.'))
                    q3 = float(row.get(col_q3, 0).replace(',', '.'))
                except:
                    continue

                if q1 < maximum:
                    wrong_ans1 += 1
                if q2 < maximum:
                    wrong_ans2 += 1
                if q3 < maximum:
                    wrong_ans3 += 1

        print(f"неверных ответов по теме «Основы законодательства РФ в области образования» (В.1 и В.2): {wrong_ans1 + wrong_ans2}")
        print(f"В.1: {wrong_ans1}")
        print(f"В.2: {wrong_ans2}")
        print(f"неверных ответов по теме «Экономико-правовое регулирование педагогической деятельности» (В.3): {wrong_ans3}")

    except FileNotFoundError:
        print(f"файл {filename} не найден")
    except Exception as e:
        print(f"ошибка: {e}")

if __name__ == "__main__":
    main()