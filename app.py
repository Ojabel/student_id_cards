import streamlit as st
import mysql.connector
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
import hashlib
import pandas as pd
import matplotlib.pyplot as plt
import base64

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='student_management'
    )

def create_admin(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, hashlib.sha256(password.encode()).hexdigest()))
    conn.commit()
    cursor.close()
    conn.close()

def check_admin(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, hashlib.sha256(password.encode()).hexdigest()))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    return admin

def insert_student(name, email, phone, address, department, reg_no, image_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, phone, address, department, reg_no, image) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (name, email, phone, address, department, reg_no, image_bytes))
    conn.commit()
    student_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return student_id

def update_student(student_id, name, email, phone, address, department, reg_no, image_bytes):
    conn = get_db_connection()
    cursor = conn.cursor()
    if image_bytes:
        cursor.execute("UPDATE students SET name=%s, email=%s, phone=%s, address=%s, department=%s, reg_no=%s, image=%s WHERE id=%s", 
                       (name, email, phone, address, department, reg_no, image_bytes, student_id))
    else:
        cursor.execute("UPDATE students SET name=%s, email=%s, phone=%s, address=%s, department=%s, reg_no=%s WHERE id=%s", 
                       (name, email, phone, address, department, reg_no, student_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_students_per_month():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATE_FORMAT(created_at, '%%Y-%%m') AS Month, COUNT(*) FROM students GROUP BY Month ORDER BY Month")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def generate_id_card(student_id, name, email, phone, address, department, reg_no, image_bytes, qr_code_img):
    id_card = Image.new('RGB', (400, 250), color = (255, 255, 255))
    draw = ImageDraw.Draw(id_card)
    draw.rectangle([(0, 0), (400, 50)], fill="black")
    draw.text((10, 10), "Student ID Card", fill="white")

    student_image = Image.open(BytesIO(image_bytes))
    student_image = student_image.resize((80, 80))
    id_card.paste(student_image, (10, 60))

    draw.text((100, 60), f"Name: {name}", fill="black")
    draw.text((100, 80), f"Email: {email}", fill="black")
    draw.text((100, 100), f"Phone: {phone}", fill="black")
    draw.text((100, 120), f"Address: {address}", fill="black")
    draw.text((100, 140), f"Dept: {department}", fill="black")
    draw.text((100, 160), f"Reg No: {reg_no}", fill="black")

    qr_code_img = qr_code_img.resize((80, 80))
    id_card.paste(qr_code_img, (300, 150))

    return id_card

def save_id_card(student_id, id_card_img):
    id_card_img.save(f"student_id_cards/id_card_{student_id}.png")

st.set_page_config(page_title="Student Management System", layout="wide")

def main():
    st.title("Student Management System")

    if "admin" not in st.session_state:
        st.session_state.admin = None

    menu = ["Login", "Sign Up", "Dashboard", "Add Student", "View Students"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            admin = check_admin(username, password)
            if admin:
                st.session_state.admin = admin
                st.success("Login successful")
            else:
                st.error("Invalid username or password")

    elif choice == "Sign Up":
        st.subheader("Admin Sign Up")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Sign Up"):
            create_admin(username, password)
            st.success("Admin account created successfully")

    elif st.session_state.admin:
        if choice == "Dashboard":
            st.subheader("Dashboard")

            # Student count
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            num_students = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM admins")
            num_admins = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            # Bar Chart for students added per month
            data = get_students_per_month()
            df = pd.DataFrame(data, columns=["Month", "Count"])
            st.bar_chart(df.set_index("Month"))

            st.write(f"Total Students: {num_students}")
            st.write(f"Total Admins: {num_admins}")

        elif choice == "Add Student":
            st.subheader("Add Student")

            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_input("Address")
            department = st.text_input("Department")
            reg_no = st.text_input("Registration Number")
            image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

            if image_file is not None:
                image_bytes = image_file.read()

            if st.button("Add Student"):
                student_id = insert_student(name, email, phone, address, department, reg_no, image_bytes)
                st.success(f"Student {name} added successfully with ID {student_id}")

        elif choice == "View Students":
            st.subheader("View Students")
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, phone, address, department, reg_no, image FROM students")
            students = cursor.fetchall()
            cursor.close()
            conn.close()

            for student in students:
                student_id, name, email, phone, address, department, reg_no, image_bytes = student

                st.write(f"### ID: {student_id}")
                st.write(f"**Name:** {name}")
                st.write(f"**Email:** {email}")
                st.write(f"**Phone:** {phone}")
                st.write(f"**Address:** {address}")
                st.write(f"**Department:** {department}")
                st.write(f"**Registration Number:** {reg_no}")

                if image_bytes:
                    student_image = Image.open(BytesIO(image_bytes))
                    st.image(student_image, width=100)

                if st.button(f"Print ID Card {student_id}", key=f"print_button_{student_id}"):
                    qr_data = f"ID: {student_id}, Name: {name}, Email: {email}, Phone: {phone}, Address: {address}, Department: {department}, Reg No: {reg_no}"
                    qr_code_img = generate_qr_code(qr_data)
                    id_card_img = generate_id_card(student_id, name, email, phone, address, department, reg_no, image_bytes, qr_code_img)
                    save_id_card(student_id, id_card_img)
                    st.success(f"ID card for {name} saved successfully!")

                    # Display the ID card with download button
                    st.image(id_card_img, caption="ID Card")
                    img_buffer = BytesIO()
                    id_card_img.save(img_buffer, format="PNG")
                    img_buffer.seek(0)
                    b64 = base64.b64encode(img_buffer.read()).decode()
                    href = f'<a href="data:file/png;base64,{b64}" download="id_card_{student_id}.png">Download ID Card</a>'
                    st.markdown(href, unsafe_allow_html=True)

                if st.button(f"Edit {student_id}", key=f"edit_button_{student_id}"):
                    st.session_state.edit_student_id = student_id
                    st.experimental_rerun()

                if st.button(f"Delete {student_id}", key=f"delete_button_{student_id}"):
                    delete_student(student_id)
                    st.success(f"Student {name} deleted successfully!")
                    st.experimental_rerun()

        # Edit Student Section
        if "edit_student_id" in st.session_state and st.session_state.edit_student_id:
            student_id = st.session_state.edit_student_id

            # Fetch student details
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, email, phone, address, department, reg_no, image FROM students WHERE id = %s", (student_id,))
            student = cursor.fetchone()
            cursor.close()
            conn.close()

            if student:
                name, email, phone, address, department, reg_no, image_bytes = student
                st.subheader("Edit Student")
                name = st.text_input("Name", value=name)
                email = st.text_input("Email", value=email)
                phone = st.text_input("Phone", value=phone)
                address = st.text_input("Address", value=address)
                department = st.text_input("Department", value=department)
                reg_no = st.text_input("Registration Number", value=reg_no)
                image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], key="edit_image")

                if image_file is not None:
                    image_bytes = image_file.read()

                if st.button("Update Student"):
                    update_student(student_id, name, email, phone, address, department, reg_no, image_bytes)
                    st.success(f"Student {name} updated successfully!")
                    st.session_state.edit_student_id = None
                    st.experimental_rerun()

        st.sidebar.button("Logout", on_click=lambda: st.session_state.update(admin=None))

if __name__ == "__main__":
    main()
