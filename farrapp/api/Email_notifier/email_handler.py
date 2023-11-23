import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailHandler:

    def __init__(self, farrapp_email, email_password, smtp_server="smtp.gmail.com"):
        self.email = farrapp_email
        self.password = email_password
        self.server = smtp_server
        self.port = 465

    def send_email(self, establishment_name, establishment_email, image):
        """Send an email for a specific establishment with the statistics of the establishment"""
        # NOTA: The 'image' parameter is the relative path of the image

        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = establishment_email
        message['Subject'] = f"{establishment_name} statistics"

        html_body = """
            <html>
            <body>
                <h2>Hello, hero you have some statistics from your establishment</h2>
                <img src="cid:imagen.jpg" alt="Imagen">
                <p>farrapp team</p>
            </body>
            </html>
            """

        message.attach(MIMEText(html_body, 'html'))

        with open(image, 'rb') as archivo_imagen:
            image_attach = MIMEImage(archivo_imagen.read())
            image_attach.add_header('Content-Disposition', 'inline', filename='imagen.jpg')
            message.attach(image_attach)

        sever = smtplib.SMTP(self.server, self.port)
        sever.starttls()

        sever.login(self.email, self.password)
        sever.sendmail(self.email, establishment_email, message.as_string())
        sever.quit()

#Para testaear esto se necesita un correo de gmail y su contraseña, el resto debe ser automatico

email = EmailHandler("correo@gmail", "contraseña")
email.send_email("nombre del establecimiento", "correo del establecimiento", "imagen.jpg")