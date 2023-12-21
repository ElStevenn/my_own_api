console.log("Hello world!");
let origin_language;
let text_to_translate;
let left_buttons;
let right_buttons;

function setCookie(name, value, daysToExpire) {
    var expires = "";
    if (daysToExpire) {
        var date = new Date();
        date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function isCookieSet(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return true;
    }
    return false;
}

function get_actual_language() {
    // Check if cookies are set
    if (!isCookieSet("origin_language") || !isCookieSet("text_to_translate")) {
        console.log("Cookies not set, setting default values...");
        origin_language = "english";
        text_to_translate = "spanish";
    } else {
        console.log("Cookies found, retrieving values...");
        origin_language = getCookie("origin_language");
        text_to_translate = getCookie("text_to_translate");
    }

    console.log("Origin Language:", origin_language, "Text to Translate:", text_to_translate);

    // Set red buttons after ensuring the buttons are built
    setButtonStylesAfterRender();
}


function setButtonStylesAfterRender() {
    // Wait until the call stack is clear to ensure DOM elements are rendered
    setTimeout(function() {
        console.log("Setting button styles...");
        setButtonStyle(`original_${origin_language}`, "#FF0000");
        setButtonStyle(`to_${text_to_translate}`, "#FF0000");
    }, 0);
}

function setButtonStyle(buttonId, style) {
    if (buttonId == 'original_english'){
        document.getElementById('original_english').style = `color:${style};`;        
        return;
    }else if (buttonId == 'original_spanish'){
        document.getElementById('original_spanish').style = `color:${style};`;        
        return;
    }else if(buttonId == 'to_english') {
        document.getElementById('to_english').style = `color:${style};`;
        return;
    }else if (buttonId == 'to_spanish') {
        document.getElementById('to_spanish').style = `color:${style};`;        
        return;
    } else if(buttonId == 'original_french'){
        document.getElementById('original_french').style = `color:${style};`;        
        return;
    }
    else if(buttonId == 'original_catalan'){
        document.getElementById('original_catalan').style = `color:${style};`;        
        return;
    }
    else if(buttonId == 'original_german'){
        document.getElementById('original_german').style = `color:${style};`;        
        return;
    }
    else if(buttonId == 'original_korean'){
        document.getElementById('original_korean').style = `color:${style};`;        
        return;
    }
    else if(buttonId == 'to_french'){
        document.getElementById('to_french').style = `color:${style};`;        
        return;
    }
    else if(buttonId == 'to_catalan'){
        document.getElementById('to_catalan').style = `color:${style};`;        
        return;
    }
    else if(buttonId == 'to_german'){
        document.getElementById('to_german').style = `color:${style};`;        
        return;
    }
    else if(buttonId == 'to_korean'){
        document.getElementById('to_korean').style = `color:${style};`;        
        return;
    }
}

function build_buttons() {
    let body_left = document.getElementById("left_trans_buttons");
    let body_right = document.getElementById("right_trans_buttons");

    let buttons_left = 
        `<a href="#" class="original-button"  onclick="left_button('english')" id="original_english">English</a>` +
        `<a href="#" class="original-button"  onclick="left_button('spanish')" id="original_spanish">Spanish</a>` +
        `<a href="#" class="original-button"  onclick="left_button('french')" id="original_french">French</a>`+
        `<a href="#" class="original-button"  onclick="left_button('catalan')" id="original_catalan">Catalan</a>`+
        `<a href="#" class="original-button"  onclick="left_button('german')" id="original_german">German</a>`+
        `<a href="#" class="original-button"  onclick="left_button('korean')" id="original_korean">Korean</a>`;

    let buttons_right = 
        `<a href="#" class="original-button" onclick="right_button('english')" id="to_english">English</a>` +
        `<a href="#" class="original-button" onclick="right_button('spanish')" id="to_spanish">Spanish</a>` +
        `<a href="#" class="original-button" onclick="right_button('french')" id="to_french">French</a>` +
        `<a href="#" class="original-button" onclick="right_button('catalan')" id="to_catalan">Catalan</a>` +
        `<a href="#" class="original-button" onclick="right_button('german')" id="to_german">German</a>`+
        `<a href="#" class="original-button" onclick="right_button('korean')" id="to_korean">Korean</a>`;

    body_left.innerHTML = buttons_left;
    body_right.innerHTML = buttons_right;
}


document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");
    build_buttons();  // Build buttons
    get_actual_language();  // Then set languages and styles
});


