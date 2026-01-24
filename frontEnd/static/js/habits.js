async function get_habits() {
const respons=await fetch('/habits/main/getHabits', {method:'GET', headers:{'Accept':'application/json'}})
if (respons.ok === true){
    const habits=await respons.json()
    const rows=document.querySelector('#tbodyHabits')
    habits.forEach(habit=>rows.append(row(habit)))
}
}

async function createCar(carName,carMark,carColor,carCost) {
    const respons=await fetch('/cars', {
        method:'POST', 
        headers: {'Accept':'application/json', 'Content-Type': 'application/json'}, 
        body: JSON.stringify({name:carName, mark:carMark, color:carColor, cost:carCost})
    }) 
    if (respons.ok===true){
        const car=await respons.json()
        document.querySelector('#tbodyCars').append(row(car))
    }
}

async function editCar(carId,carName,carMark,carColor,carCost) {
    const respons=await fetch('/cars', {
        method:'PUT',
        headers:{'Accept':'application/json', 'Content-Type': 'application/json'},
        body: JSON.stringify({id:carId, name:carName, mark:carMark, color:carColor, cost:carCost})
    })
    if (respons.ok===true){
        const car=await respons.json()
        document.querySelector(`tr[data-rowid='${car.id}']`).replaceWith(row(car))
    }
    else {
        const error=await respons.json()
        console.log(error.message)
    }
}

async function deleteCar(id) {
    const respons=await fetch(`/cars/${id}`, {
        method:'DELETE',
        headers:{'Accept':'application/json'}
    })
    if (respons.ok===true){
        const car=await respons.json()
        document.querySelector(`tr[data-rowid='${car.id}']`).remove()
    }
    else {
        const error=await respons.json()
        console.log(error.message)
    }
}



function row(habit) {
    const tr=document.createElement('tr')
    tr.setAttribute('data-rowid', habit.id)

    const nameTd=document.createElement('td')
    nameTd.append(habit.name)
    tr.append(nameTd)

    const descriptionTd=document.createElement('td')
    markTd.append(habit.description)
    tr.append(descriptionTd)

    const goalTd=document.createElement('td')
    costTd.append(habit.goal)
    tr.append(goalTd)

    const progressTd=document.createElement('td')
    costTd.append(habit.progress)
    tr.append(progressTd)

    const complitTd=document.createElement('td')
    colorTd.append(habit.complit)
    tr.append(complitTd)

    const linksTd=document.createElement('td')

    const createLink=document.createElement('button')
    buyLink.append('Купить автомобиль')
    buyLink.addEventListener('click', async()=>await buyCar(car.id, car.name, car.mark, car.color, car.cost))
    linksTd.append(createLink)

    const editHabit=document.createElement('button')
    editCar.append('Изменить автомобиль')
    editCar.addEventListener('click', async()=>await getCar(car.id))
    linksTd.append(editCar)

    const deleteLink=document.createElement('button')
    deleteLink.append('Удалить автомобиль')
    deleteLink.addEventListener('click', async()=>await deleteCar(car.id))
    linksTd.append(deleteLink)

    tr.appendChild(linksTd)
    return tr
}