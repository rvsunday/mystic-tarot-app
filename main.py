import flet as ft
import random
import asyncio

# ==================== 78-CARD TAROT DATA ====================
TAROT_DATA = [
    {"name": "The Fool",         "meaning": "จุดเริ่มต้นใหม่ โอกาสสดใส ความกล้าก้าวไปข้างหน้า",     "meaning_rev": "ความประมาท ขาดทิศทาง กลัวการเปลี่ยนแปลง",           "emoji": "🤹", "arcana": "Major"},
    {"name": "The Magician",     "meaning": "พลังส่วนตัว ทักษะ การสร้างสรรค์ ความสามารถที่ซ่อนอยู่", "meaning_rev": "การหลอกลวง ใช้พลังงานผิดทาง ขาดความมั่นใจ",          "emoji": "🪄", "arcana": "Major"},
    {"name": "The High Priestess","meaning": "สัญชาตญาณ ความรู้ลึกลับ ปัญญาภายใน",                  "meaning_rev": "ปิดกั้นสัญชาตญาณ ความลับที่ถูกซ่อนไว้",                "emoji": "🌙", "arcana": "Major"},
    {"name": "The Empress",      "meaning": "ความอุดมสมบูรณ์ ความรัก ธรรมชาติ ความเป็นแม่",          "meaning_rev": "การพึ่งพา ความไม่สมดุล ขาดการดูแลตัวเอง",             "emoji": "🌸", "arcana": "Major"},
    {"name": "The Emperor",      "meaning": "อำนาจ โครงสร้าง ความมั่นคง ระเบียบวินัย",               "meaning_rev": "เผด็จการ ขาดความยืดหยุ่น ควบคุมมากเกินไป",            "emoji": "👑", "arcana": "Major"},
    {"name": "The Hierophant",   "meaning": "ประเพณี ความเชื่อ ครูผู้สอน ระเบียบสังคม",               "meaning_rev": "ต่อต้านกฎเกณฑ์ ความคิดใหม่ ทางเลือกที่แตกต่าง",       "emoji": "⛪", "arcana": "Major"},
    {"name": "The Lovers",       "meaning": "ความรัก ความสัมพันธ์ การเลือก ความสอดคล้อง",             "meaning_rev": "ความขัดแย้ง การเลือกผิด ความสัมพันธ์ไม่สมดุล",        "emoji": "❤️", "arcana": "Major"},
    {"name": "The Chariot",      "meaning": "ความมุ่งมั่น ชัยชนะ การควบคุม ความสำเร็จ",               "meaning_rev": "ขาดทิศทาง ความก้าวร้าว สูญเสียการควบคุม",             "emoji": "🐎", "arcana": "Major"},
    {"name": "Strength",         "meaning": "ความกล้าหาญภายใน ความอดทน ความเมตตา",                   "meaning_rev": "อ่อนแอ สงสัยตัวเอง ขาดความมั่นใจ",                    "emoji": "🦁", "arcana": "Major"},
    {"name": "The Hermit",       "meaning": "การค้นหาตัวเอง ปัญญา ความสงบ นำทางภายใน",               "meaning_rev": "โดดเดี่ยว ปฏิเสธความช่วยเหลือ หลีกหนีสังคม",         "emoji": "🕯️", "arcana": "Major"},
    {"name": "Wheel of Fortune", "meaning": "โชคชะตา การเปลี่ยนแปลง จุดเปลี่ยน วงจรชีวิต",           "meaning_rev": "โชคร้าย ต้านกระแส การเปลี่ยนแปลงที่ไม่ต้องการ",      "emoji": "🎡", "arcana": "Major"},
    {"name": "Justice",          "meaning": "ความยุติธรรม ความจริง ความสมดุล ผลที่สมเหตุสมผล",       "meaning_rev": "ความอยุติธรรม ไม่ซื่อสัตย์ หลีกเลี่ยงความรับผิดชอบ",  "emoji": "⚖️", "arcana": "Major"},
    {"name": "The Hanged Man",   "meaning": "การหยุดพัก มุมมองใหม่ การยอมรับ การรอคอย",               "meaning_rev": "ชะงักงัน ปฏิเสธการเปลี่ยนแปลง เสียเวลาโดยเปล่า",     "emoji": "🙃", "arcana": "Major"},
    {"name": "Death",            "meaning": "การเปลี่ยนแปลง การสิ้นสุด เริ่มต้นใหม่ ปล่อยวาง",      "meaning_rev": "ต้านการเปลี่ยนแปลง ยึดติดอดีต การเปลี่ยนแปลงล่าช้า", "emoji": "💀", "arcana": "Major"},
    {"name": "Temperance",       "meaning": "ความสมดุล ความพอดี การรักษา ความอดทน",                  "meaning_rev": "ความไม่สมดุล ขาดความพอดี ความขัดแย้งภายใน",           "emoji": "🏺", "arcana": "Major"},
    {"name": "The Devil",        "meaning": "การยึดติด แรงกระตุ้น ความกลัว สิ่งที่มัดมือ",            "meaning_rev": "การปลดปล่อย ทำลายโซ่ตรวน ค้นพบอิสรภาพ",             "emoji": "😈", "arcana": "Major"},
    {"name": "The Tower",        "meaning": "การเปลี่ยนแปลงฉับพลัน ตื่นรู้ พังทลายเพื่อสร้างใหม่",  "meaning_rev": "หลีกเลี่ยงหายนะ กลัวเผชิญความจริง",                  "emoji": "⚡", "arcana": "Major"},
    {"name": "The Star",         "meaning": "ความหวัง การฟื้นฟู แรงบันดาลใจ ความเชื่อมั่น",           "meaning_rev": "สิ้นหวัง ขาดแรงบันดาลใจ ความไม่เชื่อมั่น",             "emoji": "⭐", "arcana": "Major"},
    {"name": "The Moon",         "meaning": "ภาพลวงตา สัญชาตญาณ จิตใต้สำนึก ความลึกลับ",             "meaning_rev": "ความสับสน ความกลัว การหลอกตัวเอง",                    "emoji": "🌑", "arcana": "Major"},
    {"name": "The Sun",          "meaning": "ความสำเร็จ ความสุข ความชัดเจน พลังงาน",                  "meaning_rev": "ขาดความสุข มองโลกในแง่ร้าย ความสำเร็จล่าช้า",         "emoji": "☀️", "arcana": "Major"},
    {"name": "Judgement",        "meaning": "การตื่นรู้ สะท้อนตัวเอง การยกระดับจิตวิญญาณ",            "meaning_rev": "สงสัยตัวเอง ปฏิเสธการเรียนรู้ ความผิดพลาดซ้ำ",      "emoji": "📯", "arcana": "Major"},
    {"name": "The World",        "meaning": "ความสำเร็จสมบูรณ์ บูรณาการ จุดสิ้นสุดที่สมบูรณ์",       "meaning_rev": "ขาดความสมบูรณ์ เป้าหมายไม่บรรลุ การชะลอตัว",         "emoji": "🌍", "arcana": "Major"},
    {"name": "Ace of Wands",    "meaning": "แรงบันดาลใจ พลังงาน ความคิดสร้างสรรค์ โอกาสใหม่",       "meaning_rev": "ความล่าช้า ขาดพลังงาน โอกาสที่หายไป",                "emoji": "🔥", "arcana": "Wands"},
    {"name": "Two of Wands",    "meaning": "การวางแผน อนาคต การตัดสินใจ ความทะเยอทะยาน",            "meaning_rev": "ขาดแผน กลัวการเปลี่ยนแปลง ความไม่แน่ใจ",             "emoji": "🌏", "arcana": "Wands"},
    {"name": "Three of Wands",  "meaning": "การขยายตัว มองไกล โอกาสทางธุรกิจ ความก้าวหน้า",         "meaning_rev": "อุปสรรค ความล่าช้า ขาดความมั่นใจ",                    "emoji": "⛵", "arcana": "Wands"},
    {"name": "Four of Wands",   "meaning": "การเฉลิมฉลอง ความสำเร็จ ความมั่นคงในบ้าน ชุมชน",       "meaning_rev": "ความขัดแย้งในบ้าน ขาดความสุข ความไม่มั่นคง",          "emoji": "🎊", "arcana": "Wands"},
    {"name": "Five of Wands",   "meaning": "การแข่งขัน ความขัดแย้ง ความท้าทาย พลังงานสับสน",       "meaning_rev": "หลีกเลี่ยงความขัดแย้ง หาทางออก ความร่วมมือ",          "emoji": "🥊", "arcana": "Wands"},
    {"name": "Six of Wands",    "meaning": "ชัยชนะ การยอมรับ ความสำเร็จ ความภาคภูมิใจ",              "meaning_rev": "ขาดการยอมรับ ความล้มเหลว ความหยิ่งยโส",               "emoji": "🏆", "arcana": "Wands"},
    {"name": "Seven of Wands",  "meaning": "การป้องกัน ความดื้อรั้น ยืนหยัดในจุดยืน",                "meaning_rev": "ยอมแพ้ ขาดความมั่นใจ อ่อนล้าจากการสู้",               "emoji": "🛡️", "arcana": "Wands"},
    {"name": "Eight of Wands",  "meaning": "ความเร็ว การเคลื่อนไหว ข่าวสาร โมเมนตัม",                "meaning_rev": "ความล่าช้า ข้อมูลผิดพลาด อุปสรรคในการสื่อสาร",       "emoji": "💨", "arcana": "Wands"},
    {"name": "Nine of Wands",   "meaning": "ความอดทน ความแข็งแกร่ง เกือบถึงเป้าหมาย",                "meaning_rev": "ล้าเกินไป ดื้อรั้น ขาดความยืดหยุ่น",                   "emoji": "🏹", "arcana": "Wands"},
    {"name": "Ten of Wands",    "meaning": "ภาระหนัก ความรับผิดชอบ ทำงานหนักเกินไป",                  "meaning_rev": "ปล่อยวางภาระ มอบหมายงาน เรียนรู้ขีดจำกัดตัวเอง",     "emoji": "😰", "arcana": "Wands"},
    {"name": "Page of Wands",   "meaning": "ความกระตือรือร้น ข่าวดี ความคิดสร้างสรรค์",               "meaning_rev": "ขาดทิศทาง ข่าวร้าย ความไม่มั่นคง",                    "emoji": "📜", "arcana": "Wands"},
    {"name": "Knight of Wands", "meaning": "พลังงาน ความกล้า ความมุ่งมั่น การผจญภัย",                 "meaning_rev": "หุนหันพลันแล่น ก้าวร้าว ขาดความระวัง",                "emoji": "🏇", "arcana": "Wands"},
    {"name": "Queen of Wands",  "meaning": "ความมั่นใจ ความสดใส เสน่ห์ ความเป็นผู้นำ",                "meaning_rev": "อิจฉา ก้าวร้าว ขาดความมั่นใจ",                        "emoji": "👸", "arcana": "Wands"},
    {"name": "King of Wands",   "meaning": "ความเป็นผู้นำ วิสัยทัศน์ ความมุ่งมั่น ผู้ประกอบการ",     "meaning_rev": "เผด็จการ หุนหันพลันแล่น ขาดความรับผิดชอบ",            "emoji": "🤴", "arcana": "Wands"},
    {"name": "Ace of Cups",    "meaning": "ความรักใหม่ ความสุข ความอุดมสมบูรณ์ทางอารมณ์",            "meaning_rev": "ความว่างเปล่าทางอารมณ์ ความรักถูกปฏิเสธ",              "emoji": "💧", "arcana": "Cups"},
    {"name": "Two of Cups",    "meaning": "ความรัก ความเป็นหุ้นส่วน การเชื่อมต่อ สัมพันธ์ที่ดี",     "meaning_rev": "สัมพันธ์แตกร้าว ขาดความไว้วางใจ เข้าใจผิด",            "emoji": "💑", "arcana": "Cups"},
    {"name": "Three of Cups",  "meaning": "การเฉลิมฉลอง มิตรภาพ ความสนุกสนาน ชุมชน",                 "meaning_rev": "การแยกตัว เพื่อนไม่จริงใจ ความขัดแย้งในกลุ่ม",        "emoji": "🥂", "arcana": "Cups"},
    {"name": "Four of Cups",   "meaning": "การทบทวน ความเบื่อหน่าย โอกาสที่ถูกมองข้าม",               "meaning_rev": "ตื่นรู้จากความเฉื่อยชา มองเห็นโอกาสใหม่",               "emoji": "🤔", "arcana": "Cups"},
    {"name": "Five of Cups",   "meaning": "การสูญเสีย ความเศร้า ความผิดหวัง ยึดติดอดีต",              "meaning_rev": "การยอมรับ การเดินหน้า ค้นพบความหวังใหม่",              "emoji": "😢", "arcana": "Cups"},
    {"name": "Six of Cups",    "meaning": "ความทรงจำ อดีต ความไร้เดียงสา ของขวัญ",                    "meaning_rev": "ติดอยู่กับอดีต ปล่อยวางเด็กภายใน มองข้างหน้า",        "emoji": "🧸", "arcana": "Cups"},
    {"name": "Seven of Cups",  "meaning": "ภาพลวงตา จินตนาการ ทางเลือกมากมาย ความฝัน",               "meaning_rev": "ความชัดเจน การตัดสินใจ หยุดฝันและลงมือทำ",             "emoji": "✨", "arcana": "Cups"},
    {"name": "Eight of Cups",  "meaning": "การละทิ้ง ค้นหาความหมาย การเดินหน้า ทิ้งสิ่งเก่า",       "meaning_rev": "ยอมแพ้ง่าย ยึดติดกับสิ่งที่ไม่ดีต่อตัว",                "emoji": "🚶", "arcana": "Cups"},
    {"name": "Nine of Cups",   "meaning": "ความพึงพอใจ ความปรารถนาสำเร็จ ความสุข ฝันเป็นจริง",      "meaning_rev": "ความไม่พอใจ ความปรารถนายังไม่สำเร็จ ความตะกละ",      "emoji": "😊", "arcana": "Cups"},
    {"name": "Ten of Cups",    "meaning": "ความสุขสมบูรณ์ ครอบครัวที่ดี ความฝันสำเร็จ",               "meaning_rev": "ครอบครัวแตกแยก ความไม่ลงรอย ความสุขผิวเผิน",          "emoji": "🌈", "arcana": "Cups"},
    {"name": "Page of Cups",   "meaning": "ความฝัน ความคิดสร้างสรรค์ ข่าวดีด้านความรัก",              "meaning_rev": "ความไร้เดียงสา อารมณ์แปรปรวน ขาดความเป็นผู้ใหญ่",    "emoji": "🎨", "arcana": "Cups"},
    {"name": "Knight of Cups", "meaning": "โรแมนติก ความฝัน ข้อเสนอใหม่ ความสร้างสรรค์",              "meaning_rev": "อ่อนไหวมากไป หลอกลวง ไม่จริงใจ",                       "emoji": "🎭", "arcana": "Cups"},
    {"name": "Queen of Cups",  "meaning": "ความเห็นอกเห็นใจ ความอ่อนโยน สัญชาตญาณ ความรัก",          "meaning_rev": "อารมณ์ซ้ำซาก พึ่งพาผู้อื่นมากเกิน ขาดเหตุผล",         "emoji": "🧘", "arcana": "Cups"},
    {"name": "King of Cups",   "meaning": "ความสมดุลทางอารมณ์ ความเมตตา ผู้นำที่ใจดี ปัญญา",         "meaning_rev": "บิดเบือนอารมณ์ ขาดความเห็นอกเห็นใจ เย็นชา",           "emoji": "🧙", "arcana": "Cups"},
    {"name": "Ace of Swords",    "meaning": "ความชัดเจน ความจริง ความคิดใหม่ ความยุติธรรม",          "meaning_rev": "ความสับสน การโกหก ความคิดทำลายล้าง",                   "emoji": "🗡️", "arcana": "Swords"},
    {"name": "Two of Swords",    "meaning": "การตัดสินใจที่ยาก ความลังเล ทางตัน ขาดข้อมูล",          "meaning_rev": "ข้อมูลเปิดเผย การตัดสินใจชัดเจนขึ้น ความขัดแย้ง",    "emoji": "🔮", "arcana": "Swords"},
    {"name": "Three of Swords",  "meaning": "ความเจ็บปวด ความโศกเศร้า การทำร้ายจิตใจ",               "meaning_rev": "การรักษาใจ การยกโทษ ปล่อยวางความเจ็บปวด",              "emoji": "💔", "arcana": "Swords"},
    {"name": "Four of Swords",   "meaning": "การพักผ่อน การฟื้นฟู การพิจารณา ความสงบ",                "meaning_rev": "กลับมาทำงาน ฟื้นตัว ความไม่สงบ",                       "emoji": "😴", "arcana": "Swords"},
    {"name": "Five of Swords",   "meaning": "ความขัดแย้ง การพ่ายแพ้ ชัยชนะที่ว่างเปล่า",              "meaning_rev": "คืนดี ยอมรับความพ่ายแพ้ เรียนรู้จากความผิดพลาด",      "emoji": "😤", "arcana": "Swords"},
    {"name": "Six of Swords",    "meaning": "การเปลี่ยนผ่าน การเคลื่อนย้าย ความสงบหลังพายุ",         "meaning_rev": "ติดอยู่กับปัญหา ต้านทาน ไม่สามารถหนีออกไป",            "emoji": "🌊", "arcana": "Swords"},
    {"name": "Seven of Swords",  "meaning": "กลยุทธ์ ความลับ หลีกเลี่ยงความรับผิดชอบ",                "meaning_rev": "ความซื่อสัตย์ สารภาพความผิด เผชิญความจริง",             "emoji": "🤫", "arcana": "Swords"},
    {"name": "Eight of Swords",  "meaning": "ถูกจำกัด ความคิดที่ขังตัวเอง ขาดอำนาจ ความกลัว",       "meaning_rev": "ปลดปล่อยตัวเอง ค้นพบอิสรภาพ ทำลายกรอบความคิด",       "emoji": "🙈", "arcana": "Swords"},
    {"name": "Nine of Swords",   "meaning": "ความวิตกกังวล ฝันร้าย กลัว ความกดดันทางจิตใจ",          "meaning_rev": "หายจากความวิตก เผชิญความกลัว ฟื้นฟูจิตใจ",             "emoji": "😱", "arcana": "Swords"},
    {"name": "Ten of Swords",    "meaning": "จุดสิ้นสุด วิกฤตที่ถึงที่สุด แต่จะดีขึ้นเสมอ",           "meaning_rev": "การฟื้นตัว เอาชีวิตรอด ความหวังหลังจุดต่ำสุด",         "emoji": "🌅", "arcana": "Swords"},
    {"name": "Page of Swords",   "meaning": "ความอยากรู้ ความคิดคมคาย ข่าวสาร การเฝ้าระวัง",         "meaning_rev": "นินทา ขาดทิศทาง การสื่อสารผิดพลาด",                    "emoji": "🔍", "arcana": "Swords"},
    {"name": "Knight of Swords", "meaning": "ปฏิบัติการด่วน ความกล้า ความตรงไปตรงมา",                 "meaning_rev": "หุนหันพลันแล่น ก้าวร้าว ขาดการวางแผน",                 "emoji": "⚡", "arcana": "Swords"},
    {"name": "Queen of Swords",  "meaning": "ความเป็นอิสระ ความคมชัด ตรงไปตรงมา ประสบการณ์",         "meaning_rev": "เย็นชา ใจแคบ ใช้ปัญญาทำร้ายผู้อื่น",                   "emoji": "🔭", "arcana": "Swords"},
    {"name": "King of Swords",   "meaning": "อำนาจทางปัญญา ความยุติธรรม การตัดสินใจเด็ดขาด",          "meaning_rev": "เผด็จการทางปัญญา เย็นชา การตัดสินที่ไม่ยุติธรรม",     "emoji": "👨‍⚖️", "arcana": "Swords"},
    {"name": "Ace of Pentacles",    "meaning": "โอกาสใหม่ทางการเงิน ความมั่งคั่ง จุดเริ่มต้นที่ดี",  "meaning_rev": "โอกาสที่สูญเสีย ความไม่มั่นคงทางการเงิน",              "emoji": "💰", "arcana": "Pentacles"},
    {"name": "Two of Pentacles",    "meaning": "สมดุล การจัดการ ความยืดหยุ่น การปรับตัว",              "meaning_rev": "ไม่สมดุล รับมือมากเกินไป ขาดการจัดระเบียบ",             "emoji": "🔄", "arcana": "Pentacles"},
    {"name": "Three of Pentacles",  "meaning": "ทีมงาน ความร่วมมือ ทักษะ การยอมรับในผลงาน",            "meaning_rev": "ขาดทีมงาน คุณภาพต่ำ ขาดแรงจูงใจ",                      "emoji": "🏗️", "arcana": "Pentacles"},
    {"name": "Four of Pentacles",   "meaning": "ความมั่นคง การประหยัด ควบคุมทรัพยากร",                  "meaning_rev": "ความโลภ กลัวสูญเสีย ยึดติดกับทรัพย์สิน",               "emoji": "💎", "arcana": "Pentacles"},
    {"name": "Five of Pentacles",   "meaning": "ความยากลำบาก สูญเสียทางการเงิน ความโดดเดี่ยว",         "meaning_rev": "ฟื้นตัวจากวิกฤต ขอความช่วยเหลือ สถานการณ์ดีขึ้น",     "emoji": "❄️", "arcana": "Pentacles"},
    {"name": "Six of Pentacles",    "meaning": "การให้ การรับ ความเอื้อเฟื้อ ความสมดุลของทรัพยากร",    "meaning_rev": "ความโลภ ไม่ยุติธรรม ให้เพราะหวังผล",                   "emoji": "🤲", "arcana": "Pentacles"},
    {"name": "Seven of Pentacles",  "meaning": "การลงทุน ความอดทน การประเมินผล รอผลลัพธ์",              "meaning_rev": "ความไม่พอใจ ผลลัพธ์น้อย ขาดความอดทน",                 "emoji": "🌱", "arcana": "Pentacles"},
    {"name": "Eight of Pentacles",  "meaning": "ความขยัน การฝึกทักษะ ทำงานหนัก พัฒนาตัวเอง",           "meaning_rev": "ขาดความตั้งใจ งานที่ไม่ดี สูญเสียแรงจูงใจ",            "emoji": "⚒️", "arcana": "Pentacles"},
    {"name": "Nine of Pentacles",   "meaning": "ความอุดมสมบูรณ์ ความสำเร็จ ความพอใจตัวเอง อิสรภาพ",   "meaning_rev": "พึ่งพาผู้อื่น สูญเสียความเป็นอิสระ ความสำเร็จไม่มั่นคง","emoji": "🌿", "arcana": "Pentacles"},
    {"name": "Ten of Pentacles",    "meaning": "ความสำเร็จระยะยาว มรดก ครอบครัวมั่งคั่ง ความมั่นคง",  "meaning_rev": "ครอบครัวแตกแยกทางการเงิน สูญเสียมรดก ไม่มั่นคง",      "emoji": "🏰", "arcana": "Pentacles"},
    {"name": "Page of Pentacles",   "meaning": "ความกระตือรือร้น การเรียนรู้ โอกาสใหม่",                "meaning_rev": "ขาดความมุ่งมั่น เรียนรู้ช้า โอกาสที่สูญเสีย",           "emoji": "📚", "arcana": "Pentacles"},
    {"name": "Knight of Pentacles", "meaning": "ความรับผิดชอบ ความขยัน มั่นคง ทำงานสม่ำเสมอ",          "meaning_rev": "เบื่อหน่าย ไม่ยืดหยุ่น ทำงานช้า",                      "emoji": "🐂", "arcana": "Pentacles"},
    {"name": "Queen of Pentacles",  "meaning": "ความเอาใจใส่ ความมั่นคง ความเลี้ยงดู ความเชี่ยวชาญ",  "meaning_rev": "ขาดการดูแล ความไม่มั่นคง ยึดติดกับวัตถุ",               "emoji": "🌻", "arcana": "Pentacles"},
    {"name": "King of Pentacles",   "meaning": "ความมั่งคั่ง ความสำเร็จทางธุรกิจ ความมั่นคง ผู้นำ",    "meaning_rev": "โลภ ใช้เงินฟุ่มเฟือย ขาดความรับผิดชอบทางการเงิน",    "emoji": "🏦", "arcana": "Pentacles"},
]

