const specializations_dropdown = document.getElementById('specialization_dropdown');
const doctors_dropdown = document.getElementById('doctors_dropdown');
const calendar = document.getElementById('visit_date_dropdown');
const hours = document.getElementById('visit_hour_dropdown');
const reserve = document.getElementById('reserve_button');

cache = {};

const load_specializations = () => {
    if (cache['specializations'])
    {
        return;
    }
    const token = localStorage.getItem('accessToken');
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
        cache['specializations'] = data;
    })
    .catch( error => console.error(error));
};

const load_doctors = (is_new_doctor) => {
    if (!is_new_doctor && cache['doctors'])
    {
        return;
    }

    const token = localStorage.getItem('accessToken');
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
        option = document.createElement('option');
        option.innerText = `Dowolny`;
        doctors_dropdown.appendChild(option);
        data.forEach(el => {
            option = document.createElement('option');
            option.innerText = `${el.user.first_name} ${el.user.last_name}`;
            option.setAttribute('value', el.id);
            doctors_dropdown.appendChild(option);
        });
        cache['doctors'] = data;
    })
    .catch( error => console.error(error));
};

const today_date = () => {
    const today = new Date();

    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    return formattedDate;
};

const load_available_dates = () => {
    const token = localStorage.getItem('accessToken');
    const doctorId = doctors_dropdown.value;
    const date = calendar.value;
    const apiUrl = `http://localhost:8000/registration/api/doctor_availability/${doctorId}/${date}/`;
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
        data = JSON.parse(data)
        hours.innerHTML = "";
        data.times.forEach(el => {
            option = document.createElement('option');
            option.innerText = el;
            hours.appendChild(option);
        });
    })
    .catch( error => console.error(error));
};

const reserve_call = () => {
    const token = localStorage.getItem('accessToken');
    const apiUrl = `http://localhost:8000/registration/api/make_appointment/`;
    bodyObject = {
        doctor_id: doctors_dropdown.value,
        date: calendar.value,
        time: hours.value,
    };
    console.log(bodyObject);
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
        },
        body:  JSON.stringify(bodyObject),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Error", response);
        }
    })
    .then(data => {
        console.log(data);
        location.reload();
    })
    .catch( error => console.error(error));
};

const getCookie = name => {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

const get_token = () => {
    localStorage.setItem('accessToken', getCookie('auth_token'));
};

window.onload = get_token;
calendar.setAttribute('min', today_date());
specializations_dropdown.addEventListener('click', load_specializations);
specializations_dropdown.addEventListener('change', () => load_doctors(true));
calendar.addEventListener('change', load_available_dates);
reserve.addEventListener('click', reserve_call);
