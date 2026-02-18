const salas = [101, 102, 201, 202, 203, 204, 301, 302, 303, 304, 305, 401, 402, 403, 404, 405, 406];

// LER EXCEL
document.getElementById('excel-file').addEventListener('change', function(e) {
    const reader = new FileReader();
    reader.readAsArrayBuffer(e.target.files[0]);
    reader.onload = function(e) {
        const data = new Uint8Array(reader.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const folha = workbook.Sheets[workbook.SheetNames[0]];
        const dadosRaw = XLSX.utils.sheet_to_json(folha, { range: 1 });

        // Limpa campos
        salas.forEach(num => {
            document.getElementById('p' + num).value = "";
            document.getElementById('t' + num).value = "";
        });

        dadosRaw.forEach(linha => {
            const colunas = {};
            Object.keys(linha).forEach(key => colunas[key.trim().toLowerCase()] = linha[key]);
            
            const num = colunas["sala"];
            if(document.getElementById('p' + num)) {
                document.getElementById('p' + num).value = colunas["professor"] || "";
                document.getElementById('t' + num).value = colunas["turma"] || "";
            }
        });
        exibirMensagem("✅ Excel carregado!", "blue");
    };
});

// SALVAR
document.getElementById('btn-save').onclick = function() {
    localStorage.setItem('turno', document.getElementById('turno').value);
    salas.forEach(num => {
        const p = document.getElementById('p' + num).value;
        const t = document.getElementById('t' + num).value;
        localStorage.setItem('s' + num, p + "|" + t); // Salva com separador |
    });
    exibirMensagem("🚀 ATUALIZADO!", "green");
};

function exibirMensagem(txt, cor) {
    const m = document.getElementById('message');
    m.innerText = txt; m.style.color = cor;
    setTimeout(() => m.innerText = "", 4000);
}