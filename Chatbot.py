import streamlit as st
import os
import re
import requests
from dotenv import load_dotenv
from groq import Groq
from prompts import (
    get_prompt, detect_category, detect_country,
    get_platform_list, get_country_meta,
    GEO_PLATFORMS, CITY_TO_COUNTRY,
)

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
MODEL_NAME     = os.environ.get("MODEL_NAME", "llama-3.3-70b-versatile")
MAX_TOKENS     = 2000

# ── CATEGORY META ──────────────────────────────────────────────────────────────
CATEGORY_EMOJIS = {
    "all": "🌐", "electronics": "📱", "grocery": "🛒", "pharmacy": "💊",
    "fashion": "👗", "beauty": "💄", "food": "🍔", "books": "📚",
    "home": "🏠", "sports": "⚽", "travel": "✈️", "tickets": "🎟️",
}

QUICK_SUGGESTIONS = {
    "US": {
        "all":         ["18 eggs + milk + bread", "iPhone 16 price Boston", "Tylenol cheapest", "Nike shoes"],
        "electronics": ["iPhone 16 Best Buy vs Amazon", "Samsung 65\" TV", "AirPods Pro", "MacBook Air M3"],
        "grocery":     ["eggs + milk + butter", "Organic milk cheapest Boston", "Coffee + sugar + creamer", "Weekly groceries list"],
        "pharmacy":    ["Tylenol + Vitamin D + Zinc", "Tylenol 500mg price", "Blood pressure monitor", "Ibuprofen price"],
        "fashion":     ["Levi's 501 jeans USA", "Nike Air Max price", "Winter jacket cheapest", "Adidas sneakers"],
        "beauty":      ["CeraVe moisturizer price", "Rare Beauty blush", "Neutrogena sunscreen", "Fenty foundation"],
        "food":        ["Pizza cheapest delivery Boston", "Burger best deal", "Sushi delivery Boston", "Healthy meal kit"],
        "books":       ["Atomic Habits USA price", "Textbook cheapest", "Harry Potter set", "Self-help books"],
        "home":        ["Air purifier + humidifier", "Standing desk price", "Instant Pot deals", "Sofa best price"],
        "sports":      ["Nike running shoes", "Yoga mat + dumbbells", "Dumbbells set price", "Bike best deal"],
        "travel":      ["Boston to NYC flight", "Boston hotels this weekend", "Amtrak Boston NYC", "Car rental Boston"],
        "tickets":     ["Red Sox tickets", "Celtics tickets", "Bruins tickets", "Boston concert tickets"],
    },
    "IN": {
        "all":         ["Rice + dal + oil", "iPhone 16 price", "Paracetamol cheapest", "Nike shoes"],
        "electronics": ["iPhone 16 all platforms", "Samsung 65\" TV", "boAt Airdopes", "MacBook Air M3"],
        "grocery":     ["Tata Salt + Amul Butter + Eggs", "Basmati rice 5kg", "Fortune Oil + dal", "Weekly groceries"],
        "pharmacy":    ["Paracetamol + Vitamin D + Zinc", "BP monitor", "Dolo 650", "Multivitamin cheapest"],
        "fashion":     ["Levi's 501 jeans", "Nike Air Max", "Saree under ₹1000", "Puma shoes"],
        "beauty":      ["Minimalist Vitamin C", "Lakme foundation", "Mamaearth sunscreen", "Nykaa lipstick"],
        "food":        ["Biryani cheapest", "Pizza best offer", "Healthy meal box", "Cake delivery"],
        "books":       ["Atomic Habits price", "UPSC books cheapest", "Harry Potter set", "NCERT Class 10"],
        "home":        ["Prestige cooker + mixer", "Wooden dining table", "Air purifier", "Ceiling fan"],
        "sports":      ["SG cricket bat", "Yoga mat cheapest", "Adidas running shoes", "Decathlon cycle"],
        "travel":      ["Mumbai to Delhi flight", "Goa hotels", "Bangalore Chennai train", "Delhi Jaipur bus"],
        "tickets":     ["IPL 2025 tickets", "Arijit Singh concert", "Coldplay India", "Stand-up Mumbai"],
    },
    "DEFAULT": {
        "all":         ["Compare 3 products", "Best grocery deals", "Electronics cheapest", "Weekly shopping list"],
        "electronics": ["Smartphone best price", "Laptop cheapest", "Headphones deal", "TV price comparison"],
        "grocery":     ["Milk + eggs + bread", "Grocery deals today", "Supermarket cheapest", "Organic food price"],
        "pharmacy":    ["Medicine price comparison", "Vitamins cheapest", "Health monitor deals", "Pharmacy comparison"],
        "fashion":     ["Shoes best price", "Jeans cheapest", "Jacket deals", "Fashion sale today"],
        "beauty":      ["Skincare cheapest", "Makeup deals", "Perfume price", "Serum comparison"],
        "food":        ["Food delivery cheapest", "Pizza best deal", "Burger delivery", "Healthy meal box"],
        "books":       ["Books cheapest", "Textbook price", "Novel best deal", "Academic books"],
        "home":        ["Furniture cheapest", "Kitchen appliance deal", "Home decor price", "Mattress comparison"],
        "sports":      ["Sports shoes price", "Gym equipment cheapest", "Fitness gear deals", "Sports brand comparison"],
        "travel":      ["Flight cheapest", "Hotel best price", "Bus vs train", "Holiday deals"],
        "tickets":     ["Concert tickets", "Sports event tickets", "Movie tickets", "Event cheapest"],
    },
}

