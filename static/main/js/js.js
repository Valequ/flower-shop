

// бургер
document.addEventListener('DOMContentLoaded', function() {
    const burgerBtn = document.getElementById('burger-btn');
    const navMenu = document.getElementById('nav-menu');

    burgerBtn.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        burgerBtn.classList.toggle('active');
        
        document.body.classList.toggle('no-scroll');
    });

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            burgerBtn.classList.remove('active');
        });
    });
});



// login.html
function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('error-message');
    
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';
    
    if (!username || !password) {
        errorDiv.textContent = 'Заполните все поля';
        errorDiv.style.display = 'block';
        return;
    }
    
    const btn = document.querySelector('.login-form-btn');
    const originalText = btn.textContent;
    btn.textContent = 'Вход...';
    btn.disabled = true;
    
    fetch('/accounts/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            showNotification('Вы вошли в систему', 'success', 1500);
                    setTimeout(function() {
                window.location.href = "/accounts/profile/";
            }, 1500);
        } else {
            errorDiv.textContent = data.error || 'Неверный логин или пароль';
            errorDiv.style.display = 'block';
            btn.textContent = originalText;
            btn.disabled = false;
        }
    })
    .catch(error => {
        errorDiv.textContent = 'Ошибка сети. Попробуйте позже.';
        errorDiv.style.display = 'block';
        btn.textContent = originalText;
        btn.disabled = false;
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    if (passwordField) {
        passwordField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                loginUser();
            }
        });
    }
});



function registerUser() {

    const formData = {
        username: document.getElementById('reg-username').value,
        full_name: document.getElementById('full_name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        password: document.getElementById('reg-password').value,
        agreed_to_terms: document.getElementById('agreed_to_terms').checked,
        agreed_to_offer: document.getElementById('agreed_to_offer').checked,
        agreed_to_privacy: document.getElementById('agreed_to_privacy').checked,
    };
    
    const errorDiv = document.getElementById('reg-error-message');
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';
    

    if (!formData.username || !formData.email || !formData.password) {
        errorDiv.textContent = 'Заполните обязательные поля';
        errorDiv.style.display = 'block';
        return;
    }
    
    const password = document.getElementById('reg-password').value;
    const password2 = document.getElementById('password2').value;
    if (password !== password2) {
        errorDiv.textContent = 'Пароли не совпадают';
        errorDiv.style.display = 'block';
        return;
    }
    
    if (!formData.agreed_to_terms) {
        errorDiv.textContent = 'Необходимо согласие на обработку данных';
        errorDiv.style.display = 'block';
        return;
    }
    

    const btn = document.querySelector('.login-form-btn');
    const originalText = btn.textContent;
    btn.textContent = 'Регистрация...';
    btn.disabled = true;
    

    fetch('/accounts/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            window.location.href = "/accounts/profile/";
        } else {
            let errorText = '';
            
            if (data.errors) {
                for (const field in data.errors) {
                    if (Array.isArray(data.errors[field])) {
                        errorText += data.errors[field].join(', ') + ' ';
                    } else {
                        errorText += data.errors[field] + ' ';
                    }
                }
            } else if (data.message) {
                errorText = data.message;
            } else {
                errorText = 'Ошибка регистрации';
            }
            
            errorDiv.textContent = errorText;
            errorDiv.style.display = 'block';
            btn.textContent = originalText;
            btn.disabled = false;
        }
    })
    .catch(error => {
        errorDiv.textContent = 'Ошибка сети. Попробуйте позже.';
        errorDiv.style.display = 'block';
        btn.textContent = originalText;
        btn.disabled = false;
    });
}


function showNotification(message, type = 'success', duration = 4000) {
    const container = document.getElementById('notification-container');
    const notification = document.getElementById('notification');
    const text = document.getElementById('notification-text');
    const closeBtn = document.querySelector('.notification-close');
    
    notification.className = 'notification ' + type;
    text.textContent = message;
    
    container.style.display = 'block';
    
    notification.classList.remove('hiding');
    
    const closeHandler = function() {
        notification.classList.add('hiding');
        setTimeout(() => {
            container.style.display = 'none';
        }, 300); 
    };
    
    closeBtn.onclick = closeHandler;
    
    let autoCloseTimer = setTimeout(closeHandler, duration);
    
    notification.addEventListener('mouseenter', () => {
        clearTimeout(autoCloseTimer);
    });
    
    notification.addEventListener('mouseleave', () => {
        autoCloseTimer = setTimeout(closeHandler, 1000);
    });
}


