const provider =
    JSON.parse(
        localStorage.getItem(
            "skilllinkUser"
        )
    );


/* =========================
   PROTECT PROVIDER PAGE
========================= */

if (
    !provider ||
    provider.role !== "provider"
) {

    window.location.href =
        "login.html";

}


/* =========================
   PROVIDER NAME
========================= */

const providerName =
    document.getElementById(
        "providerName"
    );


if (
    providerName &&
    provider
) {

    providerName.textContent =
        provider.name;

}


/* =========================
   LOGOUT
========================= */

document
    .getElementById("logoutBtn")
    .addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "isLoggedIn"
            );

            window.location.href =
                "login.html";

        }
    );