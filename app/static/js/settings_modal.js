document.addEventListener("DOMContentLoaded", function () {
    const settingsBtn = document.getElementById("settingsBtn");
    const settingsModal = new bootstrap.Modal(document.getElementById("settingsModal"));
    const settingsForm = document.getElementById("settingsForm");

    settingsBtn.addEventListener("click", function () {
        fetch("/settings")
        .then(response => response.json())
        .then(data => {
            for (const key in data) {
                const field = settingsForm.elements.namedItem(key);
                if (field) {
                    if (field.type === "checkbox") {
                        field.checked = data[key] === true || data[key] === "true";
                    } else {
                        field.value = data[key];
                    }
                }
            }
            settingsModal.show();
        });
    });

    settingsForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(settingsForm);
        fetch("/settings", {
            method: "POST",
            body: formData
        }).then(response => {
            if (response.ok) {
                alert("Saved successfully!");
                settingsModal.hide();
            } else {
                alert("Error saving settings.");
            }
        });
    });
});