import datetime


def christmas_countdown():
    # Get the current date and time
    now = datetime.datetime.now()

    # Calculate the date for Christmas this year
    christmas = datetime.datetime(now.year, 12, 25)

    # Check if Christmas has already passed this year
    if now > christmas:
        christmas = christmas.replace(year=now.year + 1)

    # Calculate the time remaining until Christmas
    time_until_christmas = christmas - now

    # Extract days, hours, minutes, and seconds
    days = time_until_christmas.days
    seconds = time_until_christmas.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # Create a dictionary to store the countdown values
    countdown_values = {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }

    return countdown_values


if __name__ == "__main__":
    christmas_countdown()
