document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const response = await fetch('/auth', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('errorMessage').style.display = 'none';
                // Handle successful login (e.g., redirect or store tokens)
                console.log('Authenticated successfully');
                window.location.replace("/admin")
            } else {
                document.getElementById('errorMessage').textContent = data.detail || 'Ошибка авторизации';
                document.getElementById('errorMessage').style.display = 'block';
            }
        });
