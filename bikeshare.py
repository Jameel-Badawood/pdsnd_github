import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, Washington?').title()
            if city not in ['Chicago', 'New York City', 'Washington']:
                print('Please enter one of three cities again')
                continue
            break
        except ValueError:
            print('Try Again')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Which month would you like to filter the data by? All, January, February, March, April, May,or June ?').title()
            if month not in ['All', 'January', 'February', 'March', 'April', 'May', 'June']:
                print('Please enter one of six months again')
                continue
            break
        except ValueError:
            print('Try Again')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Which day would you like to filter the data by? All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday ?').title()
            if day not in ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
                print('Please enter one of seven days again')
                continue
            break
        except ValueError:
            print('Try Again')
            continue
        else:
            continue


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
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Start Time'].dt.month_name().mode()[0]
    print('\n What is the most popular month for traveling? \n', popular_month)


    # display the most common day of week
    popular_day = df['Start Time'].dt.day_name().mode()[0]
    print('\n What is the most popular day for traveling? \n', popular_day)


    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print('\n What is the most popular hour of the day to start your travels? \n', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('\n The most popular start station is:\n',popular_start_station)


    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('\n The most popular end station is:\n',popular_end_station)


    # display most frequent combination of start station and end station trip
    df['Popular Trip'] = df['Start Station'] +"  " +df['End Station']
    popular_trip = df['Popular Trip'].value_counts().idxmax()
    print('\n what was the most popular trip from start to end?\n',popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'],unit='s')
    tot_travel_time = df['Trip Duration'].sum()
    print('\n What was the total traveling time spent on each trip? \n', tot_travel_time)


    # display mean travel time
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'],unit='s')
    avg_travel_time = df['Trip Duration'].mean()
    print('\n What was the mean traveling time spent on each trip? \n', avg_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nWhat is the breakdown of users? \n",user_types)


    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("\nWhat is the breakdown of users? \n",gender_types)
    except KeyError:
        print("\nWhat is the breakdown of gender? \n")
        print('No gender data to share')


    # Display earliest, most recent, and most common year of birth
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        popular_birth_year = int(df['Birth Year'].mode()[0])

        print("\nWhat is the oldest, youngest, and most popular year of birth, respectively? \n")
        print('oldest: ',oldest)
        print('\n youngest: ',youngest)
        print('\n most popular year of birth:',popular_birth_year)
    except KeyError:
        print("\nWhat is the oldest, youngest, and most popular year of birth, respectively? \n")
        print('No birth year data to share')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays statistics on bikeshare individual trip data."""

    print('\nCalculating Raw Stats...\n')
    start_time = time.time()

    # Display rew data

    while True:
        try:
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n')
            start_loc = 0
            end_loc =5
            while view_data.lower() == 'yes':
                print(df.iloc[start_loc:end_loc])
                start_loc +=5
                end_loc +=5
                view_display = input("Do you wish to continue?: Enter yes or no.\n").lower()
                if view_display != 'yes':
                    break
                continue
            break
        except ValueError:
            print('Try Again')
            continue



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

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
