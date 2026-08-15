const storedUser =
    JSON.parse(
        localStorage.getItem(
            "skilllinkUser"
        )
    );


/* =========================
   PROTECT PAGE
========================= */

if (
    !storedUser ||
    storedUser.role !== "user"
) {

    window.location.href =
        "login.html";

}


/* =========================
   USER NAME
========================= */

const userName =
    document.getElementById(
        "userName"
    );


if (userName && storedUser) {

    userName.textContent =
        storedUser.name;

}


/* =========================
   PROVIDERS
========================= */

const providers = [

    {
        name: "Thandi M.",
        skill: "Hairdresser",
        location: "Soweto",
        phone: "27820000001"
    },

    {
        name: "Sipho K.",
        skill: "Plumber",
        location: "Johannesburg",
        phone: "27820000002"
    },

    {
        name: "Lerato P.",
        skill: "Graphic Designer",
        location: "Sandton",
        phone: "27820000003"
    },

    {
        name: "Mpho T.",
        skill: "Computer Technician",
        location: "Alexandra",
        phone: "27820000004"
    },

    {
        name: "Nomsa D.",
        skill: "Tutor",
        location: "Tembisa",
        phone: "27820000005"
    }

];


const providerGrid =
    document.getElementById(
        "providerGrid"
    );


function displayProviders(list) {

    providerGrid.innerHTML = "";


    list.forEach(provider => {

        const initials =
            provider.name
                .split(" ")
                .map(word => word[0])
                .join("");


        const card =
            document.createElement("div");


        card.className =
            "provider-card";


        card.innerHTML = `

            <div class="provider-avatar">
                ${initials}
            </div>

            <h3>
                ${provider.name}
            </h3>

            <p class="skill">
                ${provider.skill}
            </p>

            <p class="location">
                📍 ${provider.location}
            </p>

            <button
                class="whatsapp-btn"
                onclick="contactProvider('${provider.phone}')"
            >
                WhatsApp Provider
            </button>

        `;


        providerGrid.appendChild(card);

    });

}


displayProviders(providers);


/* =========================
   SEARCH
========================= */

const searchBtn =
    document.getElementById(
        "searchBtn"
    );

const searchInput =
    document.getElementById(
        "serviceSearch"
    );


searchBtn.addEventListener(
    "click",
    searchProviders
);


function searchProviders() {

    const query =
        searchInput.value
            .toLowerCase()
            .trim();


    if (!query) {

        displayProviders(providers);

        return;

    }


    const results =
        providers.filter(
            provider =>

                provider.name
                    .toLowerCase()
                    .includes(query)

                ||

                provider.skill
                    .toLowerCase()
                    .includes(query)

                ||

                provider.location
                    .toLowerCase()
                    .includes(query)
        );


    displayProviders(results);

}


/* =========================
   WHATSAPP
========================= */

function contactProvider(phone) {

    const message =
        encodeURIComponent(
            "Hi, I found your service on SkillLink and would like to enquire about your services."
        );


    window.open(
        `https://wa.me/${phone}?text=${message}`,
        "_blank"
    );

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