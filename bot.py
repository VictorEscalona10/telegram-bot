import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import dotenv
import os 

# Cargar variables de entorno desde un archivo .env
dotenv.load_dotenv()

# Configurar el registro
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)
logger = logging.getLogger(__name__)

# Clave de API y URL de ExchangeRate-API    
URL = os.getenv("URL")

# Función para obtener las tasas de cambio
def get_rates():
    response = requests.get(URL)
    if response.status_code != 200:
        logger.error("No se pudo obtener las tasas de cambio.")
        return None
    data = response.json()
    return data["conversion_rates"]

# Función para convertir divisas
def convert_currency(amount, from_currency, to_currency, rates):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency != "USD":
        amount = amount / rates[from_currency]
    return amount * rates[to_currency]

# Función de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "👋 ¡Hola! Bienvenido al Bot Conversor de Divisas 🌍💱\n\n"
        "🛠️ **Cómo usar el bot:**\n"
        "1. Usa el comando /convert seguido de la cantidad, la divisa de origen y la divisa de destino.\n"
        "   Por ejemplo: `/convert 100 USD EUR`\n\n"
        "🔄 **Ejemplo de uso:**\n"
        "   `/convert 50 EUR USD`\n"
        "   Esto convertirá 50 euros a dólares estadounidenses.\n\n"
        "💡 **Divisas disponibles:**\n"
        "   Usa el comando /divisas para ver la lista de códigos de divisas válidos.\n\n"
        "❓ **Donar:**\n"
        "   Si te gusta el bot y quieres contribuir al proyecto, puedes utilizar /donate.\n\n"
        "¡Empieza a convertir divisas ahora! 🚀"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

# Función para mostrar los códigos de las divisas disponibles
async def divisas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"💱 **Divisas disponibles:**\n\n"
                                    "USD: Dólar Estadounidense\n"
                                    "AED: Dirham de los Emiratos Árabes Unidos\n"
                                    "AFN: Afghani\n"
                                    "ALL: Lek\n"
                                    "AMD: Dram Armenio\n"
                                    "ANG: Florín de las Antillas Neerlandesas\n"
                                    "AOA: Kwanza\n"
                                    "ARS: Peso Argentino\n"
                                    "AUD: Dólar Australiano\n"
                                    "AWG: Florín Arubeño\n"
                                    "AZN: Manat Azerbaiyano\n"
                                    "BAM: Marco Convertible\n"
                                    "BBD: Dólar de Barbados\n"
                                    "BDT: Taka\n"
                                    "BGN: Lev Búlgaro\n"
                                    "BHD: Dinar Bahreiní\n"
                                    "BIF: Franco Burundés\n"
                                    "MD: Dólar de Bermudas\n"
                                    "BND: Dólar de Brunei\n"
                                    "BOB: Boliviano\n"
                                    "BRL: Real Brasileño\n"
                                    "BSD: Dólar Bahameño\n"
                                    "BTN: Ngultrum\n"
                                    "BWP: Pula\n"
                                    "BYN: Rublo Bielorruso\n"
                                    "BZD: Dólar de Belice\n"
                                    "CAD: Dólar Canadiense\n"
                                    "CDF: Franco Congoleño\n"
                                    "CHF: Franco Suizo\n"
                                    "CLP: Peso Chileno\n"
                                    "CNY: Yuan Renminbi\n"
                                    "COP: Peso Colombiano\n"
                                    "CRC: Colón Costarricense\n"
                                    "CUP: Peso Cubano\n"
                                    "CVE: Escudo Caboverdiano\n"
                                    "CZK: Corona Checa\n"
                                    "DJF: Franco Yibutiano\n"
                                    "DKK: Corona Danesa\n"
                                    "DOP: Peso Dominicano\n"
                                    "DZD: Dinar Argelino\n"
                                    "EGP: Libra Egipcia\n"
                                    "ERN: Nakfa\n"
                                    "ETB: Birr Etíope\n"
                                    "EUR: Euro\n"
                                    "FJD: Dólar Fiyiano\n"
                                    "FKP: Libra de las Islas Malvinas\n"
                                    "FOK: Corona Feroesa\n"
                                    "GBP: Libra Esterlina\n"
                                    "GEL: Lari\n"
                                    "GGP: Libra de Guernsey\n"
                                    "GHS: Cedi\n"
                                    "GIP: Libra de Gibraltar\n"
                                    "GMD: Dalasi\n"
                                    "GNF: Franco Guineano\n"
                                    "GTQ: Quetzal\n"
                                    "GYD: Dólar de Guyana\n"
                                    "HKD: Dólar de Hong Kong\n"
                                    "HNL: Lempira\n"
                                    "HRK: Kuna Croata\n"
                                    "HTG: Gourde Haitiano\n"
                                    "HUF: Florín Húngaro\n"
                                    "IDR: Rupia Indonesia\n"
                                    "ILS: Nuevo Shekel Israelí\n"
                                    "IMP: Libra de la Isla de Man\n"
                                    "INR: Rupia India\n"
                                    "IQD: Dinar Iraquí\n"
                                    "IRR: Rial Iraní\n"
                                    "ISK: Corona Islandesa\n"
                                    "JEP: Libra de Jersey\n"
                                    "JMD: Dólar Jamaicano\n"
                                    "JOD: Dinar Jordano\n"
                                    "JPY: Yen\n"
                                    "KES: Chelín Keniano\n"
                                    "KGS: Som\n"
                                    "KHR: Riel\n"
                                    "KID: Dólar Kiribatiano\n"
                                    "KMF: Franco Comorense\n"
                                    "KRW: Won Surcoreano\n"
                                    "KWD: Dinar Kuwaití\n"
                                    "KYD: Dólar de las Islas Caimán\n"
                                    "KZT: Tenge\n"
                                    "LAK: Kip\n"
                                    "LBP: Libra Libanesa\n"
                                    "LKR: Rupia de Sri Lanka\n"
                                    "LRD: Dólar Liberiano\n"
                                    "LSL: Loti\n"
                                    "LYD: Dinar Libio\n"
                                    "MAD: Dirham Marroquí\n"
                                    "MDL: Leu Moldavo\n"
                                    "MGA: Ariary\n"
                                    "MKD: Denar\n"
                                    "MMK: Kyat\n"
                                    "MNT: Tugrik\n"
                                    "MOP: Pataca\n"
                                    "MRU: Ouguiya\n"
                                    "MUR: Rupia de Mauricio\n"
                                    "MVR: Rufiyaa\n"
                                    "MWK: Kwacha Malauí\n"
                                    "MXN: Peso Mexicano\n"
                                    "MYR: Ringgit\n"
                                    "MZN: Metical\n"
                                    "NAD: Dólar Namibio\n"
                                    "NGN: Naira\n"
                                    "NIO: Córdoba\n"
                                    "NOK: Corona Noruega\n"
                                    "NPR: Rupia Nepalesa\n"
                                    "NZD: Dólar Neozelandés\n"
                                    "OMR: Rial Omaní\n"
                                    "PAB: Balboa\n"
                                    "PEN: Sol\n"
                                    "PGK: Kina\n"
                                    "PHP: Peso Filipino\n"
                                    "PKR: Rupia Pakistaní\n"
                                    "PLN: Zloty\n"
                                    "PYG: Guaraní\n"
                                    "QAR: Rial Catarí\n"
                                    "RON: Leu Rumano\n"
                                    "RSD: Dinar Serbio\n"
                                    "RUB: Rublo Ruso\n"
                                    "RWF: Franco Ruandés\n"
                                    "SAR: Riyal Saudí\n"
                                    "SBD: Dólar de las Islas Salomón\n"
                                    "SCR: Rupia de Seychelles\n"
                                    "SDG: Libra Sudanesa\n"
                                    "SEK: Corona Sueca\n"
                                    "SGD: Dólar de Singapur\n"
                                    "SHP: Libra de Santa Elena\n"
                                    "SLE: Leone\n"
                                    "SLL: Leone\n"
                                    "SOS: Chelín Somalí\n"
                                    "SRD: Dólar Surinamés\n"
                                    "SSP: Libra del Sur de Sudán\n"
                                    "STN: Dobra\n"
                                    "SYP: Libra Siria\n"
                                    "SZL: Lilangeni\n"
                                    "THB: Baht Tailandés\n"
                                    "TJS: Somoni\n"
                                    "TMT: Manat Turcomano\n"
                                    "TND: Dinar Tunecino\n"
                                    "TOP: Paʻanga\n"
                                    "TRY: Lira Turca\n"
                                    "TTD: Dólar de Trinidad y Tobago\n"
                                    "TVD: Dólar Tuvaluano\n"
                                    "TWD: Dólar de Taiwán\n"
                                    "TZS: Chelín Tanzano\n"
                                    "UAH: Grivna\n"
                                    "UGX: Chelín Ugandés\n"
                                    "UYU: Peso Uruguayo\n"
                                    "UZS: Sum\n"
                                    "VES: Bolívar Soberano\n"
                                    "VND: Dong\n"
                                    "VUV: Vatu\n"
                                    "WST: Tala\n"
                                    "XAF: Franco CFA de África Central\n"
                                    "XCD: Dólar del Caribe Oriental\n"
                                    "XDR: Derechos Especiales de Giro\n"
                                    "XOF: Franco CFA de África Occidental\n"
                                    "XPF: Franco CFP\n"
                                    "YER: Rial Yemení\n"
                                    "ZAR: Rand Sudafricano\n"
                                    "ZMW: Kwacha Zambiano\n"
                                    "ZWL: Dólar Zimbabuense"            
                                    , parse_mode='Markdown')

