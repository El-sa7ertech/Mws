from flask import Flask
import os

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return "Hello World from Render 🚀"

# Webhook تجريبي
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    return "OK", 200

# تشغيل السيرفر
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
