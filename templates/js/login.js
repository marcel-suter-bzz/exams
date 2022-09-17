/**
 * main listener
 */
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("loginform").addEventListener("submit", sendLogin);
});

function sendLogin(event) {
    event.preventDefault();
    const personForm = document.getElementById("loginform");
    if (personForm.checkValidity() == true) {
        const url = API_URL + "/login";

        let data = new URLSearchParams();
        data.set("email", document.getElementById("email").value);
        data.set("password", document.getElementById("password").value);

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: data
        })
            .then(function (response) {
                if (!response.ok) {
                    showMessage("error", "Login nicht erfolgreich")
                } else return response;
            })
            .then(response => response.json())
            .then((data) => {
                writeStorage(data)
                window.location.href = "./examlist.html";
            })
            .catch(function (error) {
                console.log(error);
            });
    }
}