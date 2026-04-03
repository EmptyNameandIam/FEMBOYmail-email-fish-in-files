import os
import re
from core.phone_finder import PhoneFinder



class EmailProcessor:
    def __init__(self, triggers, domains, phones, settings):

        self.triggers = triggers
        self.domains = domains
        self.phones = phones
        self.settings = settings
        self.phone_finder = PhoneFinder()

    def validate(self, email):
        """проверка на валидность email"""
        email = email.strip()
        if not email or "@" not in email:
            return False
        parts = email.split("@")
        if len(parts) != 2:
            return False
        return "." in parts[1]

    def safe_save(self, folder, filename, data):

        # Очистка от запрещенных символов Windows
        clean_name = re.sub(r'[\\/*?:"<>|]', "", filename)
        path = os.path.join(folder, clean_name)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(data + '\n')

    def process(self, emails, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Основной файл для всего, что не попало под фи филтьры
        main_file = "all_emails_refined.txt"


        unique_emails = set(emails)
        processed_count = 0

        for raw_email in unique_emails:

            email = raw_email.replace('\x00', '').strip().lower()

            if not self.validate(email):
                continue

            try:
                local_part, domain = email.split('@')
            except ValueError:
                continue

            was_sorted = False
            processed_count += 1


            for tg in self.triggers:
                if tg and tg.lower() in local_part:
                    self.safe_save(output_dir, "triggered_hits.txt", f"[{tg}] {email}")



            if self.settings.get('split_phones'):
                phone_data = self.phone_finder.find_phone_in_email(local_part)
                if phone_data:

                    p_dir = os.path.join(output_dir, "phones")
                    if not os.path.exists(p_dir): os.makedirs(p_dir)

                    filename = f"{phone_data['region']}_{phone_data['country']}.txt"
                    self.safe_save(p_dir, filename, f"{email} | {phone_data['phone']}")
                    was_sorted = True


            if self.settings.get('split_countries'):
                tld = domain.split('.')[-1]

                if tld in self.domains or len(tld) == 2:
                    c_dir = os.path.join(output_dir, "countries")
                    if not os.path.exists(c_dir): os.makedirs(c_dir)
                    self.safe_save(c_dir, f"{tld}.txt", email)
                    was_sorted = True


            if self.settings.get('split_domains'):
                self.safe_save(output_dir, f"domain_{domain}.txt", email)
                was_sorted = True


            if not was_sorted:
                self.safe_save(output_dir, main_file, email)

        print(f"[+] Successfully processed {processed_count} unique emails.")