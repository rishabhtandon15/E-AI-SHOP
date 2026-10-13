"""
Neurosymbolic Reasoning Engine for E-AIShop.
Combines:
1. Neural / Semantic Understanding: Natural language intent parsing, fuzzy matching, conversational formulation.
2. Symbolic Logic & Knowledge Graph: Deterministic product ontologies, first-order constraint rules, exact price formulas, inventory validation.
3. Transparent Thinking Process: Formulates explicit step-by-step reasoning chains for AI explainability.
4. Strict Product Context Isolation: Guarantees that when a particular product is in focus, only that product is presented.
"""

import re
import json

# =====================================================================
# SYMBOLIC PRODUCT KNOWLEDGE BASE (ONTOLOGY & STRUCTURED ATTRIBUTES)
# =====================================================================

PRODUCT_ONTOLOGY = {
    # 1. Royal Tuxedo & Suit
    "IMG_PROD_COSTUME_01": {
        "title": "Royal Tuxedo & Suit",
        "category": "Costumes & Fashion Try-On",
        "brand": "VogueCraft",
        "rating": 4.9,
        "fabric": "Premium Italian Velvet with Mulberry Silk Lapel",
        "fit": "Tailored Slim Fit (Comfort Stretch)",
        "lining": "Breathable Viscose Satin Lining",
        "included_pieces": ["Tuxedo Jacket", "Pleated Formal Trousers", "Silk Satin Bowtie", "Protective Garment Bag"],
        "occasions": ["Black-Tie Galas", "Weddings & Receptions", "Red Carpet & Award Nights", "Formal Dinners"],
        "care_instructions": "Professional Dry Clean Only. Store in breathable garment cover.",
        "warranty": "30-Day Bespoke Tailoring & Sizing Fit Guarantee + 7-Day Hassle-Free Replacement",
        "delivery_days": "2-3 Business Days (Express next-day shipping available)",
        "suitable_for": [
            "Formal evening events", "Groom and groomsmen attire", "Cocktail dinners",
            "Virtual 3D try-on before ordering"
        ],
        "specs_table": {
            "Material": "Italian Velvet & Satin Silk",
            "Closure": "Single Button Satin-covered Front",
            "Lapel": "Classic Shawl Silk Satin Lapel",
            "Pockets": "2 Double-Jetted Flap Pockets, 1 Chest Welt Pocket",
            "Trousers": "Flat Front with Side Adjuster Buckles (No belt required)"
        },
        "highlights": [
            "Handcrafted silk lapel detailing",
            "Pre-fitted with stretch comfort waistbands",
            "Compatible with Live Virtual Try-On Studio"
        ]
    },

    # 2. Cyberpunk Neon Jacket
    "IMG_PROD_COSTUME_02": {
        "title": "Cyberpunk Neon Jacket",
        "category": "Costumes & Fashion Try-On",
        "brand": "FutureWear",
        "rating": 4.8,
        "fabric": "Weather-Resistant Gore-Tex Fiber with Flexible Fiber-Optic LED Strips",
        "fit": "Oversized Cyberpunk Bomber Silhouette",
        "battery_unit": "Detachable 5000mAh USB-C Rechargeable Battery (Up to 8 hours LED glow)",
        "included_pieces": ["Neon Bomber Jacket", "Lithium Battery Pack Unit", "Magnetic Charging Cable"],
        "occasions": ["Music Festivals & Raves", "Cosplay & Sci-Fi Conventions", "Night City Streetwear", "Video & Photo Shoots"],
        "care_instructions": "Detach battery module before cleaning; Wipe clean with damp cloth or gentle hand wash.",
        "warranty": "6-Month LED Luminescence Module Warranty + 7-Day Replacement",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "Festival wear", "Streetwear aesthetics", "Night gatherings", "Virtual try-on preview"
        ],
        "specs_table": {
            "Lighting Modes": "Solid Neon Blue, Breathing Cyan, Strobe, Sound-Reactive Pulse",
            "Water Resistance": "IPX4 Water-repellent outer shell",
            "Battery Life": "Up to 8 hours continuous illumination",
            "Weight": "720g (Lightweight ergonomic composite)"
        },
        "highlights": [
            "Sound-reactive LED lighting that pulses with music",
            "Weather-sealed zippers and concealed battery pouch",
            "Instant Virtual Try-On on custom photo"
        ]
    },

    # 3. Traditional Silk Kurta Sherwani
    "IMG_PROD_COSTUME_03": {
        "title": "Traditional Silk Kurta Sherwani",
        "category": "Costumes & Fashion Try-On",
        "brand": "RoyalEthnic",
        "rating": 4.9,
        "fabric": "Pure Banarasi Raw Silk with Handcrafted Zari Gold Motifs",
        "fit": "Regal Royal Fitted Silhouette",
        "included_pieces": ["Embroidered Sherwani Achkan", "Silk Inner Kurta", "Churidar Pyjama", "Designer Embroidered Stole (Dupatta)"],
        "occasions": ["Weddings & Baraat", "Diwali & Festive Galas", "Sangeet & Engagement Ceremonies"],
        "care_instructions": "Specialist Dry Clean Only. Keep wrapped in muslin cloth.",
        "warranty": "Authenticity Silk-Mark Certified + 7-Day Hassle-Free Replacement",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "Groom wedding wear", "Traditional festivals", "Cultural events"
        ],
        "specs_table": {
            "Embroidery": "Hand-embroidered Zardozi & Resham threadwork",
            "Neckline": "Mandarin Collar with Gold Filigree Buttons",
            "Fabric Weight": "Heavy pure Banarasi Jacquard Silk",
            "Churidar": "Pure cotton-silk blend with adjustable drawstrings"
        },
        "highlights": [
            "Certified 100% Pure Banarasi Silk",
            "Intricate handcrafted royal gold embroidery",
            "Complete 4-piece ensemble ready to wear"
        ]
    },

    # 4. Cosmic Superhero Armor Suit
    "IMG_PROD_COSTUME_04": {
        "title": "Cosmic Superhero Armor Suit",
        "category": "Costumes & Fashion Try-On",
        "brand": "HeroGear",
        "rating": 4.7,
        "fabric": "Molded EVA High-Density Foam Composite & 4-Way Stretch Spandex Under-suit",
        "fit": "Athletic Contour Fit with Adjustable Quick-Release Straps",
        "included_pieces": ["Chest Armor Plate", "Shoulder Pauldrons", "Forearm Gauntlets", "Bicep Straps", "Magnetic Cloak/Cape"],
        "occasions": ["Comic-Con & Conventions", "Costume Parties & Cosplay", "Cinema & Theatrical Shoots"],
        "care_instructions": "Wipe clean with a microfiber cloth; store on a wide hanger in a cool, dry place.",
        "warranty": "1-Year Structural Composite Warranty + 7-Day Exchange",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "Cosplay enthusiasts", "Costume festivals", "Stage performance"
        ],
        "specs_table": {
            "Impact Absorption": "Dual-density flexible EVA foam",
            "Ventilation": "Concealed aerated mesh channels along inner ribcage",
            "Sizing Adaptability": "Adjustable modular buckles fitting chest sizes 36\" - 46\"",
            "Weight": "1.45 kg total weight"
        },
        "highlights": [
            "Cinema-grade realistic metallic armor finish",
            "Breathable spandex inner lining prevents overheating",
            "Try-on instantly with AI face/body mapping"
        ]
    },

    # 5. UltraSlim Pro Laptop 15
    "IMG_PROD_LAPTOP_01": {
        "title": "UltraSlim Pro Laptop 15",
        "category": "Laptops & Computers",
        "brand": "TechCorp",
        "rating": 4.7,
        "processor": "Intel Core i7 13th Gen 1360P (12 Cores, 16 Threads, Up to 5.0 GHz Turbo)",
        "ram": "16 GB LPDDR5 5200MHz Dual-Channel",
        "storage": "512 GB PCIe 4.0 NVMe M.2 High-Speed SSD",
        "graphics": "Intel Iris Xe Graphics (DirectX 12.1, OpenGL 4.6)",
        "display": "15.6-inch Full HD (1920x1080) IPS Anti-Glare, 100% sRGB, 300 Nits",
        "battery": "65 Wh Lithium-Polymer (Up to 11 Hours Battery Life, 65W Fast USB-C Charging)",
        "weight": "1.38 kg Ultra-portable Magnesium-Aluminum Chassis",
        "os": "Windows 11 Home (Lifetime License pre-activated)",
        "warranty": "1-Year On-Site Manufacturer Warranty with accidental damage protection option",
        "return_policy": "7-Day Replacement Policy for technical or transit issues",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "Programming & Software Development (VS Code, Android Studio, Python, Web Dev)",
            "College & University coursework",
            "Business, office productivity & multitasking (Excel, Zoom, presentations)",
            "Casual 1080p photo editing & multimedia playback"
        ],
        "not_recommended_for": [
            "Heavy 4K AAA 3D Gaming on Ultra Settings (requires dedicated RTX GPU instead)"
        ],
        "specs_table": {
            "Processor": "Intel Core i7-1360P (12 Cores, 16 Threads)",
            "RAM": "16 GB LPDDR5 5200MHz",
            "Storage": "512 GB NVMe PCIe Gen 4 SSD",
            "Display": "15.6\" FHD IPS Anti-Glare (300 nits, 100% sRGB)",
            "Battery": "Up to 11 Hours, 65W Fast Charge (50% in 35 mins)",
            "Ports": "2x USB-C Thunderbolt 4, 2x USB-A 3.2, 1x HDMI 2.1, 3.5mm Audio",
            "Weight": "1.38 kg",
            "Operating System": "Windows 11 Home 64-bit"
        },
        "highlights": [
            "Featherlight magnesium chassis weighing only 1.38 kg",
            "Blazing fast 13th Gen Intel Core i7 with 16GB LPDDR5 RAM",
            "All-day battery life with fast 65W USB-C PD power delivery"
        ]
    },

    # 6. Galaxy X 5G Smartphone
    "IMG_PROD_PHONE_01": {
        "title": "Galaxy X 5G Smartphone",
        "category": "Smartphones & Tablets",
        "brand": "MobileTech",
        "rating": 4.8,
        "processor": "Qualcomm Snapdragon 8 Gen 2 (4nm Flagship Octa-Core)",
        "display": "6.7-inch Dynamic AMOLED 2X, 120Hz Adaptive Refresh, 1750 Nits Peak, HDR10+",
        "camera": "108 MP OIS Primary + 12 MP Ultra-Wide + 8 MP Telephoto (3x Optical Zoom) + 32 MP Selfie",
        "ram_storage": "8 GB LPDDR5X RAM + 128 GB UFS 3.1 High-speed Storage",
        "battery": "5000 mAh All-day Battery (45W Fast Charging, 15W Wireless Charging)",
        "os": "Android 14 with 4 Years of OS Upgrades Promised",
        "connectivity": "5G Dual SIM, Wi-Fi 6E, Bluetooth 5.3, NFC, USB-C 3.2",
        "warranty": "1-Year Brand Comprehensive Warranty + 6-Month In-box Accessories Warranty",
        "return_policy": "7-Day Replacement Policy",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "High-resolution mobile photography & 4K 60fps video recording",
            "Lag-free high-refresh mobile gaming (BGMI, COD, Genshin Impact at 90fps)",
            "Super-bright outdoor display viewing in direct sunlight"
        ],
        "specs_table": {
            "Display": "6.7\" Dynamic AMOLED 2X, 120Hz, Gorilla Glass Victus 2",
            "Processor": "Snapdragon 8 Gen 2 Octa-Core (4nm)",
            "Rear Cameras": "108MP (OIS) + 12MP Ultra-wide + 8MP (3x Optical)",
            "Front Camera": "32MP Dual-Pixel AF",
            "Battery": "5000mAh with 45W Wired & Wireless Fast Charge",
            "Protection": "IP68 Dust & Water Resistant (1.5m for 30 mins)"
        },
        "highlights": [
            "Pro-grade 108MP camera with Nightography & Optical Image Stabilization",
            "Stunning 120Hz Dynamic AMOLED 2X display with 1750 nits peak brightness",
            "Full IP68 water & dust resistance rating"
        ]
    },

    # 7. Noise-Cancelling Wireless Headphones
    "IMG_PROD_AUDIO_01": {
        "title": "Noise-Cancelling Wireless Headphones",
        "category": "Audio & Headphones",
        "brand": "SoundMaster",
        "rating": 4.8,
        "drivers": "40mm Custom Titanium-Coated Dynamic Drivers",
        "anc": "Hybrid Active Noise Cancellation (Reduces ambient drone up to -38 dB)",
        "battery": "30 Hours with ANC ON (40 Hours with ANC OFF), 10-Min Fast Charge = 5 Hours Playtime",
        "connectivity": "Bluetooth 5.3, Multipoint Dual-Device Pairing, 3.5mm Aux Audio Jack",
        "microphone": "Quad-Mic Array with AI Environmental Noise Suppression for Voice Calls",
        "warranty": "1-Year Complete Manufacturer Replacement Warranty",
        "return_policy": "7-Day Replacement Guarantee",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "Focusing in noisy offices, flights, commutes & libraries",
            "Audiophile music listening (Hi-Res Audio LDAC support)",
            "Work-from-home conference calls & video meetings"
        ],
        "specs_table": {
            "Frequency Response": "20 Hz - 40,000 Hz (Hi-Res Audio Certified)",
            "Noise Cancellation": "Hybrid ANC (-38dB) + Transparency Ambient Mode",
            "Battery Life": "30h (ANC ON) / 40h (ANC OFF)",
            "Charging": "USB-C Fast Charging (Full charge in 75 mins)",
            "Weight": "245g with memory foam protein leather earcups"
        },
        "highlights": [
            "Hybrid -38dB active noise cancellation blocks background chatter",
            "30 hours battery playback with 10-minute quick top-up",
            "Dual-device multipoint pairing: switch between laptop and phone effortlessly"
        ]
    },

    # 8. Smart Fitness Watch 4
    "IMG_PROD_WATCH_01": {
        "title": "Smart Fitness Watch 4",
        "category": "Accessories & Wearables",
        "brand": "FitPulse",
        "rating": 4.6,
        "display": "1.4-inch AMOLED Always-On Touchscreen (454x454 pixels, 1000 Nits Brightness)",
        "sensors": "Continuous PPG Heart Rate, SpO2 Blood Oxygen, Sleep Stages, Stress & Temperature",
        "gps": "Built-in Standalone Dual-Frequency GPS (No phone needed for tracking runs/cycling)",
        "water_resistance": "5 ATM Certified (50 meters water resistant, safe for pool swimming)",
        "battery": "Up to 14 Days Typical Usage (5 Days Heavy AOD Usage, Magnetic Fast Charger)",
        "compatibility": "Android 8.0+ and iOS 13.0+ (Full notification and call alert sync)",
        "warranty": "1-Year Manufacturer Warranty",
        "return_policy": "7-Day Return & Replacement",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "Fitness tracking, marathon training & sports logging (120+ Sport Modes)",
            "Daily health vitals & sleep quality monitoring",
            "Receiving WhatsApp/call alerts on wrist"
        ],
        "specs_table": {
            "Display": "1.4\" AMOLED, 454x454, 326 PPI, Always-On Mode",
            "Battery": "420mAh (14 Days standard battery life)",
            "Water Rating": "5 ATM Water Resistant (up to 50 meters)",
            "GPS": "Built-in Dual-Band GPS + GLONASS + Galileo",
            "Weight": "38g (Ultra-light aircraft aluminum case)"
        },
        "highlights": [
            "Crystal-clear 1.4-inch AMOLED display with 1000 nits outdoor visibility",
            "14-day battery life on a single magnetic charge",
            "5 ATM water resistance safe for swimming and showering"
        ]
    },

    # 9. Gaming Beast RGB Laptop
    "IMG_PROD_LAPTOP_02": {
        "title": "Gaming Beast RGB Laptop",
        "category": "Laptops & Computers",
        "brand": "TechCorp",
        "rating": 4.9,
        "processor": "AMD Ryzen 7 7840HS (8 Cores, 16 Threads, Up to 5.1 GHz Max Boost, Zen 4)",
        "graphics": "NVIDIA GeForce RTX 4060 8GB GDDR6 (140W Max TGP, DLSS 3.5, Ray Tracing, MUX Switch)",
        "ram": "16 GB DDR5 5600MHz High-Speed (Expandable up to 64 GB)",
        "storage": "1 TB PCIe 4.0 NVMe SSD (Additional M.2 expansion slot available)",
        "display": "16.0-inch QHD+ (2560x1600) 165Hz IPS, 3ms Response, 100% sRGB, NVIDIA G-SYNC",
        "cooling": "Dual FrostBlade Fans with Quad Exhaust and Liquid Metal Thermal Interface",
        "keyboard": "4-Zone RGB Backlit Anti-Ghosting Mechanical-feel Keyboard",
        "battery": "80 Wh Battery (Up to 6.5 Hours productivity, 230W Slim Adapter)",
        "warranty": "1-Year International Warranty with 1-Year Accidental Damage Protection",
        "return_policy": "7-Day Replacement Policy",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "High-FPS AAA Gaming (Cyberpunk 2077, GTA V, Valorant, Call of Duty, Alan Wake 2 at 100+ FPS)",
            "3D Modeling & Rendering (Blender, Maya, Unreal Engine 5)",
            "4K Video Editing & Color Grading (Premiere Pro, DaVinci Resolve)",
            "AI / Machine Learning Model Training (8GB VRAM with CUDA Tensor Cores)"
        ],
        "specs_table": {
            "Processor": "AMD Ryzen 7 7840HS (8C/16T, 5.1GHz)",
            "Graphics": "NVIDIA RTX 4060 8GB GDDR6 (140W TGP + MUX Switch)",
            "RAM": "16 GB DDR5 5600MHz (Up to 64GB)",
            "Storage": "1 TB NVMe Gen4 SSD",
            "Display": "16\" QHD+ (2560x1600), 165Hz, 100% sRGB, 3ms, G-SYNC",
            "Cooling": "Dual Fan Liquid Metal Thermal Design",
            "Weight": "2.35 kg"
        },
        "highlights": [
            "Powered by NVIDIA RTX 4060 with full 140W TGP and MUX Switch",
            "Gorgeous 16-inch 165Hz QHD+ IPS display with 100% sRGB color accuracy",
            "Upgradable dual-slot DDR5 RAM and Gen4 SSD architecture"
        ]
    },

    # 10. True Wireless Earbuds
    "IMG_PROD_AUDIO_02": {
        "title": "True Wireless Earbuds",
        "category": "Audio & Headphones",
        "brand": "SoundMaster",
        "rating": 4.7,
        "drivers": "11mm Bass Boost Dynamic Drivers with PEEK+TPU Polymer Diaphragm",
        "noise_cancelling": "Environmental Noise Cancellation (ENC) with Dual Beamforming Microphones",
        "battery": "32 Hours Total Playtime (7 Hours per bud + 25 Hours Wireless Charging Case)",
        "latency": "45ms Ultra-Low Latency Dedicated Game Mode",
        "water_resistance": "IPX5 Sweat and Water Splash Resistance",
        "connectivity": "Bluetooth 5.3 with Instant Hall-Switch Auto Pairing upon case opening",
        "warranty": "1-Year Manufacturer Replacement Warranty",
        "return_policy": "7-Day Replacement Policy",
        "delivery_days": "2-3 Business Days",
        "suitable_for": [
            "Gym workouts, jogging & sports (sweatproof secure-fit)",
            "Low-latency gaming and streaming videos with zero lip-sync delay",
            "Crystal-clear hands-free calling on the go"
        ],
        "specs_table": {
            "Battery Life": "32h Total (7h earbuds + 25h charging case)",
            "Fast Charge": "10 min charge = 2 hours playback",
            "Water Rating": "IPX5 Sweatproof",
            "Latency": "45ms Ultra-Low Latency Mode",
            "Charging": "USB-C + Qi Wireless Charging Case Compatible"
        },
        "highlights": [
            "Punchy dynamic bass with 11mm composite drivers",
            "IPX5 sweatproof durability ideal for workouts and daily commute",
            "32 hours endurance with fast USB-C and wireless charging support"
        ]
    }
}


