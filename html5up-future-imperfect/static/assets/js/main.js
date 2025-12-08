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

function login() {
    document.getElementById("loginForm").submit();
}
const urlParams = new URLSearchParams(window.location.search);
    const errorType = urlParams.get('error_type');

    if (errorType) {
        if (errorType === 'username') {
            alert('錯誤的帳號');
        } else if (errorType === 'password') {
            alert('錯誤的密碼');
        }
    }

    function login() {
        document.getElementById('loginForm').submit();
    }
