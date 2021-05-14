import datetime as dt


class Record:
    """Преобразование данных в списке Calculator.records."""

    def __init__(self, amount: float, comment: str, date: str = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    """Создаем класс калькулятор."""

    def __init__(self, limit: float):
        """Инициализация общего класса калькулятора."""
        self.limit = limit
        self.records: list = []

    def add_record(self, record):
        """Метод сохранения записей."""
        self.records.append(record)

    def get_today_stats(self):
        """Метод расчета потраченного сегодня."""
        today = dt.date.today()
        today_amount = sum(record.amount for record in self.records
                           if record.date == today)
        return today_amount

    def get_week_stats(self):
        """Метод расчета, сколько денег потрачено за последние 7 дней."""
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        week_amount = sum(record.amount for record in self.records
                          if week_ago < record.date <= today)
        return week_amount

    def get_remained(self):
        remained = self.limit - self.get_today_stats()
        return remained


class CashCalculator(Calculator):
    """Создаем подкласс - калькулятор денег."""
    USD_RATE: float = 75.0
    EURO_RATE: float = 90.0
    RUB_RATE: float = 1.0

    def get_today_cash_remained(self, currency='rub'):
        """Метод расчета, сколько денег еще можно потратить."""
        cash_remained = self.get_remained()
        if cash_remained == 0:
            return 'Денег нет, держись'
        currencies = {'usd': ('USD', self.USD_RATE),
                      'eur': ('Euro', self.EURO_RATE),
                      'rub': ('руб', self.RUB_RATE)}
        if currency not in currencies:
            return 'Нет такой валюты'
        currency_name, currency_rate = currencies[currency]
        money = round(cash_remained / currency_rate, 2)
        amoney = abs(money)
        if cash_remained > 0:
            return f'На сегодня осталось {money} {currency_name}'
        return f'Денег нет, держись: твой долг - {amoney} {currency_name}'


class CaloriesCalculator(Calculator):
    """Создаем подкласс - калькулятор калорий."""

    def get_calories_remained(self):
        """Метод расчета, сколько ещё калорий можно/нужно получить сегодня."""
        calories_remained = self.get_remained()
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с '
                    f'общей калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'
