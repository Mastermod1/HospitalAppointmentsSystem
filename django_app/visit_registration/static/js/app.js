const fill = document.getElementById('to_fill')
const login_btn = document.getElementById('Login_button');
const fetch_btn = document.getElementById('Fetch_button');

const login = (username, password) => {
    fetch("http://localhost:8000/registration/api/token/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'username': username, 
            'password': password}),
    })
    .then(response => response.json())
    .then( data => {
        if (data.token) {
            console.log("Authorized");
            localStorage.setItem('accessToken', data.token);
        } else {
            console.error("No token");
        }
    });
};

const fetch_data = () => {
    const token = localStorage.getItem('accessToken');
    console.log(token)
    fetch("http://localhost:8000/registration/api/get_visits/", {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Unaurhorized");
        }
    })
    .then(data => {
        console.log("Got response with data: ", data);
        fill.innerText = data.message;
    })
    .catch( error => console.error(error));
};

login_btn.addEventListener('click', () => login('wujek', 'wodawoda15'));
fetch_btn.addEventListener('click', fetch_data);
