async function getUserInfo(profile_id) {
    try {
        const response=await fetch(`/profile/main/${profile_id}/info`, {
            method: 'GET',
            headers: { 
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
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

async function updateProfile(profile_id, profile_nickname, profile_password, profile_email, profile_phone_number, profile_city) {
    const newNickname=prompt('Введите новый никнейм:', profile_nickname);
    if (!newNickname) return;
    const newPassword=prompt('Введите новый пароль:', profile_password);
    if (!newPassword) return;
    const newEmail=prompt('Введите новую почту:', profile_email);
    if (!newEmail) return;
    const newPhone_number=prompt('Введите новый номер телефона:', profile_phone_number);
    if (!newPhone_number) return;
    const newCity=prompt('Введите новый город:', profile_city);
    if (!newCity) return;

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
        const nicknameElement=document.querySelector("#profile-nickname");
        nicknameElement.innerHTML=result['nickname'];
        const passwordElement=document.querySelector("#profile-password");
        passwordElement.innerHTML=result['password'];
        const emailElement=document.querySelector("#profile-email");
        emailElement.innerHTML=result['email'];
        const phone_numberElement=document.querySelector("#profile-phone_number");
        phone_numberElement.innerHTML=result['phone_number'];
        const cityElement=document.querySelector("#profile-city");
        cityElement.innerHTML=result['city'];
        window.location.reload()
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
    nicknameElement.id='profile-nickname';
    nicknameElement.className='profile-nickname';
    nicknameElement.textContent=profile.nickname;
    
    const passwordElement=document.createElement('p');
    passwordElement.id='profile-password';
    passwordElement.className='profile-password';
    passwordElement.textContent=profile.password;

    const emailElement=document.createElement('p');
     emailElement.id='profile-email';
    emailElement.className='profile-email';
    emailElement.textContent=profile.email;

    const phone_numberElement=document.createElement('p');
    phone_numberElement.id='profile-phone_number';
    phone_numberElement.className='profile-phone_number';
    phone_numberElement.textContent=profile.phone_number;

    const cityElement=document.createElement('p');
    cityElement.id='profile-city';
    cityElement.className='profile-city';
    cityElement.textContent=profile.city;

    profileInfo.appendChild(nicknameElement);
    profileInfo.appendChild(passwordElement);
    profileInfo.appendChild(emailElement);
    profileInfo.appendChild(phone_numberElement);
    profileInfo.appendChild(cityElement);

    const actionsDiv=document.createElement('div');
    actionsDiv.className='profile-actions';

    const updateButton=document.createElement('button');
    updateButton.className='info-change';
    updateButton.textContent='Изменить данные профиля'
    updateButton.addEventListener('click', ()=> updateProfile(
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

function getProfileIdFromUrl() {
    const matches=window.location.pathname.match(/\/profile\/main\/(\d+)/);
    return matches ? matches[1] : null;
}

(function initializeApp() {
    const profileId=getProfileIdFromUrl();
    if (document.readyState==='loading') {
        document.addEventListener('DOMContentLoaded', ()=> {
            getUserInfo(profileId);
        });
    } else {
        getUserInfo(profileId);
    }
})();