document.addEventListener('DOMContentLoaded', () => {
    const addButton = document.getElementById('addPostButton');
    const postModal = document.getElementById('postModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const newPostForm = document.getElementById('newPostForm');
    if (addButton) {
        addButton.addEventListener('click', () => {
            postModal.style.display = 'block';
        });
    }
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            postModal.style.display = 'none';
        });
    }
    window.addEventListener('click', (event) => {
        if (event.target === postModal) {
            postModal.style.display = 'none';
        }
    });
    if (newPostForm) {
        newPostForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const postData = {
                title: document.getElementById('postTitle').value,
                content: document.getElementById('postContent').value,
                category: document.getElementById('postCategory').value,
            };

            try {
                const response = await fetch('/posts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(postData)
                });
                const result = await response.json();
                if (response.ok) {
                    alert(`文章發佈成功`);
                    postModal.style.display = 'none';
                    newPostForm.reset();
                    window.location.reload(); 
                } else {
                    alert(`發佈失敗: ${result.message}`);
                }
            } catch (error) {
                console.error('API 請求出錯:', error);
                alert('發佈文章時發生網路錯誤，請檢查連線。');
            }
        });
    }
});

//====================================================================
// login
//====================================================================


    document.addEventListener('DOMContentLoaded', () => {
    const loginRegisterBtn = document.getElementById('loginRegisterBtn');
    const authModal = document.getElementById('authModal');
    const closeAuthModalBtn = document.getElementById('closeAuthModalBtn');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    if (loginRegisterBtn && authModal) {
        loginRegisterBtn.addEventListener('click', (e) => {
            e.preventDefault();
            authModal.style.display = 'block';
            if (loginForm && registerForm) {
                loginForm.style.display = 'block';
                registerForm.style.display = 'none';
            }
        });
    }
    if (closeAuthModalBtn && authModal) {
        closeAuthModalBtn.addEventListener('click', () => {
            authModal.style.display = 'none';
        });
    }
    window.addEventListener('click', (event) => {
        if (event.target === authModal) {
            authModal.style.display = 'none';
        }
    });
    if (showRegisterLink && loginForm && registerForm) {
        showRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.style.display = 'none';
            registerForm.style.display = 'block';
        });
    }
    if (showLoginLink && loginForm && registerForm) {
        showLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            registerForm.style.display = 'none';
            loginForm.style.display = 'block';
        });
    }
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const loginData = {
                username: document.getElementById('loginUsername').value,
                password: document.getElementById('loginPassword').value,
            };

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(loginData),
                });

                const result = await response.json();

                if (response.ok) {
                    alert(`登入成功！歡迎您，${result.username}`);
                    authModal.style.display = 'none';
                    window.location.reload();
                } else {
                    alert(`登入失敗: ${result.message}`);
                }
            } catch (error) {
                console.error('登入時發生錯誤:', error);
                alert('連線錯誤，無法登入。');
            }
        });
    }
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const registerData = {
                username: document.getElementById('regUsername').value,
                email: document.getElementById('regEmail').value,
                password: document.getElementById('regPassword').value,
            };
            if (!registerData.email.endsWith("@gmail.com")) {
                 alert("Email 格式不符，必須是 @gmail.com 結尾。");
                 return;
            }
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(registerData),
                });

                const result = await response.json();

                if (response.ok) {
                    alert(`註冊成功！您已自動登入。`);
                    authModal.style.display = 'none';
                    window.location.reload();
                } else {
                    alert(`註冊失敗: ${result.message}`);
                }
            } catch (error) {
                console.error('註冊時發生錯誤:', error);
                alert('連線錯誤，無法完成註冊。');
            }
        });
    }
});