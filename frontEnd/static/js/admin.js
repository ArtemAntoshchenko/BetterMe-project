async function getProfiles() {
    try {
        const response=await fetch('/admin/main/info', {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) {
            alert('Произошла ошибка при получении данных о пользователях');
            return;
        }
        const profiles=await response.json();
        const rows=document.querySelector('#tbodyUsers');
        rows.innerHTML='';
        profiles.forEach(profile=> {
            rows.append(row(profile));
        });
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

async function deleteProfile(event, profile_id, profile_nickname) {
    event.preventDefault();
    if (!confirm(`Вы уверены, что хотите удалить профиль "${profile_nickname}"?`)) {
        return;
    }
    try {
        const response=await fetch(`/admin/main/delete/${profile_id}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при удалении профиля!');
            return;
        }
        const result=await response.json();
        alert(result.message);
        const rowToRemove=document.querySelector(`tr[data-rowid="${profile_id}"]`);
        if (rowToRemove) {
            rowToRemove.remove();
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

async function makeSuperuser(event, profile) {
    event.preventDefault();
    if (profile.super_user==true) {
        alert('Профиль уже имеет права суперпользователя');
        return;
    }
    if (!confirm(`Вы уверены, что хотите сделать профиль "${profile.nickname}" суперпользователем?`)) {
        return;
    }
    try {
        const response=await fetch(`/admin/main/delete/${profile.id}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при передаче прав суперпользователя!');
            return;
        }
        // const result=await response.json();
        alert('Пользователь стал суперюзером!');
        const rowToUpdate=document.querySelector(`tr[data-rowid="${profile.id}"]`);
        if (rowToUpdate) {
            rowToUpdate.replaceWith(row(profile));
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

function row(profile) {
    const tr=document.createElement('tr');
    tr.setAttribute('data-rowid', profile.id);

    const nicknameTd=document.createElement('td');
    nicknameTd.append(profile.nickname);
    tr.append(nicknameTd);

    const loginTd=document.createElement('td');
    loginTd.append(profile.login);
    tr.append(loginTd);

    const emailTd=document.createElement('td');
    emailTd.append(profile.email);
    tr.append(emailTd);

    const phone_numberTd=document.createElement('td');
    phone_numberTd.append(profile.phone_number);
    tr.append(phone_numberTd);

    const first_nameTd=document.createElement('td');
    first_nameTd.append(profile.first_name);
    tr.append(first_nameTd);

    const last_nameTd=document.createElement('td');
    last_nameTd.append(profile.last_name);
    tr.append(last_nameTd);

    const cityTd=document.createElement('td');
    cityTd.append(profile.city);
    tr.append(cityTd);

    const date_of_birthTd=document.createElement('td');
    date_of_birthTd.append(profile.date_of_birth);
    tr.append(date_of_birthTd);

    const premiumTd=document.createElement('td');
    premiumTd.append(profile.premium);
    tr.append(premiumTd);

    const super_userTd=document.createElement('td');
    super_userTd.append(profile.super_user);
    tr.append(super_userTd);

    const actionsTd=document.createElement('td');

    const deleteButton=document.createElement('button');
    deleteButton.className='delete-btn';
    deleteButton.innerHTML='Удалить профиль'
    deleteButton.addEventListener('click', (e)=> deleteProfile(e, profile.id, profile.nickname));
    actionsTd.append(deleteButton);

    const makeSuperuserButton=document.createElement('button');
    makeSuperuserButton.className='makeSuperuser-btn';
    makeSuperuserButton.innerHTML='Дать профилю права суперпользователя'
    makeSuperuserButton.addEventListener('click', (e)=> makeSuperuser(e, profile));
    actionsTd.append(makeSuperuserButton);

    tr.appendChild(actionsTd);
    return tr;
}

async function createAchievement() {
    const Name=prompt('Введите название для достижения:');
    if (!Name) {return};
    const Description=prompt('Введите описание для достижения:');
    if (!Description) {return};
    try {
        const response=await fetch('/admin/main/createAchievement', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: Name,
                description: Description,
            })
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при создании достижения');
            return;
        }
        alert('Достижение успешно создано!');
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

async function deleteAchievement() {
    const achievementName=prompt('Введите название достижения, которое вы хотите удалить:');
    if (!achievementName) {return}
    if (!confirm(`Вы уверены, что хотите удалить достижение "${achievementName}"?`)) {
        return;
    }
    try {
        const response=await fetch(`/admin/main/deleteAchievement/${achievementName}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при удалении достижения! Возможно вы ввели не верное название!');
            return;
        }
        const result=await response.json();
        alert(result.message);
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

(function initializeApp() {
    if (document.readyState==='loading') {
        document.addEventListener('DOMContentLoaded', ()=> {
            getProfiles();
        });
    } else {
        getProfiles();
    }
})();