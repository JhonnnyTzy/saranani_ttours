import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CONFIGURACIÓN ---
# He puesto el token exacto de tu imagen aquí abajo:
TOKEN = "8205854308:AAFKpunPBu40oA6pvV8kNikL0KyNGxsAcSU" 
WEB_URL = "https://saranani-ttours.vercel.app"

# Configuración de registro (para ver errores en pantalla)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- CEREBRO DE SARABOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    mensaje = (
        f"¡Jallalla, {user_name}! 🇧🇴\n\n"
        "Soy **SaraBot**, tu guía virtual oficial del proyecto **Sarañani**.\n"
        "Mi misión es conectar cultura, raíces y tecnología.\n\n"
        "🏔️ Puedo ayudarte con rutas en los 9 departamentos.\n"
        "💻 Visita nuestros mapas interactivos aquí: " + WEB_URL + "\n\n"
        "¿En qué departamento estás interesado hoy?"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)

async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    respuesta = ""

    # 1. IDIOMAS NATIVOS (Saludo)
    if "kamisaraki" in texto:
        respuesta = "¡Waliki! (¡Bien!). Es un honor saludarte en nuestra lengua Aymara. Sigamos explorando Bolivia en español. ¿Qué ruta buscas?"
    elif any(x in texto for x in ["allin", "rimaykullayki", "napaykullayki"]):
        respuesta = "¡Allinllachu! (¡Hola!). Qué belleza escuchar el Quechua. Continuemos en español para guiarte mejor. ¿A dónde quieres viajar?"
    
    # 2. PRECIOS (Siempre a la web)
    elif any(x in texto for x in ["precio", "costo", "cuanto", "vale", "tarifa", "paquete"]):
        respuesta = (
            "💰 **Sobre nuestros precios:**\n\n"
            "Para darte la información más exacta y transparente, revisa los paquetes actualizados en nuestra web oficial:\n"
            f"👉 {WEB_URL}\n\n"
            "¡Vale cada centavo invertir en nuestras raíces!"
        )

    # 3. DEPARTAMENTOS (Detectar nombres)
    elif any(d in texto for d in ["la paz", "cochabamba", "santa cruz", "oruro", "potosí", "potosi", "chuquisaca", "tarija", "beni", "pando"]):
        # Busca cuál departamento se mencionó
        dept_encontrado = next((d for d in ["la paz", "cochabamba", "santa cruz", "oruro", "potosí", "potosi", "chuquisaca", "tarija", "beni", "pando"] if d in texto), "Bolivia")
        respuesta = (
            f"¡Excelente elección! **{dept_encontrado.title()}** tiene una riqueza cultural increíble. 🇧🇴\n\n"
            f"Tenemos circuitos listos esperando por ti. Descubre los mapas interactivos de {dept_encontrado.title()} aquí:\n"
            f"🔗 {WEB_URL}"
        )

    # 4. RESPUESTA GENERAL
    else:
        respuesta = (
            "¡Esa suena como una gran aventura! 🎒\n"
            "Recuerda que cubro rutas en los **9 departamentos de Bolivia**.\n\n"
            "Si buscas precios, escribe 'precio'. Si quieres ver rutas, dime el nombre del departamento (ej: 'La Paz') o visita:\n"
            f"👉 {WEB_URL}"
        )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta)

# --- ARRANQUE ---
if __name__ == '__main__':
    # Usamos el token que me pasaste
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Conectamos las funciones
    start_handler = CommandHandler('start', start)
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensajes)
    
    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    
    print("🇧🇴 SaraBot se ha conectado correctamente a Telegram...")
    application.run_polling()