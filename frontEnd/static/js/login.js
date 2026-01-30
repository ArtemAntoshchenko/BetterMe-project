async function loginFunction(event) {
    event.preventDefault(); 
    const form=document.getElementById('login-form');
    const formData=new FormData(form);
    const data=Object.fromEntries(formData.entries());
    try {
        const response=await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const errorData = await response.json();
            displayErrors(errorData);
            return; 
        }
        const result=await response.json();
        if (result.message) { 
            window.location.href='/dashboard/main'; 
        } else {
            alert(result.message || 'Неизвестная ошибка');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
    }
}