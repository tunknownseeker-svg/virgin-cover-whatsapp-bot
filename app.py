from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = "123456789"
WHATSAPP_TOKEN = "EAAaeTQFCFPEBQ9Fgq0rnfKZArEmr9oVlCY8JjkVZAZCSUtfPSsOddWjMamvjeouMWpZBwNSZAPBXERSsN39Ybo0rn9CHeDUSs9ngBQ7Ei6EiU8uPkH0ZA3BjWXRkSkb3wZBfS2jP4YG4MbgtyTRUOM0DZAMRKIZBw1Wo6FW0eLZCskIWkdw7pczvEnpNYpTvKfEU6q7d8QIF2laO9BYZCeij424NlLL7a2x6JLMzJMLwXAZAVOyMCCzLD1dHT5hgluJZAef4nJbNs0VvrXjDFIXASPnN21GZCBbwZDZD"
PHONE_NUMBER_ID = "1053793971143397"
LIVE_AGENT_NUMBER = "971XXXXXXXX"  # Replace with your live agent WhatsApp number

FAQ = {
    "coverage_duration": {
        "title": "Coverage Duration",
        "answer": "⏳ *How Long Does My Coverage Last?*\n\nYour Virgin Cover protection starts the day after your manufacturer warranty ends and can last up to 3 years, depending on the plan you choose.\n\nAccidental Damage coverage starts from the date of purchase."
    },
    "coverage_details": {
        "title": "What's Covered?",
        "answer": "✅ *What's Covered?*\n\n• Extended Warranty (EW) covers electrical or mechanical breakdowns after your manufacturer warranty expires.\n• Accidental Damage (ADH) covers sudden damage like drops, spills, or breaks.\n• Product attachments like controllers or styluses are also covered if included in your plan.\n• Coverage applies internationally, except in war zones."
    },
    "not_covered": {
        "title": "What's Not Covered?",
        "answer": "❌ *What's Not Covered?*\n\n• Cosmetic damage (scratches, dents)\n• Liquid immersion or combined liquid and physical damage\n• Damage while item is left unattended or used improperly\n• Pre-existing defects or those under manufacturer warranty\n• Wear and tear, consumables (batteries, ink), or routine maintenance\n• Damage due to negligence or unauthorized repairs\n• Items used commercially or for rental\n• Software, media, or data loss"
    },
    "protection_limits": {
        "title": "Protection Limits",
        "answer": "🛡️ *Protection Limits*\n\nUnlimited claims up to the product's purchase price.\n\nIf repair cost ≥ item value, you may receive a replacement (minus depreciation).\n\n*Depreciation (VAT excluded):*\n• EW: 25% yr1 / 40% yr2 / 55% yr3\n• ADH: 25% yr1 / 40% yr2 / 75% yr3\n\n💰 Processing Fee: AED 100 flat fee for Accidental Damage claims."
    },
    "claim_process": {
        "title": "How to Make a Claim?",
        "answer": "📋 *How to Make a Claim?*\n\n1. Report the issue within 5 days\n2. Make sure it's not fixable via manufacturer's guide\n3. Drop item at any Virgin Megastore customer service counter or email claims@amnly.com\n4. Repairs usually take about one week\n5. We'll deliver it back to your address\n\n📎 Remember to attach your purchase receipt!"
    },
    "international_claims": {
        "title": "International Claims",
        "answer": "🌍 *International Claims*\n\nIf a breakdown occurs outside the country of purchase:\n\n1. Email claims@amnly.com with issue description and documents\n2. If approved, repair locally and send us the final invoice\n3. Reimbursement via bank transfer based on the lower value between the invoice and estimated item value in original country of purchase."
    }
}


def send_menu(to):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Virgin Cover Support 🛡️"
            },
            "body": {
                "text": "👋 Welcome to Virgin Cover!\n\nHow can I help you today? Please select an option below:"
            },
            "footer": {
                "text": "Virgin Megastore Cover"
            },
            "action": {
                "button": "View Options",
                "sections": [
                    {
                        "title": "FAQ Topics",
                        "rows": [
                            {"id": "coverage_duration", "title": "Coverage Duration", "description": "How long does my coverage last?"},
                            {"id": "coverage_details", "title": "What's Covered?", "description": "Details of your coverage"},
                            {"id": "not_covered", "title": "What's Not Covered?", "description": "Exclusions and limitations"},
                            {"id": "protection_limits", "title": "Protection Limits", "description": "Claims limits and depreciation"},
                            {"id": "claim_process", "title": "Make a Claim", "description": "How to submit a claim"}
                        ]
                    },
                    {
                        "title": "More Options",
                        "rows": [
                            {"id": "international_claims", "title": "International Claims", "description": "Claims outside country of purchase"},
                            {"id": "live_agent", "title": "Live Agent 💬", "description": "Chat with a human agent"}
                        ]
                    }
                ]
            }
        }
    }
    r = requests.post(url, headers=headers, json=payload)
    print("Menu sent:", r.json())


def send_text(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    r = requests.post(url, headers=headers, json=payload)
    print("Text sent:", r.json())


@app.route("/")
def home():
    return "Virgin Cover Bot is running"


@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token"

    if request.method == "POST":
        data = request.get_json()
        print("Incoming:", data)

        try:
            entry = data["entry"][0]["changes"][0]["value"]

            # Handle regular text messages → show menu
            if "messages" in entry:
                msg = entry["messages"][0]
                from_number = msg["from"]
                msg_type = msg.get("type")

                if msg_type == "text":
                    # Any text message → show the menu
                    send_menu(from_number)

                elif msg_type == "interactive":
                    # User selected an option from the list
                    interactive = msg["interactive"]
                    if interactive["type"] == "list_reply":
                        selected_id = interactive["list_reply"]["id"]

                        if selected_id == "live_agent":
                            send_text(from_number, f"💬 *Live Agent*\n\nPlease click the link below to chat with a live agent:\nhttps://wa.me/{971547263830}")
                        elif selected_id in FAQ:
                            send_text(from_number, FAQ[selected_id]["answer"])
                            # After answering, show menu again
                            send_menu(from_number)
                        else:
                            send_menu(from_number)

        except Exception as e:
            print("Error:", e)

        return jsonify(status="ok"), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)

    