import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CONFIGURACIÓN ---
# ¡OJO! Mantén este token en secreto.
TOKEN = "8205854308:AAFKpunPBu40oA6pvV8kNikL0KyNGxsAcSU" 
WEB_URL = "https://saranani-ttours.vercel.app"

# Configuración de registro
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- BASE DE DATOS MENTAL (Sincronizada con tu HTML) ---
DATOS_TURISTICOS = {
    "la paz": {
        "modismos": ["¡Yaaaa!", "¡Qué bestia!", "¿No ve?", "¡Super!", "¡Alalau!"],
        # Actualizado con datos de tu HTML: Calle Jaén, Mercado de Brujas, Titicaca
        "reco": "Para La Paz, lo clásico es el **Lago Titicaca** y sus islas flotantes. Pero si te quedas en la ciudad, tienes que caminar por la mística **Calle Jaén** y el **Mercado de las Brujas**.",
        "emoji": "🏔️🚠"
    },
    "santa cruz": {
        "modismos": ["¡Elay!", "¡Belleza, pariente!", "¡Vej!", "¡Qué buri!", "Oiga pariente"],
        # Actualizado con: Amboró y Samaipata
        "reco": "En la tierra camba tienes que conocer el **Parque Nacional Amboró** para ver naturaleza pura, o escaparte a **Samaipata** para recargar energías en el Fuerte.",
        "emoji": "🌴🦜"
    },
    "cochabamba": {
        "modismos": ["¡Qué rico!", "Caserito/a", "¡Chorizo!", "Pucha qué lindo"],
        # Actualizado con: Cristo y Tunari
        "reco": "¡La Llajta se respeta! Sube al **Cristo de la Concordia** (más alto que el de Río) o haz trekking en el **Parque Nacional Tunari**. Y claro, ¡come un buen Silpancho!",
        "emoji": "🌽🦕"
    },
    "potosí": {
        "modismos": ["¡Irupana!", "¡Carajo!", "Vale un Potosí"],
        # Actualizado con: Uyuni y Cerro Rico
        "reco": "El destino estrella es el **Salar de Uyuni**, es el espejo del mundo. También debes sentir la historia entrando a las minas del **Cerro Rico**.",
        "emoji": "🧂🦙"
    },
    "tarija": {
        "modismos": ["¡Churo!", "¡Mozo/a!", "¡Ahicito nomás!"],
        # Actualizado con: Viñedos y Chorros de Jurina
        "reco": "Tierra chapaca. Tienes que hacer la **Ruta de Viñedos y Bodegas** en el Valle de la Concepción. Si quieres agua y sol, ve a los **Chorros de Jurina**.",
        "emoji": "🍷🍇"
    },
    "chuquisaca": {
        "modismos": ["¡Paaaque!", "Chukuta", "¡Ay juna!"],
        # Actualizado con: Sucre y Tarabuco
        "reco": "La Ciudad Blanca es historia pura. Camina por las calles coloniales de **Sucre** y no te pierdas el mercado tradicional de **Tarabuco** para ver tejidos únicos.",
        "emoji": "🦖🏛️"
    },
    "oruro": {
        "modismos": ["¡Quirquincho!", "¡Fuerza!"],
        # Actualizado con: Carnaval y Sajama
        "reco": "Capital del Folklore. Si no es época del majestuoso **Carnaval**, te recomiendo ir al **Parque Nacional Sajama** a ver el nevado y las aguas termales.",
        "emoji": "🎭🌋"
    },
    "beni": {
        "modismos": ["¡Pariente!", "¡Mierda che!", "¡Qué calor!"],
        # Actualizado con: Madidi y Rurrenabaque
        "reco": "Naturaleza salvaje. **Rurrenabaque** es tu puerta de entrada. Desde ahí saltas al **Parque Madidi** o a las pampas. ¡Verás caimanes y delfines rosados!",
        "emoji": "🐬🐆"
    },
    "pando": {
        "modismos": ["¡Elay!", "¡Vej!", "Amazónico"],
        # Actualizado con: Cobija y Manuripi
        "reco": "El corazón de la Amazonía. Conoce **Cobija** en la frontera o adéntrate en la **Reserva Manuripi** para ver la selva virgen de verdad.",
        "emoji": "🌳🥥"
    }
}

FRASES_INICIO = [
    "¡Uff, buena pregunta!",
    "¡Claro que sí, me encanta ese lugar!",
    "¡Qué buen plan tienes en mente!",
    "Mira, te cuento lo mejor que puedes hacer:",
    "Déjame darte mis mejores datos sobre eso:",
    "¡Excelente elección! Te va a encantar."
]

# --- LÓGICA DEL BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    mensaje = (
        f"¡Jallalla, {user_name}! 🇧🇴\n\n"
        "Soy Saranañi_bot, tu guía oficial de Sarañani Tours.\n"
        "Mi misión es conectar cultura, raíces y tecnología.\n\n"
        "🏔️ Conozco secretos de los 9 departamentos.\n"
        "💻 Mira nuestros mapas 360° aquí: " + WEB_URL + "\n\n"
        "**Cuéntame, ¿a qué departamento quieres viajar?**"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)

async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    respuesta = ""
    
    # Detectar departamento
    dept_detectado = None
    for dept in DATOS_TURISTICOS:
        if dept in texto or (dept == "potosí" and "potosi" in texto):
            dept_detectado = dept
            break

    # 1. IDIOMAS NATIVOS
    if "kamisaraki" in texto:
        respuesta = "¡Waliki jilata/kullaka! 🇧🇴 Es un honor saludarte en Aymara. Sigamos en español para darte los mejores tips."
    elif any(x in texto for x in ["allin", "rimaykullayki", "napaykullayki"]):
        respuesta = "¡Allinllachu! 🇧🇴 Qué lindo escuchar el Quechua. Sigamos en español para guiarte mejor."

    # 2. PRECIOS
    elif any(x in texto for x in ["precio", "costo", "cuanto", "vale", "tarifa", "paquete"]):
        respuesta = (
            "💰 **Sobre los precios:**\n\n"
            "Los costos dependen de la temporada y el paquete (si vas solo o en grupo).\n"
            "Checa los precios oficiales y reserva aquí:\n"
            f"👉 {WEB_URL}"
        )

    # 3. RECOMENDACIÓN INTELIGENTE
    elif dept_detectado:
        info = DATOS_TURISTICOS[dept_detectado]
        modismo = random.choice(info["modismos"])
        inicio = random.choice(FRASES_INICIO)
        
        respuesta = (
            f"{modismo} {inicio} {info['emoji']}\n\n"
            f"{info['reco']}\n\n"
            f"🗺️ **Ver mapa y detalles:**\n"
            f"🔗 {WEB_URL}"
        )

    # 4. RESPUESTA GENÉRICA
    else:
        respuesta = (
            "¡Esa suena como una gran aventura! 🎒\n"
            "Pero necesito que me digas el nombre del lugar.\n\n"
            "¿Buscas info de **La Paz**, **Santa Cruz**, **Tarija**...? \n"
            "Dime el departamento y te doy mis secretos."
        )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta)

# --- ARRANQUE ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensajes)
    
    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    
    print("🇧🇴 SaraBot está lista y conectada. ¡Jallalla!...")
    application.run_polling()