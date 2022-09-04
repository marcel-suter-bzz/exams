/**
 * utility functions
 * @author Marcel Suter
 */

/*
 * shows a info/warn/error-message
 * @param type  message type
 * @param message
 */
function showMessage(type, message) {
    (async () => {
        let exists = false;
        while (!exists) {
            exists = document.readyState === "complete";
            if (!exists)
                await new Promise(resolve => setTimeout(resolve, 100));
        }
        const field = document.getElementById("messages");
        field.className = type;
        field.innerHTML = message;
    })();
}

/**
 * creates an input field element
 * @param name
 * @param type
 * @param value
 * @param size
 */
function makeField(name, type, value, size = 0) {
    let inputField = document.createElement("input");
    inputField.name = name;
    if (type === "integer") {
        inputField.type = "number";
        inputField.step = 1;
    } else {
        inputField.type = type;
    }
    inputField.value = value;
    if (size !== 0) inputField.size = size;

    return inputField;
}

/**
 * locks / unlocks all fields in a form
 * @param formId  the id of the form containing the fields
 * @param locked  true=lock fields
 */
function lockForm(formId, locked = true) {
    const form = document.getElementById(formId);
    const fields = form.querySelectorAll("select,input");
    for (let i=0; i<fields.length; i++) {
        const field = fields[i];
        if (field.tagName === "INPUT") {
            field.readOnly = locked;
        } else if (field.tagName === "SELECT") {
            field.disabled = locked;
        }

    }
}

/**
 * gets the value of the cookie with the specified name
 * Source: https://www.w3schools.com/js/js_cookies.asp
 * @param cname  the name of the cookie
 * @returns {string}
 */
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let cookieArray = decodedCookie.split(';');
    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
}

/**
 * saves the JWToken in SessionStorage
 * @param data  response data
 */
function writeStorage(data) {
    for (let key in data) {
        sessionStorage.setItem(key, data[key]);
    }
}

/**
 * reads the JWToken from SessionStorage
 * @returns {string}
 */
function readStorage(item) {
    return sessionStorage.getItem(item);
}