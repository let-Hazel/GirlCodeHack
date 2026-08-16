/* =========================================================
   SKILLINK AUTHENTICATION
   Handles:
   - Sign up
   - Login
   - Role selection
   - Session storage
   - Logout
========================================================= */


/* =========================================================
   SIGN UP
========================================================= */

const signupForm = document.getElementById("signupForm");

if (signupForm) {

    /*
     * Pre-select the role from the URL.
     *
     * Example:
     * signup.html?role=provider
     *
     * or:
     * signup.html?role=user
     */

    const params = new URLSearchParams(
        window.location.search
    );

    const requestedRole = params.get("role");

    if (
        requestedRole === "user" ||
        requestedRole === "provider"
    ) {

        const roleInput =
            document.querySelector(
                `input[name="role"][value="${requestedRole}"]`
            );

        if (roleInput) {
            roleInput.checked = true;
        }
    }


    /* =====================================================
       SUBMIT SIGNUP
    ===================================================== */

    signupForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            /* ---------------------------------------------
               GET FORM VALUES
            --------------------------------------------- */

            const nameElement =
                document.getElementById("signupName");

            const surnameElement =
                document.getElementById("signupSurname");

            const emailElement =
                document.getElementById("signupEmail");

            const phoneElement =
                document.getElementById("signupPhone");

            const locationElement =
                document.getElementById("signupLocation");

            const passwordElement =
                document.getElementById("signupPassword");


            const name =
                nameElement
                    ? nameElement.value.trim()
                    : "";

            const surname =
                surnameElement
                    ? surnameElement.value.trim()
                    : "";

            const email =
                emailElement
                    ? emailElement.value.trim()
                    : "";

            const phone =
                phoneElement
                    ? phoneElement.value.trim()
                    : "";

            const location =
                locationElement
                    ? locationElement.value.trim()
                    : "";

            const password =
                passwordElement
                    ? passwordElement.value
                    : "";


            /* ---------------------------------------------
               GET ROLE
            --------------------------------------------- */

            const selectedRole =
                document.querySelector(
                    'input[name="role"]:checked'
                );

            const role =
                selectedRole
                    ? selectedRole.value
                    : "user";


            /* ---------------------------------------------
               VALIDATION
            --------------------------------------------- */

            if (!name) {

                alert(
                    "Please enter your first name."
                );

                return;
            }


            if (!surname) {

                alert(
                    "Please enter your surname."
                );

                return;
            }


            if (!email) {

                alert(
                    "Please enter your email."
                );

                return;
            }


            if (!password) {

                alert(
                    "Please enter a password."
                );

                return;
            }


            if (password.length < 6) {

                alert(
                    "Password must be at least 6 characters."
                );

                return;
            }


            /* ---------------------------------------------
               DISABLE BUTTON
            --------------------------------------------- */

            const submitButton =
                signupForm.querySelector(
                    'button[type="submit"]'
                );


            const originalText =
                submitButton
                    ? submitButton.textContent
                    : "";


            if (submitButton) {

                submitButton.disabled = true;

                submitButton.textContent =
                    "Creating account...";

            }


            /* ---------------------------------------------
               SEND TO FLASK
            --------------------------------------------- */

            try {

                const result =
                    await api(
                        "/users",
                        {

                            method: "POST",

                            body: JSON.stringify({

                                name: name,

                                surname: surname,

                                email: email,

                                password: password,

                                phone: phone,

                                location: location,

                                role: role

                            })

                        }
                    );


                console.log(
                    "SIGNUP SUCCESS:",
                    result
                );


                alert(
                    "Account created successfully! Please log in."
                );


                /* -----------------------------------------
                   GO TO LOGIN
                ----------------------------------------- */

                window.location.href =
                    "login.html";


            } catch (error) {

                console.error(
                    "SIGNUP ERROR:",
                    error
                );


                alert(
                    error.message ||
                    "Unable to create account."
                );


            } finally {

                if (submitButton) {

                    submitButton.disabled = false;

                    submitButton.textContent =
                        originalText;

                }

            }

        }
    );

}


