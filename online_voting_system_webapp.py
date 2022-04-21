import pywebio
import pywebio.input as inp
import pywebio.output as out
import mysql.connector

try:
    mydb = mysql.connector.connect(user='root', password='1234', host='localhost', database='Online_Voting_System')
    if mydb:
        print("connection successfull...!!!")

    myCursor = mydb.cursor()

    # myCursor.execute("CREATE DATABASE Online_Voting_System")

    # myCursor.execute("CREATE TABLE users(username VARCHAR(50), pswd varchar(20), age INT, vote VARCHAR(50))")


except Exception as error:
    print("error : ", error.__context__)

def voting():
    out.put_markdown("# Online Voting System")
    out.put_button('Login', login)
    out.put_button('Sign-Up', signUp)

def check_age(age):
    if age<18:
        return "Invalid age...!!! (Only 18 and above can vote.)" 

def check_name(name):
    myCursor.execute(f"SELECT * FROM users WHERE username = '{name}'")
    result = myCursor.fetchall()
    if result:
        return "Username already exists...!!! Try another one."

def signUp():
    out.clear()
    out.put_markdown("# Sign-Up")
    name = inp.input("Name : ", type=inp.TEXT, validate=check_name)
    age = inp.input("Age : ", type=inp.NUMBER, validate=check_age)
    pswd = inp.input("Password : ", type=inp.PASSWORD)

    myCursor.execute('INSERT INTO users(username, pswd, age) values(%s, %s, %s)', [name, pswd, age])
    mydb.commit()

    out.put_html("<h6>Account Created Successfully, headup towards the login page.</h6>")
    out.put_button('Login', login)

def login():
    out.clear()
    out.put_markdown("# Login")
    name = inp.input("Name : ", type=inp.TEXT)
    pswd = inp.input("Password : ", type=inp.PASSWORD)

    myCursor.execute(f"SELECT * FROM users WHERE username = '{name}'")
    result = myCursor.fetchall()

    
    if result:
        
        if result[0][1] == pswd:
            vote(name, result)
        else:
            out.put_html('<h6>Invalid Password, Try Again...!!!</h6>')
            out.put_button('Login', login)
        
    else:
        out.put_html('<h6>Username does not Exist...!!!</h6>')
        out.put_button('Sign-Up', signUp)

def vote(name, result):
    # out.put_text(result[0][3])
    if result[0][3]:
        out.clear()
        out.put_markdown("# Online Voting System")
        out.put_table([['Name', 'Age', 'Vote'], [result[0][0], result[0][2], result[0][3]]])
        out.put_html("<h6>You have already voted, thanks for your kind support.</h6>")
        out.put_button('Check Results', results)
    
    else:
        vote = inp.radio("Vote", options=['Congress', 'Bhartiya Janta Party', 'Aam Aadmi Party'])
        myCursor.execute(f"UPDATE users SET vote='{vote}' WHERE username='{name}'")
        mydb.commit()

        myCursor.execute(f"SELECT * FROM users WHERE username = '{name}'")
        result = myCursor.fetchall()

        out.put_table([['Name', 'Age', 'Vote'], [result[0][0], result[0][2], result[0][3]]])
        out.put_html("<h6>Your vote has been recorded, thanks for your kind support.</h6>")
        out.put_button('Check Results', results)

def count_votes():
    myCursor.execute("SELECT * FROM users")
    result = myCursor.fetchall()
    
    aapCount=0
    bjpCount=0
    congCount=0
    
    for entry in result:

        if entry[3] == 'Bhartiya Janta Party':
            bjpCount+=1
        
        elif entry[3] == 'Congress':
            congCount+=1
        
        elif entry[3] == 'Aam Aadmi Party':
            aapCount+=1
    
    return aapCount, bjpCount, congCount

def results():
    out.clear()
    out.put_markdown("# Results")
    voteCount = count_votes()
    out.put_table([['Political Party', 'Votes'], ['AAP', voteCount[0]], ['BJP', voteCount[1]], ['Congress', voteCount[2]]])

if __name__ == '__main__':
    pywebio.start_server(voting, port=80)
