/**
 * view-controller for examlist
 */


readEventList();
document.addEventListener("DOMContentLoaded", () => {
});

/**
 * reads all events matching a filter
 */
function readEventList() {
    fetch(API_URL + "/events",
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
        let dateEdit = document.getElementById("event_uuid");
        data.forEach(event => {
            key = event.event_uuid;
            eventList[key] = event;

            let option = document.createElement("option");
            option.value = event.event_uuid;
            option.text = event.datetime;
            dateSearch.appendChild(option);
            let copy = option.cloneNode(true);
            dateEdit.appendChild(copy);
        });
    })();
}