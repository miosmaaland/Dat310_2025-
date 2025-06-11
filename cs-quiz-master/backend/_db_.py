import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'csquiz.db'

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            profile_image TEXT DEFAULT 'default.jpg',
            score INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            theme TEXT DEFAULT 'light'
        )
    ''')

    # Categories
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Questions
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            wrong_answers TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            level INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    # Achievements
    c.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # User Achievements (join table)
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (achievement_id) REFERENCES achievements(id),
            UNIQUE(user_id, achievement_id)
        )
    ''')

    # SEED DATA
    hashed_password = generate_password_hash('test123')
    c.execute('INSERT OR IGNORE INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)', 
              ('quiz_master', 'quiz_master@example.com', hashed_password, 1))

    categories = [
        ('Networking', 'Questions about networks, protocols, and internet basics'),
        ('Security', 'Covers cybersecurity, encryption, and safe computing'),
        ('Development', 'Programming languages, concepts, and practices'),
        ('System Engineering', 'Operating systems, architecture, and file systems'),
        ('Databases', 'SQL, NoSQL, and data modeling')
    ]
    c.executemany('INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)', categories)

    
    achievements = [
        ("First Correct Answer", "Answer your first question correctly."),
        ("100 Points", "Reach 100 points."),
        ("500 Points", "Reach 500 points."),
        ("Quiz Streak", "Answer 5 questions correctly in a row."),
        ("Quiz Master", "Reach 1000 points."),
        ("Category Explorer", "Answer a question in every category."),
        ("Perfectionist", "Get 10 correct answers in a row."),
        ("First Quiz", "Complete your first quiz."),
    ]
    c.executemany('INSERT OR IGNORE INTO achievements (name, description) VALUES (?, ?)', achievements)


    questions = [
    
        ("What does HTTP stand for?", "HyperText Transfer Protocol", '["HyperText Transmission Protocol", "HighText Transfer Protocol", "HyperTool Transfer Protocol"]', 1, 1),
        ("Which device connects different networks together?", "Router", '["Switch", "Modem", "Repeater"]', 1, 1),
        ("What is the main function of DNS?", "Translating domain names to IP addresses", '["Encrypting data", "Routing packets", "Blocking malware"]', 1, 2),
        ("Which protocol is used to securely transfer files over the Internet?", "SFTP", '["FTP", "SMTP", "POP3"]', 1, 2),
        ("Which layer of the OSI model does IP operate on?", "Network", '["Transport", "Data Link", "Session"]', 1, 3),
        ("What port does HTTPS use by default?", "443", '["80", "21", "25"]', 1, 2),
        ("Which protocol is connectionless?", "UDP", '["TCP", "FTP", "SMTP"]', 1, 2),
        ("Which protocol is used for sending emails?", "SMTP", '["HTTP", "FTP", "IMAP"]', 1, 1),
        ("What does LAN stand for?", "Local Area Network", '["Large Area Network", "Long Area Network", "Light Area Network"]', 1, 1),
        ("Which device amplifies signals in a network?", "Repeater", '["Router", "Switch", "Bridge"]', 1, 2),
        ("What is the maximum length of a standard Ethernet cable?", "100 meters", '["10 meters", "1000 meters", "1 meter"]', 1, 2),
        ("Which protocol secures web traffic?", "HTTPS", '["HTTP", "FTP", "SMTP"]', 1, 3),
        ("What is the main function of ARP?", "Mapping IP addresses to MAC addresses", '["Routing packets", "Encrypting data", "Assigning IP addresses"]', 1, 3),

    
        ("What is the main goal of a firewall?", "To block unauthorized access", '["To increase internet speed", "To store passwords", "To manage bandwidth"]', 2, 2),
        ("What does 'phishing' refer to?", "Fraudulent attempts to obtain sensitive data", '["Catching software bugs", "Scanning ports", "Encrypting files"]', 2, 2),
        ("What is two-factor authentication?", "Using two methods to verify identity", '["Using two passwords", "Using two devices", "Using two browsers"]', 2, 1),
        ("Which is a strong password?", "T!m3$Qw8z", '["password123", "qwerty", "123456"]', 2, 1),
        ("What does SSL stand for?", "Secure Sockets Layer", '["Secure System Login", "System Socket Layer", "Secure Software License"]', 2, 2),
        ("Which type of malware demands payment?", "Ransomware", '["Spyware", "Adware", "Rootkit"]', 2, 3),
        ("What is the purpose of encryption?", "To protect data by making it unreadable without a key", '["To speed up data transfer", "To compress files", "To backup data"]', 2, 1),
        ("Which of these is a type of social engineering attack?", "Phishing", '["Brute force", "DDoS", "SQL Injection"]', 2, 1),
        ("What is a common tool for password cracking?", "John the Ripper", '["Wireshark", "Nmap", "Metasploit"]', 2, 2),
        ("Which protocol is used for secure remote login?", "SSH", '["Telnet", "FTP", "SMTP"]', 2, 2),
        ("What is a zero-day vulnerability?", "A vulnerability unknown to the vendor", '["A patched vulnerability", "A virus", "A firewall rule"]', 2, 3),
        ("What does VPN stand for?", "Virtual Private Network", '["Very Private Network", "Virtual Public Network", "Verified Private Network"]', 2, 1),
        ("Which is NOT a type of malware?", "Firewall", '["Trojan", "Worm", "Spyware"]', 2, 1),

    
        ("What does 'HTML' stand for?", "HyperText Markup Language", '["HighText Markdown Language", "HyperTransfer Markup Language", "Hyperlink Text Mark Language"]', 3, 1),
        ("Which language is primarily used for styling web pages?", "CSS", '["JavaScript", "Python", "HTML"]', 3, 1),
        ("Which of these is a JavaScript framework?", "React", '["Django", "Flask", "Laravel"]', 3, 2),
        ("What does 'API' stand for?", "Application Programming Interface", '["Advanced Programming Index", "Application Protocol Interface", "Automated Program Interaction"]', 3, 1),
        ("Which keyword is used to define a function in Python?", "def", '["function", "define", "fun"]', 3, 1),
        ("Which version control system is most widely used?", "Git", '["SVN", "Mercurial", "CVS"]', 3, 2),
        ("What is the output of 2 + '2' in JavaScript?", "22", '["4", "Error", "undefined"]', 3, 3),
        ("Which language is used for Android app development?", "Kotlin", '["Swift", "Ruby", "PHP"]', 3, 2),
        ("What does CSS stand for?", "Cascading Style Sheets", '["Computer Style Sheets", "Creative Style Syntax", "Colorful Style Sheets"]', 3, 1),
        ("Which of these is a backend framework?", "Django", '["React", "Vue", "Bootstrap"]', 3, 2),
        ("What is the output of print(2 ** 3) in Python?", "8", '["6", "9", "5"]', 3, 1),
        ("Which HTML tag is used for the largest heading?", "<h1>", '["<h6>", "<head>", "<header>"]', 3, 1),
        ("Which of these is NOT a programming paradigm?", "Circular", '["Functional", "Object-Oriented", "Procedural"]', 3, 3),

        
        ("Which of the following is a Linux package manager?", "apt", '["brew", "exe", "iso"]', 4, 3),
        ("What is a kernel in an operating system?", "The core component managing system resources", '["An antivirus program", "A bootloader", "A BIOS replacement"]', 4, 3),
        ("Which command lists files in Unix/Linux?", "ls", '["cd", "rm", "pwd"]', 4, 1),
        ("What does BIOS stand for?", "Basic Input Output System", '["Binary Input Output System", "Basic Internal Output System", "Basic Input Output Software"]', 4, 2),
        ("Which file system is commonly used by Windows?", "NTFS", '["ext4", "FAT32", "HFS+"]', 4, 2),
        ("What is the default shell in most Linux distributions?", "bash", '["zsh", "fish", "csh"]', 4, 2),
        ("Which command is used to change file permissions in Unix?", "chmod", '["chperm", "perm", "setperm"]', 4, 3),
        ("Which command is used to display the current directory in Linux?", "pwd", '["ls", "cd", "dir"]', 4, 1),
        ("Which of these is NOT an operating system?", "Python", '["Linux", "Windows", "macOS"]', 4, 1),
        ("What is the main function of the BIOS?", "Initialize hardware during booting", '["Run applications", "Manage files", "Connect to the internet"]', 4, 2),
        ("Which file permission allows users to execute a file?", "x", '["r", "w", "e"]', 4, 2),
        ("What is a process in computing?", "An instance of a running program", '["A file", "A user", "A network connection"]', 4, 1),
        ("Which command is used to display running processes in Linux?", "ps", '["ls", "top", "chmod"]', 4, 3),

        
        ("Which SQL keyword is used to retrieve data?", "SELECT", '["GET", "FETCH", "QUERY"]', 5, 2),
        ("Which database is known for storing data in JSON format?", "MongoDB", '["MySQL", "PostgreSQL", "SQLite"]', 5, 2),
        ("What does SQL stand for?", "Structured Query Language", '["Simple Query Language", "Structured Question Language", "Sequential Query Language"]', 5, 1),
        ("Which command is used to remove all records from a table but keep its structure?", "TRUNCATE", '["DELETE", "DROP", "REMOVE"]', 5, 3),
        ("Which SQL clause is used to filter results?", "WHERE", '["ORDER", "GROUP", "HAVING"]', 5, 1),
        ("Which type of database is PostgreSQL?", "Relational", '["NoSQL", "Graph", "Document"]', 5, 2),
        ("Which command is used to add a new row in SQL?", "INSERT", '["ADD", "UPDATE", "APPEND"]', 5, 1),
        ("Which SQL statement is used to update data?", "UPDATE", '["INSERT", "SELECT", "DELETE"]', 5, 2),
        ("Which of these is a NoSQL database?", "Cassandra", '["MySQL", "PostgreSQL", "Oracle"]', 5, 2),
        ("What is a primary key?", "A unique identifier for a record", '["A type of index", "A database user", "A table name"]', 5, 1),
        ("Which SQL clause is used to sort results?", "ORDER BY", '["GROUP BY", "WHERE", "HAVING"]', 5, 1),
        ("Which command removes a table from a database?", "DROP", '["DELETE", "REMOVE", "TRUNCATE"]', 5, 3),
        ("Which database is developed by Microsoft?", "SQL Server", '["MySQL", "MongoDB", "PostgreSQL"]', 5, 2),
    ]

    c.executemany('''
        INSERT OR IGNORE INTO questions (question, correct_answer, wrong_answers, category_id, level)
        VALUES (?, ?, ?, ?, ?)
    ''', questions)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()