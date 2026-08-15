/* =========================
   SIGN UP
========================= */

const signupForm =
    document.getElementById("signupForm");


if (signupForm) {

    signupForm.addEventListener(
        "submit",
        function(event) {

            event.preventDefault();


            const name =
                document.getElementById(
                    "signupName"
                ).value;

            const email =
                document.getElementById(
                    "signupEmail"
                ).value;

            const phone =
                document.getElementById(
                    "signupPhone"
                ).value;

            const password =
                document.getElementById(
                    "signupPassword"
                ).value;


            const role =
                document.querySelector(
                    'input[name="role"]:checked'
                ).value;


            const user = {

                name: name,

                email: email,

                phone: phone,

                password: password,

                role: role

            };


            /*
             * DEMO ONLY
             *
             * Do not store real passwords
             * in localStorage in a production app.
             */

            localStorage.setItem(
                "skilllinkUser",
                JSON.stringify(user)
            );


            localStorage.setItem(
                "isLoggedIn",
                "true"
            );


            if (role === "provider") {

                window.location.href =
                    "service-provider.html";

            } else {

                window.location.href =
                    "service-user.html";

            }

        }
    );

}


/* =========================
   LOGIN
========================= */

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        function(event) {

            event.preventDefault();


            const email =
                document.getElementById(
                    "loginEmail"
                ).value;

            const password =
                document.getElementById(
                    "loginPassword"
                ).value;

            const role =
                document.getElementById(
                    "loginRole"
                ).value;


            const storedUser =
                JSON.parse(
                    localStorage.getItem(
                        "skilllinkUser"
                    )
                );


            if (!storedUser) {

                alert(
                    "No account found. Please sign up first."
                );

                return;

            }


            if (
                storedUser.email !== email ||
                storedUser.password !== password
            ) {

                alert(
                    "Incorrect email or password."
                );

                return;

            }


            if (
                storedUser.role !== role
            ) {

                alert(
                    "This account belongs to a different user type."
                );

                return;

            }


            localStorage.setItem(
                "isLoggedIn",
                "true"
            );


            if (role === "provider") {

                window.location.href =
                    "service-provider.html";

            } else {

                window.location.href =
                    "service-user.html";

            }

        }
    );

}