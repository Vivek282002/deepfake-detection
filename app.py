from flask import Flask, render_template, url_for, request
import sqlite3
import os
from image_test import *
from video_test import *
from audio_test import *
from video_test import process_video

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name=? AND password=?"
        cursor.execute(query, (name, password))

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('home.html')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", 
               (name, password, mobile, email))
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/detectimage', methods=['GET', 'POST'])
def detectimage():
    if request.method == 'POST':

        src = "static/imgs/"+request.form['src']
        dst = "static/imgs/"+request.form['dst']
        out = "static/image_output/output.jpg"

        command = f"python main.py --src {src} --dst {dst} --out {out} --correct_color"
        os.system(command)

        return render_template('Image.html', inputimage=dst, outputimage=out)
    return render_template('Image.html')

@app.route('/detectvideo', methods=['GET', 'POST'])
def detectvideo():
    if request.method == 'POST':
        src_file = request.files['src']
        dst_file = request.files['dst']

        src_path = os.path.join('static/uploads', src_file.filename)
        dst_path = os.path.join('static/uploads', dst_file.filename)

        src_file.save(src_path)
        dst_file.save(dst_path)

        # ✅ Process video and get results
        result = process_video(src_path)

        return render_template(
            'video.html',
            inputvideo=src_path,
            outputvideo='output.avi',
            videoresult=result['classification'],
            fake_frames=result['fake_frames'],
            total_frames=result['total_frames']
        )
    return render_template('video.html')

@app.route('/detectlive', methods=['GET', 'POST'])
def detectlive():
    if request.method == 'POST':
        src = "static/imgs/"+request.form['src']
        out = "static/video_output/output.mp4"

        command = f"python main_video.py --src_img {src} --show --correct_color --save_path {out}"
        os.system(command)
        return render_template('Live.html', inputvideo='static/videos/input.mp4', outputvideo=out)
    return render_template('Live.html')

@app.route('/detection')
def detection():
    return render_template('testimage.html')


@app.route('/testimage', methods=['GET', 'POST'])
def testimage():
    if request.method == 'POST':

        src = "static/imgs/"+request.form['src']
        out = "static/testimage_output/output.jpg"

        process_image(src, out)

        return render_template('testimage.html', inputimage=src, outputimage=out)
    return render_template('testimage.html')

@app.route('/testvideo', methods=['GET', 'POST'])
def testvideo():
    if request.method == 'POST':
        src = "static/videos/"+request.form['src']
        out = "static/testvideo_output/output.mp4"

        # Process video and get results
        result = process_video(src, out)
        
        if result is None:
            return render_template('testvideo.html', error="Error processing video")
            
        # Calculate percentage
        fake_percentage = (result['fake_frames']/result['total_frames']*100)
        
        # Create result message
        result_message = f"""DETAILED ANALYSIS REPORT
================================
Final Classification: {result['classification']}
--------------------------------
Frames Analysis:
• Total Frames: {result['total_frames']}
• Fake Frames: {result['fake_frames']}
• Fake Frame Percentage: {fake_percentage:.1f}%
--------------------------------
Decision Criteria:
• Threshold: 10 or more fake frames
• Classification: {'FAKE' if fake_percentage >= 10 else 'REAL'}"""

        return render_template('testvideo.html', 
                            inputvideo=src, 
                            outputvideo=out,
                            result=result_message)
    return render_template('testvideo.html')

@app.route('/testaudio', methods=['GET', 'POST'])
def testaudio():
    if request.method == 'POST':
        src = "static/audio/"+request.form['src']
        out = runtest(src)
        return render_template('testaudio.html', inputaudio=src, output=out)
    return render_template('testaudio.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
