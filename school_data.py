# school_data.py
# AUTHOR NAME : ABHIJITH DAVID
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import numpy as np
import pandas as pd

# Global variable to store the data
enrollment_data = None


class SchoolStats:
    """
    A class to hold and manipulate school enrollment data.
    
    Attributes:
        data (pd.DataFrame): The dataframe holding school enrollment data.
        enrollment_array (np.ndarray): 3D NumPy array for enrollment data.
        school_codes (dict): Dictionary mapping school names to their codes.
    """
    def __init__(self, data):
        """
        Initializes the SchoolStats with the provided data.
        
        Parameters:
            data (pd.DataFrame): The dataframe holding school enrollment data.
        """
        self.data = data
        self.enrollment_array = None
        self.school_codes = {name: code for name, code in zip(data['School Name'], data['School Code'])}

    def create_enrollment_array(self):
        """
        Create a 3-dimensional array from the provided data.
        """
        schools = self.data['School Name'].unique()
        years = self.data['School Year'].unique()
        grades = ['Grade 10', 'Grade 11', 'Grade 12']

        self.enrollment_array = np.empty((len(schools), len(years), len(grades)), dtype=int)

        for i, school in enumerate(schools):
            for j, year in enumerate(years):
                for k, grade in enumerate(grades):
                    value = self.data[(self.data['School Name'] == school) & (self.data['School Year'] == year)][grade]
                    self.enrollment_array[i, j, k] = int(value) if not pd.isna(value).any() else 0

        print(f"Shape of the full Data Array: {self.enrollment_array.shape}")
        print(f"Dimensions of the full Data Array: {self.enrollment_array.ndim}")

    def get_school_index(self, identifier):
        """
        Get the index of the school in the array.
        
        Parameters:
            identifier (str or int): The name or code of the school.
        
        Returns:
            int: The index of the school in the array.
        
        Raises:
            ValueError: If the school name or code is invalid.
        """
        if isinstance(identifier, int):
            school_name = next((name for name, code in self.school_codes.items() if code == identifier), None)
        else:
            school_name = identifier

        if school_name not in self.school_codes:
            raise ValueError("You must enter a valid school name or code.")

        return list(self.school_codes.keys()).index(school_name)

    def calculate_school_stats(self, identifier):
        """
        Calculate statistics for the given school.
        
        Parameters:
            identifier (str or int): The name or code of the school.
        
        Returns:
            dict: A dictionary containing the school-specific statistics.
        """
        index = self.get_school_index(identifier)
        school_name = list(self.school_codes.keys())[index]
        school_code = self.school_codes[school_name]

        school_data = self.enrollment_array[index, :, :]

        stats = {
            "school_name": school_name,
            "school_code": school_code,
            "mean_grade_10": np.floor(np.mean(school_data[:, 0])),
            "mean_grade_11": np.floor(np.mean(school_data[:, 1])),
            "mean_grade_12": np.floor(np.mean(school_data[:, 2])),
            "highest_enrollment": np.max(school_data),
            "lowest_enrollment": np.min(school_data),
            "yearly_totals": np.sum(school_data, axis=1),
            "total_enrollment": np.sum(school_data),
            "mean_yearly_enrollment": np.floor(np.mean(np.sum(school_data, axis=1))),
            "enrollments_over_500": school_data[school_data > 500]
        }

        if len(stats["enrollments_over_500"]) > 0:
            stats["median_over_500"] = int(np.median(stats["enrollments_over_500"]))
        else:
            stats["median_over_500"] = "No enrollments over 500"

        return stats

    def calculate_general_stats(self):
        """
        Calculate general statistics for all schools.
        
        Returns:
            dict: A dictionary containing the general statistics.
        """
        stats = {
            "mean_2013": np.floor(np.mean(self.data[self.data['School Year'] == 2013][['Grade 10', 'Grade 11', 'Grade 12']])),
            "mean_2022": np.floor(np.mean(self.data[self.data['School Year'] == 2022][['Grade 10', 'Grade 11', 'Grade 12']])),
            "total_graduating_2022": np.sum(self.data[self.data['School Year'] == 2022]['Grade 12']),
            "highest_enrollment": np.max(self.enrollment_array),
            "lowest_enrollment": np.min(self.enrollment_array)
        }

        return stats


def load_data(filename):
    """
    Load the enrollment data from a CSV file.
    
    Parameters:
        filename (str): The name of the CSV file.
    
    Returns:
        pd.DataFrame: The dataframe containing the enrollment data.
    
    Raises:
        ValueError: If the CSV file cannot be loaded.
    """
    try:
        data = pd.read_csv(filename)
        return data
    except Exception as e:
        raise ValueError(f"Error reading {filename}: {e}")


def main():
    print("ENSF 692 School Enrollment Statistics")

    # Load the data
    global enrollment_data
    enrollment_data = load_data("Assignment3Data.csv")
    print("Data loaded successfully.")

    # Initialize SchoolStats
    stats = SchoolStats(enrollment_data)

    # Stage 1: Create array and print its shape and dimensions
    stats.create_enrollment_array()

    # Prompt for user input
    school_identifier = input("Enter the high school name or school code: ")

    try:
        if school_identifier.isdigit():
            school_identifier = int(school_identifier)
        school_stats = stats.calculate_school_stats(school_identifier)

        # Stage 2: Print school-specific statistics
        print("\n***Requested School Statistics***\n")
        print(f"School Name: {school_stats['school_name']}")
        print(f"School Code: {school_stats['school_code']}")
        print(f"Mean enrollment for Grade 10: {school_stats['mean_grade_10']}")
        print(f"Mean enrollment for Grade 11: {school_stats['mean_grade_11']}")
        print(f"Mean enrollment for Grade 12: {school_stats['mean_grade_12']}")
        print(f"Highest enrollment for a single grade: {school_stats['highest_enrollment']}")
        print(f"Lowest enrollment for a single grade: {school_stats['lowest_enrollment']}")
        print(f"Total enrollment for each year from 2013 to 2022: {school_stats['yearly_totals']}")
        print(f"Total ten-year enrollment: {school_stats['total_enrollment']}")
        print(f"Mean total yearly enrollment over 10 years: {school_stats['mean_yearly_enrollment']}")
        if isinstance(school_stats["median_over_500"], str):
            print(school_stats["median_over_500"])
        else:
            print(f"Median enrollment over 500: {school_stats['median_over_500']}")

    except ValueError as e:
        print(e)
        return

    # Stage 3: Print general statistics
    general_stats = stats.calculate_general_stats()
    print("\n***General Statistics for All Schools***\n")
    print(f"Mean enrollment in 2013: {general_stats['mean_2013']}")
    print(f"Mean enrollment in 2022: {general_stats['mean_2022']}")
    print(f"Total graduating class of 2022: {general_stats['total_graduating_2022']}")
    print(f"Highest enrollment for a single grade within the entire time period: {general_stats['highest_enrollment']}")
    print(f"Lowest enrollment for a single grade within the entire time period: {general_stats['lowest_enrollment']}")


if __name__ == '__main__':
    main()
