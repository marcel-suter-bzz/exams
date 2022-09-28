/**
 * view-controller for events
 */
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("dateSearch").addEventListener("change", searchExamlist);
});

/**
 * search people with delay upon input
 */
function searchExamlist() {
        let filter = "date=" + document.getElementById("dateSearch").value;
        filter += "&status=all";
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
                cell.innerHTML = exam.room;
                cell = row.insertCell(-1);
                cell.innerHTML = exam.student.firstname + " " + exam.student.lastname;
                cell.innerHTML += "<br />" + exam.student.email;
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