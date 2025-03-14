//SIDEBAR
const menuItems = document.querySelectorAll('.menu-item');

//MESSAGES
// const messagesNotification = document.querySelector('#messages-notification');
// const messages = document.querySelector('.messages');
// const message = messages.querySelectorAll('.message');
// const messageSearch = document.querySelector('#message-search');

//THEME
const theme  = document.querySelector('#theme');
const themeModel = document.querySelector('.customize-theme');
const fontSizes = document.querySelectorAll('.choose-size span');
var root = document.querySelector(':root');
const colorPlatte = document.querySelectorAll('.choose-color span');
const Bg1 = document.querySelector('.bg-1');
const Bg2 = document.querySelector('.bg-2');
const Bg3 = document.querySelector('.bg-3');
let primaryHue = 252;
//theme background values
let lightColorLightness;
let whiteColorLightness;
let darkColorLightness;

// ===============SIDEBAR =================//

//remove active class from all menu item
const changeActiveItem = () =>{
    menuItems.forEach(item =>{
        item.classList.remove('active');
    })
}

menuItems.forEach(item =>{
    item.addEventListener('click',() =>{
        changeActiveItem();
        item.classList.add('active');
        if(item.id != 'notifications'){
            document.querySelector('.notification-popup').
            style.display ='none';
        } else{
            document.querySelector('.notification-popup').
            style.display ='block';
            document.querySelector('#notifications .notification-count').
            style.display = 'none';
        }
    })
})

// ===============MESSAGES =================//
//searches chats
// const searchMessage = () => {
//     const val = messageSearch.value.toLowerCase();

//     message.forEach(chat => {
//         const header = chat.querySelector('h5');
        
//         if (header) {
//             const name = header.textContent.toLowerCase();
//             if (name.indexOf(val) !== -1) {
//                 chat.style.display = 'flex';
//             } else {
//                 chat.style.display = 'none';
//             }
//         } else {
//             chat.style.display = 'none'; // Hide chat if <h5> is not found
//         }
//     });
// }

// //search chat
// messageSearch.addEventListener('keyup',searchMessage);

//highlight message box when message icon is clicked
// messagesNotification.addEventListener('click',() =>{
//     messages.style.boxShadow = '0 0 1rem var(--color-primary)';
//     messagesNotification.querySelector('.notification-count').style.display = "none";
//     setTimeout(() => {
//         messages.style.boxShadow = "none";
//     },2000);
// })


// Function to save settings to localStorage
const saveSettings = (fontSize, primaryHue, background) => {
    const settings = {
        fontSize,
        primaryHue,
        background: {
            lightColorLightness,
            whiteColorLightness,
            darkColorLightness
        }
    };
    localStorage.setItem('themeSettings', JSON.stringify(settings));
};

// Function to load settings from localStorage
const loadSettings = () => {
    const settings = localStorage.getItem('themeSettings');
    if (settings) {
        return JSON.parse(settings);
    }
    return null;
};


//THEME CUSTOMIZATION

//opens modal
const openThemeModel = () =>{
    themeModel.style.display = 'grid';
}

//close modal
const closeThemeModel = (e) =>{
    if(e.target.classList.contains('customize-theme')){
        themeModel.style.display = 'none';
    }
}

themeModel.addEventListener('click',closeThemeModel);

theme.addEventListener('click',openThemeModel);

//edit pop up 
document.addEventListener('DOMContentLoaded', function() {
    // Function to close all popups
    function closeAllPopups() {
        document.querySelectorAll('.control-popup').forEach(popup => {
            popup.style.display = 'none';
        });
    }

    // Function to handle popup toggle
    function togglePopup(button) {
        const popup = button.nextElementSibling;
        const isVisible = popup.style.display === 'grid';
        
        // Close all popups first
        closeAllPopups();
        
        // If this popup wasn't visible, show it
        if (!isVisible) {
            popup.style.display = 'grid';
        }
    }

    // Delegate click events to handle dynamically loaded content
    document.body.addEventListener('click', function(e) {
        // Handle popup trigger clicks
        if (e.target.closest('.popup-trigger')) {
            e.preventDefault();
            e.stopPropagation();
            const button = e.target.closest('.popup-trigger');
            togglePopup(button);
        }
        // Handle clicks outside popups
        else if (!e.target.closest('.control-popup .card'))  {
            closeAllPopups();
                 }
    });
});


 // ==============FONTS=========================

  //remove active class from spans or font size selectors
const removeSizeSelector = () =>{
    fontSizes.forEach(size =>{
        size.classList.remove('active');
    })
}

