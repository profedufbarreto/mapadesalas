const salas = [101, 102, 201, 202, 203, 204, 301, 302, 303, 304, 305, 401, 402, 403, 404, 405, 406];

function atualizarMural() {
    const grid = document.getElementById('grid-tv');
    document.getElementById('display-turno').innerText = localStorage.getItem('turno') || "---";
    
    let htmlFinal = "";

    salas.forEach(num => {
        const dados = localStorage.getItem('s' + num);
        if (dados) {
            const [prof, turma] = dados.split('|');
            if (prof && prof.trim() !== "") {
                htmlFinal += `
                    <div class="card">
                        <div class="card-header">SALA ${num}</div>
                        <div class="card-body">
                            <div class="prof-name">${prof.toUpperCase()}</div>
                            ${turma ? `<div class="class-name">${turma}</div>` : ""}
                        </div>
                    </div>
                `;
            }
        }
    });

    grid.innerHTML = htmlFinal || "<h2 style='color:gray'>Nenhuma aula agora</h2>";
}

setInterval(atualizarMural, 3000);
atualizarMural();