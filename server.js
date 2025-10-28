const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.static('frontend')); // zeigt Dateien aus ./frontend

app.get('/health', (_, res) => res.send('OK'));
app.listen(PORT, () => console.log(`Server läuft auf http://localhost:${PORT}`));
