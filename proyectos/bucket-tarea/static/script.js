document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const loginView = document.getElementById('login-view');
    const dashboardView = document.getElementById('dashboard-view');
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');
    const logoutBtn = document.getElementById('logout-btn');

    const profileTrigger = document.getElementById('profile-trigger');
    const profileImg = document.getElementById('profile-img');
    const fileInput = document.getElementById('file-input');
    const uploadStatus = document.getElementById('upload-status');
    const statusText = document.getElementById('status-text');

    const imageModal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-img');
    const closeModal = document.querySelector('.close-modal');
    const changePhotoBtn = document.getElementById('change-photo-btn');

    // --- State ---
    let token = localStorage.getItem('jwt_token');

    // --- Init ---
    if (token) {
        showDashboard();
        loadSavedProfileImage();
    } else {
        showLogin();
    }

    // --- Load Saved Profile Image ---
    async function loadSavedProfileImage() {
        if (token) {
            try {
                // 1. Get user info (including fileKey)
                const meRes = await fetch('/api/me', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (!meRes.ok) return;
                const { fileKey } = await meRes.json();

                if (fileKey) {
                    // 2. Get Read URL
                    const res = await fetch(`/api/read-url?key=${encodeURIComponent(fileKey)}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });

                    if (res.ok) {
                        const { readUrl } = await res.json();
                        profileImg.src = readUrl;
                    }
                }
            } catch (err) {
                console.error('Failed to load profile image:', err);
            }
        }
    }

    // --- Auth Functions ---
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;

        try {
            const res = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();

            if (res.ok) {
                token = data.token;
                localStorage.setItem('jwt_token', token);
                showDashboard();
                loadSavedProfileImage();
            } else {
                loginError.textContent = data.message || 'Login failed';
            }
        } catch (err) {
            loginError.textContent = 'Network error';
        }
    });

    logoutBtn.addEventListener('click', () => {
        token = null;
        localStorage.removeItem('jwt_token');
        showLogin();
    });

    function showLogin() {
        loginView.classList.remove('hidden');
        setTimeout(() => loginView.classList.add('active'), 10);
        dashboardView.classList.remove('active');
        setTimeout(() => dashboardView.classList.add('hidden'), 300);
    }

    function showDashboard() {
        loginView.classList.remove('active');
        setTimeout(() => loginView.classList.add('hidden'), 300);
        dashboardView.classList.remove('hidden');
        setTimeout(() => dashboardView.classList.add('active'), 10);
    }

    // --- Profile Image Logic ---

    // Open Modal
    profileTrigger.addEventListener('click', () => {
        modalImg.src = profileImg.src;
        imageModal.classList.remove('hidden');
    });

    // Close Modal
    closeModal.addEventListener('click', () => {
        imageModal.classList.add('hidden');
    });

    window.addEventListener('click', (e) => {
        if (e.target === imageModal) {
            imageModal.classList.add('hidden');
        }
    });

    // Trigger File Input from Modal
    changePhotoBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle File Selection & Upload
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Close modal if open
        imageModal.classList.add('hidden');

        // Show loading
        uploadStatus.classList.remove('hidden');
        statusText.textContent = `Uploading ${file.name}...`;

        try {
            // 1. Get Presigned URL
            const urlRes = await fetch('/api/upload-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    filename: file.name,
                    fileType: file.type
                })
            });

            if (!urlRes.ok) throw new Error('Failed to get upload URL');
            const { uploadUrl, fileKey } = await urlRes.json();

            // 2. Upload to S3
            const uploadRes = await fetch(uploadUrl, {
                method: 'PUT',
                headers: { 'Content-Type': file.type },
                body: file
            });

            if (!uploadRes.ok) throw new Error('Failed to upload to S3');

            statusText.textContent = 'Upload complete! Fetching image...';

            // 3. Get Read URL (since bucket is private)
            const readRes = await fetch(`/api/read-url?key=${encodeURIComponent(fileKey)}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!readRes.ok) throw new Error('Failed to get read URL');
            const { readUrl } = await readRes.json();

            // 4. Save profile image key to backend
            const saveRes = await fetch('/api/save-profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ fileKey })
            });

            if (!saveRes.ok) throw new Error('Failed to save profile');

            // 5. Update UI
            profileImg.src = readUrl;
            statusText.textContent = 'Done';
            setTimeout(() => uploadStatus.classList.add('hidden'), 2000);

        } catch (err) {
            console.error(err);
            statusText.textContent = 'Error: ' + err.message;
            statusText.style.color = 'red';
        }
    });
});
