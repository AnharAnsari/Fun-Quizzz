import mysql.connector as my

# Database connection
con = my.connect(host="localhost", user="root", passwd="meow", database="quiz_app")
cur = con.cursor()

def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    con.commit()
    print("Registration successful! Please log in to continue.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cur.execute("SELECT username FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    if user:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None

def get_questions_by_topic(topic):
    query = "SELECT question, option1, option2, option3, option4, answer FROM questions WHERE topic = %s ORDER BY RAND() LIMIT 5"
    cur.execute(query, (topic,))
    return cur.fetchall()

def take_quiz(username):
    cur.execute("SELECT DISTINCT topic FROM questions")
    topics = [row[0] for row in cur.fetchall()]
    
    if not topics:
        print("No topics available in the database.")
        return
    
    print("\nAvailable Topics:")
    for topic in topics:
        print(f"- {topic}")
    topic = input("Choose a topic: ").strip()
    
    if topic not in topics:
        print("Invalid topic selected.")
        return
    
    questions = get_questions_by_topic(topic)
    if not questions:
        print(f"No questions available for the topic '{topic}'.")
        return

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q[0]}")
        print(f"A. {q[1]}")
        print(f"B. {q[2]}")
        print(f"C. {q[3]}")
        print(f"D. {q[4]}")
        answer = input("Your answer (A/B/C/D): ").upper()

        correct_option = q[5]
        if (answer == 'A' and q[1] == correct_option) or \
           (answer == 'B' and q[2] == correct_option) or \
           (answer == 'C' and q[3] == correct_option) or \
           (answer == 'D' and q[4] == correct_option):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {correct_option}")

    print(f"\nQuiz completed! Your score is {score}/5.")
    cur.execute("UPDATE users SET score = %s WHERE username = %s", (score, username))
    con.commit()

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Quit")
        choice = input("Select an option: ")
        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                take_quiz(username)
        elif choice == "3":
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please try again.")

main()

cur.close()
con.close()
