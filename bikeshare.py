import time
import datetime as dt
import pandas as pd
import numpy as np

# Declare global variables.

CITIES = { 'c': 'chicago.csv',
           'n': 'new_york_city.csv',
           'w': 'washington.csv' }

MONTHS = { 'all' : [1, 2, 3, 4, 5, 6],
           'jan' : 1,
           'feb' : 2,
           'mar' : 3,
           'apr' : 4,
           'may' : 5,
           'jun' : 6 }

DAYS = { 'all' : [0, 1, 2, 3, 4, 5, 6],
         'mon' : 0,
         'tue' : 1,
         'wed' : 2,
         'thu' : 3,
         'fri' : 4,
         'sat' : 5,
         'sun' : 6  }

def user_input (question, valid_answers):
    """
    Takes in a string question and a set of valid answers and repeatadly
    prompts the user with the question until they have entered an answer
    from the valid ansers list.

    Args:
        question (str) : Any string used as a question to prompt user input.
        valid_ansers: A list of valid answers from which the user much choose.
    Return:
        answer: The answer, in lowercase, string format, entered by the user.
    """


    answer = '' # Start the while loop with a blank answer.

    while answer not in valid_answers: # User hasn't provided an answer within the valid answer list.
        answer = input(str(question)).lower() # Do comparisons in lowercase to be safe and consistent.
        if answer not in valid_answers: # User still hasn't provided an answer within the valid answer list.
                if input('An invalid answer was given. Would you like to try again? [y/n] ')[0] != 'y':
                    break # User does not want to try, return nothing.
    return answer

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    
    
    # Get user input for city.
    
    city = user_input('Please select a city - [c] for Chicago, [n] for New York City or [w] for Washington: ', list(CITIES.keys()))
    if city not in list(CITIES.keys()):
        return 'Invalid', 'Invalid', 'Invalid'  # A valid city wasn't chosen, so exit now.
    
    # Get user input for month.

    month = user_input('Please select a month - [all, jan, feb, mar, apr, may or jun]: ', list(MONTHS.keys()))
    if month not in list(MONTHS.keys()):
        return city, 'Invalid', 'Invalid' # A valid city was chosen but not a valid month.
    
    # Get user input for day of week.

    day = user_input('Please select a day - [mon, tue, wed, thu, fri, sat or sun]: ', list(DAYS.keys()))
    if day not in list(DAYS.keys()):
        return city, month, 'Invalid' # A valid city and month were chosen but not a valid day.

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
    # Note the csv files must be in the same directory as this python script.
    
    try:
        df = pd.read_csv(CITIES[city], index_col=[0]) # Having reviewed the CSV files, the first column appears to be an index column.
    except:
        print('An unexpected error has occured. Please check if the file exists in the directory')
        return [] # Return an empty list so no further functions are called.

    # Now filter by the selected month and day.

    if month != 'all': # A specific month was chosen. Otherwise assume 'all' was chosen and don't filter.
        try:
            month_number = MONTHS[month] # Lookup the numeric value for the month from our global dictionary.
            df = df[(pd.DatetimeIndex(df['Start Time']).month == month_number)] # Filter the dataframe to include only data from that month.
        except:
            print('An unexpected error has occured.') # These errors are generic for brevity's sake. No need for verbose error messaging.
            return [] # Return an empty list so no further functions are called.

    if day != 'all': # A specific day was chosen. Otherwise assume 'all' was chosen and don't filter.
        try:
            day_number = DAYS[day] # Lookup the numeric value for the day from our global dictionary.
            df = df[(pd.DatetimeIndex(df['Start Time']).dayofweek == day_number)] # Filter the datetime to include only data for this day.
        except:
            print('An unexpected error has occured.')
            return [] # Return an empty list so no further functions are called.
    
    # The file loaded fine and has been filtered, now return the dataframe.

    return df 

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df : Pandas dataframe containing the filtered bikeshare data.
    Returns:
        none
    """
    
    try: # Just wrapping it all in a general try clause, not getting specific with error handling.

        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # Convert the Start Time into the three fields we're determing the frequency / mode of.

        df['Start Time Month'] = pd.DatetimeIndex(df['Start Time']).month_name()
        df['Start Time Day Of Week'] = pd.DatetimeIndex(df['Start Time']).day_name()
        df['Start Time Hour'] = pd.DatetimeIndex(df['Start Time']).hour 
    
        # Calculate the mode of each and select the first value in the object returned.

        most_common_month = df['Start Time Month'].mode()[0]
        most_common_day = df['Start Time Day Of Week'].mode()[0]
        most_common_hour = df['Start Time Hour'].mode()[0]

        # Print the results.

        print('The most common month is: ' + most_common_month)
        print('The most common day of week is: ' + most_common_day)
        print('The most common starting hour is: ' + str(most_common_hour))

        print("\nThis took %s seconds." % round((time.time() - start_time),3))
        print('-'*40)

    except:
        print('Unable to calculate time stats - an exception has occured.')

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (dataframe) df : Pandas dataframe containing the filtered bikeshare data.
    Returns:
        none
    
    """

    try: # Just wrapping it all in a general try clause, not getting specific with error handling.

        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # Concatenate the Start and End Stations into a Station Route.

        df['Station Route'] = df['Start Station'] + ' -> ' + df['End Station']

        # Calculate the mode of each value and select the first value in the object returned.

        most_common_start_station = df['Start Station'].mode()[0]
        most_common_end_station = df['End Station'].mode()[0]
        most_common_station_route = df['Station Route'].mode()[0]

        # Print the results.

        print('The most common starting station is: ' + most_common_start_station)
        print('The most common ending station is: ' + most_common_end_station)
        print('The most common starting and ending station combination is: ' + most_common_station_route)

        print("\nThis took %s seconds." % round((time.time() - start_time),3))
        print('-'*40)

    except:
        print('Unable to calculate station stats - an exception has occured.')

