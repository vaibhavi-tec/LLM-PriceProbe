"""
prompts.py — PriceProbe LLM Prompt Templates (Geo-Location Aware)

RULES FOR ALL PROMPTS:
- Always tailor platform suggestions to the user's detected country/region
- Never fabricate prices — only report what web search finds
- Always sort results lowest price first
- Always highlight the best deal clearly
- Always include direct links
- Surface local cashback, bank offers, EMI, and subscription discounts
- For quick-commerce, only suggest platforms that operate in the user's city
"""

# ── GEO: Country detection keywords ──────────────────────────────
# Maps city/region mentions → country code
CITY_TO_COUNTRY = {
    # India
    "mumbai": "IN", "delhi": "IN", "bangalore": "IN", "bengaluru": "IN",
    "hyderabad": "IN", "chennai": "IN", "kolkata": "IN", "pune": "IN",
    "ahmedabad": "IN", "jaipur": "IN", "surat": "IN", "lucknow": "IN",
    "kanpur": "IN", "nagpur": "IN", "indore": "IN", "bhopal": "IN",
    "visakhapatnam": "IN", "patna": "IN", "vadodara": "IN", "goa": "IN",
    "india": "IN",
    # USA
    "boston": "US", "new york": "US", "los angeles": "US", "chicago": "US",
    "houston": "US", "phoenix": "US", "philadelphia": "US", "san antonio": "US",
    "san diego": "US", "dallas": "US", "san francisco": "US", "seattle": "US",
    "denver": "US", "austin": "US", "nashville": "US", "miami": "US",
    "atlanta": "US", "portland": "US", "las vegas": "US", "usa": "US",
    "america": "US", "united states": "US",
    # UK
    "london": "UK", "manchester": "UK", "birmingham": "UK", "glasgow": "UK",
    "edinburgh": "UK", "bristol": "UK", "leeds": "UK", "uk": "UK",
    "england": "UK", "britain": "UK",
    # Canada
    "toronto": "CA", "vancouver": "CA", "montreal": "CA", "calgary": "CA",
    "ottawa": "CA", "edmonton": "CA", "canada": "CA",
    # Australia
    "sydney": "AU", "melbourne": "AU", "brisbane": "AU", "perth": "AU",
    "adelaide": "AU", "australia": "AU",
    # UAE
    "dubai": "AE", "abu dhabi": "AE", "sharjah": "AE", "uae": "AE",
    "emirates": "AE",
    # Singapore
    "singapore": "SG",
    # Germany
    "berlin": "DE", "munich": "DE", "hamburg": "DE", "germany": "DE",
}

