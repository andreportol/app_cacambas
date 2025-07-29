document.addEventListener('DOMContentLoaded', function() {
    const cnpjInput = document.getElementById('cnpj');

    // Permite apenas números e aplica a máscara
    cnpjInput.addEventListener('input', function(e) {
      // Remove tudo que não é número
      let value = e.target.value.replace(/\D/g, '');

      // Aplica a máscara: XX.XXX.XXX/XXXX-XX
      if (value.length > 2) {
        value = value.substring(0, 2) + '.' + value.substring(2);
      }
      if (value.length > 6) {
        value = value.substring(0, 6) + '.' + value.substring(6);
      }
      if (value.length > 10) {
        value = value.substring(0, 10) + '/' + value.substring(10);
      }
      if (value.length > 15) {
        value = value.substring(0, 15) + '-' + value.substring(15, 17);
      }

      // Atualiza o valor do campo
      e.target.value = value;
    });

    // Impede a digitação de caracteres não numéricos
    cnpjInput.addEventListener('keypress', function(e) {
      if (e.key.match(/\D/)) {
        e.preventDefault();
      }
    });
  });