fontSizes.forEach(size =>{
    size.addEventListener('click',() =>{
    removeSizeSelector();
    let fontSize;
    size.classList.toggle('active');

    if(size.classList.contains('font-size-1')){
        fontSize = '10px';
        root.style.setProperty('----sticky-top-left','5.4rem');
        root.style.setProperty('----sticky-top-right','5.4rem');
    }else if (size.classList.contains('font-size-2')){
        fontSize = '13px';
        root.style.setProperty('----sticky-top-left','5.4rem');
        root.style.setProperty('----sticky-top-right','-7rem');
    }else if (size.classList.contains('font-size-3')){
        fontSize = '16px';
        root.style.setProperty('----sticky-top-left','-2rem');
        root.style.setProperty('----sticky-top-right','-17rem');
    }else if (size.classList.contains('font-size-4')){
        fontSize = '19px';
        root.style.setProperty('----sticky-top-left','-5rem');
        root.style.setProperty('----sticky-top-right','-25rem');
    }else if (size.classList.contains('font-size-5')){
        fontSize = '22px';
        root.style.setProperty('----sticky-top-left','-12rem');
        root.style.setProperty('----sticky-top-right','-35rem');
    }

    //change font size of the root html element
    document.querySelector('html').style.fontSize = fontSize;
    saveSettings(fontSize, primaryHue, {
        lightColorLightness,
        whiteColorLightness,
        darkColorLightness
    });
   })
})

//remove active class from colors
const changeActiveColorClass = () => {
    colorPlatte.forEach(colorPlatte => {
        colorPlatte.classList.remove('active');
    })
}

//change primary colors
colorPlatte.forEach(color =>{
    color.addEventListener('click',() => {
        let primary;
        //remove active class from colors
        changeActiveColorClass();

        if(color.classList.contains('color-1')){
            primaryHue = 252;
        } else if(color.classList.contains('color-2')){
            primaryHue = 352;
        }else if(color.classList.contains('color-3')){
            primaryHue = 152;
        }else if(color.classList.contains('color-4')){
            primaryHue = 52;
        }else if(color.classList.contains('color-5')){
            primaryHue = 202;
        }
        color.classList.add('active');

        root.style.setProperty('--primary-color-hue',primaryHue);
        saveSettings(document.querySelector('html').style.fontSize, primaryHue, {
            lightColorLightness,
            whiteColorLightness,
            darkColorLightness
        });
    })
})


//change background color
const changeBG = () =>{
    root.style.setProperty('--light-color-lightness',lightColorLightness);
    root.style.setProperty('--white-color-lightness',whiteColorLightness);
    root.style.setProperty('--dark-color-lightness',darkColorLightness);
}

Bg1.addEventListener('click',() =>{
    //add active class
    Bg1.classList.add('active');
    //remove active class from the others
    Bg2.classList.remove('active');
    Bg3.classList.remove('active');

    lightColorLightness = '95%';
    whiteColorLightness = '100%';
    darkColorLightness = '17%';
    
    changeBG();
    saveSettings(document.querySelector('html').style.fontSize, primaryHue, {
        lightColorLightness,
        whiteColorLightness,
        darkColorLightness
    });
})

Bg2.addEventListener('click',() =>{
    darkColorLightness = '95%';
    whiteColorLightness = '20%';
    lightColorLightness = '15%';

    //add active class
    Bg2.classList.add('active');
    //remove active class from the others
    Bg1.classList.remove('active');
    Bg3.classList.remove('active');
    changeBG();
    saveSettings(document.querySelector('html').style.fontSize, primaryHue, {
        lightColorLightness,
        whiteColorLightness,
        darkColorLightness
    });
})

Bg3.addEventListener('click',() =>{
    darkColorLightness = '95%';
    whiteColorLightness = '10%';
    lightColorLightness = '0%';

    //add active class
    Bg3.classList.add('active');
    //remove active class from the others
    Bg1.classList.remove('active');
    Bg2.classList.remove('active');
    changeBG();
    saveSettings(document.querySelector('html').style.fontSize, primaryHue, {
        lightColorLightness,
        whiteColorLightness,
        darkColorLightness
    });
});


// Apply saved settings on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedSettings = loadSettings();
    if (savedSettings) {
        // Apply font size
        document.querySelector('html').style.fontSize = savedSettings.fontSize;
        
        // Apply color
        root.style.setProperty('--primary-color-hue', savedSettings.primaryHue);
        
        // Apply background
        lightColorLightness = savedSettings.background.lightColorLightness;
        whiteColorLightness = savedSettings.background.whiteColorLightness;
        darkColorLightness = savedSettings.background.darkColorLightness;
        changeBG();
        
        // Set active classes
        fontSizes.forEach(size => {
            if (size.dataset.size === savedSettings.fontSize) {
                removeSizeSelector();
                size.classList.add('active');
            }
        });
        
        colorPlatte.forEach(color => {
            if (color.dataset.hue === savedSettings.primaryHue.toString()) {
                changeActiveColorClass();
                color.classList.add('active');
            }
        });
        
        // Set active background
        if (lightColorLightness === '95%') {
            Bg1.classList.add('active');
        } else if (whiteColorLightness === '20%') {
            Bg2.classList.add('active');
        } else {
            Bg3.classList.add('active');
        }
    }
});