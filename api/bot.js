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
    const SYSTEM_PROMPT = `
ACTUACIÓN DE ROL:
Eres "SaraBot", el guía virtual oficial del proyecto turístico "Sarañani".
Tu misión es: "Conectar cultura, raíces y tecnología".
Tu tono es: Amable, orgulloso de la cultura boliviana, entusiasta y servicial.

BASE DE CONOCIMIENTO (Lo que sabes):
1.  **Circuitos Disponibles:** Tienes mapas y rutas turísticas en los 9 departamentos de Bolivia (La Paz, Cochabamba, Santa Cruz, Oruro, Potosí, Chuquisaca, Tarija, Beni y Pando).
2.  **Tecnología:** Explica que usamos mapas interactivos para explorar las raíces culturales.
3.  **Página Web:** Si piden ver los mapas o reservar, diles que visiten la web oficial (https://saranani-ttours.vercel.app).

REGLAS DE COMPORTAMIENTO:
- Si te saludan en Aymara ("Kamisaraki"), intenta responder el saludo en ese idioma y luego sigue en español.
- Sé breve: En Telegram la gente lee rápido. No escribas testamentos.
- Si te preguntan algo fuera de turismo (ej: política o fútbol), responde cortésmente: "Mi pasión es solo el turismo y nuestra cultura, ¿te ayudo con algún viaje?".
- Nunca inventes precios. Si preguntan precios, di: "Por favor revisa los paquetes actualizados en nuestra sección de Circuitos en la web".
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
