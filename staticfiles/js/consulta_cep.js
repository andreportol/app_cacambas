document.getElementById('cep').addEventListener('input', function() {
    let cep = this.value.replace(/\D/g, '');  // Remove caracteres não numéricos

    // Máscara do CEP no formato 00000-000
    if (cep.length > 5) {
        cep = cep.slice(0, 5) + '-' + cep.slice(5, 8);
    }

    this.value = cep;  // Atualiza o valor do campo com a máscara correta

    // Verifica se o CEP tem 8 números (9 com o hífen)
    if (cep.length === 9) {
        // Limpa os campos antes de realizar a nova busca
        document.getElementById('logradouro').value = '';
        document.getElementById('cidade').value = '';
        document.getElementById('bairro').value = '';
        document.getElementById('numero').value = '';
        document.getElementById('numero').focus();
        // Realiza a busca no ViaCEP
        fetch(`https://viacep.com.br/ws/${cep.replace('-', '')}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById('logradouro').value = data.logradouro;
                    document.getElementById('cidade').value = data.localidade;
                    document.getElementById('bairro').value = data.bairro;
                   
                    // Aqui você aplica a borda vermelha ao campo "Número"
                    document.getElementById('numero').style.border = '4px solid red';
                
                } else {
                    alert('CEP não encontrado.');
                    limparCampos();  // Limpa os campos caso o CEP não seja encontrado
                }
            })
            .catch(error => {
                console.error('Erro ao buscar o CEP:', error);
            });
    }else {
        limparCampos();  // Limpa os campos se o CEP estiver incompleto
    }
});

// Função para limpar os campos de logradouro e cidade
function limparCampos() {
    document.getElementById('logradouro').value = '';
    document.getElementById('cidade').value = '';
    document.getElementById('numero').value = '';
    document.getElementById('bairro').value = '';
    document.getElementById('numero').style.border = 'none';
}

/**
Explicação:
1) Verificação do CEP: O evento keyup verifica se o usuário digitou o último dígito do CEP.
2) Requisição ViaCEP: Ao detectar que o CEP tem 8 dígitos, o código faz a requisição para a API do ViaCEP.
3) Preenchimento dos campos: Quando a resposta da API é retornada com sucesso (e sem erro), os campos de "Logradouro" e "Cidade" são preenchidos.
4) Alteração da borda: Após a consulta, a borda do campo de número é alterada para vermelha (2px solid red).

*/

