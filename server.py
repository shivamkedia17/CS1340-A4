from prettytable import PrettyTable
import socketserver


class Course():
    def __init__(self, name: str, prereq_list: list[str] = ['None']):
        self.name   = name
        self.prereq_list = prereq_list

    def __repr__(self) -> str:
        listrepr = ', '.join(self.prereq_list)
        return f"""
    Course: {self.name}
    Prerequisites: {listrepr}
    """

class CourseList():
    def __init__(self):
        self.list   = dict()
        self.count  = 0

    def add_course(self, course: Course):
        self.count += 1
        self.list[self.count] = course

    def __repr__(self) -> str:
        return self.list.__repr__()

courses     = CourseList()
electives   = CourseList()

class TCPHandler(socketserver.BaseRequestHandler):
    def recv_msg(self):
        block_size = 2048
        data = self.request.recv(block_size).strip()
        response = data.decode()
        # Log the received message to the console
        print(f"{self.client_address}: {data.decode()}")
        return response

    # communication protocol is such that first the size of the data is sent
    # and then the data itself is sent
    def send_msg(self, message):
        data = message.encode()
        size = f"{len(data)}"
        self.request.send(size.encode())
        if self.recv_msg() == "Ok":
            self.request.sendall(data)

    def handle(self):
        _ = self.recv_msg()
        self.greet()
        while True:
            client_response = self.recv_msg()
            if client_response == "close":
                self.send_msg("Connection Closed")
                self.request.close()
                break
            elif client_response == "greet":
                self.greet()
            else:
                self.use_features(client_response)

    # Please don't sue me, I couldn't think of too many related questions,
    # So I drew inspiration from the CS@Ashoka Handbook v3
    # (Some question-answers are copy-pasted from there)
    def greet(self):
        greeting = """
Welcome! Below is a list of queries related to the Computer Science major at Ashoka University.
You can choose a question by typing the corresponding number.
E.g: You want the core course list. In your prompt, enter "3" (without the quotes).
You can ask as many questions as you want until you close the connection.
----------------------------------------------------------------------------------------------
1.  What is the total number of CS credits required to complete the 4-year BSc Hons
        degree in CS?
2.  Could you provide a breakdown of CS credits?
3.  What are the core courses?
4.  Can you give a list a pre-requisites for core courses?
5.  What are some electives offered?
6.  What is the Recommended Trajectory for a pure CS major?
7.  What are ISMs? What is the CS department's policy on ISM credit?
8.  What Internship and Research opportunities are availabe for undergraduates?
9.  Awards and Recognitions by the CS department
10. What are Teaching Assistantships?
11. Clubs and Societies - CS@Ashoka
12. Please give some advice on obtaining LORs from faculty.
----------------------------------------------------------------------------------------------
Type "greet" to see this message again later. Lastly, type "close" to close the connection.
        """
        self.send_msg(greeting)

    def use_features(self, option):
        global courses
        global electives
        message = ""

        match option:
            case "1":
                message = """
Minimum CS Credits Required:
--------------------------------------
A student needs a minimum of 86 credits from the Computer Science Department.
--------------------------------------
"""

            case "2":
                message = """
The 86 CS credits are broken down into:
--------------------------------------
    1. Core Courses: 70
    2. Electives   : 12
    3. Project     : 4
--------------------------------------
                """

            case "3":
                bsm = '\n'.join(f"\t{i}.\t{courses.list[i].name}" for i in range(1,  6 ))
                cpt = '\n'.join(f"\t{i}.\t{courses.list[i].name}" for i in range(6,  15))
                sas = '\n'.join(f"\t{i}.\t{courses.list[i].name}" for i in range(15, 19))
                message = """
List of Core Courses:
---------------------
    Basic Science and Math:
    -----------------------
    """+bsm+"""

    Computational Thinking:
    -----------------------
    """+cpt+"""

    Systems and Software:
    -----------------------
    """+sas+"""
------------------------------------------
Each course is 4 credits except Information Security (2 credits).
 Including the Capstone Project, this sums upto 74 credits.
------------------------------------------
                """

            case "4":
                self.send_msg(message="""
        > Sure, enter the number of the core course from the list in (3) to
        > show its prerequisites. Enter 0 to go back to other options.\n""")
                while True:
                    try:
                        choice = int(self.recv_msg())
                        if choice < 0 or choice > courses.count:
                            raise Exception("Client: Invalid choice for course.")
                        elif choice == 0:
                            break
                        else:
                            self.send_msg(message=courses.list[choice].__repr__()+"\n\tEnter next choice or 0 to go up.\n")
                    # when choice is out of range and not zero, or not a number
                    except:
                        self.send_msg(message="\a\tInvalid Choice. Please enter a number from course list or 0.\n")
                        continue
                    # when choice is 0 => break out of prereq loop
                message = "Select a choice from the query list.\n"

            case "5":
                def pp_list(x, y, structure=electives):
                    return '\n'.join(f"\t{i}.\t{structure.list[i].name}" for i in range(x, y))
                message = """
List of Elective Courses:
-------------------------
    Algorithms and Computational Thinking:
    -------------------------------------
    """+pp_list(1, 8)+"""

    Machine learning and AI:
    -----------------------
    """+pp_list(8, 16)+"""

    Security and Privacy:
    -----------------------
    """+pp_list(16, 20)+"""

    Systems:
    -----------------------
    """+pp_list(20, 24)+"""

    Applications and Software:
    -------------------------
    """+pp_list(24, 25)+"""

------------------------------------------
Please note this is only a non-exhaustive list of potential electives.
You can see the electives being offered per-semester on AMS.
------------------------------------------
                """

            case "6":
                x = PrettyTable()
                x.title = "Recommended Trajectory for a Pure CS Major"
                x.field_names = ["Monsoon Sem","Spring Sem"]
                x.add_row(row=["Sem 1", "Sem 2"], divider=True)
                x.add_row(row=["Calculus\nFC\nFC\nFC",
                               "Intro to CS\nDiscrete Math\nFC\nFC\nFC"], divider=True)
                x.add_row(row=["Sem 3", "Sem 4"], divider=True)
                x.add_row(row=["Probability & Stats\nLinear Algebra\nData Structures & Algos\nFC\nFC\nFC",
                               "Theory of Computation\nComputer Organisation & Systems\nPhysics Course\nBio Course\nCS Elective"], divider=True)
                x.add_row(row=["Sem 5", "Sem 6"], divider=True)
                x.add_row(row=["Design Practices in CS\nIntroduction to Machine Learning\nComputer Networks\nInformation Security\nCS Elective",
                               "Design & Analysis of Algos\nData Science & Management\nEmbedded Systems\nCS Elective\nCS Elective"], divider=True)
                x.add_row(row=["Sem 7", "Sem 8"], divider=True)
                x.add_row(row=["Capstone Project\nProgramming Languages & Translation\nCS Elective\nCS Elective",
                                "\nCS Elective\nCS Elective"], divider=True)
                message = x.get_string()+"""

Note: Incorporate one Physics and one Biology course,
  along with 12 credits of CS electives, within your
  four-year curriculum in addition to CCs and FCs as per availability.
------------------------------------------
"""

            case "7":
                message = """
Independent Study Modules (ISMs):
-------------------------------
These are 4-credit (or 2-credit) courses that provide students an opportunity
to work closely with a faculty member. These projects can either be research
that faculty members are already working on or any other research topic that
students may be interested in.

If interested, you can simply approach a faculty member through email prior
to the start of the semester, requesting them for guidance through an ISM.

Note: These count towards your electives. There is a cap on the no. of ISMs
    you can take. You can audit an ISM, in which case it won't count towards
    the quota.
------------------------------------------
"""
            case "8":
                message = """
Internship and Research Advice:
-------------------------------
Internships are often a great way to explore work-roles. Ashoka University offers a 3-month
 long summer break, which you can utilize productively by interning. It is advisable to search
 for summer internships at least 2-3 months prior to the start of the break - most firms
 or research centers have deadlines that you should research about as early as possible.

Moreover, Ashoka University’s Career Development Offices (CDO) also provide internship
opportunities through firms that recruit interns on campus. If you’re applying through CDO,
keep your SuperSet profile updated to avoid last-minute hassle.

For CS specific internships, do occasionally brush up on your Data Structures and Algorithms.
------------------------------------------
"""
            case "9":
                message = """
Awards and Recognitions:
-------------------------------
• Dean’s List: The Dean’s List at Ashoka for any given semester includes the names of all students
   who, in the courses they have taken that semester, have scored a GPA of 3.65 or above.
   The Dean’s List is awarded on a semester basis.

• Latin Honors: Students who have achieved scholastic distinction may be awarded the bachelor’s
  degree with Latin honors at graduation. Honors appear on the official transcript and diploma.
    The criteria for these honors is as follows:
        1. Cum Laude (With Distinction)                - GPA > 3.6
        2. Magna Cum Laude (With High Distinction)     - GPA > 3.75
        3. Summa Cum Laude (With Highest Distinction)  - GPA > 3.9

• Academic Achievement Awards: Gold, Silver, and Bronze Awards are awarded respectively to the
  students attaining the Top 3 Major CGPAs during graduation.

• Undergraduate Research Excellence Awards: Awarded to the graduating student with the best
  track record in academic research, evaluated on the basis of publications and
  thesis quality.

• Service Excellence Awards: Awarded for extraordinary service in department building
   through various activities.

• Teaching Assistantship Excellence Awards (Semester-wise): Awarded for students for excellence
   in TAship duties during an academic semester, as determined by the faculty.
------------------------------------------
"""
            case "10":
                message = """

Teaching Assistantships:
-------------------------------
The CS department allows 3rd and 4th year UG students to become Teaching Assistants.
As a TA, you would be responsible for grading quizzes, holding discussion sessions
and doubt clearing office hours, as well as helping with the logistics for classes.
A prospective applicant can apply to TA for only those courses which they have
already studied in Ashoka in the past. While preference may be given to seniors,
anyone is welcome to apply for TAship by approaching the professor directly. Some
courses may have different procedures, so do confirm it with the instructor.
------------------------------------------
"""
            case "11":
                message = """
Clubs and Societies - CS@Ashoka
-------------------------------
There is a cross-batch whatsapp group run by the CS representatives where you will get all
major updates related to events, talks, and important course/degree related notifications.
It is a platform to stay connected to CS people at Ashoka.

We have the following CS clubs and Societies:
1. CS Society
    The Computer Science Society at Ashoka University was founded in 2016 to strengthen
    the emerging CS culture on campus. It is an academic society that aims to create
    opportunities and resources for all students interested in this field through a host
    of activities. Past events include Mahavamsa - Ashoka’s first programming contest,
    hackathons, cryptic hunts, talks and workshops.
2. WiCS - Women in Computing Society
    WiCS helps promote inclusivity and diversity and is open to everyone regardless of
    their major or gender. It is meant to provide a safe space to connect with like-minded
    people who share your interest and enthusiasm for the vast uncanny world of CS.
3. IEEE Ashoka Student Branch
    IEEE is a leading society on the Internet. You can read more about it online. The Ashoka
    Student Branch is an attempt to create opportunities by leveraging connections in IEEE
    from across the globe.
------------------------------------------
"""
            case "12":
                message = """
Advice on Obtaining Letters of Recommendation:
-------------------------------
Graduation School applications often require letters of recommendation from faculty during
the admissions process. An optimal letter-writer should ideally have you in at least one class
or should have supervised you in research, thesis, or other work.

Moreover, their contact with you should be relatively recent. You might also want to consider
how well you performed in their class or work and whether you have had interactions with them
outside of the classroom.

Note that different professors may have different rules related to Letters of Recommendation,
thus make it a point to get in touch with your desired letter-writer and clarify all details
well in advanced. Also, approach the faculty at least 2 weeks in advanced for them to be prepared.
------------------------------------------
"""
            case _:
                message = "\aOption Not Recognised. Enter a correct option. Type 'greet' to see choices and 'close' to disconnect."
        self.send_msg(message)
        return

