import os, uuid
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------- DEMO DATA ----------
programs = [
    {
        'title': 'Certificate in Dialysis Technology',
        'description': 'A 6-month certificate program covering kidney anatomy, hemodialysis, peritoneal dialysis, machine handling, and patient care. Includes hands-on training on real dialysis machines.',
        'duration': '6 Months',
        'fee': '₹35,000',
        'image': 'https://images.unsplash.com/photo-1631217868264-e5b90bb7e133?w=600'
    },
    {
        'title': 'Diploma in Dialysis Technology',
        'description': 'A comprehensive 1-year diploma for students and working staff. Covers advanced dialysis procedures, vascular access, complications management, and clinical internship.',
        'duration': '1 Year',
        'fee': '₹65,000',
        'image': 'https://images.unsplash.com/photo-1579154204601-01588f351e67?w=600'
    },
    {
        'title': 'Advanced Certificate for Medical Staff',
        'description': 'Fast-track 3-month upskilling program for existing nurses and technicians. Focus on advanced dialysis techniques, troubleshooting, and ICU dialysis.',
        'duration': '3 Months',
        'fee': '₹25,000',
        'image': 'https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=600'
    },
    {
        'title': 'Hands-on Dialysis Workshop',
        'description': 'Intensive 2-week practical workshop. Learn machine setup, cannulation, monitoring, and emergency handling directly on dialysis equipment.',
        'duration': '2 Weeks',
        'fee': '₹10,000',
        'image': 'https://images.unsplash.com/photo-1666214280557-f1b5022eb634?w=600'
    },
]

instructors = [
    {
        'name': 'Dr. Rajesh Kumar',
        'designation': 'Nephrologist & Chief Instructor',
        'image': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400'
    },
    {
        'name': 'Sr. Anita Sharma',
        'designation': 'Senior Dialysis Nurse Trainer',
        'image': 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400'
    },
    {
        'name': 'Mr. Suresh Patel',
        'designation': 'Dialysis Technician Expert',
        'image': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400'
    },
]

gallery = [
    'https://images.unsplash.com/photo-1631217868264-e5b90bb7e133?w=600',
    'https://images.unsplash.com/photo-1579154204601-01588f351e67?w=600',
    'https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=600',
    'https://images.unsplash.com/photo-1666214280557-f1b5022eb634?w=600',
    'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=600',
    'https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=600',
]

messages = []

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


def save(file):
    if file and file.filename:
        name = str(uuid.uuid4()) + "_" + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        return "uploads/" + name
    return ""


# ---------- PUBLIC ----------
@app.route('/')
def index():
    return render_template('index.html', programs=programs, instructors=instructors, gallery=gallery)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        messages.append({
            'name': request.form['name'],
            'email': request.form['email'],
            'message': request.form['message']
        })
        return "<h3>Thanks! Our team will contact you soon. <a href='/'>Go Home</a></h3>"
    return render_template('contact.html')


@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html', images=gallery)


@app.route('/instructors')
def instructors_page():
    return render_template('instructors.html', instructors=instructors)


# ---------- ADMIN ----------
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == ADMIN_USER and request.form['pass'] == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin')
        return "Wrong login. <a href='/admin/login'>Try again</a>"
    return '''
        <h2>Admin Login</h2>
        <form method="POST">
            <input name="user" placeholder="Username" required><br><br>
            <input name="pass" type="password" placeholder="Password" required><br><br>
            <button>Login</button>
        </form>
    '''


@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin/login')
    return render_template('admin.html',
                           programs=programs,
                           instructors=instructors,
                           gallery=gallery,
                           messages=messages)


@app.route('/admin/add_program', methods=['POST'])
def add_program():
    if not session.get('admin'):
        return redirect('/admin/login')
    img = request.form.get('image_url') or save(request.files.get('image'))
    programs.append({
        'title': request.form['title'],
        'description': request.form['description'],
        'duration': request.form.get('duration', ''),
        'fee': request.form.get('fee', ''),
        'image': img
    })
    return redirect('/admin')


@app.route('/admin/add_instructor', methods=['POST'])
def add_instructor():
    if not session.get('admin'):
        return redirect('/admin/login')
    img = request.form.get('image_url') or save(request.files.get('image'))
    instructors.append({
        'name': request.form['name'],
        'designation': request.form['designation'],
        'image': img
    })
    return redirect('/admin')


@app.route('/admin/add_gallery', methods=['POST'])
def add_gallery():
    if not session.get('admin'):
        return redirect('/admin/login')
    urls = request.form.get('image_urls', '')
    for url in urls.split(','):
        url = url.strip()
        if url:
            gallery.append(url)
    for f in request.files.getlist('images'):
        path = save(f)
        if path:
            gallery.append(path)
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)