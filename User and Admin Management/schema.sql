-- চালানোর নিয়ম:  mysql -u root -p < schema.sql
-- অন্য মেম্বাররা নিজেদের টেবিল এই ফাইলের শেষে যোগ করবে।
-- ইউজারের সাথে জুড়তে:  user_id INT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

CREATE DATABASE IF NOT EXISTS student_assistance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_assistance;

-- University -> Department -> Intake -> Section: একটার ভেতরে আরেকটা
CREATE TABLE IF NOT EXISTS universities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS departments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  university_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS intakes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  department_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS sections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  intake_id INT NOT NULL,
  name VARCHAR(20) NOT NULL,
  FOREIGN KEY (intake_id) REFERENCES intakes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(150) NOT NULL UNIQUE,
  password_hash CHAR(64) NOT NULL,          -- পাসওয়ার্ড নয়, শুধু হ্যাশ
  salt CHAR(32) NOT NULL,
  role ENUM('student','admin') NOT NULL DEFAULT 'student',
  is_active TINYINT(1) NOT NULL DEFAULT 0,  -- ০ = ভেরিফাই হয়নি, লগইন বন্ধ
  full_name VARCHAR(100) NULL,
  student_id VARCHAR(30) NULL,
  university_id INT NULL,
  department_id INT NULL,
  intake_id INT NULL,
  section_id INT NULL,
  birthday DATE NULL,
  code VARCHAR(6) NULL,                     -- ৬ সংখ্যার কোড
  code_purpose VARCHAR(10) NULL,            -- 'verify' বা 'reset'
  code_expires DATETIME NULL,               -- কোডের মেয়াদ
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE SET NULL,
  FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
  FOREIGN KEY (intake_id) REFERENCES intakes(id) ON DELETE SET NULL,
  FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE SET NULL
);