ARCANA_COLORS = {
    "Major": "#FFD700", "Wands": "#FF8C42",
    "Cups": "#6BA3FF", "Swords": "#B0A0FF", "Pentacles": "#7EC87E",
}

# กองและ labels
SPREADS = [
    {"n": 1, "label": "1 ใบ",  "desc": "คำตอบตรงๆ",              "emoji": "🔮", "labels": ["✦ คำตอบ"]},
    {"n": 3, "label": "3 ใบ",  "desc": "อดีต · ปัจจุบัน · อนาคต","emoji": "🃏", "labels": ["✦ อดีต", "✦ ปัจจุบัน", "✦ อนาคต"]},
    {"n": 5, "label": "5 ใบ",  "desc": "Celtic Cross",            "emoji": "⭐", "labels": ["✦ สถานการณ์", "✦ อุปสรรค", "✦ อดีต", "✦ อนาคต", "✦ ผลลัพธ์"]},
]


# กอง
SPREADS = [
    {"n": 1, "emoji": "🔮", "label": "1 ใบ",  "sub": "คำตอบตรงๆ",
     "pos_labels": ["✦ คำตอบ"]},
    {"n": 3, "emoji": "🃏", "label": "3 ใบ",  "sub": "อดีต · ปัจจุบัน · อนาคต",
     "pos_labels": ["อดีต", "ปัจจุบัน", "อนาคต"]},
    {"n": 5, "emoji": "⭐", "label": "5 ใบ",  "sub": "Celtic Cross",
     "pos_labels": ["สถานการณ์", "อุปสรรค", "อดีต", "อนาคต", "ผลลัพธ์"]},
]


