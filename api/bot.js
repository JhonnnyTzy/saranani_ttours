import { OpenAI } from 'openai';

// Configuración de DeepSeek (usando librería OpenAI)
const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY, // La clave estará segura en el servidor
  baseURL: 'https://api.deepseek.com',
});

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;

// Función para enviar mensaje a Telegram
async function sendMessage(chatId, text) {
  await fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text: text }),
  });
}

// Esta es la función principal que Vercel ejecutará
export default async function handler(req, res) {
  // Solo aceptamos peticiones POST (que vienen de Telegram)
  if (req.method !== 'POST') {
    return res.status(200).send('El bot está vivo, pero espera peticiones POST.');
  }

  try {
    const { message } = req.body;

    // Verificar si hay mensaje y texto
    if (!message || !message.text) {
      return res.status(200).send('OK'); // Ignorar mensajes sin texto
    }

    const chatId = message.chat.id;
    const userText = message.text;
    const userName = message.from.first_name;

    // --- LÓGICA DE NEGOCIO (SARAÑANI) ---
    const systemPrompt = `
      Eres el asistente virtual de "Sarañani", un proyecto de turismo que conecta cultura, raíces y tecnología.
      Tu nombre es "SaraBot".
      - Responde de forma amable, cultural y entusiasta.
      - Si preguntan por circuitos, menciona que tenemos rutas en La Paz, Oruro y Potosí.
      - Invita a visitar la web para ver el mapa interactivo.
    `;

    // Llamada a la IA (DeepSeek)
    const completion = await client.chat.completions.create({
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userText }
      ],
      model: "deepseek-chat",
    });

    const botReply = completion.choices[0].message.content;

    // Responder a Telegram
    await sendMessage(chatId, botReply);

    return res.status(200).json({ status: 'Mensaje enviado' });

  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({ error: 'Error interno del bot' });
  }
}