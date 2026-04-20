# PriceProbe 🔍

> **Smart, AI-powered price comparison assistant for students and budget shoppers.**  
> Compare prices across 50+ platforms in real time — groceries, electronics, pharmacy, fashion, food delivery, travel, and more. Built with Groq LLM + Tavily web search, geo-aware for Boston, USA and 8 countries.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-red?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange)
![Firebase](https://img.shields.io/badge/Firebase-Auth_%26_DB-yellow?logo=firebase&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Demo

![PriceProbe Demo](Images/home_1.png)

> Live app: *(add your deployed URL here after AWS deployment)*

---

## What it does

PriceProbe helps users who find it challenging to compare prices across multiple websites. Instead of opening 10 tabs manually, users simply type a product (or a list of products) and PriceProbe fetches real-time prices from all relevant platforms, calculates the cheapest total basket, surfaces promo codes, and explains how to use them.

### Key features

**🧠 Smart Basket Comparison**  
Type `eggs + milk + bread` — PriceProbe fetches prices for each item across all platforms, adds delivery fees, and tells you which single store gives the cheapest total. No more mental math across tabs.

**🎟️ Promo Codes & Savings Tips**  
Ask "any Walmart coupons today?" and get active promo codes in styled boxes with step-by-step redemption instructions.

**📦 Size Advisor**  
Type `16 eggs` — PriceProbe recognises this is an unusual quantity and automatically compares 12, 18, and 24-count options side by side with a recommendation.

**💬 Conversational AI**  
Natural greetings and chitchat are handled like a real assistant. The chatbot routes intelligently — greeting → conversational reply, product query → price search, multi-product → basket comparison.

**🌍 Geo-Aware**  
Detects your city (Boston, Bangalore, London, Dubai, Singapore, etc.) and switches platforms, currency, and suggestions accordingly. 8 countries, 50+ platforms.

**🔐 Firebase Authentication**  
Full user account system — sign up, login, password reset — powered by Firebase Auth with REST API.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| LLM | Groq API — LLaMA 3.3 70B Versatile |
| Web Search | Tavily Search API (real-time prices) |
| Authentication | Firebase Auth (REST API) |
| Database | Firebase Firestore |
| Prompt Engineering | Custom multi-template prompt system (`prompts.py`) |
| Environment | Python 3.11, dotenv |
| Version Control | Git + GitHub |

---

## Architecture

```
User Input
    │
    ▼
Intent Router (Chatbot.py)
    ├── Greeting        → Groq (conversational, no search)
    ├── Promo request   → Tavily (coupon search) → Groq (format)
    ├── Multi-product   → Tavily (per-item + fees) → Groq (basket total)
    ├── Ambiguous qty   → Tavily (standard sizes) → Groq (compare)
    └── Single product  → Tavily (price search) → Groq (format)
                                    │
                              prompts.py
                         (geo + category aware
                          prompt templates)
                                    │
                              Groq LLM
                          (LLaMA 3.3 70B)
                                    │
                           Streamlit UI
                        (HTML-rendered bubbles,
                         color-coded prices,
                         promo code cards)
```

---

## Project structure

```
PriceProbe/
├── main.py              # App entry point, navigation, Firebase init guard
├── Chatbot.py           # Core chatbot — intent routing, LLM calls, UI
├── prompts.py           # Geo-aware prompt templates (6 categories × 8 countries)
├── Home.py              # Landing page
├── About.py             # Team & mission page
├── Account.py           # Firebase Auth — login, signup, password reset
├── Feedback.py          # User feedback form
├── Contact.py           # Contact page
├── Images/              # UI assets
├── .env                 # API keys (not committed)
├── requirements.txt     # Dependencies
└── README.md
```

---

## Setup & installation

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/PriceProbe.git
cd PriceProbe
```

### 2. Create and activate virtual environment

```bash
python -m venv priceprobe
source priceprobe/bin/activate        # Mac/Linux
priceprobe\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
# Groq API — free at console.groq.com
GROQ_API_KEY=your_groq_api_key_here

# Groq model
MODEL_NAME=llama-3.3-70b-versatile

# Tavily Search API — free tier at tavily.com (1000 searches/month)
TAVILY_API_KEY=your_tavily_api_key_here

# Firebase
FIREBASE_API_KEY=your_firebase_web_api_key
GOOGLE_APPLICATION_CREDENTIALS=/full/path/to/your/firebase-adminsdk.json
```

### 5. Run the app

```bash
cd PriceProbe          # make sure you're in the folder with main.py
streamlit run main.py
```

---

## Usage examples

| You type | PriceProbe does |
|---|---|
| `hi` | Friendly greeting, introduces itself |
| `18 eggs` | Compares 12, 18, 24 count options with prices |
| `16 eggs` | Detects unusual quantity → shows standard size options |
| `eggs + milk + bread` | Full basket comparison — cheapest total store + delivery fees |
| `iPhone 16 price` | Compares across Amazon, Best Buy, Walmart, Target, Costco... |
| `any Walmart coupons?` | Fetches active promo codes with how-to-use instructions |
| `how do I use this code?` | Step-by-step redemption guide |
| `Paracetamol 500mg` | Pharmacy comparison + doctor consultation reminder |
| `Boston to NYC flight` | Travel platforms — MakeMyTrip → Expedia, Kayak, Google Flights |

---

## Platforms covered (by category)

| Category | Platforms |
|---|---|
| 🛒 Grocery | Amazon Fresh, Whole Foods, Instacart, Walmart, Target, Kroger, Gopuff, FreshDirect |
| 📱 Electronics | Amazon, Best Buy, Walmart, Target, Newegg, Costco, B&H, Micro Center |
| 💊 Pharmacy | CVS, Walgreens, Rite Aid, Amazon Pharmacy, GoodRx, Cost Plus Drugs |
| 👗 Fashion | Amazon, Nordstrom, Macy's, ASOS, H&M, Zara, Shein, Poshmark |
| 💄 Beauty | Sephora, Ulta, Amazon Beauty, Dermstore, Revolve |
| 🍔 Food | DoorDash, Uber Eats, Grubhub, Seamless |
| 📚 Books | Amazon, Barnes & Noble, ThriftBooks, AbeBooks, Chegg |
| ✈️ Travel | Expedia, Kayak, Google Flights, Booking.com, Airbnb, Hopper |
| 🎟️ Tickets | Ticketmaster, StubHub, SeatGeek, Vivid Seats, Eventbrite |

---

## Geo support

| Country | Currency | Example platforms |
|---|---|---|
| 🇺🇸 USA | $ | Amazon.com, Walmart, Target, CVS |
| 🇮🇳 India | ₹ | Amazon.in, Flipkart, BigBasket, 1mg |
| 🇬🇧 UK | £ | Amazon.co.uk, Currys, Boots, ASOS |
| 🇨🇦 Canada | CA$ | Amazon.ca, Best Buy CA, Shoppers Drug Mart |
| 🇦🇺 Australia | A$ | JB Hi-Fi, Woolworths, Chemist Warehouse |
| 🇦🇪 UAE | AED | Noon, Talabat, Aster Pharmacy |
| 🇸🇬 Singapore | S$ | Lazada, Shopee, Guardian |
| 🇩🇪 Germany | € | MediaMarkt, Zalando, DocMorris |

---

## Roadmap

- [ ] **Phase 1** — MySQL price history DB + ETL pipeline (pandas, SQLAlchemy)
- [ ] **Phase 2** — Price prediction ML model (XGBoost) — "Will it be cheaper next week?"
- [ ] **Phase 2** — Deal anomaly detection (Isolation Forest) — auto-flag flash deals
- [ ] **Phase 2** — Product name matching with sentence embeddings (NLP)
- [ ] **Phase 3** — Analytics dashboard page (Matplotlib/Seaborn/Power BI)
- [ ] **Phase 4** — AWS EC2 deployment + Lambda ETL cron job
- [ ] **Phase 4** — GitHub Actions CI/CD pipeline
- [ ] **Phase 5** — Barcode scanner (OpenCV + ZBar)
- [ ] **Phase 5** — Receipt scanner (OCR → item extraction → comparison)
- [ ] **RAG** — ChromaDB vector store over price history for semantic historical queries

---

## API keys needed

| Service | Free tier | Link |
|---|---|---|
| Groq | Free — fast LLaMA inference | [console.groq.com](https://console.groq.com) |
| Tavily | 1,000 searches/month free | [tavily.com](https://tavily.com) |
| Firebase | Free Spark plan | [firebase.google.com](https://firebase.google.com) |

---

## Contributing

Pull requests welcome. For major changes, open an issue first.

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/price-alerts`
3. Commit changes: `git commit -m 'Add price alert notifications'`
4. Push: `git push origin feature/price-alerts`
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Vaibhavi Braj**  
[GitHub](https://github.com/vaibhavi-tec) · [LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN)

> *Built to help students and budget shoppers stop wasting time checking 10 websites manually.*