document.addEventListener('DOMContentLoaded', () => {
    const productsList = document.getElementById('products-list');
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalAmount = document.getElementById('cart-total-amount');
    const createOrderBtn = document.getElementById('create-order-btn');
    const invoiceResult = document.getElementById('invoice-result');
    const clienteIdInput = document.getElementById('cliente-id');
    const productsUrlInput = document.getElementById('products-url');
    const pedidosUrlInput = document.getElementById('pedidos-url');
    const facturasUrlInput = document.getElementById('facturas-url');
    const ipDetectSpan = document.querySelector('.ip-detectada-span'); // Usamos una clase por si cambia el HTML

    let cart = [];
    let apiConfig = {};

    function initialize() {
        autoDetectUrls();
        addEventListeners();
        loadProducts();
        updateCartUI();
    }

    function autoDetectUrls() {
        const detectedHost = window.location.hostname;
        
        if (ipDetectSpan) {
            ipDetectSpan.textContent = `IP Detectada: ${detectedHost}`;
        }

        apiConfig = {
            products: `http://${detectedHost}:5001`,
            pedidos: `http://${detectedHost}:5002`,
            facturas: `http://${detectedHost}:5003`
        };

        productsUrlInput.value = apiConfig.products;
        pedidosUrlInput.value = apiConfig.pedidos;
        facturasUrlInput.value = apiConfig.facturas;
        console.log("URLs configuradas:", apiConfig);
    }

    async function loadProducts() {
        productsList.innerHTML = '<p>Cargando productos...</p>';
        try {
            const response = await fetch(`${apiConfig.products}/api/products`);
            if (!response.ok) {
                throw new Error(`El servidor respondió con el estado: ${response.status}`);
            }
            const xmlText = await response.text();
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, "application/xml");

            const products = xmlDoc.querySelectorAll('product');
            productsList.innerHTML = '';
            if (products.length === 0) {
                productsList.innerHTML = '<p>No hay productos disponibles.</p>';
                return;
            }

            products.forEach(product => {
                const id = product.querySelector('id').textContent;
                const nombre = product.querySelector('nombre').textContent;
                const precio = parseFloat(product.querySelector('precio').textContent);
                const stock = product.querySelector('stock').textContent;
                const descripcion = product.querySelector('descripcion').textContent;

                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <h3>${nombre}</h3>
                    <p>${descripcion}</p>
                    <p class="precio">Precio: $${precio.toFixed(2)}</p>
                    <p>Stock: ${stock}</p>
                    <button class="add-to-cart-btn" data-id="${id}" data-nombre="${nombre}" data-precio="${precio}">Agregar al Carrito</button>
                `;
                productsList.appendChild(card);
            });
        } catch (error) {
            console.error('Error al cargar productos:', error);
            productsList.innerHTML = `<p style="color: red;">Error al cargar productos: ${error.message}. Revisa la consola (F12) para más detalles.</p>`;
        }
    }

    function addToCart(product) {
        const existingItem = cart.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.cantidad++;
        } else {
            cart.push({ ...product, cantidad: 1 });
        }
        updateCartUI();
    }

    function removeFromCart(productId) {
        cart = cart.filter(item => item.id !== productId);
        updateCartUI();
    }

    function updateCartUI() {
        cartItemsContainer.innerHTML = '';
        let total = 0;
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p>El carrito está vacío.</p>';
        } else {
            cart.forEach(item => {
                const itemEl = document.createElement('div');
                itemEl.className = 'cart-item';
                itemEl.innerHTML = `
                    <span>${item.nombre} (x${item.cantidad})</span>
                    <span>$${(item.precio * item.cantidad).toFixed(2)}</span>
                    <button class="remove-from-cart-btn" data-id="${item.id}">&times;</button>
                `;
                cartItemsContainer.appendChild(itemEl);
                total += item.precio * item.cantidad;
            });
        }
        cartTotalAmount.textContent = `$${total.toFixed(2)}`;
        createOrderBtn.disabled = cart.length === 0;
    }

    async function handleCreateOrder() {
        const clienteId = clienteIdInput.value;
        if (!clienteId) {
            alert('Por favor, ingresa un ID de cliente.');
            return;
        }

        const orderData = {
            cliente_id: parseInt(clienteId),
            items: cart.map(item => ({ id: item.id, cantidad: item.cantidad }))
        };

        try {
            const pedidoResponse = await fetch(`${apiConfig.pedidos}/api/pedidos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(orderData)
            });

            if (!pedidoResponse.ok) {
                const errorText = await pedidoResponse.text();
                throw new Error(`Error del servidor al crear pedido: ${errorText}`);
            }

            const pedidoResult = await pedidoResponse.json();
            alert(`Pedido creado con éxito. ID: ${pedidoResult.pedido_id}.`);
            
            await handleGenerateInvoice(pedidoResult.pedido_id);

            cart = [];
            updateCartUI();

        } catch (error) {
            console.error("Error en el proceso de pedido:", error);
            alert(error.message);
        }
    }

    async function handleGenerateInvoice(pedidoId) {
        invoiceResult.innerHTML = '<p>Generando factura...</p>';
        try {
            const facturaResponse = await fetch(`${apiConfig.facturas}/api/facturas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pedido_id: pedidoId })
            });

            if (!facturaResponse.ok) {
                const errorText = await facturaResponse.text();
                throw new Error(`Error del servidor al generar factura: ${errorText}`);
            }

            const [xmlFactura, xslTemplate] = await Promise.all([
                facturaResponse.text(),
                fetch('/factura.xsl').then(res => res.text())
            ]);

            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlFactura, 'application/xml');
            const xslDoc = parser.parseFromString(xslTemplate, 'application/xml');

            const xsltProcessor = new XSLTProcessor();
            xsltProcessor.importStylesheet(xslDoc);
            const resultFragment = xsltProcessor.transformToFragment(xmlDoc, document);

            invoiceResult.innerHTML = '';
            invoiceResult.appendChild(resultFragment);

        } catch (error) {
            console.error("Error al generar factura:", error);
            invoiceResult.innerHTML = `<p style="color:red;">${error.message}</p>`;
        }
    }

    function addEventListeners() {
        productsList.addEventListener('click', e => {
            if (e.target.classList.contains('add-to-cart-btn')) {
                addToCart({
                    id: e.target.dataset.id,
                    nombre: e.target.dataset.nombre,
                    precio: parseFloat(e.target.dataset.precio)
                });
            }
        });

        cartItemsContainer.addEventListener('click', e => {
            if (e.target.classList.contains('remove-from-cart-btn')) {
                removeFromCart(e.target.dataset.id);
            }
        });

        createOrderBtn.addEventListener('click', handleCreateOrder);
    }
    
    initialize();
});