# ── GEO: Platform registry by country ────────────────────────────
GEO_PLATFORMS = {
    "IN": {
        "electronics": [
            "Amazon.in", "Flipkart", "Croma", "Reliance Digital",
            "Vijay Sales", "Tata CLiQ", "Bajaj Electronics",
            "Poorvika", "Sangeetha Mobiles", "Snapdeal", "JioMart",
        ],
        "grocery": [
            "BigBasket", "Blinkit", "Zepto", "Swiggy Instamart",
            "Amazon Fresh", "JioMart", "Flipkart Grocery",
            "DMart Ready", "Milkbasket", "Country Delight", "BB Now",
        ],
        "pharmacy": [
            "1mg", "PharmEasy", "Netmeds", "Apollo Pharmacy",
            "MedPlus", "Practo", "Flipkart Health+",
            "Amazon Pharmacy", "Wellness Forever", "Healthkart",
        ],
        "fashion": [
            "Myntra", "Ajio", "Amazon Fashion", "Flipkart Fashion",
            "Nykaa Fashion", "Meesho", "Tata CLiQ Fashion",
            "Limeroad", "Zivame", "Clovia",
        ],
        "beauty": [
            "Nykaa", "Purplle", "Amazon Beauty", "Flipkart Beauty",
            "Tira (Reliance)", "Smytten", "Sephora India",
            "Mamaearth", "Sugar Cosmetics",
        ],
        "food": [
            "Swiggy", "Zomato", "EatSure", "Domino's India",
            "McDonald's India", "KFC India", "Pizza Hut India",
            "Licious", "FreshToHome",
        ],
        "books": [
            "Amazon.in", "Flipkart", "Crossword", "Sapna Online",
            "IndiaBound", "Kitabay", "AbeBooks India",
        ],
        "home": [
            "Amazon.in", "Flipkart", "Pepperfry", "Urban Ladder",
            "IKEA India", "Godrej Interio", "HomeTown", "WoodenStreet",
        ],
        "sports": [
            "Amazon.in", "Flipkart", "Decathlon India",
            "Sportsuncle", "Khelmart", "ProSportsIndia",
        ],
        "travel": [
            "MakeMyTrip", "Goibibo", "Yatra", "Cleartrip",
            "EaseMyTrip", "IRCTC", "Ixigo", "RedBus", "Booking.com",
        ],
        "tickets": [
            "BookMyShow", "Paytm Insider", "Zomato Live",
            "District (by Zomato)", "SportsFlick", "IRCTC",
        ],
        "currency": "₹",
        "country_name": "India",
    },

    "US": {
        "electronics": [
            "Amazon.com", "Best Buy", "Walmart", "Target", "Newegg",
            "B&H Photo", "Micro Center", "Apple Store", "Costco",
            "Sam's Club", "eBay",
        ],
        "grocery": [
            "Amazon Fresh", "Whole Foods", "Instacart", "Walmart Grocery",
            "Target Same-Day", "Kroger", "Safeway", "Shipt",
            "FreshDirect", "Gopuff", "DoorDash Grocery",
        ],
        "pharmacy": [
            "CVS Pharmacy", "Walgreens", "Rite Aid", "Walmart Pharmacy",
            "Costco Pharmacy", "Amazon Pharmacy", "GoodRx",
            "Mark Cuban Cost Plus Drugs", "Blink Health",
        ],
        "fashion": [
            "Amazon Fashion", "Nordstrom", "Macy's", "ASOS",
            "H&M", "Zara", "Gap", "Target Fashion", "Walmart Fashion",
            "Shein", "Poshmark", "ThredUp",
        ],
        "beauty": [
            "Sephora", "Ulta Beauty", "Amazon Beauty", "Target Beauty",
            "Walmart Beauty", "Dermstore", "Revolve",
        ],
        "food": [
            "DoorDash", "Uber Eats", "Grubhub", "Instacart",
            "Seamless", "Postmates", "Gopuff",
        ],
        "books": [
            "Amazon.com", "Barnes & Noble", "ThriftBooks",
            "AbeBooks", "eBay Books", "Chegg", "Book Depository",
        ],
        "home": [
            "Amazon.com", "Wayfair", "IKEA", "Home Depot",
            "Lowe's", "Target", "Walmart", "Costco",
        ],
        "sports": [
            "Amazon.com", "Dick's Sporting Goods", "Nike",
            "Adidas", "Under Armour", "Walmart Sports", "REI",
        ],
        "travel": [
            "Expedia", "Google Flights", "Kayak", "Priceline",
            "Booking.com", "Hotels.com", "Airbnb", "Hopper",
            "Scott's Cheap Flights", "Skyscanner",
        ],
        "tickets": [
            "Ticketmaster", "StubHub", "SeatGeek", "Vivid Seats",
            "AXS", "Eventbrite", "Live Nation",
        ],
        "currency": "$",
        "country_name": "USA",
    },

    "UK": {
        "electronics": [
            "Amazon.co.uk", "Currys", "Argos", "John Lewis",
            "Very", "AO.com", "Richer Sounds", "ebuyer", "eBay UK",
        ],
        "grocery": [
            "Tesco", "Sainsbury's", "Asda", "Morrisons",
            "Waitrose", "Ocado", "Amazon Fresh UK", "Aldi UK",
            "Lidl UK", "Getir", "Gorillas",
        ],
        "pharmacy": [
            "Boots", "LloydsPharmacy", "Superdrug",
            "Amazon Pharmacy UK", "Chemist Direct", "Pharmacy2U",
        ],
        "fashion": [
            "ASOS", "Next", "M&S", "Topshop", "H&M UK",
            "Zara UK", "Amazon Fashion UK", "Very", "Boohoo",
        ],
        "beauty": [
            "Boots Beauty", "Superdrug Beauty", "Lookfantastic",
            "Cult Beauty", "Space NK", "Sephora UK",
        ],
        "food": [
            "Deliveroo", "Uber Eats UK", "Just Eat",
            "Amazon Fresh UK",
        ],
        "books": [
            "Amazon.co.uk", "Waterstones", "Book Depository",
            "Hive", "eBay UK Books",
        ],
        "home": [
            "Amazon.co.uk", "IKEA UK", "Argos", "John Lewis",
            "Wayfair UK", "Dunelm", "B&Q",
        ],
        "sports": [
            "Amazon.co.uk", "Sports Direct", "JD Sports",
            "Decathlon UK", "Nike UK", "Adidas UK",
        ],
        "travel": [
            "Skyscanner", "Google Flights", "Expedia UK",
            "Booking.com", "TravelSupermarket", "easyJet",
            "British Airways", "Trainline",
        ],
        "tickets": [
            "Ticketmaster UK", "Eventbrite UK", "See Tickets",
            "AXS UK", "StubHub UK", "Dice",
        ],
        "currency": "£",
        "country_name": "UK",
    },

    "CA": {
        "electronics": [
            "Amazon.ca", "Best Buy Canada", "Walmart Canada",
            "Canada Computers", "Memory Express", "Costco Canada",
        ],
        "grocery": [
            "Amazon Fresh Canada", "Instacart Canada", "Walmart Grocery CA",
            "Loblaws", "Metro", "Sobeys", "Voila by Sobeys",
        ],
        "pharmacy": [
            "Shoppers Drug Mart", "Rexall", "London Drugs",
            "Walmart Pharmacy CA", "Amazon Pharmacy CA",
        ],
        "fashion": [
            "Amazon.ca", "Hudson's Bay", "Roots", "Aritzia",
            "ASOS CA", "H&M Canada", "Zara Canada",
        ],
        "beauty": [
            "Sephora Canada", "Shoppers Beauty", "Amazon Beauty CA",
            "Ulta Canada", "Well.ca",
        ],
        "food": [
            "SkipTheDishes", "DoorDash Canada", "Uber Eats Canada",
            "Ritual", "Fantuan",
        ],
        "books": [
            "Amazon.ca", "Indigo/Chapters", "AbeBooks CA",
            "eBay Canada Books",
        ],
        "home": [
            "Amazon.ca", "IKEA Canada", "Wayfair CA",
            "Walmart Canada", "Home Depot Canada",
        ],
        "sports": [
            "Amazon.ca", "Sport Chek", "MEC",
            "Decathlon Canada", "Nike Canada",
        ],
        "travel": [
            "Expedia.ca", "Skyscanner", "Google Flights",
            "Booking.com", "Hopper", "Air Canada", "WestJet",
        ],
        "tickets": [
            "Ticketmaster Canada", "StubHub Canada",
            "Eventbrite Canada", "Live Nation Canada",
        ],
        "currency": "CA$",
        "country_name": "Canada",
    },

    "AU": {
        "electronics": [
            "Amazon.com.au", "JB Hi-Fi", "Harvey Norman",
            "Officeworks", "The Good Guys", "Kogan", "eBay AU",
        ],
        "grocery": [
            "Woolworths", "Coles", "Amazon Fresh AU",
            "IGA", "ALDI Australia", "Instacart AU",
        ],
        "pharmacy": [
            "Chemist Warehouse", "Priceline Pharmacy",
            "Terry White Chemists", "Amazon AU Pharmacy",
        ],
        "fashion": [
            "ASOS AU", "THE ICONIC", "David Jones",
            "Myer", "Amazon AU Fashion", "H&M AU",
        ],
        "beauty": [
            "Sephora AU", "Priceline Beauty", "MECCA",
            "Adore Beauty", "Amazon AU Beauty",
        ],
        "food": [
            "Uber Eats AU", "DoorDash AU",
            "Menulog", "Deliveroo AU",
        ],
        "books": [
            "Amazon.com.au", "Booktopia", "Book Depository AU",
            "Angus & Robertson",
        ],
        "home": [
            "Amazon.com.au", "IKEA AU", "Temple & Webster",
            "Harvey Norman", "Bunnings",
        ],
        "sports": [
            "Amazon.com.au", "Rebel Sport", "Decathlon AU",
            "Wiggle AU", "Nike AU",
        ],
        "travel": [
            "Webjet", "Skyscanner", "Google Flights",
            "Booking.com", "Expedia AU", "Qantas", "Jetstar",
        ],
        "tickets": [
            "Ticketek", "Ticketmaster AU",
            "Moshtix", "Eventbrite AU",
        ],
        "currency": "A$",
        "country_name": "Australia",
    },

    "AE": {
        "electronics": [
            "Amazon.ae", "Noon", "Sharaf DG", "Jumbo Electronics",
            "Virgin Megastore UAE", "eXtra", "Carrefour UAE",
        ],
        "grocery": [
            "Amazon Fresh UAE", "Noon Daily", "Carrefour UAE",
            "Talabat Grocery", "Instashop", "Kibsons", "Spinneys",
        ],
        "pharmacy": [
            "Aster Pharmacy", "Boots UAE", "Life Pharmacy",
            "Mediclinic Pharmacy", "Amazon Pharmacy UAE",
        ],
        "fashion": [
            "Noon Fashion", "Amazon.ae Fashion", "Namshi",
            "6thStreet", "H&M UAE", "Zara UAE",
        ],
        "beauty": [
            "Sephora UAE", "Noon Beauty", "Amazon Beauty UAE",
            "Faces", "Lifestyle UAE",
        ],
        "food": [
            "Talabat", "Careem Food", "Deliveroo UAE",
            "Uber Eats UAE", "Zomato UAE",
        ],
        "books": [
            "Amazon.ae", "Kinokuniya UAE", "Book Depository",
        ],
        "home": [
            "Amazon.ae", "IKEA UAE", "Noon Home",
            "Carrefour UAE", "PAN Emirates",
        ],
        "sports": [
            "Amazon.ae", "Sun & Sand Sports",
            "Decathlon UAE", "Nike UAE",
        ],
        "travel": [
            "Booking.com", "Expedia UAE", "Skyscanner",
            "Google Flights", "Emirates", "flydubai", "Wego",
        ],
        "tickets": [
            "Platinumlist", "Ticketmaster UAE",
            "Virgin Megastore Tickets", "Eventbrite UAE",
        ],
        "currency": "AED",
        "country_name": "UAE",
    },

    "SG": {
        "electronics": [
            "Amazon.sg", "Lazada SG", "Shopee SG",
            "Courts", "Harvey Norman SG", "Gain City",
        ],
        "grocery": [
            "RedMart (Lazada)", "Amazon Fresh SG", "Shopee Supermarket",
            "FairPrice Online", "Cold Storage", "Grab Mart",
        ],
        "pharmacy": [
            "Guardian", "Watsons SG", "Unity Pharmacy",
            "Amazon SG Pharmacy",
        ],
        "fashion": [
            "Lazada SG", "Shopee SG", "ASOS SG",
            "Zalora", "Amazon.sg Fashion",
        ],
        "beauty": [
            "Sephora SG", "Watsons Beauty SG",
            "Guardian Beauty", "Lazada Beauty",
        ],
        "food": [
            "GrabFood", "Foodpanda", "Deliveroo SG",
            "McDonald's SG", "KFC SG",
        ],
        "books": [
            "Amazon.sg", "Popular Bookstore",
            "Kinokuniya SG", "Book Depository",
        ],
        "home": [
            "Amazon.sg", "IKEA SG", "Lazada Home",
            "Shopee Home", "Courts SG",
        ],
        "sports": [
            "Amazon.sg", "Decathlon SG",
            "Lazada Sports", "Nike SG",
        ],
        "travel": [
            "Booking.com", "Expedia SG", "Skyscanner",
            "Google Flights", "Singapore Airlines", "Scoot",
        ],
        "tickets": [
            "SISTIC", "Ticketmaster SG",
            "Eventbrite SG", "Sports Hub Tix",
        ],
        "currency": "S$",
        "country_name": "Singapore",
    },

    "DE": {
        "electronics": [
            "Amazon.de", "MediaMarkt", "Saturn", "Cyberport",
            "Notebooksbilliger", "Conrad", "eBay DE",
        ],
        "grocery": [
            "Amazon Fresh DE", "Rewe Online", "Edeka",
            "Bringmeister", "Flink", "Gorillas DE", "Picnic",
        ],
        "pharmacy": [
            "DocMorris", "Apotheke.com", "Shop Apotheke",
            "Amazon Pharmacy DE",
        ],
        "fashion": [
            "Zalando", "About You", "H&M DE",
            "Amazon Fashion DE", "ASOS DE", "Otto",
        ],
        "beauty": [
            "Douglas", "Amazon Beauty DE", "Notino",
            "Flaconi", "Sephora DE",
        ],
        "food": [
            "Lieferando", "Uber Eats DE",
            "Wolt DE", "Foodpanda DE",
        ],
        "books": [
            "Amazon.de", "Thalia", "Hugendubel",
            "eBay DE Books", "Book Depository",
        ],
        "home": [
            "Amazon.de", "IKEA DE", "Otto",
            "Wayfair DE", "Home24",
        ],
        "sports": [
            "Amazon.de", "Decathlon DE", "SportScheck",
            "Nike DE", "Adidas DE",
        ],
        "travel": [
            "Booking.com", "Expedia DE", "Skyscanner",
            "Google Flights", "Lufthansa", "Eurowings", "Bahn",
        ],
        "tickets": [
            "Eventim", "Ticketmaster DE",
            "Eventbrite DE", "StubHub DE",
        ],
        "currency": "€",
        "country_name": "Germany",
    },
}

