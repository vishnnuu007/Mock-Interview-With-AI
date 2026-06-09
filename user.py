from flask import*
from database import*

user=Blueprint(__name__,'user')


@user.route("/user_home")
def userhome():
    return render_template('user_home.html',name=session['name'])

@user.route("/view_user",methods=['get','post'])
def view_user():
    data={}
    qry="select * from user where user_id='%s'"%(session['user'])
    res=select(qry)
    if res:
    # print(res,"////////////////////////////////////////")
        data['view']=res

    if 'Update' in request.form:
        fname= request.form['fname']
        lname= request.form['lname']
        place= request.form['place']
        phone= request.form['phone']
        email= request.form['email']


        qry1 = "update user set fname='%s', lname='%s',place='%s',phone='%s',email='%s' where user_id='%s'"%(fname,lname,place,phone,email,session['user'])
        vv=update(qry1)
        print(vv,"////////")

        return """<script>alert('Updated');window.location="/view_user"</script>"""



    return render_template('view_user.html',data=data)

# @user.route("/user_view_user")
# def user_view_user():
#     data={}
#     qry="select * from user"
#     res=select(qry)
#     print(res,"////////////////////////////////////////")
#     data['view']=res
#     if 'update' in request.form:
#         fname=request.form['fname']
#         lname=request.form['lname']
#         place=request.form['place']
#         phone=request.form['phone']
#         email=request.form['email']
#         qry2="update user set fname='%s',lname='%s',place='%s',phone='%s',email='%s' where User_id='%s'"%(session['fname'],['lname'],['place'],['phone'],['email'])
#         update(qry2)


#     return render_template('user_view_user.html',data=data)


@user.route("/user_view_role")
def user_view_user():
    data={}
    qry="select * from roles"
    res=select(qry)
    print(res,"////////////////////////////////////////")
    data['view']=res

    return render_template('user_view_role.html',data=data)







@user.route("/send_complaint",methods=['get','post'])
def send_complaint():
    data={}
    if 'submit' in request.form:
       complaint=request.form['complaint']
       a="insert into complaint values(null,'%s','%s',curdate(),'pending')"%( session['user'],complaint)
       insert(a)
       return """<script>alert('Submitted');window.location="/send_complaint"</script>"""
    qry="select * from complaint where sender_id='%s'"%(session['user'])
    res=select(qry)
    if res:
        data['view']=res
    return render_template('send_complaint.html',data=data)



@user.route("/view_notification")
def user_view_notification():
    data={}
    qry="select * from notification"
    res=select(qry)
    print(res,"////////////////////////////////////////")
    data['view']=res

    return render_template('view_notification.html',data=data)







from voice import *

@user.route('/role_selection')
def role_selection():
    a="select * from roles"
    r=select(a)
    return render_template('role_selection.html',r=r)

def create_and_store_question(role):
    # Fetch the role_id based on the provided role name
    cursor.execute("SELECT role_id FROM roles WHERE role_name = %s", (role,))
    role_id = cursor.fetchone()

    if role_id:
        role_id = role_id[0]

        # Fetch existing questions for the role to avoid duplication
        cursor.execute("SELECT question_text FROM question WHERE role_id = %s", (role_id,))
        existing_questions = [row[0] for row in cursor.fetchall()]

        question_and_answer = []

        for _ in range(10):  # Attempt to generate 10 unique questions
            # Updated question generation prompt
            question_prompt = f"""Generate ONE technical interview question for a {role} that meets these exact criteria:
1. Must be exactly one line
2. Must test a specific technical skill required for {role}
3. Must be answerable by a fresh graduate in under 30 words
4. Must be unique and not similar to: {existing_questions}
5. Must focus on fundamental technical concepts, not advanced topics"""

            question_text = generate_gemini_response(question_prompt)

            # Check for uniqueness before proceeding
            if question_text and question_text not in existing_questions:
                # Updated answer generation prompt
                answer_prompt = f"""Provide a technical answer for: {question_text}
                Requirements:
                - Exactly one line
                - Maximum 30 words
                - Focus on key technical concept only
                - Use beginner-friendly terminology"""

                answer_text = generate_gemini_response(answer_prompt)

                if answer_text:
                    question_and_answer.append((question_text, answer_text))
                    existing_questions.append(question_text)  # Add to existing questions to track uniqueness
                else:
                    print("Failed to generate an answer for the question.")
            else:
                print("Failed to generate a unique question or duplication detected.")

        # Insert questions and answers into the database
        for question_text, answer_text in question_and_answer:
            cursor.execute(
                "INSERT INTO question (question_text, role_id, user_id, date) VALUES (%s, %s, %s, CURDATE())",
                (question_text, role_id, session['user'])
            )
            question_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO answer (question_id, correct_answer) VALUES (%s, %s)",
                (question_id, answer_text)
            )

        db.commit()
        print("Questions and answers successfully stored in the database.")
        return True
    else:
        print("Role not found in the database.")
        return False




        
