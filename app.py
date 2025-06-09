from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔹 Routes for static pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/10th.html')
def pass10():
    return render_template('10th.html')

@app.route('/12th.html')
def pass12():
    return render_template('12th.html')

@app.route('/homework.html')
def homework():
    return render_template('homework.html')

@app.route('/8th.html')
def admin_jobs():
    return render_template('8th.html')

@app.route('/all.html')
def all_jobs():
    return render_template('all.html')
# 🔹 Route for login page
@app.route('/admin.html', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            entries = []
            with open('registrations.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 8:
                        entries.append(parts)
            return render_template('dashboard.html', entries=entries)  # ✅ file needed
        else:
            error = "❌ Invalid username or password"

    return render_template('admin.html')






# 🔹 Route for form page
@app.route('/formcode.html')
def form():
    return render_template('formcode.html')

# 🔹 Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form['fullname']
    age = request.form['age']
    mobile = request.form['mobile']
    whatsapp = request.form['whatsapp']
    gmail = request.form['gmail']
    education = request.form['education']
    id_type = request.form['idType']
    pdf_file = request.files['rusemPdf']

    # Save PDF
    filename = ""
    if pdf_file and pdf_file.filename != "":
        filename = f"{fullname.replace(' ', '_')}_{pdf_file.filename}"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(pdf_path)

    # Save text data
    with open('registrations.txt', 'a') as f:
        f.write(f"{fullname}, {age}, {mobile}, {whatsapp}, {gmail}, {education}, {id_type}, {filename}\n")

    return render_template('formcode.html', fullname=fullname)
    # 🔹 Delete entry and stay on dashboard
@app.route('/delete', methods=['POST'])
def delete_entry():
    line_to_delete = request.form['line_data']

    with open('registrations.txt', 'r') as file:
        lines = file.readlines()
    with open('registrations.txt', 'w') as file:
        for line in lines:
            If line.strip() != line_to_delete.strip():
                file.write(line)

    updated_entries = []
    with open('registrations.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 8:
                updated_entries.append(parts)

    return render_template('dashboard.html', entries=updated_entries)

if __name__ == '__main__':
    app.run(debug=True)