function switch_languages(){
    var new_text_to_translate = "";
    var new_origint_text = "";
}

function left_button(language) {
    var element = document.getElementById(`original_${language}`);

    // Check if the current button is already active
    if (element.style.color === "rgb(255, 0, 0)") {
        console.log("This button is red, nothing to do");
    } else {
        // Update the style of the previously active language button
        if (origin_language) {
            setButtonStyle(`original_${origin_language}`, "#7928CA"); // Previous language set to purple
        }

        // Update the style of the newly selected language button
        setButtonStyle(`original_${language}`, "#FF0000"); // New language set to red

        // Update the origin language and its cookie
        origin_language = language;
        setCookie("origin_language", origin_language, 90);
        console.log(`The origin language has been changed to ${origin_language}`);
    }
}

function right_button(language) {
    var element = document.getElementById(`to_${language}`);

    // Check if the current button is already active
    if (element.style.color === "rgb(255, 0, 0)") {
        console.log("This button is red, nothing to do");
    } else {
        // Update the style of the previously active target language button
        if (text_to_translate) {
            setButtonStyle(`to_${text_to_translate}`, "#7928CA"); // Previous language set to purple
        }

        // Update the style of the newly selected target language button
        setButtonStyle(`to_${language}`, "#FF0000"); // New language set to red

        // Update the target language and its cookie
        text_to_translate = language;
        setCookie("text_to_translate", text_to_translate, 90);
        console.log(`The target language has been changed to ${text_to_translate}`);
    }
}

function connectWebSocket() {
    const ws = new WebSocket('wss://paumateu.com/ws_endpoint_translate');

    ws.onopen = () => {
        console.log('WebSocket Connected');
    };

    ws.onmessage = (event) => {
        const response = JSON.parse(event.data);
        if (response.translated_text) {
            // Remove the quotation marks before setting the value
            const translatedTextWithoutQuotes = response.translated_text.replace(/^"|"$/g, '');
            document.getElementById('text_translated_text_area').value = translatedTextWithoutQuotes;
        } else if (response.error) {
            console.error('Error:', response.error);
        }
    };
    

    ws.onerror = (error) => {
        console.error('WebSocket Error:', error);
    };

    ws.onclose = (event) => {
        console.log('WebSocket Disconnected:', event.reason);
    };

    return ws;
}

const wsConnection = connectWebSocket();

// Event listener for text area
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('texto_to_translate_text_area').addEventListener('change', (event) => {
        const textToTranslate = event.target.value;
        const data = {
            text_to_translate: textToTranslate,
            origin_language: origin_language,  
            language_to_translate: text_to_translate  
        };

        if (wsConnection.readyState === WebSocket.OPEN) {
            wsConnection.send(JSON.stringify(data));
        } else {
            console.error('WebSocket is not connected');
        }
    });
});

// TextArea config
document.addEventListener('input', function(event) {
    if (event.target.tagName.toLowerCase() === 'textarea') {
        autoExpand(event.target);
    }
});

function autoExpand(field) {
    // Reset field height
    field.style.height = 'inherit';

    // Get the computed styles for the element
    var computed = window.getComputedStyle(field);

    // Calculate the height
    var height = field.scrollHeight;
    var borderTop = parseInt(computed.getPropertyValue('border-top-width'), 10);
    var borderBottom = parseInt(computed.getPropertyValue('border-bottom-width'), 10);
    var paddingTop = parseInt(computed.getPropertyValue('padding-top'), 10);
    var paddingBottom = parseInt(computed.getPropertyValue('padding-bottom'), 10);
    var maxHeight = 500; // maximum height the textarea can expand to (in pixels)

    height = borderTop + paddingTop + height + paddingBottom + borderBottom;

    if (height > maxHeight) {
        height = maxHeight;
        field.style.overflowY = 'auto'; // Add scrollbar if the content is too long
    } else {
        field.style.overflowY = 'hidden'; // Hide scrollbar for content that fits within the max height
    }

    field.style.height = height + 'px';
}
