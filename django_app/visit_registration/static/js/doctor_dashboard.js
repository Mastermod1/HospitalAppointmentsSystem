function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
}

function viewDetails(item) {
    document.getElementById('listPanel').classList.remove('active');
    document.getElementById('detailsPanel').classList.add('active');
    document.getElementById('detailsContent').textContent = `You are viewing details for: ${item}`;
}

function goBack() {
    document.getElementById('detailsPanel').classList.remove('active');
    document.getElementById('listPanel').classList.add('active');
}

const load_visit_infos = (data) => {
    const visitsContainer = document.getElementById('visits');
    visitsContainer.innerHTML = '';
    data.forEach(({ date, time, patient_name }) => {
        const visitElement = document.createElement('div');
        visitElement.classList.add('visit');

        const visitInfo = document.createElement('div');
        visitInfo.classList.add('visit-info');

        const visitDate = document.createElement('span');
        visitDate.classList.add('visit-date');
        visitDate.textContent = `${date} ${time}`;

        const visitName = document.createElement('span');
        visitName.classList.add('visit-name');
        visitName.textContent = patient_name;

        visitInfo.appendChild(visitDate);
        visitInfo.appendChild(visitName);

        const detailsButton = document.createElement('button');
        detailsButton.classList.add('visit-details-btn');
        detailsButton.textContent = 'Details →';

        detailsButton.addEventListener('click', () => {
            viewDetails(patient_name);
        });

        visitElement.appendChild(visitInfo);
        visitElement.appendChild(detailsButton);
        visitsContainer.appendChild(visitElement);
    });
};

function updateVisits(selectedDate) {
    const token = localStorage.getItem('accessToken');
    const apiUrl = `http://localhost:8000/registration/api/doctor_visits/${selectedDate}/`;
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
            load_visit_infos(data.appointments);
        })
        .catch(error => console.error(error));
}

function setActiveDate(selectedBox) {
    const dateNav = document.getElementById('date-nav');
    const allDateBoxes = dateNav.querySelectorAll('.date-box');
    allDateBoxes.forEach(box => box.classList.remove('active'));
    selectedBox.classList.add('active');
}

const createSelectableDates = () => {
    const dateNav = document.getElementById('date-nav');
    let dates = [];
    const today = new Date();
    for (let i = 0; i < 5; i++) {
        const nextDay = new Date(today);
        nextDay.setDate(today.getDate() + i);
        dates.push(formatDate(nextDay));
    }

    dates.forEach(date => {
        const dateBox = document.createElement('div');
        dateBox.classList.add('date-box');
        dateBox.innerHTML = `
                    <div class="date-day">${date.split('.')[0]}</div>
                    <div class="date-month">${date.split('.')[1]}.${date.split('.')[2]}</div>
                `;
        dateBox.dataset.date = date;

        dateBox.addEventListener('click', () => {
            updateVisits(date);
            setActiveDate(dateBox);
        });

        dateNav.appendChild(dateBox);
    });
};

document.addEventListener('DOMContentLoaded', () => {
    createSelectableDates();

    const dateNav = document.getElementById('date-nav');
    const firstDateBox = dateNav.querySelector('.date-box');
    firstDateBox.classList.add('active');
    updateVisits(firstDateBox.dataset.date);

});

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
