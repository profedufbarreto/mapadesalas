const listaSalas = [101, 102, 201, 202, 203, 204, 301, 302, 303, 304, 305, 401, 402, 403, 404, 405, 406];

function atualizarMural() {
    const grid = document.getElementById('grid-tv');
    const displayTurno = document.getElementById('display-turno');
    
    // Atualiza o Turno
    displayTurno.innerText = localStorage.getItem('turno') || "NÃO DEFINIDO";

    let htmlFinal = "";

    listaSalas.forEach(num => {
        const nomeProf = localStorage.getItem('s' + num);

        // LÓGICA: Só adiciona o HTML se o campo não estiver vazio
        if (nomeProf && nomeProf.trim() !== "") {
            htmlFinal += `
                <div class="card">
                    <span class="room-no">SALA ${num}</span>
                    <div class="prof-name">${nomeProf.toUpperCase()}</div>
                </div>
            `;
        }
    });

    // Se nenhuma sala tiver aula, mostra um aviso
    if (htmlFinal === "") {
        grid.innerHTML = "<h2 style='grid-column: 1/-1; text-align:center;'>Nenhuma aula agendada para este turno.</h2>";
    } else {
        grid.innerHTML = htmlFinal;
    }
}

// Verifica mudanças a cada 2 segundos
setInterval(atualizarMural, 2000);
atualizarMural();