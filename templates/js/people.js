/**
 * view-controller for examlist
 */
let peopleDelay;
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("student.fullname").addEventListener("keyup", searchPeople);
    document.getElementById("student.fullname").addEventListener("change", setPerson);
    document.getElementById("teacher.fullname").addEventListener("keyup", searchPeople);
    document.getElementById("teacher.fullname").addEventListener("change", setPerson);
});

/**
 * search people
 * @param the calling event
 */
function searchPeople(event) {
    clearTimeout(peopleDelay);
    peopleDelay = setTimeout(() => {
        let fieldname = event.target.id;
        let filter = document.getElementById(fieldname).value;
        if (filter.length >= 2) {
            loadPeople(filter, fieldname);
        }
    }, 500);
}

/**
 * loads all people mathicng a filter
 * @param filter
 */
function loadPeople(filter, fieldname) {
    fetch(API_URL + "/people/" + filter,
        {
            headers: {
                "Authorization": "Bearer " + readStorage("token")
            },
        })
        .then(function (response) {
            if (response.ok) {
                return response;
            } else if (response.status === 401) {
                window.location.href = "./";
            } else if (response.status === 404) {
                showMessage("warning", "Keine Daten gefunden");
            } else {
                showMessage("error", "Fehler");
                console.log(response); // TODO error handling
            }
        })
        .then(response => response.json())
        .then(data => {
            setPeopleList(data, fieldname);
        })
        .catch(function (error) {
            console.log(error);
        });
}

/**
 * updates the data list for searching people
 * @param data
 */
function setPeopleList(data, fieldname) {
    let parts = fieldname.split(".");
    let datalist = document.getElementById(parts[0] + ".list");
    datalist.innerHTML = "";
    data.forEach(person => {
        let option = document.createElement("option");
        option.value = person.fullname + " (" + person.email + ")";
        option.setAttribute("data-email", person.email);
        datalist.appendChild(option);
    });
    document.getElementById(fieldname).focus();
}

/**
 * sets the values of the selected person
 * @param the calling event
 */
function setPerson(event) {
    let fieldname = event.target.id;
    let parts = fieldname.split(".");
    let datalist = document.getElementById(parts[0] + ".list");
    let fullname = document.getElementById(fieldname).value;

    for (let i = 0; i < datalist.options.length; i++) {
        let option = datalist.options[i];
        if (option.value == fullname) {
            document.getElementById(parts[0]).value = option.getAttribute("data-email");
        }
    }

}