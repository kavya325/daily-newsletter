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

# App Password from GitHub secret
app_password = os.environ.get("APP_PASSWORD")

# Recipient (yourself, or later multiple)
recipients = [sender_email]

# RSS Feed URL (general news)
rss_url = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"

# -------------------------
# KEYWORDS TO FILTER
# -------------------------

keywords = [
    "car parking",
    "automated parking",
    "parking system",
    "warehouse automation",
    "automated warehouse",
    "textile machinery",
    "spinning machine",
    "automated storage",
    "robotic system",
    "automation"
]

# -------------------------
# FETCH NEWS
# -------------------------

feed = feedparser.parse(rss_url)

html_content = """
<h2>📰 Filtered News – Relevant to Automation</h2>
<ul>
"""

filtered_count = 0

for entry in feed.entries:
    combined_text = (entry.title + entry.get("summary", "")).lower()
    if any(keyword in combined_text for keyword in keywords):
        html_content += f'<li><a href="{entry.link}">{entry.title}</a></li>'
        filtered_count += 1

html_content += "</ul>"

if filtered_count == 0:
    html_content += "<p>No relevant articles found today.</p>"

html_content += "<hr><p>This is an automated email sent from GitHub Actions.</p>"

# -------------------------
# COMPOSE EMAIL
# -------------------------

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = sender_email
msg["Subject"] = "Daily Automation Newsletter"

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
    print("✅ Filtered newsletter sent successfully!")
except Exception as e:
    print("❌ Error:", e)
