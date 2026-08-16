const signupForm = document.getElementById('signupForm');

if (signupForm) {
    signupForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const fullName = document.getElementById('signupName').value.trim();
        const parts = fullName.split(/\s+/);
        const name = parts.shift() || '';
        const surname = parts.join(' ') || 'User';
        const role = document.querySelector('input[name="role"]:checked')?.value || 'user';

        try {
            await api('/users', {
                method: 'POST',
                body: JSON.stringify({
                    name,
                    surname,
                    email: document.getElementById('signupEmail').value.trim(),
                    phone: document.getElementById('signupPhone').value.trim(),
                    password: document.getElementById('signupPassword').value,
                    location: document.getElementById('signupLocation')?.value.trim() || '',
                    role
                })
            });
            alert('Account created successfully. Please log in.');
            window.location.href = 'login.html';
        } catch (error) {
            alert(error.message);
        }
    });
}

const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;
        const role = document.getElementById('loginRole')?.value || 'user';

        try {
            const user = await api('/login', {
                method: 'POST',
                body: JSON.stringify({ email, password, role })
            });
            saveSession(user);
            window.location.href = user.role === 'provider'
                ? 'service-provider.html'
                : 'service-user.html';
        } catch (error) {
            alert(error.message);
        }
    });
}