from face_recognize import *  

    
@user.route('/face_recog', methods=['POST','GET'])
def face_recog():
    s=session['user']
    print(s)
    a=camclick(s)
    return a


import numpy as np
import cv2
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import winsound
from flask import render_template, request, session, flash, redirect, url_for
import threading

# Global variables
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
classifier = load_model('model_78.h5')
classifier.load_weights('model_weights_78.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global state variables
latest_emotion = None
latest_confidence_score = 0
emotion_detection_running = False
global_camera = None

def cleanup_camera():
    """Cleanup function to properly release camera resources"""
    global emotion_detection_running, global_camera
    
    emotion_detection_running = False
    if global_camera is not None:
        global_camera.release()
        global_camera = None
        cv2.destroyAllWindows()

def emotion_detect():
    """Main emotion detection function"""
    global latest_emotion, latest_confidence_score, emotion_detection_running, global_camera
    face_absent_counter = 0

    try:
        # Initialize camera
        global_camera = cv2.VideoCapture(0)
        
        while emotion_detection_running and global_camera is not None:
            ret, frame = global_camera.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            # Handle face absence
            if len(faces) == 0:
                face_absent_counter += 1
                if face_absent_counter > 30:
                    winsound.Beep(1000, 500)
                    face_absent_counter = 0
            else:
                face_absent_counter = 0

            # Process detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = classifier.predict(roi)[0]
                    maxindex = int(np.argmax(prediction))
                    emotion_detected = emotion_labels[maxindex]
                    confidence_score = prediction[maxindex] * 100

                    # Update global state
                    latest_emotion = emotion_detected
                    latest_confidence_score = confidence_score

                    # Draw on frame
                    label_position = (x, y - 10)
                    cv2.putText(frame, f'{emotion_detected}: {confidence_score:.2f}%', 
                              label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Emotion & Confidence Detector', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
    finally:
        cleanup_camera()

def emotion_detection_thread():
    """Thread function for emotion detection"""
    global emotion_detection_running
    try:
        emotion_detection_running = True
        emotion_detect()
    except Exception as e:
        print(f"Error in emotion detection thread: {str(e)}")
    finally:
        emotion_detection_running = False # Stop the thread after the function finishes

@user.route('/start_interview', methods=['POST'])
def start_interview():
    """Route to start the interview process"""
    global emotion_detection_running

    # Clean up any existing camera session
    cleanup_camera()

    role = request.form.get('role')
    if not role:
        flash("Error: Role not specified", "error")
        return redirect(url_for('user.userhome'))

    # Validate role exists in database
    role_check = select(f"SELECT role_id FROM roles WHERE role_name='{role}'")
    if not role_check:
        flash(f"Error: Invalid role '{role}'", "error")
        return redirect(url_for('user.userhome'))
    
    print(role_check,"///rc")

    # Validate user session
    ee = session.get('user')
    print(ee,"//ss")
    if not ee:
        flash("Error: User session expired. Please login again.", "error")
        return redirect(url_for('public.login'))

    try:
        z = create_and_store_question(role)
        print(z,"///z")
        
        if z:
            question = fetch_next_question(role)
            if question:
                question_id, question_text = question

                # Start emotion detection
                emotion_thread = threading.Thread(target=emotion_detection_thread)
                emotion_thread.daemon = True
                emotion_thread.start()

                return render_template('question_page.html', 
                                    role=role, 
                                    question=question_text, 
                                    question_id=question_id)
            else:
                cleanup_camera()
                flash("No questions are currently available for this role. Please try a different role or contact support.", "warning")
                return render_template('user_home.html')
        else:
            return render_template('wait_page.html')

    except Exception as e:
        print(f"Error in start_interview: {str(e)}")
        cleanup_camera()
        flash("An error occurred while starting the interview. Please try again.", "error")
        return redirect(url_for('user.userhome'))
    
@user.route('/check_generation_status')
def check_generation_status():
    role = request.args.get('role')

    # Check if the generation process is complete
    z = check_generation_complete(role)

    if z == True:
        question = fetch_next_question(role)
        if question:
            question_id, question_text = question

            # Start the emotion detection in a separate thread
            threading.Thread(target=emotion_detection_thread).start()

            return render_template('question_page.html', role=role, question=question_text, question_id=question_id)
        else:
            return "No question available for this role. Please try again."
    else:
        return render_template('wait_page.html', role=role)

def check_generation_complete(role):
    # This function should check whether the generation process is complete
    # For simplicity, let's assume it returns True if complete, otherwise False
    return True  # Update this logic according to your application's requirement


@user.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Route to handle answer submission and exam completion"""
    global emotion_detection_running

    # role = request.form.get('role')
    role = request.form['role']

    z="select * from roles where role_name='%s'"%(role)
    cc=select(z)
    roleid=cc[0]['role_id']


    # Check if the user is quitting the exam
    if 'submit' in request.form and request.form['submit'] == 'Quit Exam':
        print("try")
        cleanup_camera()
        # Stop the emotion detection
        emotion_detection_running = False

        print("////////////////////")

        # Calculate scores for the final result
        total_result = select(f"SELECT COUNT(score) AS total FROM question INNER JOIN answer USING(question_id) WHERE user_id='{session['user']}' AND date=CURDATE() AND role_id='{roleid}'")
        mark_result = select(f"SELECT COUNT(score) AS mark FROM question INNER JOIN answer USING(question_id) WHERE user_id='{session['user']}' AND date=CURDATE() AND score=1 AND role_id='{roleid}'")
        
        total = total_result[0]['total'] if total_result else 0
        mark = mark_result[0]['mark'] if mark_result else 0
        
        per = round((float(mark) / float(total)) * 100, 2) if total > 0 else 0

        print(per,"/////////////")

        data = {}
        xx = "select * from question inner join answer using(question_id) where role_id='%s' AND user_id='%s' AND date=CURDATE()" % (roleid, session['user'])
        data['view'] = select(xx)
        print(data,"//////")
        return redirect(url_for('user.userhome'))
        # return render_template('final.html', per=per, emotion=latest_emotion, confidence=latest_confidence_score, data=data)

    # Regular answer submission
    question_id = request.form.get('question_id')
    user_answer = request.form.get('user_answer')

    if not question_id:
        flash("Error: No question specified", "error")
        return redirect(url_for('user.userhome'))

    # Get correct answer from database
    cursor.execute("SELECT correct_answer FROM answer WHERE question_id = %s", (question_id,))
    result = cursor.fetchone()
    
    if result is None:
        flash("Error: Question not found", "error")
        return redirect(url_for('user.userhome'))

    correct_answer = result[0]
    similarity_score = similarity(user_answer, correct_answer)

    # Update score in database
    if similarity_score > 0.5:
        cursor.execute("UPDATE answer SET score = 1 WHERE question_id = %s", (question_id,))
        message = "Correct! Your answer is similar to the correct answer."
    else:
        cursor.execute("UPDATE answer SET score = 0 WHERE question_id = %s", (question_id,))
        message = "Incorrect. Your answer does not match the correct answer."

    # Save user's answer
    cursor.execute("UPDATE answer SET user_answer = %s WHERE question_id = %s", (user_answer, question_id))
    db.commit()

    # Get next question or show final results
    next_question = fetch_next_question(role, current_question_id=question_id)
    if next_question:
        question_id, question_text = next_question
        return render_template('question_page.html', role=role, question=question_text, question_id=question_id, message=message)
    else:
        # No more questions, show final results
        emotion_detection_running = False
        
        total_result = select(f"SELECT COUNT(score) AS total FROM question INNER JOIN answer USING(question_id) WHERE user_id='{session['user']}' AND date=CURDATE() AND role_id='{roleid}'")
        mark_result = select(f"SELECT COUNT(score) AS mark FROM question INNER JOIN answer USING(question_id) WHERE user_id='{session['user']}' AND date=CURDATE() AND score=1 AND role_id='{roleid}'")
        
        total = total_result[0]['total'] if total_result else 0
        mark = mark_result[0]['mark'] if mark_result else 0
        
        per = round((float(mark) / float(total)) * 100, 2) if total > 0 else 0

        data = {}
        xx = "select * from question inner join answer using(question_id) where role_id='%s' AND user_id='%s' AND date=CURDATE()" % (roleid, session['user'])
        data['view'] = select(xx)

        return render_template('final.html', per=per, emotion=latest_emotion, confidence=latest_confidence_score, data=data)
    

@user.route('/quit_exam', methods=['POST'])
def quit_exam():
    global emotion_detection_running

    role = request.form['role']
    z = "select * from roles where role_name='%s'" % (role)
    cc = select(z)
    roleid = cc[0]['role_id']

    # Stop emotion detection
    emotion_detection_running = False
    cleanup_camera()

    # Calculate final scores
    total_result = select(f"SELECT COUNT(score) AS total FROM question INNER JOIN answer USING(question_id) WHERE user_id='{session['user']}' AND date=CURDATE() AND role_id='{roleid}'")
    mark_result = select(f"SELECT COUNT(score) AS mark FROM question INNER JOIN answer USING(question_id) WHERE user_id='{session['user']}' AND date=CURDATE() AND score=1 AND role_id='{roleid}'")
    
    total = total_result[0]['total'] if total_result else 0
    mark = mark_result[0]['mark'] if mark_result else 0
    
    per = round((float(mark) / float(total)) * 100, 2) if total > 0 else 0

    data = {}
    xx = "select * from question inner join answer using(question_id) where role_id='%s' AND user_id='%s' AND date=CURDATE()" % (roleid, session['user'])
    data['view'] = select(xx)

    return render_template('final.html', per=per, emotion=latest_emotion, confidence=latest_confidence_score, data=data)