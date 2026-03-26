import os
import re

price_map = {
    "3.25": "260",
    "3.50": "280",
    "3.95": "310",
    "4.25": "340",
    "4.50": "360",
    "4.75": "380",
    "4.95": "400",
    "5.25": "420",
    "5.50": "440",
    "5.75": "460",
    "6.50": "520",
    "8.75": "700",
    "9.50": "760",
    "11.00": "880",
    "12.45": "990",
}

img_map = {
    # Index placeholders
    "Our Story": "Classic Cappuccino.jpg",
    "Velvet Espresso": "Double Espresso.jpg",
    "Artisan Latte": "Artisan Flat White.jpg",
    "Ethiopian Cold Brew": "Midnight Cold Brew.jpg",
    "Espresso": "Double Espresso.jpg",
    "Latte": "Artisan Flat White.jpg",
    "Cold Brew": "Midnight Cold Brew.jpg",
    
    # Menu ones - matching the actual alt attributes or names
    "Cappuccino": "Classic Cappuccino.jpg",
    "Signature Mocha": "Luxe Dark Mocha.jpg",
    "Americano": "Signature Americano.jpg",
    "Flat White": "Artisan Flat White.jpg",
    "Iced Latte": "Iced Vanilla Latte.jpg",
    "Matcha": "Mint Green Tea.jpg", # Or whatever we have? Ceremony Matcha not there. We have Peach Iced Tea.jpg. Wait we'll match names.
    "Iced Tea": "Peach Iced Tea.jpg",
    "Mango Smoothie": "Tropical Mango Freeze.jpg",
    "Croissant": "Butter Croissant.jpg",
    "Cheesecake": "Berry Cheesecake.jpg",
    "Avocado Toast": "Artisan Avocado Toast.jpg",
    "Blueberry Muffin": "Fresh Blueberry Muffin.jpg",
    "Pancakes": "Fluffy Maple Pancakes.jpg"
}

def update_prices(content):
    # Regex for $X.XX
    def repl_dollar(m):
        val = m.group(1)
        if val in price_map:
            return "₹" + price_map[val]
        else:
            try:
                # Calculate if missing
                return "₹" + str(int(float(val)*80))
            except:
                return m.group(0)
                
    content = re.sub(r'\$(\d+\.\d{2})', repl_dollar, content)
    
    # Regex for data-price="X.XX"
    def repl_data(m):
        val = m.group(1)
        if val in price_map:
            return 'data-price="' + price_map[val] + '"'
        else:
            try:
                return 'data-price="' + str(int(float(val)*80)) + '"'
            except:
                return m.group(0)
    
    content = re.sub(r'data-price="(\d+\.\d{2})"', repl_data, content)
    
    return content

def main():
    base_dir = r"c:\Users\rp332\Downloads\Cafe_management system"
    
    # Update index.html
    index_path = os.path.join(base_dir, "templates", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = update_prices(content)
    
    # Replace images manually since we have alt attributes
    for m in re.finditer(r'<img src="([^"]+)"\s*(alt="([^"]+)"|[^>]*)>', content):
        if 'unsplash.com' in m.group(1):
            alt_match = re.search(r'alt="([^"]+)"', m.group(0))
            if alt_match:
                alt = alt_match.group(1)
                if alt in img_map:
                    img_file = img_map[alt]
                    url_f = f"{{{{ url_for('static', filename='images/{img_file}') }}}}"
                    content = content.replace(m.group(1), url_f)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Update menu.html
    menu_path = os.path.join(base_dir, "templates", "menu.html")
    with open(menu_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    content = update_prices(content)
    
    for m in re.finditer(r'<img src="([^"]+)"\s*(alt="([^"]+)"|[^>]*)>', content, flags=re.IGNORECASE):
        if 'unsplash.com' in m.group(1):
            alt_match = re.search(r'alt="([^"]+)"', m.group(0))
            if alt_match:
                alt = alt_match.group(1)
                if alt in img_map:
                    img_file = img_map[alt]
                    url_f = f"{{{{ url_for('static', filename='images/{img_file}') }}}}"
                    content = content.replace(m.group(1), url_f)
                else:
                    # Match Ceremonial Matcha -> Peach Iced Tea just to have something valid
                    url_f = f"{{{{ url_for('static', filename='images/Peach Iced Tea.jpg') }}}}"
                    content = content.replace(m.group(1), url_f)
                    
    with open(menu_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Update profile.html
    profile_path = os.path.join(base_dir, "templates", "profile.html")
    with open(profile_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    content = update_prices(content)
    with open(profile_path, "w", encoding="utf-8") as f:
        f.write(content)
        
if __name__ == "__main__":
    main()
