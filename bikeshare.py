import time
import calendar as ca
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def convert_city_input(invalid_city):
    """
    Coverts a invalid city input to a vaild city input

    Args:
        (str) invaild_city - input for name of the city to filter by which was not vaild
    Returns:
        (str) valid_city - valid name of the city to filter by
    """
    valid_city = ''

    if invalid_city == 'new york':
        valid_city = 'new york city'

    if invalid_city == 'dc':
        valid_city = 'washington'

    return valid_city


def convert_month_input(invalid_month):
    """
    Coverts a invalid month input to a vaild month input

    Args:
        (str) invaild_month - input for name of the month to filter by which was not vaild
    Returns:
        (int) valid_month - 9: all, 1: January, 2: February, 3: March ...
    """
    valid_month = ''

    if invalid_month == 'jan' or invalid_month == '1' or invalid_month == 'january':
        valid_month = 1

    if invalid_month == 'feb' or invalid_month == '2' or invalid_month == 'february':
        valid_month = 2

    if invalid_month == 'mar' or invalid_month == '3' or invalid_month == 'march':
        valid_month = 3

    if invalid_month == 'apr' or invalid_month == '4' or invalid_month == 'april':
        valid_month = 4

    if invalid_month == '5' or invalid_month == 'may':
        valid_month = 5

    if invalid_month == 'jun' or invalid_month == '6' or invalid_month == 'june':
        valid_month = 6

    if invalid_month == 'all':
        valid_month = 9

    return valid_month


def convert_day_input(invalid_day):
    """
    Coverts a invalid day input to a vaild day input

    Args:
        (str) invaild_day - input for name of the day to filter by which was not vaild
    Returns:
        (int) valid_day - 9: all, 0: Monday, 1: Tuesday, ..., 6: Sunday
    """
    valid_day = ''

    if invalid_day == 'mon' or invalid_day == '1' or invalid_day == 'monday':
        valid_day = 0

    if invalid_day == 'tue' or invalid_day == '2' or invalid_day == 'tuesday':
        valid_day = 1

    if invalid_day == 'wed' or invalid_day == '3' or invalid_day == 'wednesday':
        valid_day = 2

    if invalid_day == 'thu' or invalid_day == '4' or invalid_day == 'thursday':
        valid_day = 3

    if invalid_day == 'fri' or invalid_day == '5' or invalid_day == 'friday':
        valid_day = 4

    if invalid_day == 'sat' or invalid_day == '6' or invalid_day == 'saturday':
        valid_day = 5

    if invalid_day == 'sun' or invalid_day == '7' or invalid_day == 'sunday':
        valid_day = 6

    if invalid_day == 'all':
        valid_day = 9

    return valid_day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - number of the month to filter by or 9 to apply no month filter
        (int) day - number of the day of week to filter by or 9 to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
    valid_city_input = ['chicago', 'new york city', 'washington']
    city = input('Would you like to see data for Chicago, New York, or Washington? ').lower()

    if city not in valid_city_input:
        city = convert_city_input(city)

    while city not in valid_city_input:
        city = input('Your input was invalid. Please enter either Chicago, New York or Washington: ').lower()
        if city not in valid_city_input:
            city = convert_city_input(city)

    # get user input for month and safe input as number of each month
    valid_month_input = [1, 2, 3, 4, 5, 6, 9]
    month = input('Do you want to filter by month?\nIf yes, which month - January, February, March, April, May, or June?\nIf no, than tip \'all\'.\n').lower()

    # check if user input can be converted to a valid user input
    if month not in valid_month_input:
        month = convert_month_input(month)

    while month not in valid_month_input:
        month = input('Your input was invalid. Please enter a month or all: ').lower()
        if month not in valid_month_input:
            month = convert_month_input(month)

    # get user input for day of week
    valid_day_input = [0, 1, 2, 3, 4, 5, 6, 9]
    day = input('Do you want to filter by day?\nIf yes, which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\nIf no, than tip \'all\'.\n').lower()

    if day not in valid_day_input:
        day = convert_day_input(day)

    while day not in valid_day_input:
        day = input('Your input is invalid. Please enter a day or all: ').lower()
        if day not in valid_day_input:
            day = convert_day_input(day)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - number of the month to filter by or 9 to apply no month filter
        (int) day - number of the day of week to filter by or 9 to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # import csv from selected city
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time and End Time into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #create new colums to display only month, day of week and hour of the Start Time
    df['this_month'] = df['Start Time'].dt.month
    df['this_day'] = df['Start Time'].dt.dayofweek
    df['this_hour'] = df['Start Time'].dt.hour

    # filter just by month
    if month != 9 and day == 9:
        df = df[df['this_month'] == month]

    # filter just by day
    if day != 9 and month == 9:
        df = df[df['this_day'] == day]

    # filter by month and day
    if month != 9 and day != 9:
        df = df[df['this_month'] == month]
        df = df[df['this_day'] == day]

    #print(df.head(10))

    return df


def convert_to_weekday(day_number):
    """"
    Converts the number of the weekday to the name of the weekday

    Args:
        (int) day_number - number that relates to the weekday
    Returns:
        (str) - name of the weekday
    """
    if day_number == 0:
        return "Monday"
    if day_number == 1:
        return "Tuesday"
    if day_number == 2:
        return "Wednesday"
    if day_number == 3:
        return "Thursday"
    if day_number == 4:
        return "Friday"
    if day_number == 5:
        return "Saturday"
    if day_number == 6:
        return "Sunday"


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # displays only when the data is not filtered by month
    if df.this_month.nunique() > 1 :
        common_month = df['this_month'].mode()[0]
        print('Most Common Month:', ca.month_name[common_month])

    # display the most common day of week
    # displays only when the data ist not filtered by day
    if df.this_day.nunique() > 1 :
        common_day = df['this_day'].mode()[0]
        print('Most Common Day of the Week:', convert_to_weekday(common_day))

    # display the most common start hour
    common_hour = df['this_hour'].mode()[0]
    print('Most Common Start Hour:', common_hour, 'o\'clock')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end)

    # display most frequent combination of start station and end station trip
    print('Most frequent combination:', df.groupby(['Start Station','End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def convert_seconds(time_in_sec):
    """
    Converts time in seconds into time in hours, minutes, seconds

    Args:
        (int) time_in_sec - time in seconds
        (str) - time in hours, minutes, seconds formatted
    """
    m, s = divmod(time_in_sec, 60)
    h, m = divmod(m, 60)

    return '{:d}:{:02d}:{:02d}'.format(h, m, s)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # converted to int, because there is no need to see the total sum and mean
    # travel time in a smaller unit than seconds

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print('Total Travel Time:', convert_seconds(total_travel_time))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('Mean Travel Time:', convert_seconds(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types:')
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns and 'Birth Year' in df.columns:

        # Display counts of gender
        print('\nGender:')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth:', int(df['Birth Year'].min()))

        print('Most recent year of birth:', int(df['Birth Year'].max()))

        common_year = int(df['Birth Year'].mode()[0])
        print('Most common year of birth:', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_data = input('\nWould you like to see the first 5 lines of data? Enter yes or no.\n')
        i = 0
        j = 5
        while view_data.lower() == 'yes':
            print(df.iloc[i:j])
            view_data = input('\nWould you like to see the next more 5 lines of data? Enter yes or no.\n')
            i += 5
            j += 5


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
