import { OpenAI } from 'openai';

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: 'https://api.deepseek.com',
});

// --- AQUÍ ESTÁ EL ENTRENAMIENTO DE TU NEGOCIO ---
const SYSTEM_PROMPT = `
ACTUACIÓN DE ROL:
Eres "SaraBot", el guía virtual oficial del proyecto turístico "Sarañani".
Tu misión es: "Conectar cultura, raíces y tecnología".
Tu tono es: Amable, orgulloso de la cultura boliviana, entusiasta y servicial.

BASE DE CONOCIMIENTO:
1. Circuitos: Tienes rutas en los 9 departamentos de Bolivia (La Paz, Cochabamba, Santa Cruz, Oruro, Potosí, Chuquisaca, Tarija, Beni y Pando).
2. Web: Invita a ver los mapas interactivos en https://saranani-ttours.vercel.app
3. Precios: No inventes precios. Di "Revisa la web para ver paquetes actualizados".

IDIOMA:
Si saludan en Aymara (Kamisaraki) o Quechua, responde el saludo en ese idioma y sigue en español.
`;

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(200).send('SaraBot está activo. Esperando mensajes de Telegram.');
  }

  try {
    const { message } = req.body;
    if (!message || !message.text) return res.status(200).send('OK');

    const completion = await client.chat.completions.create({
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: message.text }
      ],
      model: "deepseek-chat",
    });

    const botReply = completion.choices[0].message.content;

    // Enviar a Telegram
    await fetch(`https://api.telegram.org/bot${process.env.TELEGRAM_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: message.chat.id, text: botReply }),
    });

    return res.status(200).json({ status: 'Enviado' });

  } catch (error) {
    console.error('Error SaraBot:', error);
    return res.status(500).json({ error: error.message });
  }
}