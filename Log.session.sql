-- Create Database
CREATE DATABASE IF NOT EXISTS logdatabase;

-- Use Database
USE logdatabase;

-- Create Users Table
CREATE TABLE IF NOT EXISTS logdatabase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);


CREATE DATABASE IF NOT EXISTS user_detail;

USE user_detail;

CREATE TABLE IF NOT EXISTS user_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    phone VARCHAR(15),
    gender VARCHAR(10),
    student_status VARCHAR(50),
    school_name VARCHAR(100),
    standard VARCHAR(50),
    college_name VARCHAR(100),
    department VARCHAR(100),
    year VARCHAR(10),
    internship_status VARCHAR(10),
    company_name VARCHAR(100),
    internship_time_period VARCHAR(50),
    internship_based VARCHAR(50),
    project_title VARCHAR(100),
    project_description TEXT,
    programming_languages TEXT,
    course_name_completed VARCHAR(100),
    course_being_taken VARCHAR(100),
    linkedin_id VARCHAR(100),
    github_id VARCHAR(100),
    course_certificate_status VARCHAR(10),
    achievement_certificate TEXT
);
