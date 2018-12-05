
from prediction import make_prediction
from generate_charts import make_charts
from generate_report import make_report

def start_script(username):

    # Make predictions
    print("Getting the tweets")
    make_prediction(username)
    print("Predictions done!")

    # Make charts
    daterange = make_charts(username)
    print("Charts created!")

    # Make report
    filename = make_report(username, daterange)
    return filename