# ── Fallback: use India if country not found ──────────────────────
DEFAULT_COUNTRY = "IN"

# ── Category keywords for auto-detection ─────────────────────────
CATEGORY_KEYWORDS = {
    "electronics": {
        "phone", "mobile", "laptop", "tablet", "tv", "television",
        "camera", "headphone", "earphone", "speaker", "watch",
        "smartwatch", "charger", "cable", "router", "printer",
        "monitor", "keyboard", "mouse", "iphone", "samsung",
        "oneplus", "realme", "redmi", "mi", "apple", "macbook",
        "ipad", "airpods", "boat", "jbl", "sony", "lg", "dell",
        "hp", "lenovo", "asus", "acer", "washing machine",
        "refrigerator", "ac", "air conditioner", "microwave",
    },
    "grocery": {
        "rice", "dal", "flour", "atta", "oil", "ghee", "salt",
        "sugar", "milk", "butter", "cheese", "egg", "bread",
        "biscuit", "snack", "chips", "juice", "tea", "coffee",
        "soap", "shampoo", "detergent", "toothpaste", "vegetables",
        "fruit", "masala", "spice", "sauce", "noodles", "pasta",
        "cereals", "oats", "honey", "jam", "pickle", "grocery",
    },
    "pharmacy": {
        "medicine", "tablet", "capsule", "syrup", "paracetamol",
        "antibiotic", "vitamin", "supplement", "protein", "whey",
        "bandage", "glucometer", "bp monitor", "thermometer",
        "sanitizer", "mask", "dolo", "crocin", "combiflam",
        "azithromycin", "multivitamin", "omega", "calcium",
        "iron", "zinc", "ayurvedic", "health", "pharma", "drug",
    },
    "fashion": {
        "shirt", "tshirt", "jeans", "trouser", "dress", "kurta",
        "saree", "lehenga", "suit", "jacket", "hoodie", "shoes",
        "sneakers", "sandals", "chappal", "handbag", "wallet",
        "belt", "cap", "hat", "socks", "innerwear", "leggings",
        "dupatta", "scarf", "ethnic", "western", "formal", "cloth",
    },
    "beauty": {
        "lipstick", "foundation", "serum", "moisturizer",
        "sunscreen", "face wash", "toner", "mascara", "kajal",
        "eyeliner", "blush", "concealer", "primer", "hair oil",
        "conditioner", "perfume", "deodorant", "body lotion",
        "face mask", "nykaa", "lakme", "maybeline", "loreal",
        "nivea", "minimalist", "skincare", "makeup", "cosmetic",
    },
    "food": {
        "pizza", "burger", "biryani", "cake", "sushi", "pasta",
        "rolls", "momos", "sandwich", "dosa", "idli", "thali",
        "chinese", "delivery", "restaurant", "takeaway", "meal",
        "combo", "order food", "hungry",
    },
    "books": {
        "book", "novel", "textbook", "ncert", "guide", "magazine",
        "comic", "fiction", "non-fiction", "autobiography",
        "biography", "self-help", "upsc", "jee", "neet", "syllabus",
    },
    "home": {
        "sofa", "bed", "mattress", "chair", "table", "wardrobe",
        "curtain", "pillow", "blanket", "pressure cooker", "pan",
        "utensil", "mixer", "grinder", "fan", "light", "lamp",
        "storage", "shelf", "rack", "carpet", "doormat", "furniture",
    },
    "sports": {
        "cricket", "football", "badminton", "tennis", "gym",
        "yoga", "cycle", "bicycle", "treadmill", "dumbbell",
        "fitness", "running", "swimming", "basketball", "bat",
        "ball", "racket", "mat", "gloves", "helmet", "sport",
    },
    "travel": {
        "flight", "hotel", "train", "bus", "cab", "holiday",
        "vacation", "trip", "tour", "booking", "resort",
        "hostel", "airbnb", "cruise", "visa", "passport",
    },
    "tickets": {
        "concert", "match", "movie", "event", "show", "ipl",
        "theatre", "stand-up", "comedy", "festival", "ticket",
        "pass", "entry", "live show",
    },
}

