import random
import mysql.connector

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="quiz_app"
    )

# Register function
def register(cursor, db):
    username = input("Enter a username: ")
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print("Username already exists! Try logging in.")
        return None
    password = input("Enter a password: ")
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    print("Registration successful!")
    return username

# Login function
def login(cursor):
    username = input("Enter your username: ")
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        print("Username not found! Try registering.")
        return None
    password = input("Enter your password: ")
    if user[2] == password:  # Password is in the third column
        print("Login successful!")
        return username
    else:
        print("Incorrect password!")
        return None

# Load topics
def load_topics(cursor):
    cursor.execute("SELECT DISTINCT topic FROM questions")
    return [row[0] for row in cursor.fetchall()]

# Quiz function
def take_quiz(cursor, db, username):
    topics = load_topics(cursor)
    if not topics:
        print("No topics available. Please add questions to the database.")
        return

    print("\nTopics available:")
    for topic in topics:
        print(f"- {topic}")
    chosen_topic = input("Choose a topic: ").capitalize()

    if chosen_topic not in topics:
        print("Invalid topic selected!")
        return

    cursor.execute("SELECT * FROM questions WHERE topic = %s", (chosen_topic,))
    all_questions = cursor.fetchall()
    quiz_questions = random.sample(all_questions, 5)

    score = 0
    for i, q in enumerate(quiz_questions, 1):
        print(f"\nQ{i}: {q[2]}")
        print(f"1. {q[3]}")
        print(f"2. {q[4]}")
        print(f"3. {q[5]}")
        print(f"4. {q[6]}")
        answer = input("Enter the option number: ")
        correct_answer = q[7]
        if q[int(answer) + 2] == correct_answer:  # Options start from index 3
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer is: {correct_answer}")

    print(f"\nYour score: {score}/5")
    cursor.execute("UPDATE users SET score = %s WHERE username = %s", (score, username))
    db.commit()

# Main loop
def main():
    db = connect_to_db()
    cursor = db.cursor()

    print("Welcome to the Quiz Application!")
    username = None
    while not username:
        action = input("Do you want to (1) Register or (2) Login? Enter 1 or 2: ")
        if action == "1":
            username = register(cursor, db)
        elif action == "2":
            username = login(cursor)
        else:
            print("Invalid choice!")

    while True:
        take_quiz(cursor, db, username)
        choice = input("\nDo you want to (1) Reattempt the quiz or (2) Exit? Enter 1 or 2: ")
        if choice == "2":
            print("Goodbye!")
            break

    cursor.close()
    db.close()

if _name_ == "_main_":
    main()
