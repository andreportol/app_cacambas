const quantidadeInput = document.getElementById('quantidade');
const somaButton = document.getElementById('soma');
const subtracaoButton = document.getElementById('subtracao');

somaButton.addEventListener('click', () => {
    let currentValue = parseInt(quantidadeInput.value) || 0;
    if (currentValue < 10) {
        quantidadeInput.value = currentValue + 1;
    }
});

subtracaoButton.addEventListener('click', () => {
    let currentValue = parseInt(quantidadeInput.value) || 0;
    if (currentValue > 1) {
        quantidadeInput.value = currentValue - 1;
    }
});
