import requests
import dryscrape
import time
from lxml import html
from bs4 import BeautifulSoup


supported_urls = [
        "amazon.com",
        "hottopic.com",
        "gamestop.com",
        "homedepot.com",
        "lowes.com"
    ]

js_urls = [
    "amazon.com",
    "gamestop.com",
    "homedepot.com",
    "lowes.com"
]


# Works with Amazon, Hot Topic, and Gamestop.
def on_query(url):
    if is_supported(url):
        if not requires_js(url):
            page = requests.get(url)
            tree = html.fromstring(page.content)

            # if "amazon.com" in url:

                # dollars = tree.xpath('//span[@class="buyingPrice"]/text()')
                # cents = tree.xpath('//span[@class="verticalAlign a-size-large priceToPayPadding"]/text()')
                # return "$" + dollars[0].replace(",", "") + "." + cents[0]

            if "hottopic.com" in url:
                dollars = tree.xpath('//span[@class="price-standard"]/text()')
                return dollars[0].replace(",", "")

        else:
            session = dryscrape.Session()
            session.visit(url)
            response = session.body()
            soup = BeautifulSoup(response, "html.parser")

            if "amazon.com" in url:
                while True:
                    try:
                        page = requests.get(url)
                        tree = html.fromstring(page.content)
                        dollars = tree.xpath('//span[@class="buyingPrice"]/text()')
                        cents = tree.xpath('//span[@class="verticalAlign a-size-large priceToPayPadding"]/text()')
                        if len(dollars) and len(cents):
                            return "$" + dollars[0].replace(",", "") + "." + cents[0]

                        price = soup.find_all('span', attrs={'id':'price_inside_buybox'})[0].get_text().strip()
                        if price:
                            return price
                    except Exception:
                        pass
            elif "gamestop.com" in url:
                while True:
                    try:
                        price = soup.find(class_="ats-prodBuy-price").span.get_text()
                        if price:
                            return "$" + price.replace(",", "")
                    except Exception:
                        pass

            elif "homedepot.com" in url:
                while True:
                    try:
                        dollars = soup.find(class_="price__dollars").get_text()
                        cents = soup.find(class_="price__cents").get_text()
                        if len(dollars) and len(cents):
                            dollars.replace(",", "")
                            return "$" + dollars + "." + cents
                    except Exception:
                        pass

            elif "lowes.com" in url:
                while True:
                    try:
                        price = soup.find(class_=lambda val: val and val.startswith("primary-font jumbo strong art-pd")).get_text()
                        return price
                    except Exception:
                        pass

    else:
        return "Unsupported URL"


def is_supported(url):
    for supported_url in supported_urls:
        if supported_url in url:
            return True
    return False


def requires_js(url):
    for js_url in js_urls:
        if js_url in url:
            return True
    return False


if __name__ == "__main__":
    test_items = True

    if test_items:
        amazon_items = [
            "https://www.amazon.com/Nintendo-Switch-Pro-Controller/dp/B01NAWKYZ0",
            "https://www.amazon.com/Legend-Zelda-Breath-Wild-Nintendo-Switch/dp/B01MS6MO77",
            "https://www.amazon.com/Marvel-Guardians-Star-Lord-Elemental-Blaster/dp/B01ISKTCGQ?pd_rd_wg=3TdAL&pd_rd_r="
            "f9f31e2f-8728-40a5-96fd-fdc58ef95161&pd_rd_w=SMOcP&ref_=pd_gw_simh&pf_rd_r=YXZKEX4Z6VGKMQBCWAR6&pf_rd_p=4c5acc25-f4b0-5ad7-9004-0f2549f94c2f"
        ]

        hottopic_items = [
            "https://www.hottopic.com/product/funko-the-nightmare-before-christmas-zero-pop-plush/11353607.html?"
                       "cgid=funko#cm_sp=Homepage-_-Grid2-_-Funko&start=14",
            "https://www.hottopic.com/product/funko-dc-comics-super-heroes-pop-heroes-wonder-woman-from-"
                       "flashpoint-vinyl-figure-hot-topic-exclusive/11403710.html"
        ]

        gamestop_items = [
            "https://www.gamestop.com/nes/consoles/nintendo-nes-classic-edition/136574",
            "https://www.gamestop.com/xbox-one/games/call-of-duty-black-ops-4-mystery-box-edition/166302"
        ]

        homedepot_items = [
            "https://www.homedepot.com/p/Ryobi-18-Volt-ONE-Cordless-Lithium-Ion-Compact-Drill-Driver-Kit-P1811/205651590",
            "https://www.homedepot.com/p/Ryobi-18-Volt-ONE-Cordless-Reciprocating-Saw-Tool-Only-P516/206824275",
            "https://www.homedepot.com/p/LG-Electronics-10-200-BTU-6-500-BTU-DOE-115-Volt-Portable-AC-w-Dehumidifier-Function-and-LCD-Remote-in-White-LP1017WSR/300422891",
        ]

        lowes_items = [
            "https://www.lowes.com/pd/TOTO-Connect-Cotton-White-WaterSense-Labeled-Elongated-Chair-Height-Bidet-Function-1-piece-12-in-Rough-In-Size/1000094615",
            "https://www.lowes.com/pd/Jacuzzi-Primo-White-WaterSense-Labeled-Dual-Elongated-Chair-Height-1-piece-Toilet-12-in-Rough-In-Size/1000181997",
            "https://www.lowes.com/pd/TOTO-Connect-Cotton-White-WaterSense-Labeled-Elongated-Chair-Height-Bidet-Function-1-piece-12-in-Rough-In-Size/1000094615"
        ]

        for items in [amazon_items, hottopic_items, gamestop_items, homedepot_items, lowes_items]:
            for item in items:
                print on_query(item)
                time.sleep(2)
