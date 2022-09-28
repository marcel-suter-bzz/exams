/**
 * view-controller for examlist
 */
let delayTimer;

searchExamlist(user);
document.addEventListener("DOMContentLoaded", () => {
    let searchForm = document.getElementById("searchForm");
    if (role !== "teacher") {
        //searchForm.style.display = "none";  // FIXME re-enable
        document.getElementById("studentSearch").value = user;
        lockForm("editform", true);
    } else {
        document.getElementById("teacherSearch").value = user;
        lockForm("editform", false);
    }

    document.getElementById("studentSearch").addEventListener("keyup", searchExamlist);
    document.getElementById("teacherSearch").addEventListener("keyup", searchExamlist);
    document.getElementById("dateSearch").addEventListener("change", searchExamlist);
    document.getElementById("editform").addEventListener("submit", saveExam);
    document.getElementById("statusSearch").addEventListener("change", searchExamlist);

    document.getElementById("examadd").addEventListener("click", function () {
        resetForm();
        document.getElementById("editform").classList.remove("d-none");
    });
    document.getElementById("cancel").addEventListener("click", resetForm);
    document.getElementById("editform").classList.add("d-none");
});

/**
 * search people with delay upon input
 */
function searchExamlist() {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(() => {
        let filter = "";
        filter += "student=" + document.getElementById("studentSearch").value;
        filter += "&teacher=" + document.getElementById("teacherSearch").value;
        filter += "&date=" + document.getElementById("dateSearch").value;

        let status = "none";
        const open = document.getElementById("open").checked;
        const closed = document.getElementById("closed").checked;
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
    document.getElementById("editform").classList.remove("d-none");
    readExam(uuid);
}

/**
 * reads a single exam identified by the uuid
 * @param uuid
 */
function readExam(uuid) {
    fetch(API_URL + "/exam/" + uuid,
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
    for (let property in exam) {
        if (typeof exam[property] === "object") {
            if (property === "student" || property === "teacher") {
                document.getElementById(property + ".fullname").value = exam[property].fullname + " (" + exam[property].email + ")";
                document.getElementById(property).value = exam[property].email;
            }
        } else {
            const field = document.getElementById(property);
            if (field !== null) {
                field.value = exam[property];
            }
        }
    }
}

/**
 * reads all exams matching a filter
 * @param filter
 */
function readExamlist(filter) {
    fetch(API_URL + "/exams?" + filter,
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

        data.sort(sortExams);
        let rows = document.getElementById("examlist")
            .getElementsByTagName("tbody")[0];
        rows.innerHTML = "";
        data.forEach(exam => {
            try {
                let row = rows.insertRow(-1);
                let cell = row.insertCell(-1);
                let button = document.createElement("button");
                button.innerHTML = "&#9998;";
                button.type = "button";
                button.id = "editExam";
                button.title = "Bearbeiten";
                button.setAttribute("data-examUUID", exam.exam_uuid);
                button.addEventListener("click", selectExam);
                cell.appendChild(button);

                if (role == "teacher") {
                    button = document.createElement("button");
                    button.innerHTML = "&#9993;";
                    button.type = "button";
                    button.id = "sendEmail";
                    button.title = "Email";
                    button.setAttribute("data-examUUID", exam.exam_uuid);
                    button.addEventListener("click", sendEmail);
                    cell.appendChild(button);
                    button = document.createElement("button");
                    button.innerHTML = "&#128438;";
                    button.type = "button";
                    button.id = "createPDF";
                    button.title = "Drucken";
                    button.setAttribute("data-examUUID", exam.exam_uuid);
                    button.addEventListener("click", createPDF);
                    cell.appendChild(button);
                }

                cell = row.insertCell(-1);
                cell.innerHTML = exam.student.firstname + " " + exam.student.lastname;
                cell.innerHTML += "<br />" + exam.student.email;
                cell = row.insertCell(-1);
                cell.innerHTML = eventList[exam.event_uuid].datetime;
                cell = row.insertCell(-1);
                cell.innerHTML = exam.teacher.firstname + " " + exam.teacher.lastname;
                cell.innerHTML += "<br />" + exam.teacher.email;
                cell = row.insertCell(-1);
                cell.innerHTML = exam.cohort;
                cell = row.insertCell(-1);
                cell.innerHTML = exam.module + " / " + exam.exam_num;
                cell = row.insertCell(-1);
                cell.innerHTML = exam.duration;
                cell = row.insertCell(-1);
                cell.innerHTML = exam.status;
            } catch (error) {
                console.log("Error in exam with uuid: " + exam.exam_uuid);
            }
        });
        showMessage("clear", "");
    })();
}

/**
 * compares to exams
 * @param examA
 * @param examB
 * @returns compare result
 */
function sortExams(examA, examB) {
    const dateA = eventList[examA.event_uuid].datetime;
    const dateB = eventList[examB.event_uuid].datetime;
    if (dateA < dateB) {
        return -1;
    }
    if (dateA > dateB) {
        return 1;
    }

    const compare = examA.student.lastname.toString().localeCompare(examB.student.lastname.toString());
    if (compare !== 0) return compare;
    return examA.student.firstname.localeCompare(examB.student.firstname);

}

/**
 * saves an exam
 * @param event
 */
function saveExam(event) {
    event.preventDefault();
    const examForm = document.getElementById("editform");
    if (examForm.checkValidity()) {
        const url = API_URL + "/exam";
        const fields = ["exam_uuid", "teacher", "module", "exam_num", "cohort", "duration", "room", "event_uuid", "student", "status", "tools", "remarks"];
        let data = new URLSearchParams();
        for (let field of fields) {
            data.set(field, document.getElementById(field).value);
        }
        let httpMethod = "POST";
        if (data.get("exam_uuid") !== "") httpMethod = "PUT";

        fetch(url, {
            method: httpMethod,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Bearer " + readStorage("token")
            },
            body: data
        })
            .then(function (response) {
                if (!response.ok) {
                    console.log(response); // TODO error handling
                } else return response;
            })
            .then(() => {
                document.getElementById("editform").classList.add("d-none");
                searchExamlist(user);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

}

/**
 * resets and closes the edit form
 */
function resetForm() {
    const form = document.getElementById("editform");
    let elements = form.getElementsByTagName("input");
    let count = elements.length;
    for (let i = 0; i < count; i++) {
        let element = elements[i];
        element.value = "";
    }
    form.classList.add("d-none");
}
