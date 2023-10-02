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

    # Print the countdown
    print(f"Time until Christmas: {time_until_christmas}")

if __name__ == "__main__":
    christmas_countdown()
