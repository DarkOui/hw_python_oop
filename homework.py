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
    """Создаем класс калькулятор"""
    def __init__(self, limit):
        """Инициализация общего класса калькулятора"""
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week_ago = self.today - dt.timedelta(7)

    def add_record(self, record):
        """Метод сохранения записей"""
        self.records.append(record)

    def get_today_stats(self):
        """Метод расчета потраченного сегодня"""
        today_amount = 0
        for record in self.records:
            if record.date == self.today:
                today_amount += record.amount
        return today_amount

    def get_week_stats(self):
        """Метод рассчета, сколько денег потрачено за последние 7 дней"""
        week_amount = 0
        for record in self.records:
            if self.week_ago <= record.date <= self.today:
                week_amount += record.amount
        return week_amount


class CashCalculator(Calculator):
    """Создаем подкласс - калькулятор денег"""
    USD_RATE = float(75)
    EURO_RATE = float(90)
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rub'):
        """Метод расчета, сколько денег еще можно потратить"""
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        cash_remained = self.limit - self.get_today_stats()
        currency_name, currency_rate = currencies[currency]
        money = abs(round(cash_remained / currency_rate))
        if cash_remained == 0:
            return('Денег нет, держись')
        if cash_remained > 0:
            return f'На сегодня осталось {money} {currency_name}'
        else:
            return f'Денег нет, держись: твой долг - {money} {currency_name}'


class CaloriesCalculator(Calculator):
    """Создаем подкласс - калькулятор калорий"""
    def get_calories_remained(self):
        """Метод рассчета, сколько ещё калорий можно/нужно получить сегодня"""
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с '
                    f'общей калорийностью не более {calories_remained} кКал')
        else:
            return ('Хватит есть!')


cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др', date='09.05.2021'))
print(cash_calculator.get_today_cash_remained('rub'))
# На сегодня осталось 555 руб
calcM = CashCalculator(10000)
calcC = CaloriesCalculator(10000)
calcM.add_record(Record(amount=145.6, comment='Безудержный шопинг'))
calcM.add_record(Record(amount=1568.9,
                        comment='Наполнение потребительской корзины'))
calcM.add_record(Record(amount=691.4, comment='Катание на такси'))
calcC.add_record(Record(amount=1186, comment='Кусок тортика. И ещё один.'))
calcC.add_record(Record(amount=84, comment='Йогурт.'))
calcC.add_record(Record(amount=1140.1, comment='Баночка чипсов.'))
print(calcM.get_today_cash_remained('rub'))
print(calcM.get_week_stats())
print(calcC.get_calories_remained())
