# User and Admin Management (Member 1)

Developed by: Fahim Islam, ID-20255103072
Project: Student Assistance (Python + MySQL, কোনো ফ্রেমওয়ার্ক নেই, টার্মিনালের মেনু)

## ফাইল
| ফাইল | কাজ |
|---|---|
| `schema.sql` | University, Department, Intake, Section ও users টেবিল |
| `db.py` | MySQL সংযোগ ও SQL ফাংশন, পাসওয়ার্ড হ্যাশ, ৬ সংখ্যার কোড, ইমেইল (console/SMTP) |
| `main.py` | লজিক (নিয়ম), মেনু ও মূল লুপ |

## প্রথমবার চালানো
1. এই ফোল্ডারে ঢুকে: `py -3.13 -m venv venv` ও `source venv/Scripts/activate`
2. `pip install -r requirements.txt`
3. MySQL চালু রেখে: `mysql -u root -p < schema.sql`
4. `local_config.example.py` কপি করে `local_config.py` বানাও, নিজের MySQL পাসওয়ার্ড বসাও
5. `python main.py`

## প্রথম অ্যাডমিন বানানো
প্রথমে মেনু থেকে Create account করে Verify করো, তারপর MySQL-এ একবার চালাও:
```sql
UPDATE users SET role='admin' WHERE username='তোমার_username';
```

## ইমেইল
ডিফল্টে কোড টার্মিনালে ছাপা হয়। আসল ইমেইল পাঠাতে `local_config.py`-তে
`EMAIL_MODE = "smtp"`, `SMTP_USER`, `SMTP_PASSWORD` (Gmail App Password) দাও।

## অন্য মেম্বারদের জন্য
- ইউজারের সাথে জুড়তে: `user_id INT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- রিপোর্ট করা কনটেন্টের জন্য মেম্বার ৪-এর টেবিল লাগবে: `resources(id, title)` ও
  `resource_reports(id, resource_id, reason)`
