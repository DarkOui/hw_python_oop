import datetime as dt


class Record:
    """Преобразование данных в списке Calculator.records"""

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    """Создаем класс калькулятор."""

    def __init__(self, limit):
        """Инициализация общего класса калькулятора."""
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Метод сохранения записей."""
        self.records.append(record)

    def get_today_stats(self):
        """Метод расчета потраченного сегодня."""
        # today_amount = []
        today = dt.date.today()
        today_amount = sum([record.amount for record in self.records
                            if record.date == today])
        # for record in self.records:
        #   if record.date == today:
        #       today_amount.append(record.amount)
        return today_amount

    def get_week_stats(self):
        """Метод расчета, сколько денег потрачено за последние 7 дней."""
        # week_amount = 0
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        week_amount = float(sum([record.amount for record in self.records
                                 if week_ago < record.date <= today]))
        # for record in self.records:
        #    if week_ago < record.date <= today:
        #        week_amount += record.amount
        return week_amount

    def get_remained(self):
        remained = self.limit - self.get_today_stats()
        return remained


class CashCalculator(Calculator):
    """Создаем подкласс - калькулятор денег."""
    USD_RATE = 75.0
    EURO_RATE = 90.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency='rub'):
        """Метод расчета, сколько денег еще можно потратить."""
        currencies = {'usd': ('USD', self.USD_RATE),
                      'eur': ('Euro', self.EURO_RATE),
                      'rub': ('руб', self.RUB_RATE)}
        cash_remained = self.get_remained()
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies.keys():
            return 'Нет такой валюты'
        currency_name, currency_rate = currencies[currency]
        money = round(cash_remained / currency_rate, 2)
        if cash_remained > 0:
            return f'На сегодня осталось {money} {currency_name}'
        return f'Денег нет, держись: твой долг - {abs(money)} {currency_name}'


class CaloriesCalculator(Calculator):
    """Создаем подкласс - калькулятор калорий."""

    def get_calories_remained(self):
        """Метод расчета, сколько ещё калорий можно/нужно получить сегодня."""
        calories_remained = self.get_remained()
        if calories_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с '
                    f'общей калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


# Проверки
# cash_calculator = CashCalculator(1000)
# cash_calculator.add_record(Record(amount=145, comment='кофе'))
# cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# cash_calculator.add_record(Record(amount=3000,
#                                comment='бар в Танин др', date='09.05.2021'))
# print(cash_calculator.get_today_cash_remained('rub'))
# На сегодня осталось 555 руб
# calcM = CashCalculator(10000)
# calcC = CaloriesCalculator(1000)
# calcM.add_record(Record(amount=145.6, comment='Безудержный шопинг'))
# calcM.add_record(Record(amount=1568.9,
#                        comment='Наполнение потребительской корзины'))
# calcM.add_record(Record(amount=691.4, comment='Катание на такси'))
# calcC.add_record(Record(amount=1186, comment='Кусок тортика. И ещё один.'))
# calcC.add_record(Record(amount=84, comment='Йогурт.'))
# calcC.add_record(Record(amount=1140.1, comment='Баночка чипсов.'))
# print(calcM.get_today_cash_remained('evr'))
# print(calcM.get_week_stats())
# print(calcC.get_calories_remained())
