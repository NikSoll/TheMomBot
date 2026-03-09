document.addEventListener('DOMContentLoaded', function() {
    const addBtn = document.getElementById('add-master');
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            const container = document.getElementById('masters-container');
            const newMaster = document.createElement('div');
            newMaster.className = 'master-item';
            newMaster.innerHTML = `
                <input type="text" name="master_name[]" placeholder="Имя мастера" value="Новый мастер">
                <input type="text" name="master_emoji[]" placeholder="Эмодзи" value="👤" maxlength="2">
                <button type="button" class="remove-master">❌</button>
            `;
            container.appendChild(newMaster);
        });
    }

    //удаление мастеров
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-master')) {
            e.target.parentElement.remove();
        }
    });
});