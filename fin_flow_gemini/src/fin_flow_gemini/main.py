#!/usr/bin/env python
from pydantic import BaseModel
from datetime import datetime
import time

from crewai.flow import Flow, listen, start, and_

from crews.visualizer_crew.visualizer_crew import VisualizerCrew
from crews.news_crew.news_crew import NewsCrew
from crews.report_crew.report_crew import ReportCrew


from dotenv import load_dotenv
load_dotenv()

class ReportState(BaseModel):
    user_question: str = ""
    present_time: str = ""  
    visualizer_result: str = "./assets/images/"
    news_result: str = "./assets/news/news_article.md"

class ReportFlow(Flow[ReportState]):

    @start()
    def visualizer_crew_kickoff(self):
        """Kickoff visualizer crew to generate visualizations"""
        print("Kicking off visualizer crew")
        
        # Try visualizer crew with retries
        attempt = 0
        while attempt < 3:
            try:
                result = (
                    VisualizerCrew()
                    .crew()
                    .kickoff(inputs={
                        "user_question": self.state.user_question,
                        "present_time": self.state.present_time
                    })
                )
                print("Visualizer crew completed")
                break
            except Exception as e:
                attempt += 1
                print(f"Visualizer crew failed (attempt {attempt}/3): {e}")
                if attempt < 3:
                    time.sleep(2)  # 2 second delay after failure
                else:
                    print("Visualizer failed even after 3 tries")

        # Try news crew with retries
        attempt = 0
        while attempt < 3:
            try:
                result = (
                    NewsCrew()
                    .crew()
                    .kickoff(inputs={
                        "user_question": self.state.user_question,
                        "present_time": self.state.present_time
                    })
                )
                print("News crew completed")
                break
            except Exception as e:
                attempt += 1
                print(f"News crew failed (attempt {attempt}/3): {e}")
                if attempt < 3:
                    time.sleep(2)  # 2 second delay after failure
                else:
                    print("News failed even after 3 tries")
        
        print("Visualizer and news crews completed")
        return "visualizer_completed"


    # @listen(visualizer_crew_kickoff)
    # def news_crew_kickoff(self):
    #     """Kickoff news crew to generate news article"""
    #     print("Kicking off news crew")
        
    #     result = (
    #         NewsCrew()
    #         .crew()
    #         .kickoff(inputs={
    #             "user_question": self.state.user_question,
    #             "present_time": self.state.present_time
    #         })
    #     )
        
    #     print("News crew completed")
    #     return "news_completed"

    @listen(visualizer_crew_kickoff)
    def report_crew_kickoff(self):
        """Kickoff report crew after both visualizer and news crews are completed"""
        print("Both visualizer and news crews completed. Kicking off report crew")
        
        result = (
            ReportCrew()
            .crew()
            .kickoff(inputs={
                "user_question": self.state.user_question,
                "visualizer_result": self.state.visualizer_result,
                "news_result": self.state.news_result
            })
        )
        
        print("Report crew completed")
        print("Final report generated:", self.state.final_report)
        return "report_completed"


def kickoff():
    """Run the report flow with hardcoded user question"""
    # Hardcoded user question as requested
    user_question = "current price of tesla stock"
    present_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Starting ReportFlow with question: {user_question}")
    print(f"Present time: {present_time}")
    
    report_flow = ReportFlow()
    report_flow.state.user_question = user_question
    report_flow.state.present_time = present_time
    
    result = report_flow.kickoff()
    print(f"Flow completed with result: {result}")


def plot():
    """Generate flow visualization"""
    report_flow = ReportFlow()
    report_flow.plot("ReportFlowPlot")
    print("Flow plot saved as ReportFlowPlot.html")


if __name__ == "__main__":
    kickoff()
    plot()
