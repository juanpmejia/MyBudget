import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def py_mail(SUBJECT, BODY, TO, FROM):
    """With this function we send out our html email"""
 
    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
Your mail reader does not support the report format.
Please visit us <a href="http://www.mysite.com">online</a>!"""
 
    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')
 
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)
 
    # The actual sending of the e-mail
    server = smtplib.SMTP('smtp.gmail.com:587')
 
    # Print debugging output when testing
    if __name__ == "__main__":
        server.set_debuglevel(0)
 
    # Credentials (if needed) for sending the mail
    password = "Aguacate2017"
 
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()
 
if __name__ == "__main__":
    """Executes if the script is run as main script (for testing purposes)"""
 
    email_content = """
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>html title</title>
  <style type="text/css" media="screen">
    table{
        background-color: #AAD373;
        empty-cells:hide;
    }
    td.cell{
        background-color: white;
    }
  </style>
</head>
<body>
  <table style="border: blue 1px solid;">
    <tr><td class="cell">Cell 1.1</td><td class="cell">Cell 1.2</td></tr>
    <tr><td class="cell">Cell 2.1</td><td class="cell"></td></tr>
  </table>
</body>
"""
 
    TO = 'jpkratos@gmail.com'
    FROM ='mybudgetstaff@gmail.com'
 
    py_mail("Test email subject", email_content, TO, FROM)
    

def create_message_and_send(subject, to, message_text_html,  sender):
    print(subject, message_text_html, to,sender)
    py_mail(subject,message_text_html, to,sender)

