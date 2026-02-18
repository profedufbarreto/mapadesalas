document.getElementById('btn-save').onclick = function() {
    // Salva o turno
    const turno = document.getElementById('turno').value;
    localStorage.setItem('turno', turno);

    // Salva cada sala automaticamente
    const inputs = document.querySelectorAll('#form-salas input');
    inputs.forEach(input => {
        localStorage.setItem(input.id, input.value);
    });

    alert("Mapa atualizado com sucesso!");
};