def populate_course_list():
    global courses
    courses.add_course(Course("Calculus"                                , ["Check with Math Dept."]))
    courses.add_course(Course("Linear Algebra"                          , ["Check with Math Dept."]))
    courses.add_course(Course("Probability and Statistics"              , ["Either Math in Class 11 & 12", "OR QRMT, Calculus"]))
    courses.add_course(Course("Physics Course"                              ))
    courses.add_course(Course("Biology Course"                              ))
    courses.add_course(Course("Introduction to Computer Science"        , ["Either Math in Class 11 & 12", "OR >= B in both QRMT, Calculus"]))
    courses.add_course(Course("Discrete Mathematics"                    , ["Either Math in Class 11 & 12", "OR >= B in both QRMT, Calculus"]))
    courses.add_course(Course("Data Structures and Algorithms"          , ["Intro to Computer Science", "Discrete Math"]))
    courses.add_course(Course("Introduction to Machine Learning"        , ["Probability and Statistics", "Linear Algebra", "Data Structures and Algorithms"]))
    courses.add_course(Course("Data Science & Management"               , ["Data Structures and Algorithms", "Introduction to Machine Learning"]))
    courses.add_course(Course("Theory of Computation"                   , ["Data Structures and Algorithms"]))
    courses.add_course(Course("Design and Analysis of Algorithms"       , ["Data Structures and Algorithms", "Linear Algebra"]))
    courses.add_course(Course("Programming Languages and Translation"   , ["Data Structures and Algorithms", "Theory of Computation"]))
    courses.add_course(Course("Information Security"                    , ["Data Structures and Algorithms", "Probability and Statistics"]))
    courses.add_course(Course("Computer Organisation and Systems"       , ["Intro to Computer Science"]))
    courses.add_course(Course("Design Practices in Computer Science"    , ["Data Structures and Algorithms", "Computer Organisation and Systems"]))
    courses.add_course(Course("Computer Networks"                       , ["Intro to Computer Science", "Data Structures and Algorithms"]))
    courses.add_course(Course("Embedded Systems"                        , ["Computer Organisation and Systems"]))
    # print(courses)

