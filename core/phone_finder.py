import re


class PhoneFinder:
    def __init__(self):
        # Словари паттернов по странам
        self.regions = {
            "Europe": {
                "Germany": r"49\d{8,11}",
                "France": r"33\d{9}",
                "Poland": r"48\d{9}",
                "UK": r"44\d{10}",
                "Italy": r"39\d{9,10}",
                "Spain": r"34\d{9}",
                "Netherlands": r"31\d{9}"
            },
            "USA_Canada": {
                "North_America": r"1[2-9]\d{9}"
            },
            "Asia": {
                "China": r"861[3-9]\d{9}",
                "Japan": r"81[789]0\d{8}",
                "South_Korea": r"8210\d{8}",
                "India": r"91[6-9]\d{9}",
                "Turkey": r"905\d{9}"
            },
            "Africa": {
                "South_Africa": r"27\d{9}",
                "Egypt": r"201[0125]\d{8}",
                "Nigeria": r"234\d{10}"
            },
            "Oceania": {
                "Australia": r"614\d{8}"
            }
        }

    def find_phone_in_email(self, local_part):
        """
        Ищет совпадение по всем регионам в local_part имейла.
        Возвращает (Region, Country, Phone) или None.
        """
        # Убираем все лишние символы, оставляем только цифры
        digits_only = "".join(filter(str.isdigit, local_part))

        if len(digits_only) < 7:
            return None

        for region_name, countries in self.regions.items():
            for country_name, pattern in countries.items():
                if re.search(pattern, digits_only):
                    return {
                        "region": region_name,
                        "country": country_name,
                        "phone": digits_only
                    }
        return None