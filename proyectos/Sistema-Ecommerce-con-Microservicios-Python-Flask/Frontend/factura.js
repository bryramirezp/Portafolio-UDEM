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

        // Intentar cargar desde localStorage primero
        const savedProductsUrl = localStorage.getItem('productsUrl');
        const savedPedidosUrl = localStorage.getItem('pedidosUrl');
        const savedFacturasUrl = localStorage.getItem('facturasUrl');

        if (savedProductsUrl && savedPedidosUrl && savedFacturasUrl) {
            apiConfig = {
                products: savedProductsUrl,
                pedidos: savedPedidosUrl,
                facturas: savedFacturasUrl
            };
        } else {
            // Configurar URLs por defecto para Docker containers
            // Cuando frontend está en mismo docker-compose, usar nombres de servicio
            // Cuando frontend está separado, usar localhost con puertos expuestos
            const isRunningInDockerNetwork = window.location.hostname.includes('joyeria') ||
                                           window.location.hostname === 'joyeria_frontend';

            if (isRunningInDockerNetwork) {
                // Frontend en docker-compose - usar nombres de servicio
                apiConfig = {
                    products: `http://products:5000`,
                    pedidos: `http://pedidos:5000`,
                    facturas: `http://facturas:5000`
                };
            } else {
                // Frontend separado o en localhost - usar puertos expuestos
                apiConfig = {
                    products: `http://localhost:5001`,
                    pedidos: `http://localhost:5002`,
                    facturas: `http://localhost:5003`
                };
            }
        }

        productsUrlInput.value = apiConfig.products;
        pedidosUrlInput.value = apiConfig.pedidos;
        facturasUrlInput.value = apiConfig.facturas;
        console.log("URLs configuradas:", apiConfig);
    }

    function saveUrlsToStorage() {
        localStorage.setItem('productsUrl', productsUrlInput.value);
        localStorage.setItem('pedidosUrl', pedidosUrlInput.value);
        localStorage.setItem('facturasUrl', facturasUrlInput.value);

        // Actualizar apiConfig con los valores guardados
        apiConfig = {
            products: productsUrlInput.value,
            pedidos: pedidosUrlInput.value,
            facturas: facturasUrlInput.value
        };

        console.log("URLs guardadas en localStorage:", apiConfig);
        alert('Configuración guardada exitosamente.');
    }

    async function loadProducts() {
        productsList.innerHTML = '<p>Cargando productos...</p>';
        try {
            console.log('DEBUG: Fetching products from:', `${apiConfig.products}/api/products`);
            const response = await fetch(`${apiConfig.products}/api/products`);
            console.log('DEBUG: Response status:', response.status);
            if (!response.ok) {
                throw new Error(`El servidor respondió con el estado: ${response.status}`);
            }
            const xmlText = await response.text();
            console.log('DEBUG: Raw XML response:', xmlText);

            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, "application/xml");
            console.log('DEBUG: Parsed XML document:', xmlDoc);

            // Check for parser errors
            const parserError = xmlDoc.querySelector('parsererror');
            if (parserError) {
                console.error('DEBUG: XML parsing error:', parserError.textContent);
                throw new Error('Error al parsear XML: ' + parserError.textContent);
            }

            const products = xmlDoc.querySelectorAll('product');
            console.log('DEBUG: Found products elements:', products.length);
            productsList.innerHTML = '';
            if (products.length === 0) {
                console.log('DEBUG: No products found in XML');
                productsList.innerHTML = '<p>No hay productos disponibles.</p>';
                return;
            }

            console.log('DEBUG: First product element:', products[0]);
            console.log('DEBUG: First product innerHTML:', products[0].innerHTML);

            products.forEach((product, index) => {
                console.log(`DEBUG: Processing product ${index + 1}:`, product);
                const id = product.querySelector('id')?.textContent;
                const nombre = product.querySelector('nombre')?.textContent;
                const precio = product.querySelector('precio')?.textContent;
                const stock = product.querySelector('stock')?.textContent;
                const descripcion = product.querySelector('descripcion')?.textContent;

                console.log(`DEBUG: Product ${index + 1} data:`, { id, nombre, precio, stock, descripcion });

                if (!id || !nombre || precio === undefined) {
                    console.warn(`DEBUG: Skipping product ${index + 1} due to missing required fields`);
                    return;
                }

                const precioFloat = parseFloat(precio);
                if (isNaN(precioFloat)) {
                    console.warn(`DEBUG: Invalid price for product ${index + 1}: ${precio}`);
                    return;
                }

                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <h3>${nombre}</h3>
                    <p>${descripcion || 'Sin descripción'}</p>
                    <p class="precio">Precio: $${precioFloat.toFixed(2)}</p>
                    <p>Stock: ${stock || 'N/A'}</p>
                    <button class="add-to-cart-btn" data-id="${id}" data-nombre="${nombre}" data-precio="${precioFloat}">Agregar al Carrito</button>
                `;
                productsList.appendChild(card);
            });

            // If no products were added, show a message
            if (productsList.children.length === 0) {
                productsList.innerHTML = '<p>No se pudieron cargar productos válidos.</p>';
            }
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
            // Crear XML para el pedido
            let xmlData = '<pedido>';
            xmlData += `<cliente_id>${orderData.cliente_id}</cliente_id>`;
            orderData.items.forEach(item => {
                xmlData += `<item><id>${item.id}</id><cantidad>${item.cantidad}</cantidad></item>`;
            });
            xmlData += '</pedido>';

            const pedidoResponse = await fetch(`${apiConfig.pedidos}/api/pedidos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/xml' },
                body: xmlData
            });

            if (!pedidoResponse.ok) {
                const errorText = await pedidoResponse.text();
                throw new Error(`Error del servidor al crear pedido: ${errorText}`);
            }

            const pedidoXmlText = await pedidoResponse.text();
            const parser = new DOMParser();
            const pedidoXml = parser.parseFromString(pedidoXmlText, 'application/xml');
            const pedidoId = pedidoXml.querySelector('pedido_id').textContent;
            alert(`Pedido creado con éxito. ID: ${pedidoId}.`);
            
            await handleGenerateInvoice(pedidoId);

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
            const xmlData = `<factura><pedido_id>${pedidoId}</pedido_id></factura>`;
            const facturaResponse = await fetch(`${apiConfig.facturas}/api/facturas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/xml' },
                body: xmlData
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

        // Event listener para guardar configuración
        const saveConfigBtn = document.getElementById('save-config');
        if (saveConfigBtn) {
            saveConfigBtn.addEventListener('click', saveUrlsToStorage);
        }
    }
    
    initialize();
});