PHARMACY_KEYWORDS = CATEGORY_KEYWORDS["pharmacy"]
TRAVEL_KEYWORDS   = CATEGORY_KEYWORDS["travel"] | CATEGORY_KEYWORDS["tickets"]


# ════════════════════════════════════════════════════════════════
# GEO HELPERS
# ════════════════════════════════════════════════════════════════

def detect_country(location: str) -> str:
    """
    Detect country code from a city/country string.
    Returns 2-letter country code or DEFAULT_COUNTRY if not found.
    """
    if not location:
        return DEFAULT_COUNTRY
    loc = location.lower().strip()
    for key, code in CITY_TO_COUNTRY.items():
        if key in loc:
            return code
    return DEFAULT_COUNTRY


def get_country_meta(country_code: str) -> dict:
    """Return metadata (currency, country_name) for a country."""
    data = GEO_PLATFORMS.get(country_code, GEO_PLATFORMS[DEFAULT_COUNTRY])
    return {
        "currency":     data.get("currency", "₹"),
        "country_name": data.get("country_name", "India"),
    }


def get_platform_list(category: str, country_code: str = DEFAULT_COUNTRY) -> str:
    """Return comma-joined platform list for category + country."""
    country_data = GEO_PLATFORMS.get(country_code, GEO_PLATFORMS[DEFAULT_COUNTRY])
    if category == "all":
        seen, result = set(), []
        for cat_platforms in country_data.values():
            if isinstance(cat_platforms, list):
                for p in cat_platforms:
                    if p not in seen:
                        seen.add(p)
                        result.append(p)
        return ", ".join(result)
    return ", ".join(country_data.get(category, []))


