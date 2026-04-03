# FEMBOYmail by kindcrew

Инструмент для извлечения email-адресов из различных файловых форматов [txt, sql, xlsx, csv, log]

Описание

Скрипт предназначен для эффективного извлечения email-адресов из зашумлённых данных с последующей обработкой и сортировкой. Поддерживает работу с логами, дампами баз данных, электронными таблицами и текстовыми файлами.

Возможности

Извлечение email-адресов из файлов форматов: txt, sql, xlsx, csv, log

Фильтрация шума в логах с автоматическим обнаружением email

Сортировка по критериям:

Поиск телефонных номеров в локальной части email

Поиск слов-триггеров в локальной части

Разделение по доменам

Группировка по странам

Автоматическое создание выходной директории

Удаление дубликатов и валидация email-адресов

Удобное CLI-меню


Пример работы с логами

Входной файл: 

Входные данные (log.txt):
2026-04-03 08:00:01 INFO: User login from admin.root@gmail.com  
2026-04-03 08:05:22 ERROR: Failed delivery to support_tech@outlook.be  
2026-04-03 08:10:15 AUTH: New registration: hr.recruitment@yahoo.co.uk  
2026-04-03 08:12:44 WARN: Suspicious activity from 89112223344_user@mail.com  
2026-04-03 08:15:00 INFO: Internal mail sent to dev-team@protonmail.com  
2026-04-03 08:20:11 INFO: Contact request from info_office@seznam.cz  
2026-04-03 08:22:33 DEBUG: Testing account helpdesk_test@fastmail.com  
2026-04-03 08:25:55 INFO: Marketing lead: sales_global@uol.com.br  
2026-04-03 08:30:10 WARN: Billing issue for invoice.pay@orange.fr  
2026-04-03 08:35:01 AUTH: Password reset for 79005554433_client@icloud.com  




Результат:

admin.root@gmail.com  
support_tech@outlook.be  
hr.recruitment@yahoo.co.uk  
89112223344_user@mail.com  
dev-team@protonmail.com  
info_office@seznam.cz  
helpdesk_test@fastmail.com  
sales_global@uol.com.br  
invoice.pay@orange.fr  
79005554433_client@icloud.com  

Удобное управление output директории для результатов сортировки
Пример:



<img width="714" height="250" alt="image" src="https://github.com/user-attachments/assets/a19435bb-e662-4879-9a43-2cc83e5b30ea" />





<img width="791" height="845" alt="image" src="https://github.com/user-attachments/assets/1b6f2186-5b0f-4992-b64c-99313f59afa2" />




--help:
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

Требования
Python 3.14

Зависимости из requirements.txt




