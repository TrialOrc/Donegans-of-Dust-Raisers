class Clock():
    """docstring for Clock."""

    def __init__(self, years, months, days, hours, minutes):
        self.years = years
        self.months = months
        self.days = days
        self.hours = hours
        self.minutes = minutes

        self.month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                           5: 'May', 6: 'June', 7: 'July', 8: 'August',
                           9: 'September', 10: 'October', 11: 'November',
                           12: 'December'}

    def am_or_pm(self):
        if self.hours >= 12:
            return 'PM'
        else:
            return 'AM'

    def check_month_for_days(self):
        if self.months == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            return 31
        elif self.months == 4 or 6 or 9 or 11:
            return 30
        elif self.months == 2 and self.years % 4 == 0:
            if self.years % 100 != 0 and self.years % 400:
                return 29
            elif self.years % 100 == 0:
                return 28
        else:
            return 28

    def twelve_hour_clock(self):
        if self.hours % 12 > 0:
            return self.hours % 12
        else:
            return 12


# game_time = Clock(1800, 1, 1, 1, 20)
# month_name = game_time.month_name
# print(f'{game_time.days:02d} {month_name[int(game_time.months)][:3]} {game_time.years} {game_time.twelve_hour_clock()}:{game_time.minutes:02d} {game_time.am_or_pm()}')
