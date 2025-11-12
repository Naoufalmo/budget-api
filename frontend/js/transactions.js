// Gestion des transactions
const Transactions = {
    // Charger les données
    async loadData() {
        try {
            // Récupérer les statistiques
            const statsResponse = await fetch(`${CONFIG.API_URL}/api/transactions/stats/summary`, {
                headers: { 'Authorization': `Bearer ${Auth.token}` }
            });

            if (statsResponse.status === 401) {
                alert('Votre session a expiré. Veuillez vous reconnecter.');
                Auth.logout();
                return;
            }

            if (!statsResponse.ok) {
                throw new Error('Erreur lors du chargement des statistiques');
            }

            const stats = await statsResponse.json();

            document.getElementById('total-income').textContent = stats.total_income.toFixed(2) + ' $';
            document.getElementById('total-expense').textContent = stats.total_expense.toFixed(2) + ' $';
            document.getElementById('balance').textContent = stats.balance.toFixed(2) + ' $';

            // Afficher l'alerte financière
            UI.updateFinancialAlert(stats.total_income, stats.total_expense);

            // Récupérer les transactions
            const transResponse = await fetch(`${CONFIG.API_URL}/api/transactions/`, {
                headers: { 'Authorization': `Bearer ${Auth.token}` }
            });

            if (transResponse.status === 401) {
                alert('Votre session a expiré. Veuillez vous reconnecter.');
                Auth.logout();
                return;
            }

            if (!transResponse.ok) {
                throw new Error('Erreur lors du chargement des transactions');
            }

            const transactions = await transResponse.json();
            this.displayTransactions(transactions);

        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors du chargement des données.');
        }
    },

    // Afficher les transactions
    displayTransactions(transactions) {
        const listDiv = document.getElementById('transactions-list');
        listDiv.innerHTML = '';

        if (transactions.length === 0) {
            listDiv.innerHTML = '<p class="no-transactions">🎯 Aucune transaction pour le moment<br>Commencez par en ajouter une !</p>';
            return;
        }

        transactions.forEach(t => {
            const div = document.createElement('div');
            div.className = 'transaction-item';

            const color = t.category === 'income' ? '#10b981' : '#ef4444';
            const icon = t.category === 'income' ? 'fa-arrow-trend-up' : 'fa-arrow-trend-down';
            div.style.borderLeftColor = color;

            div.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 15px;">
                    <div style="flex: 1;">
                        <div style="font-size: 18px; margin-bottom: 5px;">
                            <i class="fa-solid ${icon}"></i> <strong>${t.title}</strong>
                        </div>
                        <small style="color: #9ca3af;">
                            <i class="fa-regular fa-calendar"></i> ${new Date(t.date).toLocaleDateString('fr-FR', {
                                day: 'numeric',
                                month: 'long',
                                year: 'numeric'
                            })}
                        </small>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 24px; font-weight: bold; color: ${color};">
                            ${t.amount.toFixed(2)} $
                        </div>
                        <small style="color: #9ca3af;">
                            ${t.category === 'income' ? 'Revenu' : 'Dépense'}
                        </small>
                    </div>
                    <button class="delete-button" onclick="Transactions.deleteTransaction(${t.id}, '${t.title}')" title="Supprimer">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            `;
            listDiv.appendChild(div);
        });
    },

    // Créer une transaction
    async createTransaction() {
        const title = document.getElementById('new-title').value;
        const amount = parseFloat(document.getElementById('new-amount').value);
        const category = document.getElementById('new-category').value;

        if (!title || !amount || amount <= 0) {
            alert('Veuillez remplir tous les champs correctement');
            return;
        }

        try {
            const response = await fetch(`${CONFIG.API_URL}/api/transactions/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${Auth.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, amount, category, description: '' })
            });

            if (response.ok) {
                alert('Transaction ajoutée !');
                this.loadData();
                document.getElementById('new-title').value = '';
                document.getElementById('new-amount').value = '';
                document.getElementById('new-category').value = 'income';
            } else {
                throw new Error('Erreur création');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'ajout');
        }
    },

    // Supprimer une transaction
    async deleteTransaction(transactionId, transactionTitle) {
        if (!confirm(`Voulez-vous vraiment supprimer "${transactionTitle}" ?\n\nCette action est irréversible.`)) {
            return;
        }

        try {
            const response = await fetch(`${CONFIG.API_URL}/api/transactions/${transactionId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${Auth.token}` }
            });

            if (response.status === 204 || response.ok) {
                console.log('Transaction supprimée avec succès');
                await this.loadData();
            } else {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la suppression');
        }
    }
};

// Exposer globalement
window.Transactions = Transactions;