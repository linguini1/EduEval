# Sandbox for cleaning up dataset
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from utils.process import analyze_sentiment, filter_by_length, filter_not_english, filter_empty_comments

# Constants
MINIMUM_COMMENTS: int = 7

# Main
def main():

    # Read in dataset
    data = pd.read_parquet("collection/data/pre_filtered_data.parquet.gzip")

    # Set display
    pd.set_option("display.max_colwidth", 150)

    # Store courses for convenience of cleaner
    with open("courses.txt", 'w') as file:
        file.writelines([f"{course}\n" for course in data["course"].unique()])

    # Remove duplicates
    data["comment"] = data["comment"].drop_duplicates()
    data= data.drop_duplicates(subset=['professor', 'course'], keep= 'first')


    # Remove courses that don't make sense
    # Merge courses together if they are equivalent
    data["course"].replace(
        ["ITI11200", "ITI1121", "ITI1101"], "ITI1120", inplace=True
    )
    data["course"].replace(
        ["SYSC3601", "SYSC3503", "SYSC3600"], "SYSC2320", inplace=True
    )
    data["course"].replace(
        ["ECOR1051", "ECOR1044"], "ECOR1042", inplace=True
    )
    data["course"].replace(
        ["SYSC2002", "SYSC202"], "SYSC2100", inplace=True
    )
    data["course"].replace(
        ["19011902", "1902BIO", "19021903", "1902T", "1903"], "1902", inplace=True
    )
    data["course"].replace(
        ["61192193", "61492"], "61192", inplace=True
    )
    data["course"].replace(
        ["BIO"], "BIO1901", inplace=True
    )
    data["course"].replace(
        ["BIO192", "BIO19021903"], "BIO1902", inplace=True
    )
    data["course"].replace(
        ["BIO19031904"], "BIO1903", inplace=True
    )
    data["course"].replace(
        ["BIO45004501"], "BIO4501", inplace=True
    )
    data["course"].replace(
        ["97575", "575", "975705", "97575", "97533", "97553", "975XX", "97ALL"], "975XX", inplace=True

    )
    data["course"].replace(
        ["ELEC25013509", "ELEC35093909"], "ELEC3509", inplace=True
    )

    data["course"].replace(
        ["ELEC25013509"], "ELEC2501", inplace=True
    )

    data["course"].replace(
        ["ELEC25073105"], "ELEC3105", inplace=True
    )

    data ["course"].replace(
        ['SAT257', "STA257", "STA257H1F"], "STA257", inplace=True
    )

    data["course"].replace(
        ["BCH210", "BCH210BCH311"], "BCH210", inplace=True
    )

    data["course"].replace(
        ["RSM100RS", "RSM100"], "RSM100", inplace=True
    )

    data["course"].replace(
        ["1300", "CMN1300", "CRIM","CRIM1300", "CRM", "CRM1300", "CRM1300E", "CRM1300S" ], "CRIM1300", inplace=True
    )

    data["course"].replace(
        ["SOC2109A", "SOC2109"], "SOC2109", inplace=True
    )

    data["course"].replace(
        ["SOC3330A","SOC3330"], "SOC3330", inplace=True
    )

    data["course"].replace(
        ["BIO1130A", "BIO1130", "BIO113O", "BIO130", "BIO1330"], "BIO113O", inplace=True
    )

    #print(data[data["course"] == "BIO1902"]["comment"])

    quit()  # Early return until all cleaning code is in place

    # After merging, any courses with not enough reviews are dropped
    for course in data["course"].unique():
        if len(data[data["course"] == course]) < MINIMUM_COMMENTS:
            data = data[data["course"] != course]

    # Do sentiment analysis
    data = analyze_sentiment(data)

    # Save the cleaned data
    data.to_parquet("test_data.parquet.gzip", compression="gzip")


if __name__ == '__main__':
    main()