def convert_seconds_to_string(time_seconds):
    """
    Converts a large number of seconds into a readable string of day, hour, minute and seconds values.

    Args:
        (int) time_seconds : An integer containing a number of seconds.
    Retunrs:
        (str) : AAn expression of the seconds interger as a readable duration.
    """
    
    days = (time_seconds // 86400) # There are 86400 seconds in a day. 
    hours = (time_seconds - (days * 86400)) // 3600 # First remove the days that have already been calculated above.
    minutes = (time_seconds - (days * 86400) - (hours * 3600)) // 60 # Take out both days and hours.
    seconds = time_seconds - (days * 86400) - (hours * 3600) - (minutes * 60) # Take days, hours and minutes out - only seconds are left.

    return('{} days {} hours {} minutes and {} seconds'.format(days,hours,minutes,seconds))

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (dataframe) df : Pandas dataframe containing the filtered bikeshare data.
    Returns:
        none
    """
    
    try: # Just wrapping it all in a general try clause, not getting specific with error handling.

        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # Calculate the total and mean travel times.

        travel_time_total = df['Trip Duration'].sum()
        travel_time_mean = round(df['Trip Duration'].mean(),3)

        # Print the results.

        print('The total travel time is {}. '.format(convert_seconds_to_string(travel_time_total)))
        print('The mean travel time is {} seconds. '.format(str(travel_time_mean)))
        
        print("\nThis took %s seconds." % round((time.time() - start_time)),3)
        print('-'*40)

    except:
        print('Unable to calculate trip duration stats - an exception has occured.')

def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (dataframe) df : Pandas dataframe containing the filtered bikeshare data.
    Returns:
        none
    """
        
    try: # Here we know Washington doesn't have the necessary columns, so we add a "KeyError" specific check.

        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Calculate the number of User Types and Gender

        user_types = df['User Type'].value_counts()
        genders = df['Gender'].value_counts()

        # Calculate the earliest, most recent and most common year of birth.

        min_year = df['Birth Year'].min()
        max_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        
        # Print the results

        print("Counts of User Types:")
        print(user_types.to_string() + '\n') # Use to_string() method so that the data types info isn't displayed.
        
        print("Counts of Gender:")
        print(genders.to_string() + '\n')

        print("Earliest birth year: " + str(int(min_year)))
        print("Most recent birth year: " + str(int(max_year)))
        print("Most common birth year: " + str(int(most_common_year)))

        print("\nThis took %s seconds." % round((time.time() - start_time)))
        print('-'*40)
    
    except(KeyError):
        print('Unable to calculate user stats. Required fields are missing from the file.')
    except:
        print('Unable to calculate user stats - an exception has occured.')

def display_raw_data(df):
    """
    Displays the raw data of the CSV (after filtering) in rows of five. Pauses after
    every five rows and asks if the user would like to see five more.

    Args:
        (dataframe) df : Pandas dataframe containing the filtered bikeshare data.
    Returns:
        none
    """
    answer = input("\nWould you like to review the filtered data? [y/n] ").lower()
    if answer[0] == 'y': # User wants to view the data.
        df.sort_values(axis=0,by="Start Time",inplace=True) # Sort by start time so data is orderly.
        index_start = 0 # Starting index that we're going to iterate through.
    
        while index_start < df.size and answer[0] == 'y': # There is still more data to show and the user still wants to see it.
                index_end = index_start + 5 # We're diplaying 5 records at a time. This is used to construct that range.
                if index_end >= df.size: # To cater for the scenario where the last iteration has fewer than 5 records.
                        index_end = df.size - 1 # Size starts at 1, but index starts at 0 so subtract 1.
                print(df.iloc[index_start:index_end]) # Prints the data using the integer index location method.
                answer = input("\nPrint the next 5 records? [y/n] ").lower() # Check to see if the user wants to continue
                index_start += 5 # Increment the index by one every loop.
    else:
        return
    return

def main():
    while True: # Start the main method loop.
        
        city, month, day = get_filters() #  Get the filters with user input.

        try: 
            if city != 'Invalid' and month != 'Invalid' and day != 'Invalid': # Check that only valid answers were input.
                df = load_data(city, month, day) # Load the relevant CSV file and filter the data.
                if len(df) != 0: # The object has been loaded but it might not have data after filtering.    
                    
                    # Statistical methods follow:

                    time_stats(df) 
                    station_stats(df)
                    trip_duration_stats(df)
                    user_stats(df)
                    display_raw_data(df)
        
        except:
            print('\nAn unexpected error has occurred.')

        if input('\nWould you like to restart? [y/n] ')[0].lower() != 'y': # Reloop the whole main method until the user enters 'yes' to exit.
            break

if __name__ == "__main__":
	main()