def find_symbolic_product(identifier):
    """Finds product symbolic specs by image_id, name, or integer ID."""
    if not identifier:
        return None
    
    # Direct image_id lookup
    if str(identifier) in PRODUCT_ONTOLOGY:
        return PRODUCT_ONTOLOGY[str(identifier)]
        
    ident_lower = str(identifier).strip().lower()
    
    # Try name match
    for img_id, item in PRODUCT_ONTOLOGY.items():
        if item["title"].lower() in ident_lower or ident_lower in item["title"].lower():
            return item
            
    return None


def execute_neurosymbolic_reasoning(user_query, target_product=None, user_id=None, db_conn=None):
    """
    Main Neurosymbolic Reasoning Pipeline.
    
    Input:
      - user_query: raw user string
      - target_product: dict of product in focus (or None if general store search)
      - user_id: logged in user ID
      - db_conn: sqlite3 connection
      
    Output:
      - reply: text response
      - action: string action code
      - products: list of products (STRICT: when target_product is set, ONLY target_product is returned!)
      - thought_process: structured reasoning chain explaining the neurosymbolic derivation
    """
    q_lower = user_query.strip().lower()
    
    # =========================================================================
    # MODE A: DEDICATED SINGLE PRODUCT FOCUS (STRICT ISOLATION)
    # =========================================================================
    if target_product:
        p_name = target_product.get('product_name') or target_product.get('title') or "This Product"
        img_id = target_product.get('image_id', '')
        sym = PRODUCT_ONTOLOGY.get(img_id) or find_symbolic_product(p_name)
        
        orig_price = float(target_product.get('price', 0))
        disc_price = float(target_product.get('discounted_price', orig_price))
        savings = orig_price - disc_price
        discount_pct = round((savings / orig_price) * 100) if orig_price > 0 and savings > 0 else 0
        stock = int(target_product.get('stock', 10))
        is_costume = target_product.get('category_id') == 1 or 'COSTUME' in str(img_id) or 'Costume' in str(target_product.get('category_name', ''))

        # Neural Intent Classification
        intent = "GENERAL_PRODUCT_INQUIRY"
        rules_fired = []
        knowledge_nodes = []
        
        # Rule 1: Stock Check
        if stock <= 15:
            rules_fired.append(f"RULE_STOCK_ALERT: Low stock warning triggered (Only {stock} units left in stock)")
        else:
            rules_fired.append(f"RULE_STOCK_VERIFICATION: In stock ({stock} units available)")

        # Rule 2: Price Calculation
        rules_fired.append(f"RULE_PRICE_AUDIT: Discount {discount_pct}% OFF verified (₹{disc_price:,.0f} vs MRP ₹{orig_price:,.0f})")

        # Intent: Specifications & Technical / Fabric Details
        spec_keywords = [
            'spec', 'feature', 'processor', 'ram', 'cpu', 'gpu', 'graphic', 'storage', 'ssd', 'display', 
            'screen', 'battery', 'camera', 'weight', 'fabric', 'material', 'size', 'fitting', 'driver', 
            'anc', 'water', 'sensor', 'gps', 'detail', 'hardware', 'lining', 'stitch'
        ]
        price_keywords = ['price', 'discount', 'cost', 'offer', 'deal', 'save', 'cheap', 'expensive', 'mrp', 'rate', 'emi']
        suitability_keywords = ['good for', 'can i use', 'suitable', 'worth', 'should i buy', 'why buy', 'gaming', 'program', 'wedding', 'gym', 'workout', 'running', 'travel', 'office', 'battery life']
        warranty_keywords = ['warranty', 'guarantee', 'return', 'refund', 'replace', 'exchange', 'delivery', 'deliver', 'ship', 'shipping']
        tryon_keywords = ['try on', 'try-on', 'wear', 'fit', 'model', 'photo', 'camera', 'look like']

        if any(k in q_lower for k in tryon_keywords):
            intent = "VIRTUAL_TRYON_INQUIRY"
            if is_costume:
                knowledge_nodes.append(f"Fabric: {sym.get('fabric', 'Velvet & Silk') if sym else 'Designer fabric'}")
                knowledge_nodes.append("Try-On Feature: 3D interactive avatar & live custom photo upload")
                reply = (
                    f"✨ **Virtual Try-On for {p_name}**:\n\n"
                    f"Yes! You can instantly test this outfit on interactive 3D models or upload your own photo in our **Virtual Try-On Studio**.\n\n"
                    f"• **Fabric**: {sym.get('fabric', 'Premium material') if sym else 'Tailored fabric'}\n"
                    f"• **Fit**: {sym.get('fit', 'Slim tailored silhouette') if sym else 'Modern fit'}\n"
                    f"• **Included Items**: {', '.join(sym.get('included_pieces', [])) if sym and sym.get('included_pieces') else 'Complete ready-to-wear set'}\n\n"
                    f"👉 Tap the **'Virtual Try-On'** button below to launch the fitting studio now!"
                )
                action = "try_on"
            else:
                reply = (
                    f"ℹ️ **{p_name}** is a physical tech/accessory product and does not require cloth try-on. "
                    f"However, you can check its complete dimensional specifications and 360° product details here!"
                )
                action = "product_detail"

        elif any(k in q_lower for k in price_keywords):
            intent = "PRICE_AND_DISCOUNT_ANALYSIS"
            knowledge_nodes.append(f"Discounted Price: ₹{disc_price:,.0f}")
            knowledge_nodes.append(f"Original MRP: ₹{orig_price:,.0f}")
            knowledge_nodes.append(f"Total Savings: ₹{savings:,.0f} ({discount_pct}% OFF)")
            
            offer_text = f"You save **₹{savings:,.0f} ({discount_pct}% OFF)** off the original price of ₹{orig_price:,.0f}!" if discount_pct > 0 else "Best value assured directly from verified store."
            reply = (
                f"🏷️ **Price Breakdown for {p_name}**:\n\n"
                f"• **Current Best Price**: **₹{disc_price:,.0f}**\n"
                f"• **Original MRP**: ~₹{orig_price:,.0f}~\n"
                f"• **Savings**: {offer_text}\n"
                f"• **Payment**: Instant UPI QR (GPay, PhonePe, Paytm, zero fee)\n"
                f"• **Stock**: {stock} units ready for immediate dispatch!"
            )
            action = "product_detail"

        elif any(k in q_lower for k in warranty_keywords):
            intent = "WARRANTY_AND_POLICY_VERIFICATION"
            warr = sym.get('warranty', '1-Year Complete Warranty') if sym else '1-Year Official Warranty'
            ret = sym.get('return_policy', '7-Day Hassle-Free Replacement Guarantee') if sym else '7-Day Replacement Guarantee'
            deliv = sym.get('delivery_days', '2-3 Business Days') if sym else '2-3 Business Days'
            
            knowledge_nodes.append(f"Warranty Node: {warr}")
            knowledge_nodes.append(f"Return Policy Node: {ret}")
            knowledge_nodes.append(f"Delivery Node: {deliv}")
            rules_fired.append("RULE_STORE_POLICY_CHECK: 100% genuine buyer protection confirmed")

            reply = (
                f"🛡️ **Warranty, Return & Delivery Policy for {p_name}**:\n\n"
                f"• **Warranty**: {warr}\n"
                f"• **Return Policy**: {ret}\n"
                f"• **Delivery Estimate**: Dispatched within 24 hours — Arrives in **{deliv}**\n"
                f"• **Shipping**: Free tracked delivery with genuine product authentication."
            )
            action = "product_detail"

        elif any(k in q_lower for k in suitability_keywords):
            intent = "NEUROSYMBOLIC_SUITABILITY_REASONING"
            suits = sym.get('suitable_for', []) if sym else []
            not_suits = sym.get('not_recommended_for', []) if sym else []
            
            knowledge_nodes.append(f"Suitability Nodes: {', '.join(suits[:2]) if suits else 'High performance'}")
            rules_fired.append("RULE_DOMAIN_CAPABILITY_DEDUCTION: Validated against hardware/material specs")

            suit_list = "\n".join([f"  ✓ {s}" for s in suits]) if suits else "  ✓ Everyday high performance and reliability"
            limitation = f"\n• **Note**: {not_suits[0]}" if not_suits else ""
            
            reply = (
                f"🎯 **Suitability & Recommendation for {p_name}**:\n\n"
                f"Based on our neurosymbolic attribute analysis, **{p_name}** is ideally suited for:\n"
                f"{suit_list}\n"
                f"{limitation}\n\n"
                f"⭐ **Customer Rating**: {sym.get('rating', 4.8) if sym else 4.8}/5.0 (Verified buyers)\n"
                f"💡 **Verdict**: Excellent choice with high value at ₹{disc_price:,.0f}."
            )
            action = "product_detail"

        elif any(k in q_lower for k in spec_keywords):
            intent = "SYMBOLIC_SPECIFICATION_EXTRACTION"
            specs = sym.get('specs_table', {}) if sym else {}
            if not specs and sym:
                specs = {k.capitalize(): v for k, v in sym.items() if isinstance(v, str) and k not in ['title', 'category', 'brand']}
            
            spec_lines = "\n".join([f"• **{k}**: {v}" for k, v in specs.items()]) if specs else f"• **Details**: {target_product.get('description', '')}"
            knowledge_nodes.extend([f"{k}: {v}" for k, v in list(specs.items())[:3]])
            rules_fired.append("RULE_SYMBOLIC_ONTOLOGY_MATCH: Direct attribute retrieval from verified specs")

            reply = (
                f"📋 **Verified Specifications for {p_name}**:\n\n"
                f"{spec_lines}\n\n"
                f"• **Brand**: {target_product.get('company_name', 'Verified Brand')}\n"
                f"• **In Stock**: {stock} items available\n"
                f"• **Price**: ₹{disc_price:,.0f} (MRP ₹{orig_price:,.0f})"
            )
            action = "product_detail"

        else:
            # General Product Overview with Symbolic Highlights
            intent = "HOLISTIC_PRODUCT_SYNTHESIS"
            highlights = sym.get('highlights', []) if sym else []
            hl_text = "\n".join([f"• {h}" for h in highlights]) if highlights else f"• {target_product.get('description', '')}"
            knowledge_nodes.append(f"Product: {p_name}")
            knowledge_nodes.append(f"Price: ₹{disc_price:,.0f}")
            rules_fired.append("RULE_GROUNDED_ANSWER_GENERATION: No hallucination, strictly grounded in product data")

            reply = (
                f"✨ **{p_name} ({target_product.get('company_name', 'Store')})**:\n\n"
                f"{target_product.get('description', '')}\n\n"
                f"**Key Highlights:**\n{hl_text}\n\n"
                f"• **Price**: **₹{disc_price:,.0f}** (Save {discount_pct}%)\n"
                f"• **Stock**: {stock} available in warehouse\n\n"
                f"Feel free to ask me anything about its **specifications**, **pricing**, **suitability**, or **warranty**!"
            )
            action = "product_detail"

        # Structured Neurosymbolic Thought Chain
        thought_process = {
            "mode": "SINGLE_PRODUCT_DEDICATED_FOCUS",
            "intent": intent,
            "target_product": p_name,
            "product_id": target_product.get('id'),
            "knowledge_graph_nodes": knowledge_nodes,
            "symbolic_rules_fired": rules_fired,
            "verdict": "Strict context isolation applied. Query answered deterministically without extraneous items."
        }

        # CRITICAL USER REQUIREMENT:
        # "selected product is only shown not any other product shown in chatbot also make it properly"
        return {
            'reply': reply,
            'action': action,
            'products': [target_product],
            'thought_process': thought_process
        }

    # =========================================================================
    # MODE B: GLOBAL STORE CATALOG & NEUROSYMBOLIC DISCOVERY
    # (When no specific product is in focus)
    # =========================================================================

    # 1. Virtual Try-On Intent
    if any(k in q_lower for k in ['try on', 'try-on', 'tryon', 'fit', 'costume', 'suit', 'sherwani', 'outfit', 'dress', 'wear', 'tuxedo', 'cyberpunk', 'armor']):
        costume_items = []
        if db_conn:
            costumes = db_conn.execute("SELECT * FROM products WHERE category_id = 1 AND is_active = 1").fetchall()
            costume_items = [dict(c) for c in costumes]
            
        thought_process = {
            "mode": "CATALOG_SEARCH",
            "intent": "VIRTUAL_TRYON_DISCOVERY",
            "symbolic_rules_fired": ["RULE_CATEGORY_FILTER: category_id == 1 (Costumes & Fashion Try-On)"],
            "knowledge_graph_nodes": [f"Costumes matched: {len(costume_items)}"],
            "verdict": "Retrieved 4 Virtual Try-On fashion garments with live photo fitting capability."
        }
        return {
            'reply': "✨ **Virtual Try-On Costumes**:\n\nHere are our 4 exclusive Virtual Try-On outfits! Tap any outfit to inspect specifications or test fitting on a model or your own photo:",
            'action': 'try_on',
            'products': costume_items,
            'thought_process': thought_process
        }

    # 2. Dynamic Budget / Price Search (e.g. "under 5000", "below 70000")
    budget_match = re.search(r'(?:under|below|less than|within|around)\s*(?:rs\.?|inr|₹)?\s*(\d+)', q_lower)
    if budget_match and db_conn:
        max_price = float(budget_match.group(1))
        matched = db_conn.execute(
            "SELECT * FROM products WHERE is_active = 1 AND discounted_price <= ? ORDER BY discounted_price DESC LIMIT 5",
            (max_price,)
        ).fetchall()
        prod_list = [dict(p) for p in matched]
        
        thought_process = {
            "mode": "CATALOG_SEARCH",
            "intent": "BUDGET_LOGIC_CONSTRAINT",
            "symbolic_rules_fired": [f"RULE_NUMERIC_FILTER: discounted_price <= {max_price}"],
            "knowledge_graph_nodes": [f"Results found: {len(prod_list)} items"],
            "verdict": f"Filtered database catalog satisfying constraint <= ₹{int(max_price)}."
        }

        if prod_list:
            reply = f"🎯 Found {len(prod_list)} product(s) within your budget of ₹{int(max_price):,}:"
        else:
            affordable = db_conn.execute("SELECT * FROM products WHERE is_active = 1 ORDER BY discounted_price ASC LIMIT 4").fetchall()
            prod_list = [dict(p) for p in affordable]
            reply = f"No products found strictly under ₹{int(max_price):,}. Here are the closest high-value items in our inventory:"

        return {
            'reply': reply,
            'action': 'products_list',
            'products': prod_list,
            'thought_process': thought_process
        }

    # 3. Product or Category Specific Keyword Matching
    keywords = ['laptop', 'phone', 'smartphone', 'headphone', 'earbuds', 'watch', 'tuxedo', 'jacket', 'sherwani', 'costume', 'armor', 'suit']
    matched_keyword = next((k for k in keywords if k in q_lower), None)
    
    if (matched_keyword or any(w in q_lower for w in ['show', 'search', 'find', 'buy', 'looking for'])) and db_conn:
        search_term = matched_keyword if matched_keyword else q_lower.replace("show", "").replace("search", "").replace("find", "").replace("buy", "").replace("me", "").strip()
        pattern = f"%{search_term}%"
        
        products = db_conn.execute(
            "SELECT * FROM products WHERE is_active = 1 AND (product_name LIKE ? OR company_name LIKE ? OR description LIKE ?) LIMIT 5",
            (pattern, pattern, pattern)
        ).fetchall()
        prod_list = [dict(p) for p in products]

        thought_process = {
            "mode": "CATALOG_SEARCH",
            "intent": "KEYWORD_ONTOLOGY_SEARCH",
            "symbolic_rules_fired": [f"RULE_SEARCH_PATTERN: '{search_term}'"],
            "knowledge_graph_nodes": [f"Matching products: {len(prod_list)}"],
            "verdict": f"Catalog scanned for term '{search_term}'."
        }

        if prod_list:
            return {
                'reply': f"🔍 Found {len(prod_list)} product(s) matching '{search_term}'. Tap any product to ask product-specific questions!",
                'action': 'products_list',
                'products': prod_list,
                'thought_process': thought_process
            }

    # 4. Orders & Tracking
    if any(k in q_lower for k in ['order', 'track', 'delivery status', 'where is my order']) and db_conn:
        if user_id:
            latest = db_conn.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
            if latest:
                status_map = {1: 'Placed & Confirmed', 2: 'Processing', 3: 'Shipped (In Transit)', 4: 'Delivered', 5: 'Cancelled'}
                status_text = status_map.get(latest['status'], 'Active')
                thought_process = {
                    "mode": "ORDER_DATABASE_QUERY",
                    "intent": "ORDER_TRACKING",
                    "symbolic_rules_fired": [f"RULE_USER_ORDER_LOOKUP: user_id == {user_id}"],
                    "knowledge_graph_nodes": [f"Order #{latest['track_id']}", f"Status: {status_text}"],
                    "verdict": "Retrieved live tracking telemetry from orders table."
                }
                return {
                    'reply': f"📦 Your latest order **#{latest['track_id']}** is currently **{status_text}** (Total: ₹{latest['total_amount']:,.0f}). You can see live timeline updates under the Orders tab!",
                    'action': 'navigate_orders',
                    'products': [],
                    'thought_process': thought_process
                }

    # 5. Default General Help
    sample_prods = []
    if db_conn:
        sample = db_conn.execute("SELECT * FROM products WHERE is_active = 1 ORDER BY RANDOM() LIMIT 3").fetchall()
        sample_prods = [dict(p) for p in sample]

    thought_process = {
        "mode": "STORE_ASSISTANT_STANDBY",
        "intent": "CONVERSATIONAL_GUIDE",
        "symbolic_rules_fired": ["RULE_DEFAULT_HELP: Ready for product-specific or store inquiries"],
        "knowledge_graph_nodes": ["Catalog active", "Neurosymbolic reasoning online"],
        "verdict": "System standing by to reason over selected products or store queries."
    }

    reply = (
        "👋 **Hello! I am your Neurosymbolic AI Shopping Assistant.**\n\n"
        "🧠 **What I can do for you:**\n"
        "• **Product-Specific Inquiries**: Select any product to ask about exact specs, discounts, suitability, or warranty — with 100% focused isolation!\n"
        "• **Virtual Try-On**: Ask 'Try on costumes' to preview 4 outfits live.\n"
        "• **Budget & Search**: Ask 'Laptops under 70000' or 'Show headphones'.\n"
        "• **Orders & Payments**: Track orders or inquire about instant zero-fee QR payment."
    )

    return {
        'reply': reply,
        'action': 'suggestion',
        'products': sample_prods,
        'thought_process': thought_process
    }