def populate_elective_list():
    global electives
    # courses 1 - 7: algos
    electives.add_course(Course("Formal Logic"                          , ["TBA"]))
    electives.add_course(Course("Numerical Algorithms"                  , ["TBA"]))
    electives.add_course(Course("Advanced Algorithms"                   , ["TBA"]))
    electives.add_course(Course("Graph Algorithms"                      , ["TBA"]))
    electives.add_course(Course("Approximation Algorithms"              , ["TBA"]))
    electives.add_course(Course("Randomised Algorithms"                 , ["TBA"]))
    electives.add_course(Course("Quantum Algorithms"                    , ["TBA"]))
    # courses 8 - 15: AI/ML
    electives.add_course(Course("Advanced Machine Learning"             , ["TBA"]))
    electives.add_course(Course("Natural Language Processing"           , ["TBA"]))
    electives.add_course(Course("Computer Vision"                       , ["TBA"]))
    electives.add_course(Course("AI for Social Good"                    , ["TBA"]))
    electives.add_course(Course("ML in Economics"                       , ["TBA"]))
    electives.add_course(Course("ML in Healthcare"                      , ["TBA"]))
    electives.add_course(Course("ML in Natural Sciences"                , ["TBA"]))
    electives.add_course(Course("Computation Radiology"                 , ["TBA"]))
    # courses 15 - 19: Security/Privacy
    electives.add_course(Course("System Security & Privacy"             , ["TBA"]))
    electives.add_course(Course("Cryptography"                          , ["TBA"]))
    electives.add_course(Course("Post-Quantum Cryptography"             , ["TBA"]))
    electives.add_course(Course("Digitalisation & Privacy"              , ["TBA"]))
    # courses 20 - 23: Systems
    electives.add_course(Course("Database Management Systems"           , ["TBA"]))
    electives.add_course(Course("Operating Systems!"                    , ["TBA"]))
    electives.add_course(Course("Computer Architecture"                 , ["TBA"]))
    electives.add_course(Course("Advanced Networks"                     , ["TBA"]))
    # courses 24: Software
    electives.add_course(Course("Software Engineering"                  , ["TBA"]))

