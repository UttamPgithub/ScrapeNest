import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import openpyxl
from openpyxl import Workbook
app = Flask(__name__)

TEAM_MEMBERS = [
    {
        "id": "uttam",
        "name": "Uttam Prajapati",
        "role": "Head Of Technical Department",
        "bio": "Leads core technology strategy, backend system architecture, scalable data pipelines, and technical execution across engineering teams.",
        "skills": ["Python Developer", "Web Scraping", "Data Extraction", "Database Design", "Automation", "Technical Leadership"],
        "github": "https://github.com",
        "linkedin": "https://linkedin.com"
    },
    {
        "id": "ajay",
        "name": "Ajay Rajpoot",
        "role": "Head Of QC Department",
        "bio": "Oversees product quality assurance, automated test engineering, performance validation, and release quality across all web systems.",
        "skills": ["QA Automation", "Selenium / Cypress", "API Testing (Postman)", "Test Planning & Strategy", "Performance Testing", "Bug Tracking (Jira)"],
        "github": "https://github.com",
        "linkedin": "https://linkedin.com"
    },
    {
        "id": "shivam",
        "name": "Shivam Srivastava",
        "role": "Head Of Sales Department",
        "bio": "Drives business growth, client acquisition, enterprise solution sales, client relations, and revenue strategy.",
        "skills": ["B2B & Enterprise Sales", "Client Relationship Management", "Sales Pipeline & CRM", "Contract Negotiation", "Lead Generation", "Revenue Growth"],
        "github": "https://github.com",
        "linkedin": "https://linkedin.com"
    }
]
PROJECTS = [
    {
        "title": "Amazon Product Page Data Extraction",
        "description": "Engineered a high-resilience web crawler to extract comprehensive product data (pricing, buybox variations, ratings, inventory, and seller details) while bypassing aggressive anti-bot protections using smart proxy rotation and session headers.",
        "tech": "Python, Scrapy, BeautifulSoup, MySQL, Smart Proxies",
        "status": "Completed"
    },
    {
        "title": "Instamart Product Page Data Extraction",
        "description": "Developed a high-frequency quick-commerce scraper to capture location-specific catalog data, real-time SKU availability, discounts, and delivery estimates across diverse pincodes with automated structured storage in MySQL.",
        "tech": "Python, Scrapy, BeautifulSoup, MySQL, Rotating Proxies",
        "status": "Completed"
    },
    {
        "title": "Flipkart Product Page Data Extraction",
        "description": "Built a scalable automated pipeline to harvest complex nested product specifications, customer reviews, discount pricing, and stock metrics, featuring custom parsing fallbacks and schema validation for clean dataset delivery.",
        "tech": "Python, Scrapy, BeautifulSoup, MySQL, Proxy Pools",
        "status": "Completed"
    }
]

ALL_SKILLS = {
    "Scraping": ["Python", "MongoDB", "Scrapy", "BeautifulSoup", "Requests", "MySQL", "Selenium", "playwright"],
    # "Frontend & UI": ["JavaScript", "HTML5", "CSS3 / Tailwind", "Responsive Layouts", "DOM Manipulation"],
    # "Cloud & DevOps": ["Docker", "Linux / Bash", "Git & GitHub Actions", "Cloud Hosting", "System Monitoring"]
}

PROJECT_VIDEOS = [
    {
        "title": "Amazon Product Page Scraper in Action",
        "category": "E-Commerce Scraping",
        "description": "Live demonstration of scraping Amazon PDP details (pricing, variations, stock) while automatically handling anti-bot challenges and proxy rotation.",
        "video_url": "videos/amazon_recording.mp4",
        "is_local_file": True,
        "key_highlights": [
            "Bypasses Cloudflare & Captcha",
            "Extracts BuyBox & Seller Details",
            "Stores structured records in MySQL"
        ],
        "tech": "Python, Scrapy, BeautifulSoup, Proxies"
    },
    {
        "title": "Instamart Multi-Pincode Catalog Extractor",
        "category": "Quick-Commerce Data Pipeline",
        "description": "Walkthrough of high-speed extraction across 15+ pincodes simultaneously, capturing dynamic discounts, real-time SKU availability, and fast delivery timelines.",
        "video_url": "videos/instamart_recording.mp4",
        "is_local_file": True,
        "key_highlights": [
            "Location/Pincode spoofing via headers",
            "Real-time out-of-stock detection",
            "Low-latency JSON response parsing"
        ],
        "tech": "Python, Scrapy, MySQL, Rotating IPs"
    },
    {
        "title": "Flipkart Nested Reviews & Specs Scraper",
        "category": "Large-Scale Data Harvesting",
        "description": "Screen recording showing extraction of thousands of technical specifications, nested customer reviews, and high-resolution gallery image URLs.",
        "video_url": "videos/flipkart_recording.mp4",
        "is_local_file": True,
        "key_highlights": [
            "Recursive pagination handling",
            "Clean schema validation pipeline",
            "Automated CSV/Database export"
        ],
        "tech": "Python, Requests, BeautifulSoup, MySQL"
    }
]

# Path to the Excel file
EXCEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client_details_form.xlsx")


def save_to_excel(interest, email, phone):
    """Creates or appends a new lead to leads.xlsx"""
    file_exists = os.path.exists(EXCEL_FILE)

    if not file_exists:
        wb = Workbook()
        ws = wb.active
        ws.title = "Client Leads"
        # Write headers
        ws.append(["Timestamp", "Interest", "Email", "Phone Number"])
    else:
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active

    # Append the new row
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append([timestamp, interest, email, phone])

    # Save file
    wb.save(EXCEL_FILE)


# API Route to handle the form submission
@app.route("/submit-interest", methods=["POST"])
def submit_interest():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    interest = data.get("interest", "Not Specified")
    email = data.get("email", "N/A")
    phone = data.get("phone", "N/A")

    try:
        save_to_excel(interest, email, phone)
        return jsonify({"status": "success", "message": "Saved to Excel successfully!"})
    except Exception as e:
        print("Excel write error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500


# Optional: Secret download route so you can download leads.xlsx anytime
@app.route("/download-leads")
def download_leads():
    if os.path.exists(EXCEL_FILE):
        return send_file(EXCEL_FILE, as_attachment=True, download_name="scrapenest_leads.xlsx")
    return "No leads collected yet.", 404

# Page 1: Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Page 2: Three Partners Details
@app.route("/team")
def team():
    return render_template("team.html", team=TEAM_MEMBERS)

# Page 3: Freelancer Skills & Projects
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", skills=ALL_SKILLS, projects=PROJECTS)

# New Route: Project Video Demos
@app.route("/demos")
def demos():
    return render_template("demos.html", videos=PROJECT_VIDEOS)

if __name__ == "__main__":
    # Render assigns the port dynamically via an environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)