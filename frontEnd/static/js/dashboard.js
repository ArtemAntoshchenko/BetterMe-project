async function get_daily_list_habits() {
    const respons=await fetch('/main/getActiveHabits')
    if (respons.ok === true){
        const habits=await respons.json()
        const rows=document.querySelector('#dailyHabitsList')
        habits.forEach(habit=>rows.append(habit))
    }
}

async function complete_task(task_id) {
    const respons=await fetch('')
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