function showRegistrationSuccess(message = 'Регистрация успешна! Добро пожаловать в наш магазин цветов!') {
    showNotification(message, 'success', 3000);
}


function showError(message) {
    showNotification(message, 'error', 5000);
}


function showWarning(message) {
    showNotification(message, 'warning', 4000);
}

function requireLogin(productUrl) {
    if (typeof showWarning === 'function') {
        showWarning('Для выбора товара необходимо войти в систему.');
    }
    setTimeout(() => {
        window.location.href = '/accounts/login/?next=' + encodeURIComponent(productUrl);
    }, 1500);
}

function formatApiErrors(data) {
    let errorText = '';
    
    if (data.errors && data.errors.password) {
        if (Array.isArray(data.errors.password)) {
            errorText = 'Ошибка пароля: ' + data.errors.password.join(', ');
        } else {
            errorText = data.errors.password;
        }
    } else if (data.message && data.message !== 'Ошибка регистрации. Проверьте введенные данные.') {
        errorText = data.message;
    } else if (data.errors) {
        const fieldNames = {
            'username': 'Логин',
            'email': 'Email',
            'agreed_to_terms': 'Согласие',
            'phone': 'Телефон',
            'full_name': 'ФИО'
        };
        
        for (const field in data.errors) {
            const fieldName = fieldNames[field] || field;
            
            if (Array.isArray(data.errors[field])) {
                errorText += `${fieldName}: ${data.errors[field].join(', ')} `;
            } else {
                errorText += `${fieldName}: ${data.errors[field]} `;
            }
        }
    }
    
    return errorText || 'Произошла ошибка. Попробуйте еще раз.';
}


function loadUserProfile() {
    
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        window.location.href = "/accounts/login/";
        return;
    }
        
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
    
    fetch('/accounts/api/profile/', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {        
        if (response.status === 401) {
            return refreshTokenForProfile();
        }
        
        if (!response.ok) {
            throw new Error('Ошибка сервера: ' + response.status);
        }
        
        return response.json();
    })
    .then(data => {        
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            loadUserProfile();
            return;
        }
        
        updateProfileUI(data);
        
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Ошибка загрузки профиля:', error);
        
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        
        showError('Не удалось загрузить профиль. ' + error.message);
        
        if (error.message.includes('401') || error.message.includes('токен')) {
            setTimeout(() => {
                window.location.href = "/accounts/login/";
            }, 2000);
        }
    });
}

function refreshTokenForProfile() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
        throw new Error('Нет refresh токена');
    }
    
    return fetch('/accounts/api/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            refresh: refreshToken
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Не удалось обновить токен');
        }
        return response.json();
    })
    .then(data => {
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            return { access: data.access };
        }
        throw new Error('Токен не обновлен');
    });
}


