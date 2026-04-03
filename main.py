import argparse
import os
import sys
from core.extractor import EmailExtractor
from core.processor import EmailProcessor
from core.utils import load_list


def main():
    # Создаем кастомный хелп, который выводит ВСЁ сразу
    custom_help = """
 FEMBOYmail by kindcrew 

ИСПОЛЬЗОВАНИЕ:
  python main.py extract <input> [options]
  python main.py process <input> -O <output_dir> [flags]

КОМАНДЫ:
  extract        ИЗВЛЕЧЕНИЕ: Поиск почт в логах, SQL, CSV, XLSX.
                Флаги: -o <file> (Выходной файл)

  process        ОБРАБОТКА: Валидация, удаление дублей и сортировка.
                Обязательно: -O <dir> (Папка для результатов)

ФЛАГИ СОРТИРОВКИ (для команды process):
  --sp          [PHONES] Искать номера (EU/USA/ASIA) в локал частях email. (Игнорирует СНГ!)
  --sc          [GEO] Сортировать по странам (нужен data/domen_triggers.txt).
  --sd          [DOMAINS] Делить на файлы по доменам (gmail.txt, mail.com.txt). (Игнорирует СНГ!)

ПРИМЕРЫ:
  python main.py extract logs.txt -o raw.txt
  python main.py process raw.txt -O ./RESULTS --sp --sc --sd
  python main.py process raw.txt -O ./CLEAN (Простая очистка без флагов)
-----------------------------------------------------------------------
"""

    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
    parser.add_argument('-h', '--help', action='store_true')

    subparsers = parser.add_subparsers(dest="command")


    ext_parser = subparsers.add_parser('extract', add_help=False)
    ext_parser.add_argument('input')
    ext_parser.add_argument('-o', '--output', default="raw_emails.txt")

    proc_parser = subparsers.add_parser('process', add_help=False)
    proc_parser.add_argument('input')
    proc_parser.add_argument('-O', '--output-dir', required=True)
    proc_parser.add_argument('--sp', '--split-phones', action='store_true')
    proc_parser.add_argument('--sc', '--split-countries', action='store_true')
    proc_parser.add_argument('--sd', '--split-domains', action='store_true')

    #Если юзер ввел -h или --help или вообще ничего не ввел
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        print(custom_help)
        sys.exit(0)

    args = parser.parse_args()


    if args.command == 'extract':
        extractor = EmailExtractor()
        print(f"[*] Extracting from: {args.input}")
        found = extractor.extract_from_file(args.input)
        with open(args.output, 'w', encoding='utf-8') as f:
            for e in found: f.write(e + '\n')
        print(f"[+] Done! Found {len(found)} emails.")


    elif args.command == 'process':
        base_path = os.path.join(os.getcwd(), 'data')
        triggers = load_list(os.path.join(base_path, 'world_triggers.txt'))
        domains = load_list(os.path.join(base_path, 'domen_triggers.txt'))

        settings = {
            'split_domains': args.sd,
            'split_phones': args.sp,
            'split_countries': args.sc
        }

        if not os.path.exists(args.input):
            print(f"[!] File not found: {args.input}")
            return

        with open(args.input, 'r', encoding='utf-8', errors='ignore') as f:
            emails = [line.strip() for line in f if line.strip()]

        print(f"[*] Data loaded: {len(triggers)} triggers, {len(domains)} domains.")
        print(f"[*] Processing {len(emails)} emails...")

        processor = EmailProcessor(triggers, domains, [], settings)
        processor.process(emails, args.output_dir)
        print(f"[+] Done! Check: {args.output_dir}")


if __name__ == "__main__":
    main()