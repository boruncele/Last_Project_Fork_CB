import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {"all":0, 
          "january":1, 
          "february":2, 
          "march":3, 
          "april":4, 
          "may":5, 
          "june":6,
          "july":7, 
          "august":8, 
          "september":9, 
          "october":10, 
          "november":11, 
          "december":12}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
#Added Friend throughout file
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - number of the day, or "all" to apply no day filter
    """
    print('Hello Friend! Let\'s explore some US bikeshare data!')
    print('Before we begin, this experiement is to see what my friend would choose.')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Please choose between Chicago, New York City, and Washington.")
    print("Type a city name below:")
    global MONTHS
    user_input = None
    city = None
    month = None
    day = None
    while True:
        user_input = input()
        if (user_input.lower() == "Chicago".lower()):
            city = 'chicago'
            break
            
        elif (user_input.lower() == "New York City".lower()):
            city = 'new_york_city'
            break
            
        elif (user_input.lower() == "Washington".lower()):
            city = 'washington'
            break
        else:
            print("Invalid city my friend. Must be Chicago, New York City, or Washington")
            
    print(f"user_input: {user_input}")

    # TO DO: get user input for month (all, january, february, ... , june)
    print("Please enter a month or 'all'")
  
    while True:
        user_input = input()
        if (user_input.lower() in MONTHS):
            month = user_input.lower()
            break
        else:
            print("Invalid month. Please enter a valid month or 'all'")
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("Please enter a day as a number (an integer) from 1 to 31, or 'all'")
  
    monthsWithNot30Days = ["february", "april", " june", "september", "november"]
    
    n = 31
    days=np.arange(1, n+1, 1)
    day = 1
    while True:
        user_input = input()
        
        if (user_input.lower() == "all"):
            day = "all"
            break
        
        # Try to convert the user input to an integer
        try:
            day = int(user_input)
        except ValueError:
            day = -1
            print("Invalid day entered, please enter a valid day as a number (an integer) from 1 to 31 or 'all'")
            
        if (day in days):
            if (month in monthsWithNot30Days) and (day > 30):
                print(f"Invalid day entered: {month} has 30 days, you entered {day}, please enter a valid day as a number (an integer) from 1 to 31 or 'all'")
            elif (month == 'february') and (day > 28):
                print(f"Invalid day entered: {month} has 28 days (except on leap years), you entered {day}, please enter a valid day as a number (an integer) from 1 to 31 or 'all'")
            else:
                # Valid day for the given month
                break
        else:
            print("Invalid day entered, please enter a valid day as a number (an integer) from 1 to 31 or 'all'")

    print("You've selected:")
    print(f"\tCity: {city}")
    print(f"\tMonth: {month}")
    print(f"\tday: {day}")
            
    print('-'*40)
    return city, month, day


def load_data(city, month):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Data setup
    df = pd.read_csv(f"{city}.csv")
   
    # Only filter by month if month_num_str is not 'all'
    if (month != 'all'):
        month_number = convert_month_to_number(month)
        month_num_str = f"{month_number:02}"
        df = df[df['Start Time'].str[5:7] == month_num_str]
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day
    df['Hour'] = df['Start Time'].dt.hour
    
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - number of the day, or "all" to apply no day filter
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    if month == 'all':
        # Get string name of month
        month_values, month_counts = np.unique(df['Month'], return_counts=True)
        
        # Check the count list, because it can be empty
        if len(month_counts) != 0:
            i = np.argmax(month_counts)
            most_common_month_num = month_values[i]
            most_common_month_str = None
            for key, value in MONTHS.items():
                if value == most_common_month_num:
                    most_common_month_str = key

            print(f"Most common month: {most_common_month_str}")

    # TO DO: display the most common day of week
    # Interpreting this as most common day (as a number) in a month
    day_values, day_counts = np.unique(df['Day'], return_counts=True) 
    
    # Check the count list, because it can be empty
    if len(day_counts) != 0:
        i = np.argmax(day_counts)
        most_common_day_num = day_values[i]
        print(f"Most common day (as a number) in a month: {most_common_day_num}")

    # TO DO: display the most common start hour
    hour_values, hour_counts = np.unique(df['Hour'], return_counts=True) 
    
    # Check the count list, because it can be empty
    if len(hour_counts) != 0:
        i = np.argmax(hour_counts)
        most_common_hour = hour_values[i]
        print(f"Most common hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_names, start_station_counts = np.unique(df['Start Station'], return_counts=True)
    # Check the count list, because it can be empty
    if len(start_station_counts) != 0:
        i = np.argmax(start_station_counts)
        most_common_start_station = start_station_names[i]
        print(f"Most common start station: {most_common_start_station}")

    # TO DO: display most commonly used end station
    end_station_names, end_station_counts = np.unique(df['End Station'], return_counts=True)
    # Check the count list, because it can be empty
    if len(end_station_counts) != 0:
        i = np.argmax(end_station_counts)
        most_common_end_station = end_station_names[i]
        print(f"Most common end station: {most_common_end_station}")
    
    # TO DO: display most frequent combination of start station and end station trip
    start_and_end_stations = df['Start Station'] + ' to ' + df['End Station']
    trip_names, trip_counts = np.unique(start_and_end_stations, return_counts=True)  
    # Check the count list, because it can be empty
    if len(trip_counts) != 0:
        i = np.argmax(trip_counts)
        most_frequent_station_trip = trip_names[i]
        print(f"Most frequent station trip: {most_frequent_station_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = (df['End Time'] - df['Start Time']).sum()
    print(f"Total travel time: {total_travel_time}")

    # TO DO: display mean travel time
    mean_travel_time = (df['End Time'] - df['Start Time']).mean()
    print(f"Mean travel time: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    
    if 'Subscriber' in user_type_counts:
        num_subscribers = user_type_counts['Subscriber']
    else:
        num_subscribers = 0
        
    if 'Customer' in user_type_counts:
        num_customers = user_type_counts['Customer']
    else:
        num_customers = 0
        
    print(f"Number of subscribers: {num_subscribers}")
    print(f"Number of customers: {num_customers}")

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        if 'Male' in gender_counts:
            num_male = gender_counts['Male']
        else:
            num_male = 0
        if 'Male' in gender_counts:
            num_female = gender_counts['Female']
        else:
            num_female = 0
        print(f"Number of males: {num_male}")
        print(f"Number of females: {num_female}")
        
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        # Earliest year of birth (meaning oldest person effectively)
        earliest_year = df['Birth Year'].min()
        print(f"Earliest year of birth: {earliest_year}")
        
        # Most recent year of birth (youngest person)
        recent_year = df['Birth Year'].max()
        print(f"Most recent year of birth: {recent_year}")

        # Most common year of birth
        if not df['Birth Year'].value_counts().empty:
            most_common_year = df['Birth Year'].value_counts().index[0]
            print(f"Most common year of birth: {most_common_year}")
        else:
            print(f"Most common year of birth: N/A")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

########################################################################################
# Here are helper functions that I have added:
def convert_month_to_number(month):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    Returns:
        (int) month_number - the integer value of the month or -1 if an invalid month was povided
    """
    global MONTHS
    month_number = -1
    
    if (month in MONTHS):
        month_number = MONTHS[month];
    else:
        print(f"Invalid month ({month})!")
    
    return month_number

def show_5_lines_of_data(df):
    """
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    index = 0
    while True:
        print("Would you like to see the next 5 lines of raw data? (yes or no)")
        user_input = input()
        
        if user_input.lower() == "yes":
            if index+5 < len(df):
                print(f"Showing lines {index}:{index+5}")
                print(df.iloc[index:index+5])
            else:
                print(f"Showing lines {index}:{len(df)}")
                print(df.iloc[index:len(df)])
                print("No more data to display!")
                break
                
            index += 5
                
        elif user_input.lower() == "no":
            break
        else:
            print("Invalid reponse. Must be yes or no. Would you like to see the next 5 lines of raw data? (yes or no)")
        
    
########################################################################################
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_5_lines_of_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
