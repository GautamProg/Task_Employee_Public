// document.getElementById("loginForm").addEventListener("submit", async function(event) {
//     event.preventDefault();
//     let employee_id = document.getElementById("employee_id").value;
//     let password = document.getElementById("password").value;
    
//     let response = await fetch("http://127.0.0.1:8000/login/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ employee_id, password })
//     });
//     let result = await response.json();
//     console.log("API Response:", result); 
//     document.getElementById("loginMessage").innerText = result.message;
//     if (result.success) {
//         window.location.href = "http://127.0.0.1:8000/verify-otp/";
//     }
// });






// document.addEventListener("DOMContentLoaded", function() {
//     let loginForm = document.getElementById("loginForm");

//     if (loginForm) {
//         loginForm.addEventListener("submit", async function(event) {
//             event.preventDefault();
            
//             let employee_id = document.getElementById("employee_id").value;
//             let password = document.getElementById("password").value;
//             let data = { employee_id, password };
//             console.log("Sending data:", data); // Debugging

//             let response = await fetch("http://127.0.0.1:8000/login/", {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ employee_id, password })
//             });

//             let result = await response.json();
//             console.log("Response:", result);
//             document.getElementById("loginMessage").innerText = result.message;

//             if (result.success) {
//                 window.location.href = "http://127.0.0.1:8000/verify-otp/";
//             }
//         });
//     } else {
//         console.error("Login form not found! Make sure the form has id='loginForm'.");
//     }
// });


//<!-- verify_otp.js -->




// document.addEventListener("DOMContentLoaded", function() {
//     let loginForm = document.getElementById("loginForm");

//     if (loginForm) {
//         loginForm.addEventListener("submit", async function(event) {
//             event.preventDefault();
            
//             let employee_id = document.getElementById("employee_id").value;
//             let password = document.getElementById("password").value;
//             let enable_2fa = document.getElementById("enable_2fa").checked ? 1 : 0; // Convert boolean to 1 or 0

//             let data = { employee_id, password, enable_2fa };
//             console.log("Sending data:", data); // Debugging

//             let response = await fetch("http://127.0.0.1:8000/login/", {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify(data)
//             });

//             let result = await response.json();
//             console.log("Response:", result);
//             document.getElementById("loginMessage").innerText = result.message;

//             if (result.success) {
//                 if (result.enable_2fa) {
//                     window.location.href = "http://127.0.0.1:8000/verify-otp/";
//                 } else {
//                     localStorage.setItem("auth_token", result.token); // Save token if 2FA not enabled
//                     window.location.href = "http://127.0.0.1:8000/dashboard/";
//                 }
//             }
//         });
//     } else {
//         console.error("Login form not found! Make sure the form has id='loginForm'.");
//     }
// });





document.addEventListener("DOMContentLoaded", function() {
    let loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async function(event) {
            event.preventDefault();
            
            let employee_id = document.getElementById("employee_id").value;
            let password = document.getElementById("password").value;
            let enable_2fa = document.getElementById("enable_2fa").checked ? 1 : 0;

            let data = { employee_id, password, enable_2fa };
            console.log("Sending data:", data);

            let response = await fetch("http://127.0.0.1:8000/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            let result = await response.json();
            console.log("Response:", result);
            document.getElementById("loginMessage").innerText = result.message;

            if (result.success) {
                if (result.enable_2fa) {  
                    window.location.href = "http://127.0.0.1:8000/verify-otp/";
                } else {
                    localStorage.setItem("auth_token", result.data.token); 
                    window.location.href = "http://127.0.0.1:8000/dashboard/";
                }
            }
        });
    } else {
        console.error("Login form not found! Make sure the form has id='loginForm'.");
    }
});
