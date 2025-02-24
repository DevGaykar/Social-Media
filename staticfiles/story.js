// First declare all variables and get DOM elements

const modal = document.getElementById("storyModal"); 
const addStoryIcon = document.querySelector(".add-story-icon");
const closeBtn = document.querySelector(".close");
const contentInput = document.getElementById('content');
const storyForm = document.getElementById("storyForm");
  
  
  // Function to cleanup previews
  function cleanupPreviews() {
      const imagePreview = document.getElementById('image-preview');
      const videoPreview = document.getElementById('video-preview');
      
      if (imagePreview.src) URL.revokeObjectURL(imagePreview.src);
      if (videoPreview.src) URL.revokeObjectURL(videoPreview.src);
      
      imagePreview.src = '';
      videoPreview.src = '';
      
      document.getElementById('preview-container').style.display = 'none';
  }
  
  // Modal event listeners
  addStoryIcon.addEventListener('click', function() {
      modal.style.display = "block";
  });
  
  closeBtn.addEventListener('click', function() {
      modal.style.display = "none";
      cleanupPreviews();
  });
  
  window.addEventListener('click', function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
          cleanupPreviews();
      }
  });
  
  // File input change handler
  contentInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (!file) return;
  
      const previewContainer = document.getElementById('preview-container');
      const imagePreview = document.getElementById('image-preview');
      const videoPreview = document.getElementById('video-preview');
  
      // Reset previews
      imagePreview.style.display = 'none';
      videoPreview.style.display = 'none';
      previewContainer.style.display = 'none';
  
      // Create object URL
      const objectUrl = URL.createObjectURL(file);
  
      if (file.type.startsWith('image/')) {
          // Handle image preview
          imagePreview.onload = function() {
              URL.revokeObjectURL(objectUrl);
          }
          imagePreview.src = objectUrl;
          imagePreview.style.display = 'block';
          previewContainer.style.display = 'block';
      } else if (file.type.startsWith('video/')) {
          // Handle video preview
          videoPreview.src = objectUrl;
          videoPreview.style.display = 'block';
          previewContainer.style.display = 'block';
  
          videoPreview.onload = function() {
              URL.revokeObjectURL(objectUrl);
          }
      }
  });
  
  // Form submission handler
  storyForm.addEventListener("submit", function(e) {
      e.preventDefault();
      const url = this.dataset.url;
      const formData = new FormData(this);
      
      fetch(url, {
          method: "POST",
          body: formData,
          credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
          if(data.success) {
              modal.style.display = "none";
              cleanupPreviews();
              window.location.reload();
          } else {
              alert(data.message || 'Error adding story');
          }
      })
      .catch(error => {
          console.error('Error:', error);
          alert('Error adding story');
      });
  });
  
      
// Add these functions before the Zuck initialization
document.addEventListener('DOMContentLoaded', function() {
try {
// Make sure we have stories data
if (Array.isArray(storiesData) && storiesData.length > 0) {
    console.log('Initializing Zuck with stories:', storiesData);
    
    let storiesTimeline = new Zuck('stories', {
        skin: 'snapgram',
        avatars: true,
        stories: storiesData,
        backNative: true,
        previousTap: true,
        backButton: true,
        openEffect: true,
        cubeEffect: false, 
        autoFullScreen: false,
        fullScreen: false,
        list: false, 
        callbacks: {
            onView: function(storyId) {
                console.log('Viewing story:', storyId);
            },
            onOpen: function(storyId, callback) {
                console.log('Story opened:', storyId);
                const storyContent = document.querySelector('.story-viewer .media');
                if (storyContent) {
                    storyContent.style.objectFit = 'contain';
                }
                
                callback();
            },
            onClose: function(storyId, callback) {
                document.documentElement.style.overflow = '';
                callback();
            },
            onNavigateItem: function(storyId, nextStoryId) {
                console.log('Navigating from story:', storyId, 'to:', nextStoryId);
            }
        },
        language: {
            unmute: 'Touch to unmute',
            keyboardTip: 'Press space to see next',
            visitLink: 'Visit link',
            time: {
                ago: 'ago',
                hour: 'hour',
                hours: 'hours',
                minute: 'minute',
                minutes: 'minutes',
                fromnow: 'from now',
                seconds: 'seconds',
                yesterday: 'yesterday',
                tomorrow: 'tomorrow',
                days: 'days'
            }
        }
    });
    
    console.log('Zuck initialized successfully');
} else {
}
} catch (error) {
console.error('Error initializing stories:', error);
console.error('Error details:', error.message);
}
});