# ── GREETING PATTERNS ──────────────────────────────────────────────────────────
GREET_PATTERNS = {
    "hi", "hello", "hey", "hii", "helo", "howdy", "sup", "what's up",
    "good morning", "good afternoon", "good evening", "good night",
    "how are you", "how r u", "how are u", "how do you do",
    "i'm fine", "im fine", "i am fine", "i'm good", "im good", "i am good",
    "nice", "cool", "okay", "ok", "thanks", "thank you", "thankyou",
    "bye", "goodbye", "see you", "who are you", "what are you", "what can you do",
}

PRODUCT_KEYWORDS = {
    "price", "cost", "cheap", "cheapest", "best deal", "compare", "buy",
    "purchase", "rate", "offer", "discount", "how much", "where to buy",
    "find", "search", "shop", "order", "delivery", "available",
    "rupees", "₹", "$", "£", "€", "aed", "sgd",
    "phone", "laptop", "tv", "tablet", "headphone", "earphone", "watch",
    "shirt", "shoes", "dress", "jeans", "jacket",
    "rice", "dal", "milk", "butter", "oil", "salt", "sugar", "bread",
    "eggs", "coffee", "tea", "flour", "cheese", "yogurt", "pasta",
    "medicine", "tablet", "vitamin", "supplement", "paracetamol",
    "book", "novel", "flight", "hotel", "train", "bus", "ticket",
    "pizza", "burger", "biryani", "food", "grocery",
    "iphone", "samsung", "macbook", "airpods",
    "amazon", "walmart", "target", "costco", "instacart",
}

# ── AMBIGUOUS QUANTITIES ───────────────────────────────────────────────────────
AMBIGUOUS_QUANTITIES = {
    "eggs": {
        "trigger_quantities": ["16", "14", "15", "13", "11", "10"],
        "standard_options":   [
            {"qty": "12", "label": "12 eggs (1 dozen)"},
            {"qty": "18", "label": "18 eggs (1.5 dozen)"},
            {"qty": "24", "label": "24 eggs (2 dozen)"},
        ],
        "recommendation": "18-count trays are usually the best value per egg at most Boston stores.",
    },
    "milk": {
        "trigger_quantities": ["3", "7", "9", "5"],
        "standard_options": [
            {"qty": "half gallon", "label": "Half gallon (64 oz)"},
            {"qty": "gallon",      "label": "1 Gallon (128 oz)"},
        ],
        "recommendation": "A full gallon is almost always cheaper per oz.",
    },
    "beer": {
        "trigger_quantities": ["13", "14", "15", "17", "19", "20", "10"],
        "standard_options": [
            {"qty": "12-pack", "label": "12-pack"},
            {"qty": "18-pack", "label": "18-pack"},
            {"qty": "24-pack", "label": "24-pack"},
        ],
        "recommendation": "24-packs give the best cost per can.",
    },
}