# ════════════════════════════════════════════════════════════════
# CATEGORY DETECTOR
# ════════════════════════════════════════════════════════════════

def detect_category(query: str) -> str:
    """Auto-detect product category from query. Falls back to 'all'."""
    q = query.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                scores[cat] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "all"


def needs_pharmacy_disclaimer(query: str) -> bool:
    return any(kw in query.lower() for kw in PHARMACY_KEYWORDS)


def needs_dynamic_price_note(query: str) -> bool:
    return any(kw in query.lower() for kw in TRAVEL_KEYWORDS)


# ════════════════════════════════════════════════════════════════
# PROMPT TEMPLATES (geo-aware)
# ════════════════════════════════════════════════════════════════

GENERAL_SYSTEM = """You are PriceProbe, a universal AI price comparison assistant.

The user is located in: {location} ({country_name})
Local currency: {currency}

Your ONLY job is to find and compare prices for the product the user asked about,
across platforms available in their location.

STRICT RULES:
1. Use web search to find REAL, current prices. NEVER fabricate prices.
2. Search ONLY platforms available in {country_name}.
3. Show prices in {currency} (convert if needed).
4. Sort results lowest price first.
5. Format results using HTML (responses are rendered as HTML):
   - Wrap best price in: <span class='price-best'>{currency}X.XX</span>
   - Wrap 2nd/3rd prices in: <span class='price-regular'>{currency}X.XX</span>
   - Wrap higher prices in: <span class='price-high'>{currency}X.XX</span>
   - Wrap 1st result row in: <div class='best-deal-row'> ... </div>
   - Wrap 2nd result row in: <div class='second-deal-row'> ... </div>
   - Wrap 3rd result row in: <div class='third-deal-row'> ... </div>
   - Make platform names in top 3 <strong>bold</strong>
   - Top 2 must include: <a href='URL'>View on Platform</a>
6. Use <br> for line breaks. Do not use markdown.
6. Mark best deal with ⭐.
7. Mention cashback, bank card offers, EMI, or subscription discounts.
8. Note delivery time (especially quick-commerce options in {location}).
9. If a platform is unavailable in {location}, do NOT list it.
10. End with a short RECOMMENDATION.
11. Do NOT invent data.

Platforms available in {country_name}: {platforms}

User location: {location}
Product / Query: {query}"""

