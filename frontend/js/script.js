/* =========================
   SAMPLE PROVIDERS
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
    },

    {
        name: "Kabelo R.",
        skill: "Electrician",
        location: "Roodepoort",
        phone: "27820000006"
    }
];


/* =========================
   DISPLAY PROVIDERS
========================= */

const providerGrid =
    document.getElementById("providerGrid");


function displayProviders(list) {

    providerGrid.innerHTML = "";

    if (list.length === 0) {

        providerGrid.innerHTML = `
            <p>
                No providers found.
            </p>
        `;

        return;
    }


    list.forEach(provider => {

        const initials =
            provider.name
                .split(" ")
                .map(word => word[0])
                .join("");


        const card = document.createElement("div");

        card.className = "provider-card";

        card.innerHTML = `

            <div class="provider-avatar">
                ${initials}
            </div>

            <h3>
                ${provider.name}
            </h3>

            <p class="provider-skill">
                ${provider.skill}
            </p>

            <p class="provider-location">
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
   WHATSAPP
========================= */

function contactProvider(phone) {

    const message =
        encodeURIComponent(
            "Hi, I found your service on SkillLink and would like to enquire about your services."
        );

    const whatsappURL =
        `https://wa.me/${phone}?text=${message}`;

    window.open(whatsappURL, "_blank");
}


/* =========================
   SEARCH
========================= */

const searchBtn =
    document.getElementById("searchBtn");

const serviceSearch =
    document.getElementById("serviceSearch");


searchBtn.addEventListener("click", searchProviders);


function searchProviders() {

    const searchTerm =
        serviceSearch.value
            .trim()
            .toLowerCase();


    if (!searchTerm) {

        displayProviders(providers);

        return;
    }


    const results =
        providers.filter(provider =>

            provider.skill
                .toLowerCase()
                .includes(searchTerm)

            ||

            provider.location
                .toLowerCase()
                .includes(searchTerm)

            ||

            provider.name
                .toLowerCase()
                .includes(searchTerm)

        );


    document
        .getElementById("providers")
        .scrollIntoView({
            behavior: "smooth"
        });

    displayProviders(results);
}


/* =========================
   CATEGORY SEARCH
========================= */

const categoryCards =
    document.querySelectorAll(".category-card");


categoryCards.forEach(card => {

    card.addEventListener("click", () => {

        const category =
            card.dataset.category;

        serviceSearch.value = category;

        searchProviders();

    });

});


/* =========================
   AUTH MODAL
========================= */

const authModal =
    document.getElementById("authModal");

const loginBtn =
    document.getElementById("loginBtn");

const registerBtn =
    document.getElementById("registerBtn");

const offerSkillBtn =
    document.getElementById("offerSkillBtn");

const findSkillBtn =
    document.getElementById("findSkillBtn");

const ctaRegister =
    document.getElementById("ctaRegister");

const closeModal =
    document.getElementById("closeModal");

const modalTitle =
    document.getElementById("modalTitle");


function openRegister() {

    modalTitle.textContent =
        "Create your SkillLink account";

    authModal.classList.remove("hidden");
}


function openLogin() {

    modalTitle.textContent =
        "Login to SkillLink";

    authModal.classList.remove("hidden");
}


registerBtn.addEventListener(
    "click",
    openRegister
);

offerSkillBtn.addEventListener(
    "click",
    openRegister
);

ctaRegister.addEventListener(
    "click",
    openRegister
);

loginBtn.addEventListener(
    "click",
    openLogin
);

findSkillBtn.addEventListener(
    "click",
    () => {

        document
            .getElementById("services")
            .scrollIntoView({
                behavior: "smooth"
            });

    }
);


closeModal.addEventListener(
    "click",
    () => {

        authModal.classList.add("hidden");

    }
);


authModal.addEventListener(
    "click",
    event => {

        if (event.target === authModal) {

            authModal.classList.add("hidden");

        }

    }
);


/* =========================
   REGISTRATION
========================= */

const authForm =
    document.getElementById("authForm");


authForm.addEventListener(
    "submit",
    event => {

        event.preventDefault();


        const name =
            document.getElementById("name").value;

        const email =
            document.getElementById("email").value;

        const userType =
            document.getElementById("userType").value;


        const user = {

            name,
            email,
            userType

        };


        /*
            Temporary local storage.

            Later this should be replaced
            with a real database/backend.
        */

        localStorage.setItem(
            "skilllinkUser",
            JSON.stringify(user)
        );


        alert(
            `Welcome to SkillLink, ${name}!`
        );


        authModal.classList.add("hidden");

        authForm.reset();

    }
);