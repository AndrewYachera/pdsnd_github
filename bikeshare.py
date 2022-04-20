import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city_list = ['chicago', 'new york city', 'washington']
    while True:
        try:
            city = str(input('Would you like to see bikeshare data for Chicago, New York City, or Washington? Enter city name: '))
            city = city.lower()
        except:
            print('That\'s not a valid input!')
        else:
            if city.lower() in city_list:
                break
            else:
                print('That\'s not a valid input!')

    # get user input for month (all, january, february, ... , june)
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            month = str(input('Which month would you like to see data for? Please enter one of the following: all, january, february, march, april, may, june: '))
            month = month.lower()
        except:
            print('That\'s not a valid input!')
        else:
            if month.lower() in month_list:
                break
            else:
                print('That\'s not a valid input!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        try:
            day = str(input('Which day would you like to see data for? Please enter one of the following: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday: '))
            day = day.lower()
        except:
            print('That\'s not a valid input!')
        else:
            if day.lower() in day_list:
                break
            else:
                print('That\'s not a valid input!')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month of travel was: ', popular_month)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day of travel was: ', popular_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour of travel was: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most comonly used start station was: ', popular_start)
    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most comonly used end station was: ', popular_end)
    # display most frequent combination of start station and end station trip
    df['round_trip'] = df['Start Station'] + ' + ' + df['End Station']
    popular_trip = df['round_trip'].mode()[0]
    print('The most popular round trip was: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was: ', total_travel_time, ' minutes')
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time was: ', mean_travel_time, ' minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_type_count = df['User Type'].value_counts()
        print('Counts of user types:\n', user_type_count)
        # Display counts of gender
        gender_column = df['Gender'].fillna('N/A')
        print('Gender breakdown:\n', gender_column.value_counts())
        # Display earliest, most recent, and most common year of birth
        earliest_dob = int(df['Birth Year'].min())
        print('The earliest birth year was: ', earliest_dob)
        most_recent_dob = int(df['Birth Year'].max())
        print('The most recent birth year was: ', most_recent_dob)
        most_common_dob = int(df['Birth Year'].mode()[0])
        print('The most common birth year was: ', most_common_dob)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('Gender and Birth Year data not available in this city')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_data(df):
    """Asks user if he/she wants to see raw data. If yes, raw data is displayed five rows at a time"""
    while True:
        try:
            user_info = str(input('Would you like to see raw data? Input yes or no: '))
            user_info = user_info.lower()
        except:
            print('That\'s not a valid input')
        else:
            if user_info == 'yes' or user_info == 'no':
                break
            else:
               print('That\'s not a valid input')
    row = 0
    while user_info == 'yes' and row + 5 < df.shape[0]:
        print(df.iloc[row:row + 5])
        row += 5
        while True:
            try:
                user_info = str(input('Would you like to see raw data? Input yes or no: '))
                user_info = user_info.lower()
            except:
                print('That\'s not a valid input')
            else:
                if user_info == 'yes' or user_info == 'no':
                    break
                else:
                    print('That\'s not a valid input')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
