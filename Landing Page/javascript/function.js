const getStartedButton = document.getElementById('gs');

getStartedButton.addEventListener('click', function() {
    document.getElementById('gs').disabled;
});

function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggle-icon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text'; // Change input type to text
        toggleIcon.classList.remove('fa-eye'); // Change icon to open eye
        toggleIcon.classList.add('fa-eye-slash'); // Add icon for visibility
    } else {
        passwordInput.type = 'password'; // Change input type back to password
        toggleIcon.classList.remove('fa-eye-slash'); // Change icon to closed eye
        toggleIcon.classList.add('fa-eye'); // Add icon for hidden
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const userTypeSelect = document.getElementById('user_type');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const greeting = document.getElementById('greeting');
    const subs = document.getElementById('subheader');

    // Disable the input fields initially
    usernameInput.disabled = true;
    passwordInput.disabled = true;

    userTypeSelect.addEventListener('change', function() {
        const userType = this.value;

        if (userType === 'Consultant') {
            document.getElementById('user_type').style.display = 'none';
            greeting.innerText = 'Welcome Back User';
            subs.innerText = 'Wew, balik kapa';
        } else if (userType === 'Medical Professional') {
            document.getElementById('user_type').style.display = 'none';
            greeting.innerText = 'Welcome Experts';
            subs.innerText = 'Lets take care our patients';
        } else {
            greeting.innerText = 'Welcome'; // Default greeting
        }

        // Enable or disable input fields based on user type selection
        if (userType) {
            usernameInput.disabled = false;
            passwordInput.disabled = false;
        } else {
            usernameInput.disabled = true;
            passwordInput.disabled = true;
        }
    });
});

