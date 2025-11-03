import express from 'express';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware e rotas podem ser configurados aqui

app.get('/', (req, res) => {
    res.send('Bem-vindo ao projeto de publicação no Google!');
});

app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});