//==========LikePost=========
document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const icon = this.querySelector('i');
            const postId = this.getAttribute('hx-get').split('/').slice(-2, -1)[0]; // Extract post ID from URL

            // Optimistically toggle the icon
            if (icon.classList.contains('liked')) {
                icon.classList.remove('liked'); // Unmark as liked
            } else {
                icon.classList.add('liked'); // Mark as liked
            }

            // HTMX will still make the request and update the like count
        });
    });
});


// ===========Bookmark=================
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.bookmark-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const url = this.getAttribute('bookmark-url');
            const icon = this.querySelector('i');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text); });
                }
                return response.json();
            })
            .then(data => {
                if (data.saved) {
                    icon.classList.add('saved');
                } else {
                    icon.classList.remove('saved');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

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
});