function saveProfile() {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        showError('Требуется авторизация');
        window.location.href = "/accounts/login/";
        return;
    }
    
    const formData = {
        full_name: document.getElementById('edit-full-name').value,
        phone: document.getElementById('edit-phone').value,
        email: document.getElementById('edit-email').value
    };
        
    // Валидация
    if (!formData.full_name || !formData.full_name.trim()) {
        showError('Введите ФИО');
        return;
    }
    
    if (!formData.email || !formData.email.trim()) {
        showError('Введите email');
        return;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
        showError('Введите корректный email адрес');
        return;
    }
    
    const btn = document.querySelector('.btn-primary');
    const originalText = btn.textContent;
    btn.textContent = 'Сохранение...';
    btn.disabled = true;
    
    fetch('/accounts/api/profile/update/', {
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {        
        if (response.status === 401) {
            return refreshTokenForProfile()
                .then(newToken => {
                    return fetch('/accounts/api/profile/update/', {
                        method: 'PUT',
                        headers: {
                            'Authorization': 'Bearer ' + newToken,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                });
        }
        
        if (response.status === 404) {
            throw new Error('Сервер не найден (404). Проверьте URL.');
        }
        
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(`Ошибка сервера: ${response.status} - ${JSON.stringify(errorData)}`);
            });
        }
        
        return response.json();
    })
    .then(data => {        
        if (data.success) {
            showNotification('Профиль успешно обновлен!', 'success');
            
            const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
            const updatedUser = { ...currentUser, ...formData };
            localStorage.setItem('user', JSON.stringify(updatedUser));
            
            updateProfileUI(data.user || updatedUser);
            
            setTimeout(() => {
                window.location.href = "/accounts/profile/";
            }, 1500);
        } else {
            if (data.errors) {
                let errorText = '';
                for (const field in data.errors) {
                    if (Array.isArray(data.errors[field])) {
                        errorText += data.errors[field].join(', ') + ' ';
                    } else {
                        errorText += data.errors[field] + ' ';
                    }
                }
                showError(errorText || 'Ошибка сохранения');
            } else {
                showError(data.message || 'Ошибка сохранения');
            }
            btn.textContent = originalText;
            btn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Ошибка сохранения:', error);
        showError('Ошибка сети: ' + error.message);
        btn.textContent = originalText;
        btn.disabled = false;
    });
}

function logout() {
    const token = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (token && refreshToken) {
        fetch('/accounts/api/logout/', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        })
        .catch(error => {
        });
    }
    
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    fetch('/accounts/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.redirected) {
            showNotification('Вы вышли из системы', 'warning');
            setTimeout(() => {
                window.location.href = "/accounts/login/";
            }, 1500);
        } else {
            window.location.href = "/accounts/login/";
        }
    })
    .catch(error => {
        window.location.href = "/accounts/login/";
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', function() {    
    if (window.location.pathname.includes('/profile')) {        
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = "/accounts/login/";
            return;
        }
        
        loadUserProfile();
    }
    
    const logoutBtn = document.querySelector('.logout-text');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
    
    const avatarInput = document.getElementById('avatar-input');
    if (avatarInput) {
        avatarInput.addEventListener('change', function(e) {
            handleAvatarUpload(e);
        });
    }
});
function displayStoredUserData() {
    const userData = localStorage.getItem('user');
    
    if (userData) {
        try {
            const user = JSON.parse(userData);
            
            const editUsername = document.getElementById('edit-username');
            const editFullName = document.getElementById('edit-full-name');
            const editPhone = document.getElementById('edit-phone');
            const editEmail = document.getElementById('edit-email');
            
            if (editUsername && user.username) editUsername.value = user.username;
            if (editFullName && user.full_name) editFullName.value = user.full_name;
            if (editPhone && user.phone) editPhone.value = user.phone;
            if (editEmail && user.email) editEmail.value = user.email;
            
            const fullNameElement = document.getElementById('user-full-name');
            const phoneElement = document.getElementById('user-phone');
            const emailElement = document.getElementById('user-email');
            
            if (fullNameElement && user.full_name) fullNameElement.textContent = user.full_name;
            if (phoneElement && user.phone) phoneElement.textContent = user.phone;
            if (emailElement && user.email) emailElement.textContent = user.email;
            
        } catch (error) {
        }
    }
}

function updateProfileUI(userData) {    
    const fullNameElement = document.getElementById('user-full-name');
    const phoneElement = document.getElementById('user-phone');
    const emailElement = document.getElementById('user-email');
    const profileAvatar = document.getElementById('profile-avatar');
    
    if (fullNameElement) {
        fullNameElement.textContent = userData.full_name || userData.fullName || 'Не указано';
    }
    if (phoneElement) {
        phoneElement.textContent = userData.phone || 'Не указано';
    }
    if (emailElement) {
        emailElement.textContent = userData.email || 'Не указано';
    }
    if (profileAvatar && userData.avatar_url) {
        profileAvatar.src = userData.avatar_url;
    }
    
    const editUsername = document.getElementById('edit-username');
    const editFullName = document.getElementById('edit-full-name');
    const editPhone = document.getElementById('edit-phone');
    const editEmail = document.getElementById('edit-email');
    const editAvatar = document.getElementById('current-avatar');
    
    if (editUsername) {
        editUsername.value = userData.username || '';
    }
    if (editFullName) {
        editFullName.value = userData.full_name || userData.fullName || '';
    }
    if (editPhone) {
        editPhone.value = userData.phone || '';
    }
    if (editEmail) {
        editEmail.value = userData.email || '';
    }
    if (editAvatar && userData.avatar_url) {
        editAvatar.src = userData.avatar_url;
    }
    
    localStorage.setItem('user', JSON.stringify(userData));
}

document.addEventListener('DOMContentLoaded', function() {
    displayStoredUserData();
    
    if (window.location.pathname.includes('/profile')) {
        const token = localStorage.getItem('access_token');
        if (token) {
            loadUserProfile();
        }
    }
});

let selectedAvatarFile = null;

function handleAvatarSelect(event) {
    const file = event.target.files[0];
    selectedAvatarFile = file;
    
    if (file) {
        document.getElementById('file-name').textContent = file.name;
        
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('current-avatar').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}