def main():
    # server_ip       = '10.2.94.209'
    server_ip       = 'localhost'
    server_port     = 2048
    server_address  = (server_ip, server_port)
    server          = socketserver.TCPServer(server_address, TCPHandler)

    '''
    The socketserver library is basically an elegantly written API that provides a way to deal with servers.
    Some APIs are provided, In this case it's a TCP server class.
    It's constructor does the following:
    1. Binds a server-side socket to server_address
    2. Activates the server: starts to listen for connections as long as there are less connections than the backlog
    3. By default:
        - reuseaddress is false: server enters a brief waiting state after being shut down
        - reuseport is false: two sockets cannot bind to the same port--
             this option will be useful if I plan on making the server multithreaded
    4. Requests are handled using the Handler class defined above
    '''

    populate_course_list()
    populate_elective_list()
    print(f"Server up. Listening on port {server_port}...")
    print(f"Press Ctrl-C to gracefully shut down the server.")
    print(f"--------------Message Log-----------------------")

    try:
        server.serve_forever(poll_interval=1)
    except KeyboardInterrupt:
        try:
            print(f"\n-----------------------------------------------")
            print("Shutting Down server...")
            server.shutdown()
            server.server_close()
            print("Successfully shut down server.")
        except Exception as e:
            print(f"{e} occurred while shutting down server.")

if __name__ == "__main__":
    main()
