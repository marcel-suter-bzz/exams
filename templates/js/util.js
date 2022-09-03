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