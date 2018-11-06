import datetime
from fpdf import FPDF

def make_report(username, daterange):

    daterange = daterange
    account = "Twitter Account: " + username

    pdf = FPDF()
    pdf.add_page()
    pdf.set_title("Predicted Tweet Analysis Report")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 20, txt="Predicted Tweet Analysis Report", ln=1, align="C")
    pdf.cell(200, 10, txt=account, ln=1, align="L")
    pdf.cell(200, 10, txt=daterange, ln=1, align="L")
    pdf.cell(200, 10, txt="Frequency of Categories", ln=1, align="L")
    pdf.image('/Users/bethwalsh/Documents/classifier-twitter/app/images/frequency_categories.png', x = None, y = None, w = 120, h = 0, type = 'PNG', link = '')
    pdf.cell(200, 10, txt="Frequency of Categories by Day", ln=1, align="L")
    pdf.image('/Users/bethwalsh/Documents/classifier-twitter/app/images/frequency_categories_day.png', x = None, y = None, w = 120, h = 0, type = 'PNG', link = '')
    pdf.cell(200, 10, txt="Bug Report - WordCloud", ln=1, align="L")
    pdf.image('/Users/bethwalsh/Documents/classifier-twitter/app/images/bug_report_wordcloud.png', x = None, y = None, w = 120, h = 0, type = 'PNG', link = '')
    pdf.cell(200, 10, txt="Question - WordCloud", ln=1, align="L")
    pdf.image('/Users/bethwalsh/Documents/classifier-twitter/app/images/question_wordcloud.png', x = None, y = None, w = 120, h = 0, type = 'PNG', link = '')

    # Export and save report
    now = str(datetime.datetime.now())
    pdf.output("reports/" + username + "_report_" + now + ".pdf")
    filename  = username + "_report_" + now + ".pdf"
    return filename