GENERAL_USER = "Find and compare prices for: {query}"

# ── Grocery ──────────────────────────────────────────────────────
GROCERY_SYSTEM = """You are PriceProbe, specializing in grocery and daily essentials price comparison.

User location: {location} ({country_name}) | Currency: {currency}

STRICT RULES:
1. Search ONLY grocery platforms available in {location}: {platforms}
2. For quick-commerce (e.g. Blinkit/Zepto/Getir/Gopuff), verify the platform
   delivers to {location} before listing it.
3. Always mention delivery speed — quick-commerce delivers in ~10-30 min.
4. Compare price per unit (per kg, per litre, per piece) for fair comparison.
5. Highlight subscription savings (e.g. BigBasket BB Star, Amazon Subscribe & Save).
6. Mention minimum order requirements if any.
7. Sort by effective price after discounts — lowest first. Mark best deal ⭐.
8. Show prices in {currency}.
9. NEVER fabricate prices.

User query: {query}"""

GROCERY_USER = "Find grocery prices for: {query}"

# ── Pharmacy ─────────────────────────────────────────────────────
PHARMACY_SYSTEM = """You are PriceProbe, specializing in medicine and healthcare product comparison.

User location: {location} ({country_name}) | Currency: {currency}

STRICT RULES:
1. Search ONLY pharmacy platforms in {country_name}: {platforms}
2. Check local generic/branded availability in {location}.
3. Compare price per strip/unit/pack for fair comparison.
4. Mention generic alternatives if significantly cheaper.
5. Note if prescription (Rx) is required.
6. Highlight subscription discounts.
7. Sort by price — lowest first. Mark best deal ⭐.
8. Show prices in {currency}.
9. NEVER fabricate prices.
10. ALWAYS end with:
    ⚠️ Please consult a licensed doctor or pharmacist before purchasing medicines.

User query: {query}"""