/* =========================================================
   LOGIN
========================================================= */

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            /* ---------------------------------------------
               GET FORM VALUES
            --------------------------------------------- */

            const emailElement =
                document.getElementById("loginEmail");

            const passwordElement =
                document.getElementById("loginPassword");

            const roleElement =
                document.getElementById("loginRole");


            const email =
                emailElement
                    ? emailElement.value.trim()
                    : "";

            const password =
                passwordElement
                    ? passwordElement.value
                    : "";


            let role = null;


            if (roleElement) {

                role =
                    roleElement.value;

            }


            /* ---------------------------------------------
               VALIDATION
            --------------------------------------------- */

            if (!email) {

                alert(
                    "Please enter your email."
                );

                return;
            }


            if (!password) {

                alert(
                    "Please enter your password."
                );

                return;
            }


            /* ---------------------------------------------
               DISABLE LOGIN BUTTON
            --------------------------------------------- */

            const submitButton =
                loginForm.querySelector(
                    'button[type="submit"]'
                );


            const originalText =
                submitButton
                    ? submitButton.textContent
                    : "";


            if (submitButton) {

                submitButton.disabled = true;

                submitButton.textContent =
                    "Logging in...";

            }


            /* ---------------------------------------------
               LOGIN REQUEST
            --------------------------------------------- */

            try {

                const user =
                    await api(
                        "/login",
                        {

                            method: "POST",

                            body: JSON.stringify({

                                email: email,

                                password: password,

                                role: role

                            })

                        }
                    );


                console.log(
                    "LOGIN SUCCESS:",
                    user
                );


                /* -----------------------------------------
                   CHECK USER RESPONSE
                ----------------------------------------- */

                if (!user || !user.id) {

                    throw new Error(
                        "The server returned an invalid user account."
                    );

                }


                /* -----------------------------------------
                   SAVE SESSION
                ----------------------------------------- */

                saveSession(user);


                /* -----------------------------------------
                   REDIRECT BASED ON ROLE
                ----------------------------------------- */

                if (
                    user.role === "provider"
                ) {

                    window.location.href =
                        "service-provider.html";

                } else {

                    window.location.href =
                        "service-user.html";

                }


            } catch (error) {

                console.error(
                    "LOGIN ERROR:",
                    error
                );


                alert(
                    error.message ||
                    "Login failed. Please check your details."
                );


            } finally {

                if (submitButton) {

                    submitButton.disabled = false;

                    submitButton.textContent =
                        originalText;

                }

            }

        }
    );

}


/* =========================================================
   LOGOUT
========================================================= */

const logoutButtons =
    document.querySelectorAll(
        "#logoutBtn, .logout-btn"
    );


logoutButtons.forEach(
    button => {

        button.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                logout();

            }
        );

    }
);


/* =========================================================
   SESSION HELPERS
========================================================= */


/*
 * Save the logged-in user.
 */

function saveSession(user) {

    localStorage.setItem(
        "skilllinkUser",
        JSON.stringify(user)
    );

}


/*
 * Get the currently logged-in user.
 */

function getSession() {

    try {

        const session =
            localStorage.getItem(
                "skilllinkUser"
            );


        if (!session) {
            return null;
        }


        return JSON.parse(session);


    } catch (error) {

        console.error(
            "SESSION ERROR:",
            error
        );


        return null;

    }

}


/*
 * Remove the current session.
 */

function logout() {

    localStorage.removeItem(
        "skilllinkUser"
    );


    window.location.href =
        "login.html";

}


/* =========================================================
   PAGE PROTECTION
========================================================= */


/*
 * Use these attributes on dashboard pages if needed:
 *
 * <body data-page="user-dashboard">
 *
 * or:
 *
 * <body data-page="provider-dashboard">
 */

const currentPage =
    document.body.dataset.page;


const currentUser =
    getSession();


/* ---------------------------------------------
   USER DASHBOARD
--------------------------------------------- */

if (
    currentPage === "user-dashboard"
) {

    if (!currentUser) {

        window.location.href =
            "login.html";

    } else if (
        currentUser.role !== "user"
    ) {

        window.location.href =
            "service-provider.html";

    }

}


/* ---------------------------------------------
   PROVIDER DASHBOARD
--------------------------------------------- */

if (
    currentPage === "provider-dashboard"
) {

    if (!currentUser) {

        window.location.href =
            "login.html";

    } else if (
        currentUser.role !== "provider"
    ) {

        window.location.href =
            "service-user.html";

    }

}