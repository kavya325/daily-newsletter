import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# -------------------------
# CONFIGURATION
# -------------------------

# Sender Gmail address
sender_email = "siegerintern@gmail.com"

# App Password (stored securely in GitHub secrets)
app_password = os.environ.get("APP_PASSWORD")

# Recipient (yourself)
recipients = [sender_email]

# RSS Feed URL
rss_url = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"

# -------------------------
# FETCH NEWS
# -------------------------

feed = feedparser.parse(rss_url)

html_content = """
<h2>📰 Times of India - Top 5 Headlines</h2>
<ul>
"""
for entry in feed.entries[:5]:
    html_content += f'<li><a href="{entry.link}">{entry.title}</a></li>'
html_content += "</ul>"
html_content += "<hr><p>This is an automated newsletter sent from GitHub Actions.</p>"

# -------------------------
# COMPOSE EMAIL
# -------------------------

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = sender_email
msg["Subject"] = "Daily Newsletter - Times of India Headlines"

msg.attach(MIMEText(html_content, "html"))

# -------------------------
# SEND EMAIL
# -------------------------

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, [sender_email], msg.as_string())
    server.quit()
    print("✅ Newsletter sent successfully!")
except Exception as e:
    print("❌ Error:", e)