def main(page: ft.Page):
    page.title = "Celestial Arcana"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0b0616"
    page.window_width = 420
    page.window_height = 820
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO

    state = {"spread_idx": 0}

    # ════════════════════════════════════════
    # BIG CARD MODAL (จาก original reveal_card)
    # ════════════════════════════════════════
    # ── Zone A: Emoji (ครึ่งบน พื้นหลังเข้มกว่า) ──
    card_symbol = ft.Text("", size=80, text_align=ft.TextAlign.CENTER)
    pos_label_text = ft.Text("", size=10, color="#aaaaaa",
                             text_align=ft.TextAlign.CENTER)

    zone_top = ft.Container(
        width=300, height=160,
        bgcolor="#0d0720",
        border_radius=ft.border_radius.only(top_left=22, top_right=22),
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            [card_symbol, pos_label_text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
    )

    # ── Zone B: ชื่อ + badge (แถบกลาง) ──
    card_title   = ft.Text("", size=20, weight=ft.FontWeight.BOLD,
                           color="#FFD700", text_align=ft.TextAlign.CENTER)
    arcana_badge = ft.Container(
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=12, vertical=3),
        bgcolor="#ffffff11",
        content=ft.Text("", size=10, color="#aaaaaa",
                        text_align=ft.TextAlign.CENTER),
    )
    rev_badge = ft.Container(
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=10, vertical=3),
        bgcolor="#FF6B9D22",
        content=ft.Text("", size=11, color="#FF6B9D",
                        text_align=ft.TextAlign.CENTER),
    )

    zone_mid = ft.Container(
        width=300,
        bgcolor="#1a0e35",
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        content=ft.Column(
            [card_title, ft.Container(height=6),
             ft.Row([arcana_badge, rev_badge],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=8)],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
    )

    # ── Zone C: ความหมาย (ล่างสุด) ──
    card_meaning = ft.Text("", size=14, text_align=ft.TextAlign.CENTER,
                           color="#D0C8F0", max_lines=6)

    zone_bot = ft.Container(
        width=300,
        bgcolor="#160d2e",
        border_radius=ft.border_radius.only(bottom_left=22, bottom_right=22),
        padding=ft.padding.symmetric(horizontal=22, vertical=18),
        content=ft.Column(
            [ft.Container(
                height=1, bgcolor="#FFFFFF18", width=240,
                margin=ft.margin.only(bottom=14),
             ),
             card_meaning],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
    )

    reveal_card = ft.Container(
        width=300,
        border_radius=22,
        border=ft.border.all(2, "#FFD700"),
        scale=0, opacity=0,
        animate_scale=300,
        animate_opacity=300,
        animate_rotation=300,
        shadow=[ft.BoxShadow(blur_radius=50, color="#8B2BE255")],
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            [zone_top, zone_mid, zone_bot],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    def show_big_card(card, is_rev, pos_label=""):
        color = ARCANA_COLORS.get(card["arcana"], "#FFD700")

        # Zone A
        card_symbol.value    = card["emoji"]
        pos_label_text.value = pos_label.upper() if pos_label else ""
        zone_top.bgcolor     = "#0d0720"

        # Zone B
        card_title.value     = card["name"]
        card_title.color     = color
        arcana_badge.content.value = f"{card['arcana']} Arcana"
        arcana_badge.bgcolor = color + "22"
        if is_rev:
            rev_badge.content.value = "🔻 กลับหัว (Reversed)"
            rev_badge.bgcolor       = "#FF6B9D22"
            rev_badge.content.color = "#FF6B9D"
        else:
            rev_badge.content.value = "▲ ตรง (Upright)"
            rev_badge.bgcolor       = "#88EE8822"
            rev_badge.content.color = "#88EE88"

        # Zone C
        card_meaning.value   = card["meaning_rev"] if is_rev else card["meaning"]

        # Card border + glow
        reveal_card.border   = ft.border.all(2, color)
        reveal_card.shadow   = [ft.BoxShadow(blur_radius=55, color=color + "66")]
        reveal_card.rotation = 3.14 if is_rev else 0

        dark_overlay.visible = True
        modal_stack.visible  = True
        reveal_card.scale    = 1
        reveal_card.opacity  = 1
        page.update()

    def close_modal(e=None):
        reveal_card.scale   = 0
        reveal_card.opacity = 0
        page.update()
        async def _hide():
            import asyncio as _a
            await _a.sleep(0.3)
            modal_stack.visible  = False
            dark_overlay.visible = False
            page.update()
        page.run_task(_hide)

    dark_overlay = ft.Container(
        bgcolor="#000000bb", expand=True,
        visible=False, on_click=close_modal,
    )
    modal_stack = ft.Stack([
        dark_overlay,
        ft.Column([
            reveal_card,
            ft.Container(height=16),
            ft.Row([
                ft.TextButton("🔮 สุ่มใหม่", on_click=lambda e: do_draw(e)),
                ft.TextButton("✨ ปิด",       on_click=close_modal),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=40),
        ], alignment=ft.MainAxisAlignment.CENTER,
           horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           expand=True),
    ], expand=True, visible=False)

    # ════════════════════════════════════════
    # MINI CARD (กด → big card modal)
    # ════════════════════════════════════════
    def make_mini_card(card, is_rev, pos_label):
        color = ARCANA_COLORS.get(card["arcana"], "#FFD700")
        return ft.GestureDetector(
            on_tap=lambda e, c=card, r=is_rev, l=pos_label: show_big_card(c, r, l),
            content=ft.Container(
                width=88, height=124,
                bgcolor="#160d2e",
                border_radius=12,
                border=ft.border.all(1.5, color),
                shadow=[ft.BoxShadow(blur_radius=14, color=color + "55")],
                padding=ft.padding.symmetric(horizontal=5, vertical=7),
                alignment=ft.Alignment(0, 0),
                content=ft.Column([
                    ft.Text(pos_label, size=8, color="#aaaaaa",
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        content=ft.Text(card["emoji"], size=28),
                        rotate=ft.Rotate(3.14) if is_rev else ft.Rotate(0),
                    ),
                    ft.Text(card["name"], size=8, weight=ft.FontWeight.BOLD,
                            color=color, text_align=ft.TextAlign.CENTER, max_lines=2),
                    ft.Text("🔻 Rev" if is_rev else "▲ Up", size=7,
                            color="#FF6B9D" if is_rev else "#88EE88",
                            text_align=ft.TextAlign.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER,
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                   spacing=2),
            ),
        )

    # ════════════════════════════════════════
    # RESULT AREA
    # ════════════════════════════════════════
    result_cards_col = ft.Column(
        [], spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    hint_text = ft.Text("", size=12, color="#9977CC",
                        italic=True, text_align=ft.TextAlign.CENTER)
    result_area = ft.Container(
        visible=False,
        padding=ft.padding.symmetric(vertical=4),
        content=ft.Column(
            [result_cards_col, ft.Container(height=4), hint_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
    )

    # ════════════════════════════════════════
    # DRAW LOGIC
    # ════════════════════════════════════════
    async def do_draw(e):
        draw_button.disabled = True
        result_area.visible  = False
        hint_text.value      = ""
        page.update()
        await asyncio.sleep(0.35)

        sp     = SPREADS[state["spread_idx"]]
        n      = sp["n"]
        labels = sp["pos_labels"]
        drawn  = random.sample(TAROT_DATA, n)
        revs   = [random.random() < 0.35 for _ in drawn]

        result_cards_col.controls.clear()

        if n == 1:
            show_big_card(drawn[0], revs[0], labels[0])
        elif n == 3:
            result_cards_col.controls.append(
                ft.Row(
                    [make_mini_card(drawn[i], revs[i], labels[i]) for i in range(3)],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=8,
                )
            )
            hint_text.value    = "✨ กดที่ไพ่เพื่อดูความหมาย"
            result_area.visible = True
        else:  # 5 ใบ
            result_cards_col.controls.append(
                ft.Row(
                    [make_mini_card(drawn[i], revs[i], labels[i]) for i in range(3)],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=8,
                )
            )
            result_cards_col.controls.append(
                ft.Row(
                    [make_mini_card(drawn[i], revs[i], labels[i]) for i in range(3, 5)],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=8,
                )
            )
            hint_text.value    = "✨ กดที่ไพ่เพื่อดูความหมาย"
            result_area.visible = True

        draw_button.disabled = False
        page.update()

    # ════════════════════════════════════════
    # SPREAD SELECTOR (3 กอง)
    # ════════════════════════════════════════
    spread_containers = []

    def refresh_spread_ui():
        idx = state["spread_idx"]
        for i, c in enumerate(spread_containers):
            active = (i == idx)
            c.border = ft.border.all(2, "#FFD700" if active else "#2a1a4a")
            c.shadow = [ft.BoxShadow(blur_radius=22, color="#FFD70055")] if active else []
            c.content.controls[1].color = "#FFD700" if active else "#666666"
        sp = SPREADS[idx]
        draw_button.text = f"{sp['emoji']}  สุ่มไพ่ {sp['label']}"
        page.update()

    def make_spread_btn(i, sp):
        def on_tap(e, idx=i):
            state["spread_idx"] = idx
            result_area.visible = False
            hint_text.value     = ""
            if modal_stack.visible:
                close_modal()
            refresh_spread_ui()

        c = ft.Container(
            width=110, height=82,
            bgcolor="#1a0a38",
            border_radius=16,
            border=ft.border.all(2, "#FFD700" if i == 0 else "#2a1a4a"),
            shadow=[ft.BoxShadow(blur_radius=22, color="#FFD70055")] if i == 0 else [],
            alignment=ft.Alignment(0, 0),
            padding=ft.padding.all(8),
            content=ft.Column([
                ft.Text(sp["emoji"], size=24, text_align=ft.TextAlign.CENTER),
                ft.Text(sp["label"], size=14, weight=ft.FontWeight.BOLD,
                        color="#FFD700" if i == 0 else "#666666",
                        text_align=ft.TextAlign.CENTER),
                ft.Text(sp["sub"], size=8, color="#777777",
                        text_align=ft.TextAlign.CENTER, max_lines=1),
            ], alignment=ft.MainAxisAlignment.CENTER,
               horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               spacing=2),
        )
        spread_containers.append(c)
        return ft.GestureDetector(on_tap=on_tap, content=c)

    spread_row = ft.Row(
        [make_spread_btn(i, sp) for i, sp in enumerate(SPREADS)],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # ════════════════════════════════════════
    # DRAW BUTTON
    # ════════════════════════════════════════
    draw_button = ft.ElevatedButton(
        f"{SPREADS[0]['emoji']}  สุ่มไพ่ {SPREADS[0]['label']}",
        width=240, height=54,
        style=ft.ButtonStyle(
            bgcolor="#4a1e8c",
            color="#FFD700",
            shape=ft.RoundedRectangleBorder(radius=18),
        ),
        on_click=do_draw,
    )

    # ════════════════════════════════════════
    # CRYSTAL BALL + MAIN LAYOUT
    # ════════════════════════════════════════
    crystal_ball = ft.Container(
        content=ft.Text("🔮", size=100),
        width=180, height=180, border_radius=90,
        bgcolor="#130b28",
        alignment=ft.Alignment(0, 0),
        shadow=[ft.BoxShadow(blur_radius=60, color="#8a2be266")],
    )

    page.add(ft.Stack([
        ft.Column([
            ft.Container(height=50),
            ft.Text("CELESTIAL ARCANA", size=28,
                    weight=ft.FontWeight.BOLD, color="#FFD700"),
            ft.Text("ไพ่ทาโร่ 78 ใบ  ·  ทำนายโชคชะตา",
                    size=13, color="#8866AA"),
            ft.Container(height=24),
            crystal_ball,
            ft.Container(height=24),
            ft.Text("เลือกกอง", size=13, color="#9977CC"),
            ft.Container(height=10),
            spread_row,
            ft.Container(height=20),
            draw_button,
            ft.Container(height=14),
            result_area,
            ft.Container(height=40),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        modal_stack,
    ], expand=True))


ft.app(target=main)
