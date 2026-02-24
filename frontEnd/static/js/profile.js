async function getUserInfo() {
    try {
        const response=await fetch('/habits/main/getHabits', {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        
        if (!response.ok) {
            alert('Произошла ошибка при получении привычек или ещё не было создано ни одной привычки');
            return;
        }
        
        const habits=await response.json();
        const rows=document.querySelector('#tbodyHabits');
        rows.innerHTML='';
        
        habits.forEach(habit=> {
            rows.append(row(habit));
        });
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

async function createHabit() {
    window.location.href='/habits/main/createNewHabit';
}

async function editHabit(event, habit_id, habit_name, habit_description, habit_goal) {
    event.preventDefault();
    const newName=prompt('Введите новое название привычки:', habit_name);
    if (!newName) return;
    const newDescription=prompt('Введите новое описание:', habit_description || '');
    const newGoal=prompt('Введите новую цель (количество дней):', habit_goal || '30');
    if (!newGoal || isNaN(newGoal) || parseInt(newGoal)<= 0) {
        alert('Цель должна быть положительным числом');
        return;
    }
    try {
        const response=await fetch('/habits/main/updateHabit', {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: habit_id,
                name: newName,
                description: newDescription,
                goal: parseInt(newGoal)
            })
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при обновлении привычки');
            return;
        }
        const result=await response.json();
        alert('Привычка успешно обновлена!');
        const rowToUpdate=document.querySelector(`tr[data-rowid="${habit_id}"]`);
        if (rowToUpdate) {
            rowToUpdate.replaceWith(row(result));
        } else {
            get_habits();
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

async function deleteHabit(event, habit_id, habit_name) {
    event.preventDefault();
    if (!confirm(`Вы уверены, что хотите удалить привычку "${habit_name}"?`)) {
        return;
    }
    try {
        const response=await fetch(`/habits/main/delete/${habit_id}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) {
            const errorData=await response.json();
            alert(errorData.detail || 'Произошла ошибка при удалении привычки');
            return;
        }
        const result=await response.json();
        alert(result.message);
        const rowToRemove=document.querySelector(`tr[data-rowid="${habit_id}"]`);
        if (rowToRemove) {
            rowToRemove.remove();
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте снова');
    }
}

function row(habit) {
    const tr=document.createElement('tr');
    tr.setAttribute('data-rowid', habit.id);

    const nameTd=document.createElement('td');
    nameTd.append(habit.name);
    tr.append(nameTd);

    const descriptionTd=document.createElement('td');
    descriptionTd.append(habit.description || '');
    tr.append(descriptionTd);

    const goalTd=document.createElement('td');
    goalTd.append(habit.goal || '0');
    tr.append(goalTd);

    const progressTd=document.createElement('td');
    progressTd.append(habit.progress || '0');
    tr.append(progressTd);

    const actionsTd=document.createElement('td');

    const editButton=document.createElement('button');
    editButton.className='edit-btn';
    editButton.addEventListener('click', (e)=> editHabit(
        e, 
        habit.id, 
        habit.name, 
        habit.description, 
        habit.goal
    ));
    actionsTd.append(editButton);

    const deleteButton=document.createElement('button');
    deleteButton.className='delete-btn';
    deleteButton.addEventListener('click', (e)=> deleteHabit(e, habit.id, habit.name));
    actionsTd.append(deleteButton);

    tr.appendChild(actionsTd);
    return tr;
}