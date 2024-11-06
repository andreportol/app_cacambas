// scripts.js
function formatarTelefone(input) {
    let valor = input.value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
    let formatado = valor;

    if (valor.length <= 2) {
        formatado = `(${valor}`;
    } else if (valor.length <= 7) {
        formatado = `(${valor.slice(0, 2)}) ${valor.slice(2)}`;
    } else {
        formatado = `(${valor.slice(0, 2)}) ${valor.slice(2, 7)}-${valor.slice(7, 11)}`;
    }
    
    input.value = formatado;
}
