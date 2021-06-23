import os
import smtplib
import uuid
from email.header import Header
from email.mime.text import MIMEText

import pandas
from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv('EMAIL')
my_password = os.getenv('PASSWORD')

try:
    data = pandas.read_csv('output/supporters.csv', skipinitialspace=True)

    for (index, data_row) in data.iterrows():
        print(data_row["email"])
        file_path = "content.txt"

        with open(file_path) as letter_file:
            contents = letter_file.read()
            contents = contents.replace("[NAME]", data_row["name"])
            contents = contents.replace("[id]", data_row["id"])
            contents = contents.replace("[content]", data_row["content"])

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)

            charset = 'iso-2022-jp'
            subject = "題名"

            msg = MIMEText(contents, 'plain', charset)
            msg['Subject'] = Header(subject, charset)

            connection.sendmail(
                from_addr=my_email,
                to_addrs=data_row["email"],
                msg=msg.as_string()
            )
            print("mail sent")
except FileNotFoundError as e:
    print("creating output file...")
    df = pandas.read_csv('input/supporters.csv')

    df['id'] = [f"t{str(uuid.uuid4().hex)[:5]}" for _ in range(len(df.index))]

    df.to_csv('output/supporters.csv')
    print("Completed!!")
    print("try again!")
