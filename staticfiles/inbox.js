// // Get the message form element
// const messageForm = document.getElementById('message-form');

// // Only add event listener if the form exists
// if (messageForm) {
//     messageForm.addEventListener('submit', function(e) {
//         e.preventDefault();
        
//         const form = e.target;
//         const formData = new FormData(form);
        
//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === 'success') {
//                 // Add the new message to the message list
//                 const messageList = document.querySelector('.message-list');
//                 const messageDiv = document.createElement('div');
//                 messageDiv.className = 'message sent';
                
//                 const pre = document.createElement('pre');
//                 pre.textContent = data.message.body;
//                 messageDiv.appendChild(pre);
                
//                 const messageTime = document.createElement('div');
//                 messageTime.className = 'message-time';
//                 messageTime.textContent = new Date(data.message.created).toLocaleString();
//                 messageDiv.appendChild(messageTime);
                
//                 messageList.appendChild(messageDiv);
                
//                 // Clear the input
//                 form.reset();
                
//                 // Scroll to bottom
//                 messageList.scrollTop = messageList.scrollHeight;
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     });
// }

// Scroll to the bottom of the message list when the page loads
window.addEventListener('load', function() {
    const messageList = document.querySelector('.message-list');
    if (messageList) {
        messageList.scrollTop = messageList.scrollHeight;
    }
});

document.getElementById('create-group-button').addEventListener('click', function() {
    const modal = document.getElementById('create-group-modal');
    if (modal) {
        modal.style.display = 'block';
    }
});

const closeButtons = document.querySelectorAll('.close');
closeButtons.forEach(button => {
    button.addEventListener('click', function() {
        const modal = this.closest('.modal');
        if (modal) {
            modal.style.display = 'none';
        }
    });
});

window.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (modal && event.target == modal) {
            modal.style.display = 'none';
        }
    });
});

// Image preview functionality
const groupImageInput = document.getElementById('group-image-input');
if (groupImageInput) {
    groupImageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imagePreview = document.getElementById('group-image-preview');
                if (imagePreview) {
                    imagePreview.src = e.target.result;
                }
            }
            reader.readAsDataURL(file);
        }
    });
}

// Add this to your existing script section
document.querySelectorAll('.group-header').forEach(element => {
    element.addEventListener('click', function() {
        const groupDetailsModal = document.getElementById('group-details-modal');
        if (groupDetailsModal) {
            groupDetailsModal.style.display = 'block';
        }
    });
});

// Close button for group details modal
document.querySelectorAll('.modal .close').forEach(element => {
    element.addEventListener('click', function() {
        const modal = this.closest('.modal');
        if (modal) {
            modal.style.display = 'none';
        }
    });
});

// Admin controls
const addParticipantsBtn = document.getElementById('add-participants-btn');
if (addParticipantsBtn) {
    addParticipantsBtn.addEventListener('click', function() {
        const addParticipantsModal = document.getElementById('add-participants-modal');
        if (addParticipantsModal) {
            addParticipantsModal.style.display = 'block';
        }
    });
};

document.querySelectorAll('.make-admin-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const userId = this.dataset.userid;
        const conversationId = this.dataset.conversationid;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        if (confirm('Make this user the new admin?')) {
            fetch(`/inbox/make-admin/${conversationId}/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Failed to make admin');
                }
            }).catch(error => console.error('Error:', error));
        }
    });
});

document.querySelectorAll('.remove-participant-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const userId = this.dataset.userid;
        const conversationId = this.dataset.conversationid;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        if (confirm('Remove this participant?')) {
            fetch(`/inbox/remove-participant/${conversationId}/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Failed to remove participant');
                }
            }).catch(error => console.error('Error:', error));
        }
    });
});

const deleteGroupBtn = document.getElementById('delete-group-btn');
if (deleteGroupBtn) {
    deleteGroupBtn.addEventListener('click', function() {
        const conversationId = this.dataset.conversationid;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        if (confirm('Are you sure you want to delete this group? This action cannot be undone.')) {
            fetch(`/inbox/delete-group/${conversationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => {
                if (response.ok) {
                    window.location.href = '/inbox/';
                } else {
                    console.error('Failed to delete group');
                }
            }).catch(error => console.error('Error:', error));
        }
    });
};

// Add edit group functionality
document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.querySelector('.edit-group-btn');
    const editForm = document.querySelector('.edit-group-form');
    
    if (editButton && editForm) {
        editButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
        });
    }
});

function toggleEditForm() {
    const form = document.getElementById('edit-group-form');
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
}

// Add this to your existing script section
document.querySelectorAll('.world-header').forEach(element => {
    element.addEventListener('click', function() {
        const participantsModal = document.getElementById('participants-modal');
        if (participantsModal) {
            participantsModal.style.display = 'block';
        }
    });
});
