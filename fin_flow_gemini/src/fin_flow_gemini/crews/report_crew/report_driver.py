#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from report_crew import ReportCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print ("Running report crew")
    inputs = {
        'user_question': 'what is the ytd profit gain if I had invested 100 dollars in each of the S&P 500 stocks, and how does this compare to gold price?',
        'present_time': datetime.now().strftime("%Y-%m-%d")
    }
    
    try:
        ReportCrew().crew().kickoff()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


run()
