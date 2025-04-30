document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");
    // Client form submission
    const clientForm = document.getElementById('clientForm');
    if (clientForm) {
        clientForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(clientForm);
            
            fetch('/add_client', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Client added successfully!');
                    clientForm.reset();
                    loadTables();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }
    
    // Commission form submission
    const commissionForm = document.getElementById('commissionForm');
    if (commissionForm) {
        commissionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(commissionForm);
            
            fetch('/add_commission', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Commission added successfully!');
                    commissionForm.reset();
                    loadTables();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }
    
    // Payment form submission
    const paymentForm = document.getElementById('paymentForm');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(paymentForm);
            
            fetch('/add_payment', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Payment added successfully!');
                    paymentForm.reset();
                    loadTables();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }

    // Load table data on page load
    loadTables();
});

// Function to load all tables
function loadTables() {
    console.log("Loading all tables");
    const tableBodies = document.querySelectorAll('.styled-table tbody');
    console.log("Found table bodies:", tableBodies.length);
    
    // Client table is the first table
    if (tableBodies.length >= 1) {
        loadClientTable(tableBodies[0]);
    }
    
    // Commission table is the second table
    if (tableBodies.length >= 2) {
        loadCommissionTable(tableBodies[1]);
    }
    
    // Payment table is the third table
    if (tableBodies.length >= 3) {
        loadPaymentTable(tableBodies[2]);
    }
}

// Function to load client table data
function loadClientTable(tableBody) {
    console.log("Loading client table");
    fetch('/get_clients')
        .then(response => response.json())
        .then(data => {
            console.log("Client data received:", data);
            tableBody.innerHTML = '';
            data.forEach(client => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${client.client_id}</td>
                    <td>${client.first_name} ${client.last_name}</td>
                    <td>${client.email}</td>
                    <td>${client.phone_number}</td>
                    <td>
                        <button onclick="deleteClient('${client.client_id}')">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error loading clients:', error);
            tableBody.innerHTML = '<tr><td colspan="5">Error loading clients</td></tr>';
        });
}

// Function to load commission table data
function loadCommissionTable(tableBody) {
    console.log("Loading commission table");
    fetch('/get_commissions')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Commission data received:", data);
            tableBody.innerHTML = '';
            if (data && data.length > 0) {
                data.forEach(commission => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${commission.commission_id}</td>
                        <td>${commission.client_name || commission.client_id}</td>
                        <td>${commission.description}</td>
                        <td>${formatDate(commission.due_date)}</td>
                        <td>${commission.artwork_status}</td>
                        <td>$${commission.amount}</td>
                        <td>
                            <button onclick="deleteCommission('${commission.commission_id}')">Delete</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                tableBody.innerHTML = '<tr><td colspan="7">No commission data available</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error loading commissions:', error);
            tableBody.innerHTML = '<tr><td colspan="7">Error loading commissions</td></tr>';
        });
}

// Function to load payment table data
function loadPaymentTable(tableBody) {
    console.log("Loading payment table");
    fetch('/get_payments')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Payment data received:", data);
            tableBody.innerHTML = '';
            if (data && data.length > 0) {
                data.forEach(payment => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${payment.payment_id}</td>
                        <td>${payment.commission_id}</td>
                        <td>${formatDate(payment.payment_date)}</td>
                        <td>$${payment.amount_paid}</td>
                        <td>$${payment.amount_remaining}</td>
                        <td>${payment.payment_method}</td>
                        <td>${payment.payment_status}</td>
                        <td>
                            <button onclick="deletePayment('${payment.payment_id}')">Delete</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                tableBody.innerHTML = '<tr><td colspan="8">No payment data available</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error loading payments:', error);
            tableBody.innerHTML = '<tr><td colspan="8">Error loading payments</td></tr>';
        });
}

// Helper function to format dates properly
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString; // Return original if invalid
    return date.toLocaleDateString();
}

// Utility functions for deleting records
function deleteClient(clientId) {
    if (confirm('Are you sure you want to delete this client?')) {
        fetch(`/delete_client/${clientId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Client deleted successfully!');
                loadTables();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function deleteCommission(commissionId) {
    if (confirm('Are you sure you want to delete this commission?')) {
        fetch(`/delete_commission/${commissionId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Commission deleted successfully!');
                loadTables();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function deletePayment(paymentId) {
    if (confirm('Are you sure you want to delete this payment?')) {
        fetch(`/delete_payment/${paymentId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Payment deleted successfully!');
                loadTables();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}