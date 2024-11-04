document.addEventListener("DOMContentLoaded", function() {
    const phoneInput = document.querySelector('input[name="telefone_cliente"]');
    
    phoneInput.addEventListener("input", function() {
        let value = phoneInput.value.replace(/\D/g, ""); // Remove todos os caracteres não numéricos
        if (value.length > 11) value = value.slice(0, 11); // Limita a 11 dígitos
        
        // Aplica a máscara
        value = value.replace(/^(\d{2})(\d)/, "($1) $2"); // Adiciona parênteses ao DDD
        value = value.replace(/(\d{5})(\d{4})$/, "$1-$2"); // Adiciona o traço
        
        phoneInput.value = value; // Atualiza o valor do input com a máscara
    });
});