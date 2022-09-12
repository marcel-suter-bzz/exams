/**
 * view-controller for examlist
 */
const user = readStorage("email");
const role = readStorage("role");
let delayTimer;
let eventList = {};

readEventList(user);
searchExamlist(user);
document.addEventListener("DOMContentLoaded", () => {
    let searchForm = document.getElementById("searchForm");
    /* if (role !== "teacher") {
        searchForm.style.display = "none"; FIXME re-add
        lockForm("editform", true);
    } else {
        lockForm("editform", false);
    } */
    lockForm("editform", false);
    document.getElementById("editform").addEventListener("submit", saveExam);
    document.getElementById("studentSearch").addEventListener("keyup", searchExamlist);
    document.getElementById("teacherSearch").addEventListener("keyup", searchExamlist);
    document.getElementById("dateSearch").addEventListener("change", searchExamlist);
    document.getElementById("statusSearch").addEventListener("change", searchExamlist);
    //document.getElementById("add").addEventListener("click", addPerson);
});

/**
 * search people with delay upon input
 */
function searchExamlist() {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(() => {
        let filter = "";
        let student = document.getElementById("studentSearch").value;
        filter += "student=" + student;
        let teacher = document.getElementById("teacherSearch").value;
        filter += "&teacher=" + teacher;
        let date = document.getElementById("dateSearch").value;
        filter += "&date=" + date;
        let status = "none";
        let open = document.getElementById("open").checked;
        let closed = document.getElementById("closed").checked;
        if (open & closed) status = "all";
        else if (open) status = "open";
        else if (closed) status = "closed";
        filter += "&status=" + status;
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

/**
 * sets the values for input/select
 * @param object  data-object
 * @param parent  form-element
 */
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
    fetch("./exams?" + filter,
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
            exists = document.readyState === "complete" && Object.keys(eventList).length !== 0;
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
            cell.innerHTML = exam.student.firstname + " " + exam.student.lastname;
            cell.innerHTML += "<br />" + exam.student.email;
            cell = row.insertCell(-1);
            cell.innerHTML = exam.cohort;
            cell = row.insertCell(-1);
            cell.innerHTML = exam.teacher.firstname + " " + exam.teacher.lastname;
            cell.innerHTML += "<br />" + exam.teacher.email;
            cell = row.insertCell(-1);
            cell.innerHTML = exam.module + " / " + exam.exam_num;
            cell = row.insertCell(-1);
            cell.innerHTML = exam.duration;
            cell = row.insertCell(-1);
            cell.innerHTML = eventList[exam.event_uuid].datetime;
            cell = row.insertCell(-1);
            cell.innerHTML = exam.status;

        });
        showMessage("clear", "");
    })();
}

/**
 * reads all exams matching a filter
 */
function readEventList() {
    fetch("./events",
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
            setEventList(data);
        })
        .catch(function (error) {
            console.log(error);
        });

}

/**
 * saves the events as an array
 * @param data
 */
function setEventList(data) {
    (async () => {
        let exists = false;
        while (!exists) {
            exists = document.readyState === "complete";
            if (!exists)
                await new Promise(resolve => setTimeout(resolve, 100));
        }

        let dateSearch = document.getElementById("dateSearch");
        let dateEdit = document.getElementById("date");
        let option = document.createElement("option");
        option.value = "";
        option.text = "Alle";
        dateSearch.appendChild(option);
        data.forEach(event => {
            key = event.event_uuid;
            eventList[key] = event;

            option = document.createElement("option");
            option.value = event.event_uuid;
            option.text = event.datetime;
            dateSearch.appendChild(option);
            dateEdit.appendChild(option);
        });
    })();
}

/**
 * saves an exam
 * @param event
 */
function saveExam(event) {
    event.preventDefault();
    const examForm = document.getElementById("editform");
    if (examForm.checkValidity()) {
        const url = "./exam/"; // TODO add uuid
        const fields = ["student_uuid", "module", "exam", "cohort", "duration", "teacher_uuid", "status", "date", "tools", "remarks"];
        for (let field of fields) {
            data.set(field, document.getElementById(field).value);
        }

        fetch(url, {
            method: type,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: data
        })
            .then(function (response) {
                if (!response.ok) {
                    console.log(response); // TODO error handling
                } else return response;
            })
            .then(() => {
                readSheet();
            })
            .catch(function (error) {
                console.log(error);
            });
    }

}