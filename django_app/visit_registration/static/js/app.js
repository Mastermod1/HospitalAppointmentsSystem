const fill = document.getElementById('to_fill')
const login_btn = document.getElementById('Login_button');
const fetch_btn = document.getElementById('Fetch_button');
const specializations_dropdown = document.getElementById('specialization_dropdown');
const doctors_dropdown = document.getElementById('doctors_dropdown');

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

cache = {};

const load_specializations = () => {
    if (cache['specializations'])
    {
        return;
    }
    const token = localStorage.getItem('accessToken');
    console.log(token)
    fetch("http://localhost:8000/registration/api/specializations/", {
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
        specializations_dropdown.innerHTML = "";
        data.forEach(el => {
            option = document.createElement('option');
            option.innerText = el.name;
            option.setAttribute('value', el.id);
            specializations_dropdown.appendChild(option);
            
        });
        cache['specializations'] = specializations_dropdown;
    })
    .catch( error => console.error(error));
};

const load_doctors = () => {
    const token = localStorage.getItem('accessToken');
    console.log(token)
    const specializationId = specializations_dropdown.value;
    const apiUrl = `http://localhost:8000/registration/api/doctors/${specializationId}/`;
    fetch(apiUrl, {
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
        doctors_dropdown.innerHTML = "";
        data.forEach(el => {
            option = document.createElement('option');
            option.innerText = `${el.first_name} ${el.last_name}`;
            doctors_dropdown.appendChild(option);
            
        });
    })
    .catch( error => console.error(error));
};

login_btn.addEventListener('click', () => login('wujek', 'wodawoda15'));
fetch_btn.addEventListener('click', fetch_data);
specializations_dropdown.addEventListener('click', load_specializations);
doctors_dropdown.addEventListener('click', load_doctors);
