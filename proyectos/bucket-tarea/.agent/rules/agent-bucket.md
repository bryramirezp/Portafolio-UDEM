---
trigger: always_on
---

# ROLE
Act as a Senior Full-Stack Python Developer and AWS Cloud Architect. You have deep expertise in Flask (backend), Vanilla JavaScript/HTML/CSS (frontend), and the AWS Boto3 SDK.

# TASK
Create a functional, secure, and modular web application using Flask that acts as a "Simple S3 File Manager". The application must allow users to upload files to an AWS S3 bucket and view a list of uploaded files.

# TECHNICAL REQUIREMENTS
1.  **Backend (Flask & Python):**
    * Use `Flask` for the web server.
    * Use `boto3` to interact with AWS S3.
    * Implement two routes:
        * `GET /`: Renders the frontend and lists existing files from the bucket.
        * `POST /upload`: Handles file uploads from the frontend to S3.
    * **Security:** Do NOT hardcode AWS credentials. Use `python-dotenv` to load `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `BUCKET_NAME` from a `.env` file.

2.  **Frontend (HTML/CSS/JS):**
    * **HTML5:** Semantic structure. Create a clean interface with an upload form and a file list (grid or table).
    * **CSS3:** Modern styling (Flexbox/Grid), responsive design. No external frameworks (Bootstrap/Tailwind) allowed.
    * **JavaScript (Vanilla):** Handle the form submission via AJAX (fetch API) to prevent page reloads during upload and dynamically update the file list upon success.

# FILE STRUCTURE & OUTPUT
Please provide the complete code for the following files:
1.  `requirements.txt` (List of python dependencies).
2.  `.env.example` (Template for environment variables).
3.  `app.py` (Main Flask application logic).
4.  `templates/index.html` (The UI markup).
5.  `static/style.css` (Styling).
6.  `static/script.js` (Frontend logic).

# CONSTRAINTS
* Ensure code is error-free and commented.
* Handle basic errors (e.g., no file selected).