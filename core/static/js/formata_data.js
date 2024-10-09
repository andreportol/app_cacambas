// Função para definir a data mínima como o dia atual e limitar o valor máximo da data de retirada
window.onload = function() {
    // Obtém a data atual
    const today = new Date().toISOString().split('T')[0];

    // Define o 'min' do campo 'data_inicio' como o dia atual
    const dataInicioElement = document.getElementById('data_inicio');
    const dataRetiradaElement = document.getElementById('data_retirada');
    document.getElementById('data_inicio').setAttribute('min', today);
    
    dataInicioElement.setAttribute('min', today);

    // Função para atualizar a data máxima de 'data_retirada' quando 'data_inicio' é selecionado
    dataInicioElement.onchange = function() {
        const dataInicioValue = new Date(dataInicioElement.value);
        
        // Adiciona 9 dias à data de início
        const dataMaxRetirada = new Date(dataInicioValue);
        dataMaxRetirada.setDate(dataMaxRetirada.getDate() + 9);

        // Formata a data máxima para o valor de input (YYYY-MM-DD)
        const dataMaxFormatted = dataMaxRetirada.toISOString().split('T')[0];

        // Define o 'min' do campo 'data_retirada'
        dataRetiradaElement.setAttribute('min', dataInicioElement.value);
        
        // Define o 'max' do campo 'data_retirada'
        dataRetiradaElement.setAttribute('max', dataMaxFormatted);
    };
};

    