PHARMACY_USER = "Find medicine/health product prices for: {query}"

# ── Fashion & Beauty ─────────────────────────────────────────────
FASHION_SYSTEM = """You are PriceProbe, specializing in fashion and beauty price comparison.

User location: {location} ({country_name}) | Currency: {currency}

STRICT RULES:
1. Search ONLY platforms available in {country_name}: {platforms}
2. Check for international shipping to {location} if local stock is limited.
3. Mention size/shade/variant availability.
4. Highlight active sale events in {country_name}.
5. Note return/exchange policies — critical for fashion.
6. Sort by price — lowest first. Mark best deal ⭐.
7. Show prices in {currency}.
8. Mention loyalty points, cashback, or bank card discounts.
9. NEVER fabricate prices.

User query: {query}"""

FASHION_USER = "Find fashion/beauty prices for: {query}"

# ── Travel ───────────────────────────────────────────────────────
TRAVEL_SYSTEM = """You are PriceProbe, specializing in travel and event ticket price comparison.

User location: {location} ({country_name}) | Currency: {currency}

STRICT RULES:
1. Search travel platforms relevant to departures from {location}: {platforms}
2. For flights: compare base fare + taxes. Mention baggage allowance.
3. For hotels: compare per-night price. Mention free cancellation.
4. For trains/buses: check local rail/bus services for {country_name}.
5. For events: check ticket availability in {location}.
6. Sort by price — lowest first. Mark best deal ⭐.
7. Show prices in {currency} (note conversion if original is different).
8. Highlight loyalty programme savings.
9. NEVER fabricate prices.
10. ALWAYS end with:
    📌 Travel/ticket prices are dynamic and may change. Book quickly to lock in the price.

User query: {query}"""

