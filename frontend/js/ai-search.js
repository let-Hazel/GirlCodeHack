/* ==========================================
   SKILLINK AI SEARCH ASSISTANT
========================================== */


/*
    Example provider database.

    Later this will come from MySQL/PostgreSQL
    through your Python backend.
*/

const skillLinkProviders = [

    {
        name: "Mpho T.",
        skill: "Computer Technician",
        category: "Technology",
        location: "Alexandra",
        phone: "27820000004",
        description:
            "Laptop repairs, computer troubleshooting and software installation."
    },

    {
        name: "Lerato P.",
        skill: "Graphic Designer",
        category: "Creative",
        location: "Sandton",
        phone: "27820000003",
        description:
            "Graphic design, posters, logos and social media designs."
    },

    {
        name: "Sipho K.",
        skill: "Plumber",
        category: "Repairs",
        location: "Johannesburg",
        phone: "27820000002",
        description:
            "Plumbing repairs, leaking taps and pipe maintenance."
    },

    {
        name: "Thandi M.",
        skill: "Hairdresser",
        category: "Beauty",
        location: "Soweto",
        phone: "27820000001",
        description:
            "Hair styling, braiding, washing and hair treatments."
    },

    {
        name: "Nomsa D.",
        skill: "Tutor",
        category: "Education",
        location: "Tembisa",
        phone: "27820000005",
        description:
            "School tutoring, homework assistance and study support."
    }

];


/* ==========================================
   AI SERVICE CATEGORIES
========================================== */

const serviceKeywords = {

    Technology: [
        "computer",
        "laptop",
        "phone",
        "software",
        "wifi",
        "internet",
        "printer",
        "technology",
        "it",
        "technical",
        "screen",
        "keyboard"
    ],

    Repairs: [
        "plumber",
        "plumbing",
        "tap",
        "pipe",
        "leak",
        "water",
        "repair",
        "fix",
        "broken",
        "electrician",
        "electricity"
    ],

    Beauty: [
        "hair",
        "hairdresser",
        "braids",
        "braiding",
        "makeup",
        "nails",
        "beauty",
        "styling"
    ],

    Creative: [
        "design",
        "designer",
        "logo",
        "poster",
        "flyer",
        "photography",
        "video",
        "creative"
    ],

    Education: [
        "tutor",
        "tutoring",
        "school",
        "homework",
        "maths",
        "mathematics",
        "english",
        "lesson",
        "study",
        "teacher"
    ]

};


/* ==========================================
   GET ELEMENTS
========================================== */

const aiRequest =
    document.getElementById("aiRequest");

const aiSearchBtn =
    document.getElementById("aiSearchBtn");

const aiResult =
    document.getElementById("aiResult");

const providerGrid =
    document.getElementById("providerGrid");


/* ==========================================
   AI SEARCH
========================================== */

if (aiSearchBtn) {

    aiSearchBtn.addEventListener(
        "click",
        runAISearch
    );

}


/* Also allow CTRL + ENTER */

if (aiRequest) {

    aiRequest.addEventListener(
        "keydown",
        function(event) {

            if (
                event.ctrlKey &&
                event.key === "Enter"
            ) {

                runAISearch();

            }

        }
    );

}


/* ==========================================
   MAIN AI FUNCTION
========================================== */

function runAISearch() {

    const request =
        aiRequest.value
            .toLowerCase()
            .trim();


    if (!request) {

        aiResult.innerHTML = `
            <div class="ai-error">
                Please describe the service you need.
            </div>
        `;

        return;

    }


    /* Show loading */

    aiResult.innerHTML = `
        <div class="ai-loading">
            ✨ SkillLink AI is analysing your request...
        </div>
    `;


    /*
        Small delay to make the AI interaction
        feel natural during the prototype.
    */

    setTimeout(function() {

        const category =
            identifyService(request);


        const matchingProviders =
            findProviders(category);


        displayAIResult(
            category,
            matchingProviders,
            request
        );


    }, 700);

}


/* ==========================================
   IDENTIFY SERVICE
========================================== */

function identifyService(request) {

    let bestCategory = "General Services";

    let highestScore = 0;


    for (
        const category in serviceKeywords
    ) {

        let score = 0;


        const keywords =
            serviceKeywords[category];


        keywords.forEach(
            keyword => {

                if (
                    request.includes(keyword)
                ) {

                    score++;

                }

            }
        );


        if (
            score > highestScore
        ) {

            highestScore = score;

            bestCategory = category;

        }

    }


    return bestCategory;

}


/* ==========================================
   FIND PROVIDERS
========================================== */

function findProviders(category) {

    return skillLinkProviders.filter(
        provider =>
            provider.category === category
    );

}


/* ==========================================
   DISPLAY AI RESULT
========================================== */

function displayAIResult(
    category,
    providers,
    request
) {

    let message;


    switch (category) {

        case "Technology":

            message =
                "Your request appears to be related to computer or technology support.";

            break;


        case "Repairs":

            message =
                "Your request appears to require a repair or maintenance service.";

            break;


        case "Beauty":

            message =
                "Your request appears to be related to beauty or personal care.";

            break;


        case "Creative":

            message =
                "Your request appears to require a creative service.";

            break;


        case "Education":

            message =
                "Your request appears to require educational or tutoring support.";

            break;


        default:

            message =
                "We couldn't determine an exact service category.";

    }


    aiResult.innerHTML = `

        <div class="ai-result-card">

            <div class="ai-result-header">

                <span>
                    ✨ SKILLINK AI
                </span>

                <span class="ai-match">
                    AI MATCH
                </span>

            </div>


            <h3>
                ${category}
            </h3>


            <p>
                ${message}
            </p>


            <div class="ai-request">

                <strong>
                    Your request:
                </strong>

                <p>
                    "${request}"
                </p>

            </div>


            <strong>
                ${providers.length}
                provider(s) found
            </strong>

        </div>

    `;


    displayProviders(
        providers
    );

}


/* ==========================================
   DISPLAY PROVIDERS
========================================== */

function displayProviders(
    providers
) {

    providerGrid.innerHTML = "";


    if (
        providers.length === 0
    ) {

        providerGrid.innerHTML = `

            <div class="no-providers">

                <div>
                    🔍
                </div>

                <h3>
                    No providers found
                </h3>

                <p>
                    Try describing your request
                    differently.
                </p>

            </div>

        `;

        return;

    }


    providers.forEach(
        provider => {

            const initials =
                provider.name
                    .split(" ")
                    .map(
                        name =>
                            name[0]
                    )
                    .join("");


            const card =
                document.createElement(
                    "div"
                );


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


                <p class="provider-description">
                    ${provider.description}
                </p>


                <button
                    class="whatsapp-btn"
                    onclick="contactProvider('${provider.phone}')"
                >
                    💬 WhatsApp Provider
                </button>

            `;


            providerGrid.appendChild(
                card
            );

        }
    );

}


/* ==========================================
   WHATSAPP
========================================== */

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