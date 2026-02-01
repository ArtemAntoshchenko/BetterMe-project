async function get_daily_list_habits() {
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
    
    // Добавляем обработчик для обновления статуса
    checkbox.addEventListener('change', function() {
        updateHabitStatus(habit.id, this.checked);
    });
    
    // Создаем контейнер для информации о привычке
    const habitInfo = document.createElement('div');
    habitInfo.className = 'habit-info';
    
    // Название привычки
    const nameElement = document.createElement('h3');
    nameElement.className = 'habit-name';
    nameElement.textContent = habit.name;
    
    // Описание привычки
    const descriptionElement = document.createElement('p');
    descriptionElement.className = 'habit-description';
    descriptionElement.textContent = habit.description || 'Без описания';
    
    // Прогресс
    const progressElement = document.createElement('div');
    progressElement.className = 'habit-progress';
    
    const progressText = document.createElement('span');
    progressText.textContent = `Прогресс: ${habit.progress || 0}/${habit.goal} дней`;
    
    // Прогресс-бар (опционально)
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    const progressPercentage = habit.goal > 0 ? Math.min(100, ((habit.progress || 0) / habit.goal) * 100) : 0;
    
    const progressFill = document.createElement('div');
    progressFill.className = 'progress-fill';
    progressFill.style.width = `${progressPercentage}%`;
    progressBar.appendChild(progressFill);
    
    progressElement.appendChild(progressText);
    progressElement.appendChild(progressBar);
    
    // Собираем все вместе
    habitInfo.appendChild(nameElement);
    habitInfo.appendChild(descriptionElement);
    habitInfo.appendChild(progressElement);
    
    li.appendChild(checkbox);
    li.appendChild(habitInfo);
    
    return li;
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

get_daily_list_habits()