# Función para convertir divisas desde el comando /convert
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("❌ **Error en el comando /convert**\n\n"
            "Para usar este comando, introduce los parámetros en el siguiente formato:\n"
            "`/convert cantidad from_currency to_currency`\n\n"
            "🔄 **Ejemplo de uso:**\n"
            "`/convert 50 EUR USD`\n"
            "Esto convertirá 50 euros a dólares estadounidenses.\n\n"
            "💡 Usa /divisas para ver la lista de códigos de divisas válidos.",
            parse_mode='Markdown')
            return

        amount = float(args[0])
        from_currency = args[1].upper()
        to_currency = args[2].upper()

        rates = get_rates()
        if not rates:
            await update.message.reply_text("No se pudieron obtener las tasas de cambio.")
            return

        if from_currency not in rates or to_currency not in rates:
            await update.message.reply_text("Una de las divisas no es válida.")
            return

        result = convert_currency(amount, from_currency, to_currency, rates)
        await update.message.reply_text(f"{amount} {from_currency} es igual a {result:.2f} {to_currency}")

    except (ValueError, IndexError):
        await update.message.reply_text("Uso: /convert cantidad from_currency to_currency")

# Función para manejar errores
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("💰 Direccion TON: `UQCrYeiQTHwVOrtJ5TFVEf_cGtJvq_P4AjBYRv0t-aFzW6Fi`", parse_mode="Markdown")

def main() -> None:
    # Token del bot de Telegram
    token = os.getenv("TOKEN")
    
    application = Application.builder().token(token).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(CommandHandler("divisas", divisas))
    application.add_handler(CommandHandler("donate", donate))

    # Errores
    application.add_error_handler(error)

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
