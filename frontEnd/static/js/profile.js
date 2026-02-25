async function getUserInfo() {
    try {
        const response=await fetch('/profile/main/info', {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) {
            alert('Произошла ошибка при получении данных профиля');
            return;
        }
        const profile=await response.json();
        const listContainer=document.querySelector('#userInfo');
        listContainer.innerHTML='';
        const profileItem=createProfileItem(profile);
        listContainer.appendChild(profileItem);
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

async function updateProfile(event, profile_id, profile_nickname, profile_password, profile_email, profile_phone_number, profile_city) {
    event.preventDefault();
    const newNickname=prompt('Введите новый никнейм:', profile_nickname);
    const newPassword=prompt('Введите новый пароль:', profile_password);
    const newEmail=prompt('Введите новую почту:', profile_email);
    const newPhone_number=prompt('Введите новый номер телефона:', profile_phone_number);
    const newCity=prompt('Введите новый город:', profile_city);

    try {
        const response=await fetch('/profile/main/info/update', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: profile_id,
                nickname: newNickname,
                password: newPassword,
                email: newEmail,
                phone_number: newPhone_number,
                city: newCity,
            })
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при обновлении привычки');
            return;
        }
        const result=await response.json();
        alert('Профиль успешно обновлен!');
        const itemToUpdate=document.querySelector(`tr[data-rowid="${profile_id}"]`);
        if (itemToUpdate) {
            itemToUpdate.replaceWith(row(result));
        } else {
            getUserInfo();
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

function createProfileItem(profile) {
    const li=document.createElement('li');
    li.className='profile-item';

    const profileInfo=document.createElement('div');
    profileInfo.className='profile-info';
    
    const nicknameElement=document.createElement('p');
    nicknameElement.className='profile-nickname';
    nicknameElement.textContent=profile.nickname;
    
    const passwordElement=document.createElement('p');
    passwordElement.className='profile-password';
    passwordElement.textContent=profile.password;

    const emailElement=document.createElement('p');
    emailElement.className='profile-email';
    emailElement.textContent=profile.email;

    const phone_numberElement=document.createElement('p');
    phone_numberElement.className='profile-phone_number';
    phone_numberElement.textContent=profile.phone_number;

    const cityElement=document.createElement('p');
    cityElement.className='profile-city';
    cityElement.textContent=profile.city;

    profileInfo.appendChild(nicknameElement);
    profileInfo.appendChild(passwordElement);
    profileInfo.appendChild(emailElement);
    profileInfo.appendChild(phone_numberElement);
    profileInfo.appendChild(cityElement);

    const actionsDiv=document.createElement('div');
    profileInfo.className='profile-info';

    const updateButton=document.createElement('button');
    updateButton.className='info-change';
    updateButton.addEventListener('click', (e)=> updateProfile(
        e, 
        profile.id, 
        profile.nickname, 
        profile.password, 
        profile.email,
        profile.phone_number,
        profile.city
    ));
    actionsDiv.appendChild(updateButton);
    
    li.appendChild(profileInfo);
    li.appendChild(actionsDiv);
    
    return li;
}

(function initializeApp() {
    if (document.readyState==='loading') {
        document.addEventListener('DOMContentLoaded', ()=> {
            getUserInfo();
        });
    } else {
        getUserInfo();
    }
})();