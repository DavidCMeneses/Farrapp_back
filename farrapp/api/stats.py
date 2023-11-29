import xlsxwriter
from collections import Counter

import smtplib

import os
from dotenv import dotenv_values, load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

load_dotenv()


def xlsx_maker(name, data, headers):

    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()

    for col_num, headers in enumerate(headers):
        worksheet.write(0, col_num, headers)


    worksheet.write_column('A2', Counter(data[0]).keys())
    worksheet.write_column('B2', Counter(data[0]).values())

    worksheet.write_column('C2', Counter(data[1]).keys())
    worksheet.write_column('D2', Counter(data[1]).values())

    worksheet.write_column('E2', Counter(data[2]).keys())
    worksheet.write_column('F2', Counter(data[2]).values())

    worksheet.write_column('G2', Counter(data[3]).keys())
    worksheet.write_column('H2', Counter(data[3]).values())


    chart1 = workbook.add_chart({"type": "pie"})
    chart1.add_series(
        {
            "name": "Pie sex data",
            "categories": "=Sheet1!$A$2:$A$"+str(len(Counter(data[0]).keys())+1),
            "values": "=Sheet1!$B$2:$B$"+str(len(Counter(data[0]).keys())+1),
        }
    )
    chart1.set_title({"name": "Pie Chart Sexes"})
    worksheet.insert_chart("J1", chart1, {"x_offset": 25, "y_offset": 10})

    chart2 = workbook.add_chart({"type": "pie"})
    chart2.add_series(
        {
            "name": "Pie age data",
            "categories": "=Sheet1!$C$2:$C$"+str(len(Counter(data[1]).keys())+1),
            "values": "=Sheet1!$D$2:$D$"+str(len(Counter(data[1]).keys())+1),
        }
    )
    chart2.set_title({"name": "Pie Chart Ages"})
    worksheet.insert_chart("J16", chart2, {"x_offset": 25, "y_offset": 10})

    chart3 = workbook.add_chart({"type": "pie"})
    chart3.add_series(
        {
            "name": "Pie Music data",
            "categories": "=Sheet1!$E$2:$E$"+str(len(Counter(data[2]).keys())+1),
            "values": "=Sheet1!$F$2:$F$"+str(len(Counter(data[2]).keys())+1),
        }
    )
    chart3.set_title({"name": "Pie Chart Music"})
    worksheet.insert_chart("J32", chart3, {"x_offset": 25, "y_offset": 10})

    chart4 = workbook.add_chart({"type": "pie"})
    chart4.add_series(
        {
            "name": "Pie Category data",
            "categories": "=Sheet1!$G$2:$G$"+str(len(Counter(data[3]).keys())+1),
            "values": "=Sheet1!$H$2:$H$"+str(len(Counter(data[3]).keys())+1),
        }
    )
    chart4.set_title({"name": "Pie Chart Categories"})
    worksheet.insert_chart("J46", chart4, {"x_offset": 25, "y_offset": 10})

    workbook.close()

def send_email_w_attachment(to, subject, body, filename):
    gmail_pass = os.getenv('gmail_pass')
    user = os.getenv('user2')
    host = os.getenv('host2')
    port = int(os.getenv('port2'))
    
    # create message object
    message = MIMEMultipart()

    # add in header
    message['From'] = Header(user)
    message['To'] = Header(to)
    message['Subject'] = Header(subject)

    # attach message body as MIMEText
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # locate and attach desired attachments
    att_name = os.path.basename(filename)
    _f = open(filename, 'rb')
    att = MIMEApplication(_f.read(), _subtype="txt")
    _f.close()
    att.add_header('Content-Disposition', 'attachment', filename=att_name)
    message.attach(att)

    # setup email server
    server = smtplib.SMTP_SSL(host, port)
    server.login(user, gmail_pass)

    # send email and quit server
    server.sendmail(user, to, message.as_string())
    server.quit()

