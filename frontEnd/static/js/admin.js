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
        const response=await fetch(`/admin/main/makeSuperuser/${profile.id}`, {
            method: 'PUT',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при передаче прав суперпользователя!');
            return;
        } else {
            alert('Пользователь стал суперюзером!');
            window.location.reload()
        }
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

async function getAchievements() {
    try {
        const response=await fetch('/admin/main/getAchievements', {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        if (response.status===404) {
            const data=await response.json();
            alert(data.message || 'Ни одного достижения ещё не было создано');
            return;
        }
        if (!response.ok) {
            alert('Произошла ошибка при получении достижений');
            return;
        }
        const achievements=await response.json();
        const listContainer=document.querySelector('#Achievements');
        if (achievements.length===0) {
            listContainer.innerHTML='Нет доступных достижений';
            return;
        }
        listContainer.innerHTML='';
        achievements.forEach(achievement=> {
            listContainer.append(createAchievementsItem(achievement));
        });
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

function createAchievementsItem(achievement) {
    const li=document.createElement('li');
    li.className='achievement-item';

    const achievementInfo=document.createElement('div');
    achievementInfo.className='achievement-info';
    
    const nameElement=document.createElement('p');
    nameElement.id='achievement-nickname';
    nameElement.className='achievement-nickname';
    nameElement.textContent=achievement.name;
    
    const descriptionElement=document.createElement('p');
    descriptionElement.id='achievement-description';
    descriptionElement.className='achievement-description';
    descriptionElement.textContent=achievement.description;

    const typeElement=document.createElement('p');
    typeElement.id='achievement-type';
    typeElement.className='achievement-type';
    typeElement.textContent=achievement.type;

    const goalElement=document.createElement('p');
    goalElement.id='achievement-goal';
    goalElement.className='achievement-goal';
    goalElement.textContent=achievement.goal;

    achievementInfo.appendChild(nameElement);
    achievementInfo.appendChild(descriptionElement);
    achievementInfo.appendChild(typeElement);
    achievementInfo.appendChild(goalElement);

    li.appendChild(achievementInfo);
    
    return li;
}

async function createAchievement() {
    const Name=prompt('Введите название для достижения:');
    if (!Name) {return};
    const Description=prompt('Введите описание для достижения:');
    if (!Description) {return};
    const Type=await selectAchievementType();
    if (!Type) {return};
    const Goal=prompt('Введите цель для достижения (число):');
    if (!Goal) {return};
    if (isNaN(Goal)) {
        alert('Цель должна быть числом');
        return;
    }
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
                type: Type,
                goal: Goal
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

async function selectAchievementType() {
    try {
        const response=await fetch('/admin/main/getAchievementTypes');
        const types=await response.json();
        let message='Выберите тип достижения (введите номер):\n\n';
        types.forEach((type, index)=> {
            message+=`${index + 1}.${type.label} (${type.value})\n`;
        });
        const choice=prompt(message);
        if (!choice) return null;
        const index=parseInt(choice)-1;
        if (index>=0 && index<types.length) {
            return types[index].value;
        } else {
            alert('Неверный выбор! Попробуйте снова.');
            return selectAchievementType();
        }
    } catch (error) {
        console.error('Ошибка при получении типов:', error);
        alert('Не удалось получить список типов достижений');
        return null;
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
            getAchievements()
        });
    } else {
        getProfiles();
        getAchievements()
    }
})();