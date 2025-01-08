const specializations_dropdown = document.getElementById('specialization_dropdown');
const doctors_dropdown = document.getElementById('doctors_dropdown');
const calendar = document.getElementById('visit_date_dropdown');
const hours = document.getElementById('visit_hour_dropdown');
const reserve = document.getElementById('reserve_button');

let cache = {};
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
            throw new Error("Error");
        }
    })
    .then(data => {
        specializations_dropdown.innerHTML = "";
        data.forEach(el => {
            option = document.createElement('option');
            option.innerText = el.name;
            option.setAttribute('value', el.id);
            specializations_dropdown.appendChild(option);
        });
        cache['specializations'] = true;
    })
    .catch( error => console.error(error));
};

const load_doctors = () => {
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
            throw new Error("Error");
        }
    })
    .then(data => {
        doctors_dropdown.innerHTML = "";
        option = document.createElement('option');
        option.innerText = `Dowolny`;
        option.setAttribute('value', '-1');
        doctors_dropdown.appendChild(option);
        data.forEach(el => {
            option = document.createElement('option');
            option.innerText = `${el.user.first_name} ${el.user.last_name}`;
            option.setAttribute('value', el.id);
            doctors_dropdown.appendChild(option);
        });
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
    hours.disabled = false;
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
            throw new Error("Error");
        }
    })
    .then(data => {
        data = JSON.parse(data)
        hours.innerHTML = "";
        if (data.times.length > 0) {
            data.times.forEach(el => {
                option = document.createElement('option');
                option.innerText = el;
                hours.appendChild(option);
            });
        } else {
            option = document.createElement('option');
            option.innerText = "Brak wolnych terminów";
        }
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
            throw new Error("Error");
        }
    })
    .then(() => {
        location.reload();
        hours.disabled = true;
        calendar.value = "";
    })
    .catch( error => console.log(error));
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
specializations_dropdown.addEventListener('change', load_doctors);
calendar.addEventListener('change', load_available_dates);
reserve.addEventListener('click', reserve_call);