# ── INTENT DETECTION ───────────────────────────────────────────────────────────
def is_greeting(text: str) -> bool:
    t = text.lower().strip()
    return any(g in t for g in GREET_PATTERNS)

def is_product_query(text: str) -> bool:
    t = text.lower().strip()
    for kw in PRODUCT_KEYWORDS:
        if kw in t:
            return True
    if len(t.split()) > 4 and not is_greeting(t):
        return True
    return False

def detect_ambiguity(query: str) -> dict | None:
    q = query.lower().strip()
    numbers = re.findall(r"\b(\d+)\b", q)
    for product, info in AMBIGUOUS_QUANTITIES.items():
        if product in q:
            for num in numbers:
                if num in info["trigger_quantities"]:
                    return {
                        "product":        product,
                        "typed_qty":      num,
                        "options":        info["standard_options"],
                        "recommendation": info["recommendation"],
                    }
    return None

def detect_multi_product(query: str) -> list:
    """
    Detect if the user typed multiple products separated by +, comma, and, &.
    Returns list of product strings if 2+ found, else empty list.
    Example: "eggs + milk + bread" → ["eggs", "milk", "bread"]
    """
    q = query.strip()
    # Split on +, comma, ' and ', &
    parts = re.split(r"[+,&]|\band\b", q, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]
    if len(parts) >= 2:
        return parts
    return []

def is_promo_request(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in [
        "promo", "coupon", "discount code", "offer code", "voucher",
        "promo code", "deal", "how to use", "redeem", "apply code",
        "tips", "tricks", "save more", "cashback"
    ])


# ── WEB SEARCH ────────────────────────────────────────────────────────────────
def web_search(query: str, location: str = "", max_results: int = 6) -> str:
    if not TAVILY_API_KEY:
        return "Note: No TAVILY_API_KEY — using training knowledge only. Get free key at tavily.com."
    try:
        payload = {
            "api_key":        TAVILY_API_KEY,
            "query":          f"{query} {location}".strip(),
            "max_results":    max_results,
            "search_depth":   "advanced",
            "include_answer": True,
        }
        resp = requests.post("https://api.tavily.com/search", json=payload, timeout=12)
        data = resp.json()
        parts = []
        if data.get("answer"):
            parts.append(f"Summary: {data['answer']}")
        for r in data.get("results", []):
            title   = r.get("title", "")
            url     = r.get("url", "")
            content = r.get("content", "")[:350]
            parts.append(f"- [{title}]({url}): {content}")
        return "\n".join(parts) if parts else "No results found."
    except Exception as e:
        return f"Search error: {str(e)}"


