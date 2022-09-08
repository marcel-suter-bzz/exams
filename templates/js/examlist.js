/**
 * view-controller for examlist
 */
let delayTimer;
const user = readStorage("email");
const role = readStorage("role");
readExamlist(user);
document.addEventListener("DOMContentLoaded", () => {
    const search = document.getElementById("searchform");
    search.value = "";
    search.addEventListener("keyup", () => {
        searchExamlist(search.value);
    });

    document.getElementById("nameSearch").value = user;
    if (role !== "teacher") {
        //document.getElementById("searchform").style.display = "none";
        lockForm("editform", true);
    } else {
        lockForm("editform", false);
    }
    //document.getElementById("add").addEventListener("click", addPerson);
});

/**
 * search people with delay upon input
 * @param filter
 */
function searchExamlist(filter) {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(() => {
        readExamlist(filter);
    }, 500);
}

/**
 * event that fires when an exam is selected
 * @param event
 */
function selectExam(event) {
    const button = event.target;
    const uuid = button.getAttribute("data-examUUID");
    readExam(uuid);
}

/**
 * reads a single exam identified by the uuid
 * @param uuid
 */
function readExam(uuid) {
    fetch("./exam/" + uuid,
        {
            headers: {
                "Authorization": "Bearer " + readStorage("token")
            },
        })
        .then(function (response) {
            if (response.ok) {
                return response;
            } else if (response.status === 404) {
                showMessage("warning", "Keine Daten gefunden");
            } else {
                showMessage("error", "Fehler");
                console.log(response); // TODO error handling
            }
        })
        .then(response => response.json())
        .then(data => {
            showExam(data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

/**
 * shows an exam
 * @param exam
 */
function showExam(exam) {
    setValues(exam, "")

}

function setValues(object, parent) {
    for (let property in object) {
        if (typeof object[property] === "object") {
            setValues(object[property], property);

        } else {
            const field = document.getElementById(parent + property);
            if (field !== null) {
                field.value = object[property];
            }
        }
    }
}

/**
 * reads all exams matching a filter
 * @param filter
 */
function readExamlist(filter) {
    fetch("./exams/" + filter,
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
            showExamlist(data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

/**
 * show the examlist in a table
 * @param data
 */
function showExamlist(data) {
    (async () => {
        let exists = false;
        while (!exists) {
            exists = document.readyState === "complete";
            if (!exists)
                await new Promise(resolve => setTimeout(resolve, 100));
        }

        let rows = document.getElementById("examlist")
            .getElementsByTagName("tbody")[0];
        rows.innerHTML = "";
        data.forEach(exam => {
            let row = rows.insertRow(-1);
            let cell = row.insertCell(-1);
            let button = document.createElement("button");
            button.innerHTML = "&#9998;";
            button.type = "button";
            button.name = "editSheet";
            button.setAttribute("data-examUUID", exam.exam_uuid);
            button.addEventListener("click", selectExam);
            cell.appendChild(button);

            cell = row.insertCell(-1);
            cell.className = "col-xs-1";
            cell.innerHTML = exam.student.firstname + " " + exam.student.lastname;
            cell = row.insertCell(-1);
            cell.className = "col-xs-2";
            cell.innerHTML = exam.student.email;
            cell = row.insertCell(-1);
            cell.className = "col-xs-1";
            cell.innerHTML = exam.cohort;
            cell = row.insertCell(-1);
            cell.className = "col-xs-1";
            cell.innerHTML = exam.teacher.email;
            cell = row.insertCell(-1);
            cell.className = "col-xs-2";
            cell.innerHTML = exam.module;
            cell = row.insertCell(-1);
            cell.className = "col-xs-1";
            cell.innerHTML = exam.exam_num;
            cell = row.insertCell(-1);
            cell.className = "col-xs-1";
            cell.innerHTML = exam.duration;
            cell = row.insertCell(-1);
            cell.className = "col-xs-2";
            cell.innerHTML = exam.datetime;
            cell = row.insertCell(-1);
            cell.className = "col-xs-1";
            cell.innerHTML = exam.status;

        });
        showMessage("clear", "");
    })();
}