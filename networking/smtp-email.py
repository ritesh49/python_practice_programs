from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage

# Define these once; use them twice!
strFrom = 'faqritesh@gmail.com'
strTo = 'riteshramchandani123@gmail.com'

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('THIS IS TEXT MESSAGE FROM SANDBOX SERVER')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
image_text = '<h1> THIS IS TEXT MESSAGE FROM SANDBOX SERVER</h1>'
# image_text = '<br><img src="cid:image1"><br><h1> THIS IS TEXT MESSAGE FROM SANDBOX SERVER</h1>'
msgText = MIMEText(image_text, 'html')
# msgAlternative.attach(msgText)

# This example assumes the image is in the current directory
# fp = open('abhijeet_image.png', 'rb')
# msgImage = MIMEImage(fp.read())
# fp.close()

# Define the image's ID as referenced above
# msgImage.add_header('Content-ID', '<image1>')
# msgRoot.attach(msgImage)

# Send the email (this example assumes SMTP authentication is required)
def send_smtp_email():
    import smtplib
    smtp = smtplib.SMTP()
    print('connecting to SMTP Gmail!!!')
    smtp.connect('smtp.gmail.com', 587)
    print('Connecting to SMTP Server!!!')
    user = 'faqritesh@gmail.com'
    password = 'Ritesh#4149'
    smtp.starttls()
    smtp.login(user, password)
    print('Connected!!!')
    print('Sending MIME mail!!!')
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    print('Sent!!!')
    smtp.quit()
    print('Quit!!')

send_smtp_email()