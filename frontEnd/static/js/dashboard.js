async function getDailyListHabits() {
    try {
        const response=await fetch('/dashboard/main/getActiveHabits');
        if (!response.ok) {
            alert('Привычек на сегодня нет или ошибка сервера');
            return;
        }
        const habits=await response.json();
        const listContainer=document.querySelector('#dailyHabitsList');
        listContainer.innerHTML='';
        habits.forEach(habit=> {
            const habitItem=createHabitItem(habit);
            listContainer.appendChild(habitItem);
        });
        dailyUpdate(habits)
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Ошибка загрузки привычек');
            }
}

function createHabitItem(habit) {
    const li=document.createElement('li');
    li.className='habit-item';
    const checkbox=document.createElement('input');
    checkbox.type='checkbox';
    checkbox.className='habit-checkbox';
    checkbox.checked=habit.complit_today || false;
    checkbox.dataset.habitId=habit.id;
    checkbox.addEventListener('change', async function() {
    if (this.checked) {
        const success=await complitHabit(this.dataset.habitId);
        if (!success) {
            this.checked=false;
        }
    }
    else {
        alert('Сегодня эта задача уже выполнена!')
        window.location.reload()
    }
    });

    const habitInfo=document.createElement('div');
    habitInfo.className='habit-info';
    
    const nameElement=document.createElement('h3');
    nameElement.className='habit-name';
    nameElement.textContent=habit.name;
    
    const descriptionElement=document.createElement('p');
    descriptionElement.className='habit-description';
    descriptionElement.textContent=habit.description;
    
    const progressElement=document.createElement('div');
    progressElement.className='habit-progress';
    const progressText=document.createElement('span');
    progressText.textContent=`Прогресс: ${habit.progress || 0}/${habit.goal} выполнений`;
    
    const progressBar=document.createElement('div');
    progressBar.className='progress-bar';
    const progressPercentage=habit.goal>0 ? Math.min(100, ((habit.progress || 0)/habit.goal)*100):0;
    
    const progressFill=document.createElement('div');
    progressFill.className='progress-fill';
    progressFill.style.width=`${progressPercentage}%`;
    progressBar.appendChild(progressFill);
    
    progressElement.appendChild(progressText);
    progressElement.appendChild(progressBar);
    
    habitInfo.appendChild(nameElement);
    habitInfo.appendChild(descriptionElement);
    habitInfo.appendChild(progressElement);
    
    li.appendChild(checkbox);
    li.appendChild(habitInfo);
    
    return li;
}

async function complitHabit(habit_id) {
    try {
        const response=await fetch(`/dashboard/main/complitActiveHabit/${habit_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            const error=await response.json();
            alert(error.detail || 'Ошибка при отметке привычки');
            return false;
        }
        const result=await response.json();
        alert(result.message);
        window.location.reload()
        return true;
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при отметке привычки');
        return false;
    }
}

async function dailyUpdate(habits) {
    for (const habit of habits)
    try {
        const response=await fetch(`/dashboard/main/dailyUpdate/${habit.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            const error=await response.json();
            alert(error.detail || 'Ошибка ежедневного обновления статуса');
            continue
        }
        const data=await response.json()
        alert(data.message)
        return true;
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка ежедневного обновления статуса');
        return false;
    }
}

function profileInfo() {
    window.location.href='/profile/main';
}

async function logoutFunction() {
    try {
        let response=await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            window.location.href='/auth/login';
        } else {
            const errorData=await response.json();
            console.error('Ошибка при выходе:', errorData.message || response.statusText);
        }
    } catch (error) {
        console.error('Ошибка сети', error);
    }
}

(function initializeApp() {
    if (document.readyState==='loading') {
        document.addEventListener('DOMContentLoaded', ()=> {
            getDailyListHabits();
        });
    } else {
        getDailyListHabits();
    }

    // document.addEventListener('visibilitychange', ()=> {
    //     if (document.visibilityState==='visible') {
    //         getDailyListHabits();
    //     }
    // });
})();