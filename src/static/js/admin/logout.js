document.getElementById('logout-btn').addEventListener('click', async (e) => {
            e.preventDefault();
            const response = await fetch('/logout', {
                method: 'POST',
            });
            const data = await response.json();
            if (response.ok) {
                // Handle successful login (e.g., redirect or store tokens)
                console.log('Logged out');
                window.location.replace("/admin/login")
            } else {
                document.getElementById('errorMessage').textContent = data.detail || 'Ошибка';
            }
        });