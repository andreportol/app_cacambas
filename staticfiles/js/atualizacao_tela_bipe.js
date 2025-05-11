document.addEventListener("DOMContentLoaded", function () {
    let contagemAnterior = 0;

    async function atualizarDados() {
        try {
            const response = await fetch("/dashboard/dados/");
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }

            const dados = await response.json();

            document.querySelector(".card-value.text-info").textContent = dados.novos;
            document.querySelector(".card-value.text-danger").textContent = dados.pendentes;
            document.querySelector(".card-value.text-warning").textContent = dados.atendidos;
            document.querySelector(".card-value.text-success").textContent = dados.finalizados;

            if (dados.novos > contagemAnterior) {
                tocarBipe(); // Chama a função do HTML
            }

            contagemAnterior = dados.novos;
        } catch (error) {
            console.error("Erro ao atualizar dados:", error);
        }
    }

    atualizarDados(); // Inicial
    setInterval(atualizarDados, 10000); // A cada 10s
});
