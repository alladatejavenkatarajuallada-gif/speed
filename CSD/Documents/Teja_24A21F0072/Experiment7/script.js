const express = require('express');
const app = express();
const PORT = 3000;
// Middleware to log requests
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
    next();
});
// Parse JSON payloads
app.use(express.json());
// Sample product data
let products = [
    { id: 1, name: 'Watch', price: 500.99, category: 'Gadgets' },
    { id: 2, name: 'Television', price: 699.99, category: 'Electronics' },
    { id: 3, name: 'Chain', price: 149.99, category: 'Accessories' }
];
// Root endpoint
app.get('/', (req, res) => {
    res.send('Hello, Guys');
});
// GET all products
app.get('/products', (req, res) => {
    res.json(products);
});
// GET product by ID
app.get('/products/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const product = products.find(p => p.id === id);
    if (!product) {
        return res.status(404).json({ message: 'Product not found' });
    }
    res.json(product);
});
// POST new product
app.post('/products', (req, res) => {
    const { name, price, category } = req.body;
    if (!name || !price) {
        return res.status(400).json({ message: 'Name and price are required' });
    }
    const newId = products.length > 0 ? Math.max(...products.map(p => p.id)) + 1 : 1; 
    const newProduct = {
        id: newId,
        name,
        price,
        category: category || 'Uncategorized'
    }; 
    products.push(newProduct);
    res.status(201).json(newProduct);
});
// PUT update product
app.put('/products/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = products.findIndex(p => p.id === id);
    if (index === -1) {
        return res.status(404).json({ message: 'Product not found' });
    }
    const { name, price, category } = req.body;
    products[index] = {
        id,
        name: name || products[index].name,
        price: price || products[index].price,
        category: category || products[index].category
    };
    res.json(products[index]);
});
// DELETE product
app.delete('/products/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = products.findIndex(p => p.id === id);
    if (index === -1) {
        return res.status(404).json({ message: 'Product not found' });
    }
    const deletedProduct = products[index];
    products = products.filter(p => p.id !== id);
    res.json({ message: 'Product deleted', product: deletedProduct });
});
// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});