# ── GROQ LLM CALL ─────────────────────────────────────────────────────────────
def call_groq(system: str, user: str, history: list = None, temp: float = 0.2) -> str:
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not found in .env"
    client   = Groq(api_key=GROQ_API_KEY)
    messages = [{"role": "system", "content": system}]
    for msg in (history or [])[-4:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user})
    try:
        r = client.chat.completions.create(
            model=MODEL_NAME, messages=messages,
            max_tokens=MAX_TOKENS, temperature=temp,
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Groq error: {str(e)}"


# ── SINGLE PRODUCT COMPARISON ─────────────────────────────────────────────────
def get_price_comparison(query: str, category: str, location: str, history: list) -> str:
    system_prompt, _ = get_prompt(query, category, location)
    search_context   = web_search(f"{query} price", location)

    user_msg = (
        f"User query: {query}\nLocation: {location}\n\n"
        f"Live search results:\n{search_context}\n\n"
        f"Compare prices across all relevant platforms for {location}.\n"
        f"FORMATTING (HTML):\n"
        f"- Wrap best price: <span class='price-best'>$X.XX</span>\n"
        f"- 2nd/3rd prices: <span class='price-regular'>$X.XX</span>\n"
        f"- Higher prices: <span class='price-high'>$X.XX</span>\n"
        f"- 1st row: <div class='best-deal-row'>...</div>\n"
        f"- 2nd row: <div class='second-deal-row'>...</div>\n"
        f"- 3rd row: <div class='third-deal-row'>...</div>\n"
        f"- Bold platform names: <strong>PlatformName</strong>\n"
        f"- Top 2 must have links: <a href='URL'>View on Platform</a>\n"
        f"- Use <br> for line breaks."
    )
    return call_groq(system_prompt, user_msg, history)


# ── SMART BASKET COMPARISON ───────────────────────────────────────────────────
def get_basket_comparison(products: list, location: str, history: list) -> str:
    """
    Core feature: compare a list of products across all platforms.
    1. Fetches price of each product on each major platform
    2. Calculates which single platform has the lowest TOTAL basket cost
    3. Accounts for delivery fees and membership discounts
    4. Shows promo codes / tips for the winning platform
    5. Asks if user wants to buy all from one place
    """
    meta      = get_country_meta(detect_country(location))
    currency  = meta["currency"]
    country   = meta["country_name"]

    # Step 1: Fetch prices for each product
    product_data = {}
    for product in products:
        context = web_search(f"{product} price grocery {location}", location, max_results=5)
        product_data[product] = context

    # Step 2: Fetch platform delivery fees + promo codes
    fee_context   = web_search(f"grocery delivery fees comparison {location} 2024 Amazon Walmart Instacart Target", location, max_results=4)
    promo_context = web_search(f"grocery promo codes coupons {location} {country} 2024 site:retailmenot.com OR site:coupons.com OR site:honey.com", location, max_results=4)

    # Build the prompt context
    product_sections = "\n\n".join(
        f"PRODUCT: {p}\nSearch results:\n{data}"
        for p, data in product_data.items()
    )

    system = f"""You are PriceProbe, a smart basket shopping assistant for {location}, {country}.
You help students and budget shoppers find the best total deal when buying multiple products.
Currency: {currency}

Your job:
1. For each product, find its price on each major platform
2. Calculate the TOTAL basket cost per platform (sum of all products)
3. Add each platform's delivery fee to get the TRUE total cost
4. Crown the BEST PLATFORM — the one with the lowest total after fees
5. Share any active promo codes or tips to save even more
6. Ask the user if they want to buy all from one site or mix-and-match

FORMATTING — use HTML only, no markdown:
- Use <br> for line breaks
- Section headers: <strong style='font-size:17px;color:#C4B5FD;'>HEADER</strong><br>
- Best price per product: <span class='price-best'>{currency}X.XX</span>
- Other prices: <span class='price-regular'>{currency}X.XX</span>
- Higher prices: <span class='price-high'>{currency}X.XX</span>
- Best platform basket: <div class='best-deal-row'>...</div>
- 2nd platform: <div class='second-deal-row'>...</div>
- 3rd platform: <div class='third-deal-row'>...</div>
- Bold platform names: <strong>PlatformName</strong>
- Links: <a href='URL'>View on Platform</a>
- Promo codes in a box: <div style='background:rgba(74,222,128,0.15);border:1px solid #4ADE80;border-radius:8px;padding:10px 14px;margin:8px 0;'>🎟️ <strong>PROMO CODE: CODE123</strong> — description</div>
- Tips in a box: <div style='background:rgba(125,211,252,0.1);border:1px solid #7DD3FC;border-radius:8px;padding:10px 14px;margin:8px 0;'>💡 <strong>TIP:</strong> tip text</div>
"""

    user_msg = f"""The user wants to buy these {len(products)} products in {location}:
{chr(10).join(f"- {p}" for p in products)}

PRODUCT PRICE DATA:
{product_sections}

PLATFORM DELIVERY FEES:
{fee_context}

PROMO CODES & DEALS:
{promo_context}

Please:
1. Show a per-product price table across platforms
2. Show total basket cost per platform (prices + delivery fee)
3. Highlight the BEST PLATFORM to buy everything from
4. Show any active promo codes in styled boxes
5. Give 2-3 money-saving tips for the winning platform
6. Ask: "Would you like to buy all from [winning platform], or mix-and-match for even more savings?"
"""

    return call_groq(system, user_msg, history, temp=0.25)


# ── PROMO & TIPS HANDLER ──────────────────────────────────────────────────────
def get_promo_tips(query: str, location: str, history: list) -> str:
    """Handle requests about promo codes, coupons, and how to use them."""
    context = web_search(f"promo codes coupons deals {query} {location} 2024", location, max_results=6)

    # Check if asking HOW TO USE a code
    how_to = any(kw in query.lower() for kw in ["how to use", "how do i use", "apply", "redeem", "enter", "guide"])

    if how_to:
        system = (
            "You are PriceProbe, a helpful shopping guide. "
            "The user wants step-by-step instructions on how to apply a promo code. "
            "Give clear numbered steps using HTML: <ol><li>Step</li></ol>. "
            "Use <strong> for important parts. Keep it simple and friendly."
        )
        user_msg = f"How do I use this promo code / offer: {query}\nContext: {context}"
    else:
        system = (
            f"You are PriceProbe, a deals expert for {location}. "
            "Find and present active promo codes, coupons, and money-saving tips. "
            "Format each promo code in a styled box using HTML: "
            "<div style='background:rgba(74,222,128,0.15);border:1px solid #4ADE80;"
            "border-radius:8px;padding:10px 14px;margin:8px 0;'>"
            "🎟️ <strong>CODE: XXXXX</strong> — description, expiry if known</div>. "
            "Tips in: <div style='background:rgba(125,211,252,0.1);border:1px solid #7DD3FC;"
            "border-radius:8px;padding:10px 14px;margin:8px 0;'>"
            "💡 <strong>TIP:</strong> tip text</div>. "
            "End by offering: 'Want step-by-step instructions on how to use any of these?'"
        )
        user_msg = f"Find promo codes and deals for: {query} in {location}\nSearch results:\n{context}"

    return call_groq(system, user_msg, history, temp=0.3)


# ── AMBIGUITY HANDLER ─────────────────────────────────────────────────────────
def get_ambiguity_response(ambiguity: dict, location: str, history: list) -> str:
    product        = ambiguity["product"]
    typed_qty      = ambiguity["typed_qty"]
    options        = ambiguity["standard_options"]
    recommendation = ambiguity["recommendation"]

    results = []
    for opt in options:
        ctx = web_search(f"{opt['qty']} {product} price {location}", location, max_results=4)
        results.append({"label": opt["label"], "context": ctx})

    options_text = "\n\n".join(
        f"Option {i+1} — {r['label']}:\n{r['context']}"
        for i, r in enumerate(results)
    )

    system = (
        f"You are PriceProbe, a friendly shopping assistant in {location}. "
        f"The user typed '{typed_qty} {product}' which is unusual. "
        "Show prices for each standard size side by side using HTML. "
        "Use div classes best-deal-row, second-deal-row, third-deal-row. "
        "Use span classes price-best (green), price-regular (blue), price-high (red). "
        "Bold platform names. Include links for top 2. "
        f"End with 💡 <strong>Recommendation:</strong> {recommendation}<br><br>"
        "Ask: 'Which size works best for you?'"
    )
    user_msg = (
        f"User typed '{typed_qty} {product}'. Show standard size prices in {location}:\n\n"
        f"{options_text}"
    )
    return call_groq(system, user_msg, history, temp=0.3)


# ── CONVERSATIONAL REPLY ──────────────────────────────────────────────────────
CHAT_SYSTEM = """You are PriceProbe, a friendly shopping assistant based in Boston, USA.
You help students and budget-conscious shoppers find the best deals.

For greetings and small talk:
- Be warm, short, and friendly (1-3 sentences max)
- On first message: introduce yourself and mention you can compare grocery lists, electronics, medicines across Amazon, Walmart, Target, Instacart, Best Buy and 50+ stores
- Mention the smart basket feature: "Just type a few items separated by + and I'll find the best site to buy them all!"
- NEVER do price comparisons for greetings
"""

def get_conversational_reply(message: str, history: list) -> str:
    return call_groq(CHAT_SYSTEM, message, history, temp=0.7)


# ── MAIN ROUTER ───────────────────────────────────────────────────────────────
def handle_message(query: str, category: str, location: str, history: list) -> tuple:
    """
    Routes messages to the right handler:
    1. Greeting/chitchat          → conversational reply
    2. Promo/coupon/tips request  → promo tips handler
    3. Multi-product (basket)     → smart basket comparison
    4. Ambiguous quantity         → clarification with options
    5. Single product             → standard price comparison
    """
    # Route 1: greeting
    if is_greeting(query) and not is_product_query(query):
        return get_conversational_reply(query, history), "chat"

    # Route 2: promo/tips
    if is_promo_request(query):
        return get_promo_tips(query, location, history), "promo"

    # Route 3: multi-product basket
    products = detect_multi_product(query)
    if products:
        return get_basket_comparison(products, location, history), "basket"

    # Route 4: ambiguous quantity
    ambiguity = detect_ambiguity(query)
    if ambiguity:
        return get_ambiguity_response(ambiguity, location, history), "ambiguity"

    # Route 5: single product
    return get_price_comparison(query, category, location, history), "search"


# ── HELPERS ───────────────────────────────────────────────────────────────────
def get_suggestions(category: str, country_code: str) -> list:
    cs = QUICK_SUGGESTIONS.get(country_code, QUICK_SUGGESTIONS["DEFAULT"])
    return cs.get(category, cs["all"])

def flag_for_country(code: str) -> str:
    return {"IN":"🇮🇳","US":"🇺🇸","UK":"🇬🇧","CA":"🇨🇦","AU":"🇦🇺","AE":"🇦🇪","SG":"🇸🇬","DE":"🇩🇪"}.get(code,"🌍")

def spinner_text(route: str, location: str) -> str:
    return {
        "chat":      "Typing...",
        "promo":     "🎟️ Hunting for promo codes and deals...",
        "basket":    "🧠 Comparing basket totals across all platforms...",
        "ambiguity": "🔍 Checking standard sizes and prices...",
        "search":    f"🔍 Searching platforms in {location}...",
    }.get(route, "Searching...")


# ── STREAMLIT APP ──────────────────────────────────────────────────────────────
def app():
    st.markdown("""
    <style>
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* ── Bubbles ── */
    .user-bubble {
        background: #534AB7; color: #fff;
        padding: 14px 18px; border-radius: 18px 18px 4px 18px;
        margin: 4px 0 4px auto; max-width: 78%;
        font-size: 16px; line-height: 1.6; width: fit-content;
    }
    .bot-bubble {
        background: rgba(255,255,255,0.08); color: #f0f0f0;
        padding: 16px 20px; border-radius: 18px 18px 18px 4px;
        margin: 4px auto 4px 0; max-width: 92%;
        font-size: 16px; line-height: 1.75;
        border: 1px solid rgba(255,255,255,0.12); width: fit-content;
    }

    /* ── Price colors ── */
    .bot-bubble .price-best    { color: #4ADE80; font-weight: 700; font-size: 18px; }
    .bot-bubble .price-regular { color: #7DD3FC; font-weight: 600; font-size: 17px; }
    .bot-bubble .price-high    { color: #FCA5A5; font-weight: 600; font-size: 16px; }

    /* ── Result rows ── */
    .bot-bubble .best-deal-row {
        background: rgba(74,222,128,0.1); border-left: 3px solid #4ADE80;
        border-radius: 0 8px 8px 0; padding: 8px 14px; margin: 8px 0;
    }
    .bot-bubble .second-deal-row {
        background: rgba(125,211,252,0.08); border-left: 3px solid #7DD3FC;
        border-radius: 0 8px 8px 0; padding: 8px 14px; margin: 8px 0;
    }
    .bot-bubble .third-deal-row {
        background: rgba(196,181,253,0.08); border-left: 3px solid #C4B5FD;
        border-radius: 0 8px 8px 0; padding: 8px 14px; margin: 8px 0;
    }

    /* ── Links, bold, lists ── */
    .bot-bubble a      { color: #93C5FD; text-decoration: underline; }
    .bot-bubble strong { color: #ffffff; }
    .bot-bubble ol, .bot-bubble ul { padding-left: 20px; margin: 8px 0; }
    .bot-bubble li     { margin-bottom: 6px; }

    /* ── Message rows ── */
    .msg-row-user { display: flex; justify-content: flex-end; margin: 8px 0; }
    .msg-row-bot  { display: flex; justify-content: flex-start; margin: 8px 0; }
    .avatar {
        width: 32px; height: 32px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: 600; flex-shrink: 0; margin-top: 4px;
    }
    .av-bot  { background: #534AB7; color: #fff; margin-right: 10px; }
    .av-user { background: rgba(255,255,255,0.15); color: #fff; margin-left: 10px; }

    /* ── Buttons / chips ── */
    .stButton > button {
        background: rgba(83,74,183,0.25) !important; color: #AFA9EC !important;
        border: 1px solid #534AB7 !important; border-radius: 20px !important;
        font-size: 13px !important; padding: 5px 14px !important;
    }
    .stButton > button:hover {
        background: rgba(83,74,183,0.5) !important; color: #fff !important;
    }

    /* ── Input ── */
    .stTextInput > div > div > input {
        background: #1a1740 !important;
        border: 1px solid rgba(83,74,183,0.6) !important;
        border-radius: 24px !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
        font-size: 15px !important;
        padding: 12px 20px !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.4) !important;
        -webkit-text-fill-color: rgba(255,255,255,0.4) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #7F77DD !important;
        box-shadow: 0 0 0 2px rgba(127,119,221,0.25) !important;
        background: #1a1740 !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(83,74,183,0.6) !important;
        border-radius: 10px !important; color: #fff !important;
    }

    /* ── Title / subtitle ── */
    .pp-title {
        font-size: 30px; font-weight: 700;
        background: linear-gradient(90deg, #AFA9EC, #7F77DD);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .pp-sub { color: rgba(255,255,255,0.45); font-size: 14px; margin-bottom: 12px; }

    /* ── Geo bar ── */
    .geo-bar {
        display: flex; align-items: center; gap: 10px;
        background: rgba(83,74,183,0.15); border: 1px solid rgba(83,74,183,0.4);
        border-radius: 12px; padding: 7px 16px;
        font-size: 14px; color: #AFA9EC; margin-bottom: 14px;
    }

    /* ── Feature badge ── */
    .feature-hint {
        display: inline-block;
        background: rgba(74,222,128,0.12); color: #4ADE80;
        border: 1px solid #4ADE80; border-radius: 10px;
        font-size: 12px; padding: 3px 10px; margin: 2px 4px 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Session state ──────────────────────────────────────────────────────────
    defaults = {
        "messages":      [],
        "category":      "all",
        "location":      "Boston",
        "country_code":  "US",
        "pending_input": "",
        "last_route":    "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔍 PriceProbe")
        st.markdown("---")

        st.markdown("**📍 Your Location**")
        loc_input = st.text_input(
            "City or Country", value=st.session_state.location,
            placeholder="e.g. Boston, Bangalore, London...",
            label_visibility="collapsed",
        )
        if loc_input != st.session_state.location:
            st.session_state.location     = loc_input
            st.session_state.country_code = detect_country(loc_input)
            st.session_state.messages     = []
            st.rerun()

        code = st.session_state.country_code
        meta = get_country_meta(code)
        st.markdown(
            f"<div style='color:#AFA9EC;font-size:12px;margin:4px 0 12px'>"
            f"{flag_for_country(code)} <b>{meta['country_name']}</b>"
            f" &nbsp;|&nbsp; <b>{meta['currency']}</b></div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("**Category**")
        categories = list(CATEGORY_EMOJIS.keys())
        labels     = [f"{CATEGORY_EMOJIS[c]} {c.capitalize()}" for c in categories]
        selected   = st.selectbox("Filter", labels,
                                  index=categories.index(st.session_state.category),
                                  label_visibility="collapsed")
        st.session_state.category = categories[labels.index(selected)]

        st.markdown("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        st.markdown(
            "<div style='color:rgba(255,255,255,0.25);font-size:11px;margin-top:8px'>"
            "Powered by Groq + Tavily<br>Geo-aware · 50+ platforms</div>",
            unsafe_allow_html=True,
        )

    # ── Main area ──────────────────────────────────────────────────────────────
    st.markdown('<div class="pp-title">PriceProbe 🔍</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pp-sub">Smart price comparison for students & budget shoppers — '
        'Boston & beyond, every category, 50+ platforms</div>',
        unsafe_allow_html=True,
    )

    # Feature hints
    st.markdown(
        '<span class="feature-hint">🧠 Smart Basket</span>'
        '<span class="feature-hint">🎟️ Promo Codes</span>'
        '<span class="feature-hint">📦 Size Advisor</span>'
        '<span class="feature-hint">💡 Savings Tips</span>',
        unsafe_allow_html=True,
    )

    loc_display = st.session_state.location or meta["country_name"]
    cat         = st.session_state.category
    st.markdown(
        f'<div class="geo-bar">'
        f'{flag_for_country(code)} <b>{loc_display}</b>'
        f'&nbsp;&nbsp;·&nbsp;&nbsp;{CATEGORY_EMOJIS[cat]} <b>{cat.capitalize()}</b>'
        f'&nbsp;&nbsp;·&nbsp;&nbsp;<span style="color:rgba(255,255,255,0.4)">{meta["currency"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Suggestion chips ───────────────────────────────────────────────────────
    suggestions = get_suggestions(cat, code)
    cols = st.columns(len(suggestions))
    for i, s in enumerate(suggestions):
        with cols[i]:
            if st.button(s, key=f"chip_{i}"):
                st.session_state.pending_input = s
                st.rerun()

    st.markdown("---")

    # ── Chat history ───────────────────────────────────────────────────────────
    with st.container():
        if not st.session_state.messages:
            plist_sample = get_platform_list("all", code).split(", ")[:5]
            st.markdown(
                f"""<div class="msg-row-bot">
                  <div class="avatar av-bot">PP</div>
                  <div class="bot-bubble">
                    Hey! 👋 I'm <strong>PriceProbe</strong> — your smart shopping buddy in {loc_display} {flag_for_country(code)}.<br><br>
                    I'm built for <strong>students and budget shoppers</strong> who want the best deal without
                    checking 10 websites manually. Here's what I can do:<br><br>
                    🧠 <strong>Smart Basket</strong> — type <code>eggs + milk + bread</code> and I'll find
                    which single store has the cheapest total (including delivery fees!)<br>
                    🎟️ <strong>Promo Codes</strong> — ask "any Amazon coupons today?" and I'll show active codes + how to use them<br>
                    📦 <strong>Size Advisor</strong> — type "16 eggs" and I'll compare 12, 18 & 24 count options<br>
                    💡 <strong>Savings Tips</strong> — platform-specific tricks to pay less<br><br>
                    Platforms I search: <strong>{", ".join(plist_sample)} and more</strong><br><br>
                    What are you shopping for today? 🛒
                  </div>
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="msg-row-user">'
                        f'<div class="user-bubble">{msg["content"]}</div>'
                        f'<div class="avatar av-user">You</div></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="msg-row-bot">'
                        f'<div class="avatar av-bot">PP</div>'
                        f'<div class="bot-bubble">{msg["content"]}</div></div>',
                        unsafe_allow_html=True,
                    )

    # ── Input ──────────────────────────────────────────────────────────────────
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([9, 1])
        with col_input:
            user_input = st.text_input(
                "Message",
                value=st.session_state.pending_input,
                placeholder="Try: 'eggs + milk + bread'  or  'any Walmart coupons?'  or  'iPhone 16 price'",
                label_visibility="collapsed",
            )
        with col_btn:
            submitted = st.form_submit_button("➤")

    if st.session_state.pending_input and not submitted:
        user_input = st.session_state.pending_input
        submitted  = True

    if submitted and user_input.strip():
        st.session_state.pending_input = ""
        query = user_input.strip()

        st.session_state.messages.append({"role": "user", "content": query})

        # Detect route for spinner text
        if is_greeting(query) and not is_product_query(query):
            route = "chat"
        elif is_promo_request(query):
            route = "promo"
        elif detect_multi_product(query):
            route = "basket"
        elif detect_ambiguity(query):
            route = "ambiguity"
        else:
            route = "search"

        with st.spinner(spinner_text(route, loc_display)):
            reply, _ = handle_message(
                query, st.session_state.category,
                st.session_state.location or meta["country_name"],
                st.session_state.messages[:-1],
            )

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()


if __name__ == "__main__":
    app()