TRAVEL_USER = "Find travel/ticket prices for: {query}"

# ── Food Delivery ────────────────────────────────────────────────
FOOD_SYSTEM = """You are PriceProbe, specializing in food delivery price comparison.

User location: {location} ({country_name}) | Currency: {currency}

STRICT RULES:
1. Search ONLY food delivery platforms operating in {location}: {platforms}
2. If a platform doesn't operate in {location}, skip it entirely.
3. Compare total price including delivery + platform fees.
4. Mention active promo codes or offers.
5. Note estimated delivery time.
6. Mention subscription savings (Swiggy One, Zomato Gold, DashPass, etc.)
   only if available in {country_name}.
7. Sort by effective total — lowest first. Mark best deal ⭐.
8. Show prices in {currency}.
9. NEVER fabricate prices.

User query: {query}"""

FOOD_USER = "Find food delivery prices for: {query}"


# ════════════════════════════════════════════════════════════════
# PROMPT SELECTOR
# ════════════════════════════════════════════════════════════════

def get_prompt(query: str, category: str = "all", location: str = "") -> tuple:
    """
    Select the best (system_prompt, user_prompt) based on category and location.

    Args:
        query:    The user's search query.
        category: Category string or 'all' for auto-detection.
        location: City or country string (e.g. 'Boston', 'Bangalore').

    Returns:
        (system_prompt, user_prompt) tuple ready to pass to the LLM.
    """
    if category == "all":
        category = detect_category(query)

    country_code = detect_country(location)
    meta         = get_country_meta(country_code)
    platforms    = get_platform_list(category, country_code)

    ctx = {
        "query":        query,
        "location":     location or meta["country_name"],
        "country_name": meta["country_name"],
        "currency":     meta["currency"],
        "platforms":    platforms,
    }

    if category == "grocery":
        system = GROCERY_SYSTEM.format(**ctx)
        user   = GROCERY_USER.format(query=query)

    elif category == "pharmacy":
        system = PHARMACY_SYSTEM.format(**ctx)
        user   = PHARMACY_USER.format(query=query)

    elif category in ("fashion", "beauty"):
        system = FASHION_SYSTEM.format(**ctx)
        user   = FASHION_USER.format(query=query)

    elif category in ("travel", "tickets"):
        system = TRAVEL_SYSTEM.format(**ctx)
        user   = TRAVEL_USER.format(query=query)

    elif category == "food":
        system = FOOD_SYSTEM.format(**ctx)
        user   = FOOD_USER.format(query=query)

    else:
        system = GENERAL_SYSTEM.format(**ctx)
        user   = GENERAL_USER.format(query=query)

    return system, user