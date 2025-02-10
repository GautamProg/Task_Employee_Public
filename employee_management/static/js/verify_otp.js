// document.getElementById("otpForm").addEventListener("submit", async function(event) {
//     event.preventDefault();
//     let otp = document.getElementById("otp").value;
    
//     let response = await fetch("http://127.0.0.1:8000/verifyOTP/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ employee_id: localStorage.getItem("employee_id"), otp })
//     });
//     let result = await response.json();
//     document.getElementById("otpMessage").innerText = result.message;
//     if (result.success) {
//         window.location.href = "http://127.0.0.1:8000/dashboard/";
//     }
// });





// document.getElementById("otpForm").addEventListener("submit", async function(event) {
//     event.preventDefault();
    
//     let employee_id = document.getElementById("employee_id").value;
//     let otp = document.getElementById("otp").value;
    
//     let response = await fetch("http://127.0.0.1:8000/verifyOTP/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ employee_id, otp })
//     });
    
//     let result = await response.json();
//     document.getElementById("otpMessage").innerText = result.message;
    
//     if (result.success) {
//         window.location.href = "http://127.0.0.1:8000/dashboard/";
//     }
// });




// document.getElementById("otpForm").addEventListener("submit", async function(event) {
//     event.preventDefault();

//     let employee_id = document.getElementById("employee_id").value;
//     let otp = document.getElementById("otp").value;

//     let response = await fetch("http://127.0.0.1:8000/verifyOTP/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ employee_id, otp })
//     });

//     let result = await response.json();
//     console.log("Response:", result);  // Debugging
//     document.getElementById("otpMessage").innerText = result.message;

//     if (result.success) {
//         window.location.href = "http://127.0.0.1:8000/dashboard/";
//     }
// });




// document.addEventListener("DOMContentLoaded", function() {
//     let loginForm = document.getElementById("verifyOtpForm");

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
//                 if (result.enable_2fa === true || result.enable_2fa === 1) {  // Ensure correct check
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
    let verifyOtpForm = document.getElementById("verifyOtpForm"); // ✅ Corrected ID

    if (verifyOtpForm) {
        verifyOtpForm.addEventListener("submit", async function(event) {
            event.preventDefault();
            
            let employee_id = document.getElementById("employee_id").value;
            let otp = document.getElementById("otp").value;

            let data = { employee_id, otp };
            console.log("Sending OTP data:", data); // Debugging

            let response = await fetch("http://127.0.0.1:8000/verifyOTP/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            let result = await response.json();
            console.log("OTP Verification Response:", result);
            
            if (result.success) {
                window.location.href = "http://127.0.0.1:8000/dashboard/";
            } else {
                document.getElementById("otpMessage").innerText = result.message;
            }
        });
    } else {
        console.error("OTP form not found! Make sure the form has id='verifyOtpForm'.");
    }
});
